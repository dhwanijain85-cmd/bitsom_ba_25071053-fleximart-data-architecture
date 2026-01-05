# FlexiMart Star Schema Design Documentation

## Section 1: Schema Overview (4 marks)

### FACT TABLE: fact_sales

**Grain:** One row per product per order line item
**Business Process:** Sales transactions

**Measures (Numeric Facts):**
| Measure | Data Type | Description |
|---------|-----------|-------------|
| quantity_sold | INT | Number of units sold in this line item |
| unit_price | DECIMAL(10,2) | Price per unit at time of sale |
| discount_amount | DECIMAL(10,2) | Discount applied to this line item |
| total_amount | DECIMAL(10,2) | Final amount (quantity × unit_price - discount) |

**Foreign Keys:**
| Foreign Key | References | Description |
|-------------|------------|-------------|
| date_key | dim_date | Links to date dimension for time analysis |
| product_key | dim_product | Links to product dimension for product analysis |
| customer_key | dim_customer | Links to customer dimension for customer analysis |

---

### DIMENSION TABLE: dim_date

**Purpose:** Date dimension for time-based analysis
**Type:** Conformed dimension (can be reused across multiple fact tables)

**Attributes:**
| Attribute | Data Type | Description |
|-----------|-----------|-------------|
| date_key (PK) | INT | Surrogate key (format: YYYYMMDD, e.g., 20240115) |
| full_date | DATE | Actual date value |
| day_of_week | VARCHAR(10) | Day name (Monday, Tuesday, etc.) |
| day_of_month | INT | Day number (1-31) |
| month | INT | Month number (1-12) |
| month_name | VARCHAR(10) | Month name (January, February, etc.) |
| quarter | VARCHAR(2) | Quarter (Q1, Q2, Q3, Q4) |
| year | INT | Year (2023, 2024, etc.) |
| is_weekend | BOOLEAN | TRUE if Saturday or Sunday |
| is_holiday | BOOLEAN | TRUE if public holiday |

---

### DIMENSION TABLE: dim_product

**Purpose:** Product dimension for product-based analysis
**Type:** Slowly Changing Dimension (SCD Type 1 - overwrite changes)

**Attributes:**
| Attribute | Data Type | Description |
|-----------|-----------|-------------|
| product_key (PK) | INT | Surrogate key (auto-generated) |
| product_id | VARCHAR(20) | Natural key from source system |
| product_name | VARCHAR(100) | Name of the product |
| category | VARCHAR(50) | Product category (Electronics, Fashion, etc.) |
| subcategory | VARCHAR(50) | Product subcategory |
| brand | VARCHAR(50) | Brand name |
| current_price | DECIMAL(10,2) | Current selling price |
| is_active | BOOLEAN | TRUE if product is currently available |

---

### DIMENSION TABLE: dim_customer

**Purpose:** Customer dimension for customer-based analysis
**Type:** Slowly Changing Dimension (SCD Type 2 - track history for city changes)

**Attributes:**
| Attribute | Data Type | Description |
|-----------|-----------|-------------|
| customer_key (PK) | INT | Surrogate key (auto-generated) |
| customer_id | VARCHAR(20) | Natural key from source system |
| customer_name | VARCHAR(100) | Full name (first_name + last_name) |
| email | VARCHAR(100) | Customer email address |
| phone | VARCHAR(20) | Contact phone number |
| city | VARCHAR(50) | Customer city |
| registration_date | DATE | Date customer registered |
| customer_segment | VARCHAR(20) | Segment (New, Regular, Premium) based on purchase history |

---

## Section 2: Design Decisions (150 words)

### Why Transaction Line-Item Level Granularity?

We chose line-item level granularity (one row per product per order) instead of order-level because it provides maximum flexibility for analysis. Analysts can aggregate up to order-level, customer-level, or daily totals, but cannot drill down if we stored only order totals. This granularity allows questions like "which product contributed most to a large order?" or "what is the average quantity per product category?"

### Why Surrogate Keys Instead of Natural Keys?

Surrogate keys (auto-generated integers) are used instead of natural keys (like customer_id "C001") for several reasons: they are smaller and faster for joins, they remain stable even if source system IDs change, and they allow tracking historical changes through slowly changing dimensions. For example, if a customer moves cities, we can create a new surrogate key while keeping the same natural key.

### How Design Supports Drill-Down and Roll-Up?

The dim_date dimension enables time-based roll-up (day → month → quarter → year) and drill-down (year → quarter → month → day). Similarly, dim_product supports category → subcategory → product analysis. Analysts can start with yearly revenue, drill down to quarterly trends, and identify specific months or days driving performance.

---

## Section 3: Sample Data Flow (3 marks)

### Source Transaction

```
Order #101
Customer: "Rahul Sharma" (C001)
Product: "Samsung Galaxy S21 Ultra" (ELEC001)
Quantity: 2
Unit Price: 79999.00
Order Date: 2024-01-15
Status: Completed
```

### Transformation Process

1. **Extract** from OLTP database (orders, order_items, customers, products tables)
2. **Transform**: Generate surrogate keys, format dates, calculate measures
3. **Load** into star schema tables

### Result in Data Warehouse

**fact_sales:**
```
{
  sales_key: 1001,
  date_key: 20240115,
  product_key: 5,
  customer_key: 12,
  quantity_sold: 2,
  unit_price: 79999.00,
  discount_amount: 0.00,
  total_amount: 159998.00
}
```

**dim_date:**
```
{
  date_key: 20240115,
  full_date: '2024-01-15',
  day_of_week: 'Monday',
  day_of_month: 15,
  month: 1,
  month_name: 'January',
  quarter: 'Q1',
  year: 2024,
  is_weekend: FALSE,
  is_holiday: FALSE
}
```

**dim_product:**
```
{
  product_key: 5,
  product_id: 'ELEC001',
  product_name: 'Samsung Galaxy S21 Ultra',
  category: 'Electronics',
  subcategory: 'Smartphones',
  brand: 'Samsung',
  current_price: 79999.00,
  is_active: TRUE
}
```

**dim_customer:**
```
{
  customer_key: 12,
  customer_id: 'C001',
  customer_name: 'Rahul Sharma',
  email: 'rahul.sharma@gmail.com',
  phone: '+91-9876543210',
  city: 'Mumbai',
  registration_date: '2023-01-15',
  customer_segment: 'Regular'
}
```

### Sample Query Using Star Schema

```sql
-- Monthly sales by product category for Q1 2024
SELECT
    d.month_name,
    p.category,
    SUM(f.quantity_sold) AS units_sold,
    SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
WHERE d.year = 2024 AND d.quarter = 'Q1'
GROUP BY d.month_name, p.category
ORDER BY d.month, revenue DESC;
```
