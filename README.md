# FlexiMart Data Architecture - ETL Pipeline

A complete data pipeline solution for FlexiMart e-commerce company that extracts data from CSV files, cleans and transforms it, and loads it into a MySQL database.

## Project Overview

This project implements an ETL (Extract, Transform, Load) pipeline that:
- Reads customer, product, and sales data from CSV files
- Cleans data quality issues (duplicates, missing values, format inconsistencies)
- Loads cleaned data into a MySQL relational database
- Generates a comprehensive data quality report

## Files in This Project

- `etl_pipeline.py` - Main ETL script with all extract, transform, and load logic
- `create_database.sql` - SQL script to create database schema
- `customers_raw.csv` - Raw customer data (with quality issues)
- `products_raw.csv` - Raw product catalog data (with quality issues)
- `sales_raw.csv` - Raw sales transaction data (with quality issues)
- `data_quality_report.txt` - Generated report (created after running pipeline)

## Prerequisites

Before running the pipeline, you need:

1. **Python 3.8 or higher**
2. **MySQL Server** installed and running
3. **Python packages**:
   - pandas
   - mysql-connector-python

## Setup Instructions

### Step 1: Install MySQL

If you don't have MySQL installed:

**For Mac:**
```bash
brew install mysql
brew services start mysql
```

**For Windows:**
Download and install from: https://dev.mysql.com/downloads/mysql/

**For Linux:**
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo service mysql start
```

### Step 2: Install Python Dependencies

```bash
pip install pandas mysql-connector-python
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### Step 3: Create the Database

Log into MySQL:
```bash
mysql -u root -p
```

Then run the schema creation script:
```sql
source create_database.sql;
```

Or from command line:
```bash
mysql -u root -p < create_database.sql
```

### Step 4: Configure Database Connection

Open `etl_pipeline.py` and update the database configuration (around line 18):

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_MYSQL_PASSWORD',  # Update this!
    'database': 'fleximart'
}
```

### Step 5: Run the ETL Pipeline

```bash
python etl_pipeline.py
```

## What the Pipeline Does

### Extract Phase
- Reads all three CSV files
- Reports initial record counts

### Transform Phase

**Customers:**
- Removes duplicate records
- Drops records with missing emails (required field)
- Standardizes phone numbers to format: +91-XXXXXXXXXX
- Standardizes dates to YYYY-MM-DD format
- Fills missing cities with 'Unknown'

**Products:**
- Removes duplicate records
- Standardizes category names (Electronics, Fashion, Books)
- Drops products with missing prices
- Sets missing stock quantities to 0

**Sales:**
- Removes duplicate transactions
- Standardizes order dates to YYYY-MM-DD
- Drops records with missing customer/product IDs
- Creates proper order and order_item records

### Load Phase
- Inserts cleaned data into MySQL database
- Maintains referential integrity (foreign keys)
- Reports successful load counts

### Reporting Phase
- Generates `data_quality_report.txt`
- Shows records processed, cleaned, and loaded
- Provides data quality metrics

## Expected Output

When you run the pipeline, you'll see:

```
======================================================================
FLEXIMART ETL PIPELINE - STARTED
======================================================================

[PHASE 1: EXTRACT]
----------------------------------------------------------------------
✓ Loaded 22 records from customers_raw.csv
✓ Loaded 17 records from products_raw.csv
✓ Loaded 32 records from sales_raw.csv

[PHASE 2: TRANSFORM]
----------------------------------------------------------------------
--- Transforming Customer Data ---
  Removed 2 duplicate records
  Dropped 2 records with missing emails
  ...

[PHASE 3: LOAD]
----------------------------------------------------------------------
✓ Successfully connected to MySQL database
Loading customers...
  Loaded 18 customers into database
...

[PHASE 4: REPORTING]
----------------------------------------------------------------------
✓ Report saved to data_quality_report.txt
```

## Troubleshooting

**Error: "Access denied for user 'root'"**
- Update the password in `etl_pipeline.py`

**Error: "Unknown database 'fleximart'"**
- Run the `create_database.sql` script first

**Error: "ModuleNotFoundError: No module named 'pandas'"**
- Install required packages: `pip install pandas mysql-connector-python`

**Error: "Duplicate entry for key 'email'"**
- Drop and recreate tables using `create_database.sql`

## Database Schema

The database consists of 4 tables:

1. **customers** - Customer information
2. **products** - Product catalog
3. **orders** - Order header information
4. **order_items** - Individual items in each order

Refer to `create_database.sql` for detailed schema.

## Author

Data Engineering Assignment - FlexiMart ETL Pipeline