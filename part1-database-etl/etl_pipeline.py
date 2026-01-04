"""
FlexiMart ETL Pipeline
======================
This script extracts data from CSV files, cleans it, and loads it into MySQL database.

Author: Data Engineering Team
Date: 2024
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import re
from datetime import datetime


# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'fleximart123',  # Change this to your MySQL password
    'database': 'fleximart'
}


# ============================================================================
# EXTRACT FUNCTIONS
# ============================================================================

def extract_data_from_csv(file_path):
    """
    Read CSV file and return a pandas DataFrame.

    Parameters:
        file_path (str): Path to the CSV file

    Returns:
        DataFrame: Loaded data from CSV
    """
    try:
        df = pd.read_csv(file_path)
        print(f"✓ Loaded {len(df)} records from {file_path}")
        return df
    except FileNotFoundError:
        print(f"✗ Error: File not found - {file_path}")
        return None
    except Exception as e:
        print(f"✗ Error reading {file_path}: {str(e)}")
        return None


# ============================================================================
# TRANSFORM FUNCTIONS
# ============================================================================

def clean_phone_number(phone):
    """
    Standardize phone numbers to format: +91-XXXXXXXXXX

    Handles various input formats:
    - 9876543210 → +91-9876543210
    - +91-9876543210 → +91-9876543210
    - 98-7654-3210 → +91-9876543210
    - +91 9876543210 → +91-9876543210

    Parameters:
        phone (str/float): Phone number in any format

    Returns:
        str: Standardized phone or None if invalid
    """
    # Handle missing values
    if pd.isna(phone) or phone == '':
        return None

    # Extract only digits from the phone number
    digits_only = re.sub(r'\D', '', str(phone))

    # Remove leading zeros (Indian numbers with 0 prefix)
    digits_only = digits_only.lstrip('0')

    # Check if we have a valid 10-digit number
    if len(digits_only) == 10:
        return f"+91-{digits_only}"
    elif len(digits_only) == 12 and digits_only.startswith('91'):
        return f"+91-{digits_only[2:]}"
    else:
        return None


def clean_date_format(date_value):
    """
    Convert various date formats to standard YYYY-MM-DD format.

    Handles formats like:
    - 2024-01-15
    - 15/01/2024
    - 01/15/2024
    - 2024.01.15

    Parameters:
        date_value (str): Date in various formats

    Returns:
        str: Date in YYYY-MM-DD format or None
    """
    if pd.isna(date_value) or date_value == '':
        return None

    # Different date formats we might encounter
    possible_formats = [
        '%Y-%m-%d',      # 2024-01-15
        '%d/%m/%Y',      # 15/01/2024
        '%d-%m-%Y',      # 15-01-2024
        '%m-%d-%Y',      # 01-22-2024 (US format with dashes)
        '%Y/%m/%d',      # 2024/01/15
        '%Y.%m.%d',      # 2024.01.15
        '%m/%d/%Y'       # 01/15/2024 (US format with slashes)
    ]

    date_str = str(date_value).strip()

    # Try each format until one works
    for fmt in possible_formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            continue

    return None


def clean_category_name(category):
    """
    Standardize category names to proper title case.

    Examples:
    - electronics → Electronics
    - BOOKS → Books
    - fashion → Fashion

    Parameters:
        category (str): Category name in any case

    Returns:
        str: Standardized category name
    """
    if pd.isna(category) or category == '':
        return 'Uncategorized'

    return str(category).strip().title()


def transform_customers(df):
    """
    Clean and transform customer data.

    Operations:
    1. Remove duplicate records
    2. Drop records with missing emails (required field)
    3. Standardize phone numbers
    4. Standardize dates
    5. Fill missing cities

    Parameters:
        df (DataFrame): Raw customer data

    Returns:
        DataFrame: Cleaned customer data
        dict: Statistics about transformations
    """
    print("\n--- Transforming Customer Data ---")

    stats = {
        'initial_count': len(df),
        'duplicates_removed': 0,
        'missing_emails': 0,
        'records_after_cleaning': 0
    }

    # Remove duplicate rows
    initial_len = len(df)
    df = df.drop_duplicates()
    stats['duplicates_removed'] = initial_len - len(df)
    print(f"  Removed {stats['duplicates_removed']} duplicate records")

    # Handle missing emails - email is required
    stats['missing_emails'] = df['email'].isna().sum()
    df = df.dropna(subset=['email'])
    print(f"  Dropped {stats['missing_emails']} records with missing emails")

    # Clean phone numbers
    df['phone'] = df['phone'].apply(clean_phone_number)
    print(f"  Standardized phone numbers")

    # Clean dates
    df['registration_date'] = df['registration_date'].apply(clean_date_format)
    print(f"  Standardized registration dates")

    # Fill missing cities and standardize to title case
    df['city'] = df['city'].fillna('Unknown')
    df['city'] = df['city'].str.strip().str.title()

    # Keep customer_id for mapping purposes (needed to link sales data)
    # Database will still auto-generate IDs, but we need this for reference

    stats['records_after_cleaning'] = len(df)
    print(f"  Final count: {stats['records_after_cleaning']} clean records")

    return df, stats


def transform_products(df):
    """
    Clean and transform product data.

    Operations:
    1. Remove duplicate records
    2. Standardize category names
    3. Drop products with missing prices
    4. Fill missing stock quantities with 0

    Parameters:
        df (DataFrame): Raw product data

    Returns:
        DataFrame: Cleaned product data
        dict: Statistics about transformations
    """
    print("\n--- Transforming Product Data ---")

    stats = {
        'initial_count': len(df),
        'duplicates_removed': 0,
        'missing_prices': 0,
        'missing_stock': 0,
        'records_after_cleaning': 0
    }

    # Remove duplicate rows
    initial_len = len(df)
    df = df.drop_duplicates()
    stats['duplicates_removed'] = initial_len - len(df)
    print(f"  Removed {stats['duplicates_removed']} duplicate records")

    # Clean product names (remove extra spaces)
    df['product_name'] = df['product_name'].str.strip()
    print(f"  Cleaned product names")

    # Standardize categories
    df['category'] = df['category'].apply(clean_category_name)
    print(f"  Standardized category names")

    # Handle missing prices - price is required
    stats['missing_prices'] = df['price'].isna().sum()
    df = df.dropna(subset=['price'])
    print(f"  Dropped {stats['missing_prices']} products with missing prices")

    # Handle missing stock - set to 0
    stats['missing_stock'] = df['stock_quantity'].isna().sum()
    df['stock_quantity'] = df['stock_quantity'].fillna(0)
    df['stock_quantity'] = df['stock_quantity'].astype(int)
    print(f"  Filled {stats['missing_stock']} missing stock values with 0")

    # Keep product_id for mapping purposes (needed to link sales data)
    # Database will still auto-generate IDs, but we need this for reference

    stats['records_after_cleaning'] = len(df)
    print(f"  Final count: {stats['records_after_cleaning']} clean records")

    return df, stats


def transform_sales(df):
    """
    Clean and transform sales data.

    Operations:
    1. Remove duplicate records
    2. Standardize dates
    3. Drop records with missing required fields
    4. Ensure quantity is valid

    Parameters:
        df (DataFrame): Raw sales data

    Returns:
        DataFrame: Cleaned sales data
        dict: Statistics about transformations
    """
    print("\n--- Transforming Sales Data ---")

    stats = {
        'initial_count': len(df),
        'duplicates_removed': 0,
        'missing_data_dropped': 0,
        'records_after_cleaning': 0
    }

    # Remove duplicate rows
    initial_len = len(df)
    df = df.drop_duplicates()
    stats['duplicates_removed'] = initial_len - len(df)
    print(f"  Removed {stats['duplicates_removed']} duplicate records")

    # Clean dates (column is transaction_date in sales CSV)
    df = df.copy()  # Create explicit copy to avoid SettingWithCopyWarning
    df['transaction_date'] = df['transaction_date'].apply(clean_date_format)
    print(f"  Standardized transaction dates")

    # Drop records with missing critical data
    before_drop = len(df)
    df = df.dropna(subset=['customer_id', 'product_id', 'transaction_date', 'unit_price'])
    stats['missing_data_dropped'] = before_drop - len(df)
    print(f"  Dropped {stats['missing_data_dropped']} records with missing critical fields")

    # Ensure quantity is at least 1
    df['quantity'] = df['quantity'].fillna(1).astype(int)

    # Remove old transaction ID
    if 'transaction_id' in df.columns:
        df = df.drop(columns=['transaction_id'])

    stats['records_after_cleaning'] = len(df)
    print(f"  Final count: {stats['records_after_cleaning']} clean records")

    return df, stats


# ============================================================================
# LOAD FUNCTIONS
# ============================================================================

def create_database_connection():
    """
    Establish connection to MySQL database.

    Returns:
        connection: MySQL connection object or None if failed
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✓ Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"✗ Error connecting to MySQL: {e}")
        return None


def load_customers_to_db(df, connection):
    """
    Load cleaned customer data into database.

    Parameters:
        df (DataFrame): Cleaned customer data
        connection: MySQL connection object

    Returns:
        tuple: (Number of records successfully loaded, ID mapping dict)
    """
    cursor = connection.cursor()
    loaded_count = 0
    id_mapping = {}  # Maps original customer_id (C001) to database ID

    insert_query = """
    INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        try:
            values = (
                row['first_name'],
                row['last_name'],
                row['email'],
                row['phone'],
                row['city'],
                row['registration_date']
            )
            cursor.execute(insert_query, values)
            # Store mapping from original CSV ID to database auto-increment ID
            id_mapping[row['customer_id']] = cursor.lastrowid
            loaded_count += 1
        except Error as e:
            print(f"  ⚠ Error inserting customer {row['email']}: {e}")

    connection.commit()
    cursor.close()
    print(f"  Loaded {loaded_count} customers into database")
    return loaded_count, id_mapping


def load_products_to_db(df, connection):
    """
    Load cleaned product data into database.

    Parameters:
        df (DataFrame): Cleaned product data
        connection: MySQL connection object

    Returns:
        tuple: (Number of records successfully loaded, ID mapping dict)
    """
    cursor = connection.cursor()
    loaded_count = 0
    id_mapping = {}  # Maps original product_id (P001) to database ID

    insert_query = """
    INSERT INTO products (product_name, category, price, stock_quantity)
    VALUES (%s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        try:
            values = (
                row['product_name'],
                row['category'],
                float(row['price']),
                int(row['stock_quantity'])
            )
            cursor.execute(insert_query, values)
            # Store mapping from original CSV ID to database auto-increment ID
            id_mapping[row['product_id']] = cursor.lastrowid
            loaded_count += 1
        except Error as e:
            print(f"  ⚠ Error inserting product {row['product_name']}: {e}")

    connection.commit()
    cursor.close()
    print(f"  Loaded {loaded_count} products into database")
    return loaded_count, id_mapping


def load_sales_to_db(df, connection, customer_id_map, product_id_map):
    """
    Load cleaned sales data into database.
    Creates orders and order_items records.

    Parameters:
        df (DataFrame): Cleaned sales data
        connection: MySQL connection object
        customer_id_map (dict): Mapping of CSV customer IDs to database IDs
        product_id_map (dict): Mapping of CSV product IDs to database IDs

    Returns:
        int: Number of orders successfully loaded
    """
    cursor = connection.cursor()
    loaded_count = 0

    # For each sale, create an order and an order_item
    order_query = """
    INSERT INTO orders (customer_id, order_date, total_amount, status)
    VALUES (%s, %s, %s, %s)
    """

    item_query = """
    INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
    VALUES (%s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        try:
            # Map CSV IDs to database IDs
            csv_customer_id = row['customer_id']
            csv_product_id = row['product_id']

            # Skip if customer or product ID not in mapping (means they weren't loaded)
            if csv_customer_id not in customer_id_map:
                continue
            if csv_product_id not in product_id_map:
                continue

            db_customer_id = customer_id_map[csv_customer_id]
            db_product_id = product_id_map[csv_product_id]

            # Calculate total amount from unit_price and quantity
            total_amount = float(row['unit_price']) * int(row['quantity'])
            status = row.get('status', 'Completed')

            # Insert order
            order_values = (
                db_customer_id,
                row['transaction_date'],
                total_amount,
                status
            )
            cursor.execute(order_query, order_values)
            order_id = cursor.lastrowid

            # Insert order item
            item_values = (
                order_id,
                db_product_id,
                int(row['quantity']),
                float(row['unit_price']),
                total_amount
            )
            cursor.execute(item_query, item_values)
            loaded_count += 1

        except Error as e:
            print(f"  ⚠ Error inserting order: {e}")

    connection.commit()
    cursor.close()
    print(f"  Loaded {loaded_count} orders into database")
    return loaded_count


# ============================================================================
# REPORTING FUNCTIONS
# ============================================================================

def generate_quality_report(extract_stats, transform_stats, load_stats):
    """
    Generate data quality report.

    Parameters:
        extract_stats (dict): Statistics from extraction phase
        transform_stats (dict): Statistics from transformation phase
        load_stats (dict): Statistics from loading phase
    """
    report_lines = []
    report_lines.append("DATA QUALITY REPORT")
    report_lines.append("=" * 70)
    report_lines.append("")

    # Customer data section
    report_lines.append("CUSTOMERS")
    report_lines.append("-" * 70)
    report_lines.append(f"Number of records processed per file: {extract_stats['customers']['initial_count']}")
    report_lines.append(f"Number of duplicates removed: {transform_stats['customers']['duplicates_removed']}")
    report_lines.append(f"Number of missing values handled: {transform_stats['customers']['missing_emails']}")
    report_lines.append(f"Number of records loaded successfully: {load_stats['customers']}")
    report_lines.append("")

    # Product data section
    report_lines.append("PRODUCTS")
    report_lines.append("-" * 70)
    report_lines.append(f"Number of records processed per file: {extract_stats['products']['initial_count']}")
    report_lines.append(f"Number of duplicates removed: {transform_stats['products']['duplicates_removed']}")
    missing_products = transform_stats['products']['missing_prices'] + transform_stats['products']['missing_stock']
    report_lines.append(f"Number of missing values handled: {missing_products}")
    report_lines.append(f"Number of records loaded successfully: {load_stats['products']}")
    report_lines.append("")

    # Sales data section
    report_lines.append("SALES")
    report_lines.append("-" * 70)
    report_lines.append(f"Number of records processed per file: {extract_stats['sales']['initial_count']}")
    report_lines.append(f"Number of duplicates removed: {transform_stats['sales']['duplicates_removed']}")
    report_lines.append(f"Number of missing values handled: {transform_stats['sales']['missing_data_dropped']}")
    report_lines.append(f"Number of records loaded successfully: {load_stats['sales']}")
    report_lines.append("")

    # Write to file
    report_text = '\n'.join(report_lines)
    with open('data_quality_report.txt', 'w') as f:
        f.write(report_text)

    # Also print to console
    print("\n" + report_text)
    print("✓ Report saved to data_quality_report.txt")


# ============================================================================
# MAIN ETL PIPELINE
# ============================================================================

def run_etl_pipeline():
    """
    Main function to orchestrate the complete ETL pipeline.

    Steps:
    1. Extract data from CSV files
    2. Transform and clean the data
    3. Load data into MySQL database
    4. Generate quality report
    """
    print("\n" + "=" * 70)
    print("FLEXIMART ETL PIPELINE - STARTED")
    print("=" * 70)

    # Track statistics for reporting
    extract_stats = {}
    transform_stats = {}
    load_stats = {}

    # ========== EXTRACT PHASE ==========
    print("\n[PHASE 1: EXTRACT]")
    print("-" * 70)

    customers_df = extract_data_from_csv('../data/customers_raw.csv')
    products_df = extract_data_from_csv('../data/products_raw.csv')
    sales_df = extract_data_from_csv('../data/sales_raw.csv')

    # Record extraction stats
    extract_stats['customers'] = {'initial_count': len(customers_df) if customers_df is not None else 0}
    extract_stats['products'] = {'initial_count': len(products_df) if products_df is not None else 0}
    extract_stats['sales'] = {'initial_count': len(sales_df) if sales_df is not None else 0}

    # Check if extraction was successful
    if customers_df is None or products_df is None or sales_df is None:
        print("\n✗ ETL Pipeline failed - Unable to extract all required data")
        return

    # ========== TRANSFORM PHASE ==========
    print("\n[PHASE 2: TRANSFORM]")
    print("-" * 70)

    customers_clean, customer_stats = transform_customers(customers_df)
    products_clean, product_stats = transform_products(products_df)
    sales_clean, sales_stats = transform_sales(sales_df)

    transform_stats['customers'] = customer_stats
    transform_stats['products'] = product_stats
    transform_stats['sales'] = sales_stats

    # ========== LOAD PHASE ==========
    print("\n[PHASE 3: LOAD]")
    print("-" * 70)

    # Connect to database
    connection = create_database_connection()
    if connection is None:
        print("\n✗ ETL Pipeline failed - Unable to connect to database")
        return

    try:
        # Load data in correct order (respecting foreign keys)
        print("\nLoading customers...")
        customers_loaded, customer_id_map = load_customers_to_db(customers_clean, connection)
        load_stats['customers'] = customers_loaded

        print("\nLoading products...")
        products_loaded, product_id_map = load_products_to_db(products_clean, connection)
        load_stats['products'] = products_loaded

        print("\nLoading sales (orders)...")
        load_stats['sales'] = load_sales_to_db(sales_clean, connection, customer_id_map, product_id_map)

        print("\n✓ All data loaded successfully!")

    except Error as e:
        print(f"\n✗ Error during load phase: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("✓ Database connection closed")

    # ========== REPORTING PHASE ==========
    print("\n[PHASE 4: REPORTING]")
    print("-" * 70)

    generate_quality_report(extract_stats, transform_stats, load_stats)

    print("\n" + "=" * 70)
    print("FLEXIMART ETL PIPELINE - COMPLETED")
    print("=" * 70)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    run_etl_pipeline()
