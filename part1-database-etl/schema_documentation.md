# FlexiMart Database Schema Documentation

## 1. Entity-Relationship Description

### ENTITY: customers
**Purpose:** Stores customer information including personal details and contact information for all registered FlexiMart users.

**Attributes:**
| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| customer_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for each customer |
| first_name | VARCHAR(50) | NOT NULL | Customer's first name |
| last_name | VARCHAR(50) | NOT NULL | Customer's last name |
| email | VARCHAR(100) | UNIQUE, NOT NULL | Customer's email address (used for login) |
| phone | VARCHAR(20) | - | Contact phone number in +91-XXXXXXXXXX format |
| city | VARCHAR(50) | - | City where the customer resides |
| registration_date | DATE | - | Date when customer registered on the platform |

**Relationships:**
- One customer can place MANY orders (1:M with orders table)

---

### ENTITY: products
**Purpose:** Contains the product catalog with pricing and inventory details for all items sold on FlexiMart.

**Attributes:**
| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| product_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for each product |
| product_name | VARCHAR(100) | NOT NULL | Name of the product |
| category | VARCHAR(50) | NOT NULL | Product category (Electronics, Fashion, Groceries, etc.) |
| price | DECIMAL(10,2) | NOT NULL, CHECK >= 0 | Selling price of the product in INR |
| stock_quantity | INT | DEFAULT 0, CHECK >= 0 | Current stock available in inventory |

**Relationships:**
- One product can appear in MANY order_items (1:M with order_items table)

---

### ENTITY: orders
**Purpose:** Stores order header information including customer reference, order date, and total amount.

**Attributes:**
| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| order_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for each order |
| customer_id | INT | FOREIGN KEY, NOT NULL | Reference to the customer who placed the order |
| order_date | DATE | NOT NULL | Date when the order was placed |
| total_amount | DECIMAL(10,2) | NOT NULL, CHECK >= 0 | Total order value in INR |
| status | VARCHAR(20) | DEFAULT 'Pending' | Order status (Pending, Completed, Shipped, Cancelled) |

**Relationships:**
- Each order belongs to ONE customer (M:1 with customers table)
- One order can have MANY order_items (1:M with order_items table)

---

### ENTITY: order_items
**Purpose:** Stores line-item details for each order, linking products to orders with quantity and pricing information.

**Attributes:**
| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| order_item_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for each line item |
| order_id | INT | FOREIGN KEY, NOT NULL | Reference to the parent order |
| product_id | INT | FOREIGN KEY, NOT NULL | Reference to the product being purchased |
| quantity | INT | NOT NULL, CHECK > 0 | Number of units purchased |
| unit_price | DECIMAL(10,2) | NOT NULL, CHECK >= 0 | Price per unit at time of purchase |
| subtotal | DECIMAL(10,2) | NOT NULL, CHECK >= 0 | Line item total (quantity × unit_price) |

**Relationships:**
- Each order_item belongs to ONE order (M:1 with orders table)
- Each order_item references ONE product (M:1 with products table)

---

## 2. Normalization Explanation

### Why This Design is in Third Normal Form (3NF)

The FlexiMart database schema follows Third Normal Form (3NF) because it satisfies all the requirements of 1NF, 2NF, and 3NF.

**First Normal Form (1NF):** All tables have atomic values in each column. For example, customer names are split into `first_name` and `last_name` rather than storing a full name in one field. Each cell contains a single value, and there are no repeating groups or arrays.

**Second Normal Form (2NF):** The design eliminates partial dependencies. Each non-key attribute depends on the entire primary key. In the `order_items` table, attributes like `quantity` and `unit_price` depend on the complete `order_item_id`, not just part of a composite key. We avoided creating a composite primary key of (order_id, product_id) which could have led to partial dependencies.

**Third Normal Form (3NF):** There are no transitive dependencies in our schema. Non-key attributes depend only on the primary key and not on other non-key attributes. For instance, customer city information is stored directly in the customers table and not derived from another attribute. Product category is an attribute of the product itself, not dependent on any other non-key field.

### Functional Dependencies

- **customers:** customer_id → first_name, last_name, email, phone, city, registration_date
- **products:** product_id → product_name, category, price, stock_quantity
- **orders:** order_id → customer_id, order_date, total_amount, status
- **order_items:** order_item_id → order_id, product_id, quantity, unit_price, subtotal

### How the Design Avoids Anomalies

**Update Anomaly:** If a customer changes their phone number, we only need to update it in one place (customers table). Product prices are stored in the products table, and historical prices are captured in order_items at the time of purchase, so updating current prices doesn't affect past orders.

**Insert Anomaly:** We can add a new customer without them having to place an order first. Similarly, new products can be added to the catalog without any sales. The separation of entities allows independent data entry.

**Delete Anomaly:** Deleting an order doesn't remove the customer or product information. The foreign key constraint with ON DELETE RESTRICT ensures we can't accidentally delete a customer who has orders, protecting data integrity. Order items are deleted with CASCADE when an order is deleted, which is the expected behavior.

---

## 3. Sample Data Representation

### customers table
| customer_id | first_name | last_name | email | phone | city | registration_date |
|-------------|------------|-----------|-------|-------|------|-------------------|
| 1 | Rahul | Sharma | rahul.sharma@gmail.com | +91-9876543210 | Mumbai | 2023-01-15 |
| 2 | Priya | Patel | priya.patel@yahoo.com | +91-8765432109 | Delhi | 2023-02-20 |
| 3 | Amit | Kumar | amit.kumar@gmail.com | +91-9988776655 | Bangalore | 2023-03-10 |

### products table
| product_id | product_name | category | price | stock_quantity |
|------------|--------------|----------|-------|----------------|
| 1 | Wireless Bluetooth Headphones | Electronics | 2499.00 | 50 |
| 2 | Cotton T-Shirt | Fashion | 599.00 | 200 |
| 3 | Organic Honey 500g | Groceries | 349.00 | 75 |

### orders table
| order_id | customer_id | order_date | total_amount | status |
|----------|-------------|------------|--------------|--------|
| 1 | 1 | 2024-01-15 | 2499.00 | Completed |
| 2 | 2 | 2024-01-18 | 1198.00 | Completed |
| 3 | 1 | 2024-01-22 | 3047.00 | Shipped |

### order_items table
| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
|---------------|----------|------------|----------|------------|----------|
| 1 | 1 | 1 | 1 | 2499.00 | 2499.00 |
| 2 | 2 | 2 | 2 | 599.00 | 1198.00 |
| 3 | 3 | 1 | 1 | 2499.00 | 2499.00 |
| 4 | 3 | 3 | 1 | 349.00 | 349.00 |
| 5 | 3 | 2 | 1 | 599.00 | 599.00 |

---

## Entity-Relationship Diagram (Text Representation)

```
+-------------+       +-------------+       +---------------+
|  customers  |       |   orders    |       | order_items   |
+-------------+       +-------------+       +---------------+
| customer_id |<──┐   | order_id    |<──┐   | order_item_id |
| first_name  |   │   | customer_id |───┘   | order_id      |───┐
| last_name   |   │   | order_date  |       | product_id    |───┼──┐
| email       |   │   | total_amount|       | quantity      |   │  │
| phone       |   │   | status      |       | unit_price    |   │  │
| city        |   │   +-------------+       | subtotal      |   │  │
| reg_date    |   │         │               +---------------+   │  │
+-------------+   │         │                                   │  │
                  │         │ 1:M                               │  │
                  │         ▼                                   │  │
                  └─────────────────────────────────────────────┘  │
                         1:M                                       │
                                                                   │
+-------------+                                                    │
|  products   |<───────────────────────────────────────────────────┘
+-------------+                           1:M
| product_id  |
| product_name|
| category    |
| price       |
| stock_qty   |
+-------------+
```

**Relationship Summary:**
- customers (1) ──── (M) orders: One customer can place many orders
- orders (1) ──── (M) order_items: One order can have many line items
- products (1) ──── (M) order_items: One product can appear in many order items
