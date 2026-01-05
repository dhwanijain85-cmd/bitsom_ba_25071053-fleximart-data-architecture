-- ============================================================================
-- FlexiMart Data Warehouse - Sample Data
-- ============================================================================
-- Run this script after warehouse_schema.sql to populate the data warehouse
-- ============================================================================

USE fleximart_dw;

-- ============================================================================
-- DIM_DATE: 30 dates (January-February 2024)
-- ============================================================================

INSERT INTO dim_date (date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend) VALUES
-- January 2024
(20240101, '2024-01-01', 'Monday', 1, 1, 'January', 'Q1', 2024, FALSE),
(20240102, '2024-01-02', 'Tuesday', 2, 1, 'January', 'Q1', 2024, FALSE),
(20240103, '2024-01-03', 'Wednesday', 3, 1, 'January', 'Q1', 2024, FALSE),
(20240104, '2024-01-04', 'Thursday', 4, 1, 'January', 'Q1', 2024, FALSE),
(20240105, '2024-01-05', 'Friday', 5, 1, 'January', 'Q1', 2024, FALSE),
(20240106, '2024-01-06', 'Saturday', 6, 1, 'January', 'Q1', 2024, TRUE),
(20240107, '2024-01-07', 'Sunday', 7, 1, 'January', 'Q1', 2024, TRUE),
(20240108, '2024-01-08', 'Monday', 8, 1, 'January', 'Q1', 2024, FALSE),
(20240109, '2024-01-09', 'Tuesday', 9, 1, 'January', 'Q1', 2024, FALSE),
(20240110, '2024-01-10', 'Wednesday', 10, 1, 'January', 'Q1', 2024, FALSE),
(20240113, '2024-01-13', 'Saturday', 13, 1, 'January', 'Q1', 2024, TRUE),
(20240114, '2024-01-14', 'Sunday', 14, 1, 'January', 'Q1', 2024, TRUE),
(20240115, '2024-01-15', 'Monday', 15, 1, 'January', 'Q1', 2024, FALSE),
(20240118, '2024-01-18', 'Thursday', 18, 1, 'January', 'Q1', 2024, FALSE),
(20240120, '2024-01-20', 'Saturday', 20, 1, 'January', 'Q1', 2024, TRUE),
(20240121, '2024-01-21', 'Sunday', 21, 1, 'January', 'Q1', 2024, TRUE),
(20240125, '2024-01-25', 'Thursday', 25, 1, 'January', 'Q1', 2024, FALSE),
(20240127, '2024-01-27', 'Saturday', 27, 1, 'January', 'Q1', 2024, TRUE),
(20240128, '2024-01-28', 'Sunday', 28, 1, 'January', 'Q1', 2024, TRUE),
(20240130, '2024-01-30', 'Tuesday', 30, 1, 'January', 'Q1', 2024, FALSE),
-- February 2024
(20240201, '2024-02-01', 'Thursday', 1, 2, 'February', 'Q1', 2024, FALSE),
(20240202, '2024-02-02', 'Friday', 2, 2, 'February', 'Q1', 2024, FALSE),
(20240203, '2024-02-03', 'Saturday', 3, 2, 'February', 'Q1', 2024, TRUE),
(20240204, '2024-02-04', 'Sunday', 4, 2, 'February', 'Q1', 2024, TRUE),
(20240205, '2024-02-05', 'Monday', 5, 2, 'February', 'Q1', 2024, FALSE),
(20240208, '2024-02-08', 'Thursday', 8, 2, 'February', 'Q1', 2024, FALSE),
(20240210, '2024-02-10', 'Saturday', 10, 2, 'February', 'Q1', 2024, TRUE),
(20240211, '2024-02-11', 'Sunday', 11, 2, 'February', 'Q1', 2024, TRUE),
(20240214, '2024-02-14', 'Wednesday', 14, 2, 'February', 'Q1', 2024, FALSE),
(20240215, '2024-02-15', 'Thursday', 15, 2, 'February', 'Q1', 2024, FALSE);


-- ============================================================================
-- DIM_PRODUCT: 15 products across 3 categories
-- ============================================================================

INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
-- Electronics (5 products) - Price range: 2999 to 89999
('P001', 'Samsung Galaxy S21', 'Electronics', 'Smartphones', 69999.00),
('P002', 'Apple MacBook Air', 'Electronics', 'Laptops', 89999.00),
('P003', 'Sony WH-1000XM4 Headphones', 'Electronics', 'Audio', 24999.00),
('P004', 'Dell 24-inch Monitor', 'Electronics', 'Monitors', 18999.00),
('P005', 'Logitech Wireless Mouse', 'Electronics', 'Accessories', 2999.00),
-- Fashion (5 products) - Price range: 499 to 8999
('P006', 'Levis 501 Jeans', 'Fashion', 'Clothing', 3499.00),
('P007', 'Nike Air Max Sneakers', 'Fashion', 'Footwear', 8999.00),
('P008', 'Adidas Sports T-Shirt', 'Fashion', 'Clothing', 1499.00),
('P009', 'Ray-Ban Sunglasses', 'Fashion', 'Accessories', 6999.00),
('P010', 'Puma Running Shorts', 'Fashion', 'Clothing', 999.00),
-- Groceries (5 products) - Price range: 150 to 899
('P011', 'Organic Honey 500g', 'Groceries', 'Food', 450.00),
('P012', 'Basmati Rice 5kg', 'Groceries', 'Staples', 650.00),
('P013', 'Olive Oil 1L', 'Groceries', 'Cooking', 899.00),
('P014', 'Green Tea 100 bags', 'Groceries', 'Beverages', 350.00),
('P015', 'Mixed Dry Fruits 500g', 'Groceries', 'Snacks', 750.00);


-- ============================================================================
-- DIM_CUSTOMER: 12 customers across 4 cities
-- ============================================================================

INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
-- Mumbai customers (3)
('C001', 'Rahul Sharma', 'Mumbai', 'Maharashtra', 'Premium'),
('C002', 'Priya Patel', 'Mumbai', 'Maharashtra', 'Regular'),
('C003', 'Amit Kumar', 'Mumbai', 'Maharashtra', 'New'),
-- Delhi customers (3)
('C004', 'Sneha Reddy', 'Delhi', 'Delhi', 'Premium'),
('C005', 'Vikram Singh', 'Delhi', 'Delhi', 'Regular'),
('C006', 'Anjali Mehta', 'Delhi', 'Delhi', 'New'),
-- Bangalore customers (3)
('C007', 'Karthik Nair', 'Bangalore', 'Karnataka', 'Premium'),
('C008', 'Deepa Gupta', 'Bangalore', 'Karnataka', 'Regular'),
('C009', 'Arjun Rao', 'Bangalore', 'Karnataka', 'Regular'),
-- Chennai customers (3)
('C010', 'Meera Iyer', 'Chennai', 'Tamil Nadu', 'Premium'),
('C011', 'Suresh Kumar', 'Chennai', 'Tamil Nadu', 'New'),
('C012', 'Lakshmi Venkat', 'Chennai', 'Tamil Nadu', 'Regular');


-- ============================================================================
-- FACT_SALES: 40 sales transactions
-- ============================================================================
-- Pattern: Higher sales on weekends, varied quantities
-- total_amount = (quantity_sold * unit_price) - discount_amount

INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES
-- January 2024 - Weekday sales (lower volume)
(20240101, 1, 1, 1, 69999.00, 5000.00, 64999.00),   -- Rahul buys Samsung phone
(20240102, 5, 2, 2, 2999.00, 0.00, 5998.00),        -- Priya buys mice
(20240103, 8, 3, 3, 1499.00, 200.00, 4297.00),      -- Amit buys t-shirts
(20240104, 11, 4, 5, 450.00, 0.00, 2250.00),        -- Sneha buys honey
(20240105, 14, 5, 4, 350.00, 100.00, 1300.00),      -- Vikram buys green tea

-- January 2024 - Weekend sales (higher volume)
(20240106, 2, 1, 1, 89999.00, 10000.00, 79999.00),  -- Rahul buys MacBook
(20240106, 7, 6, 2, 8999.00, 1000.00, 16998.00),    -- Anjali buys sneakers
(20240106, 6, 7, 3, 3499.00, 500.00, 9997.00),      -- Karthik buys jeans
(20240107, 3, 8, 1, 24999.00, 2000.00, 22999.00),   -- Deepa buys headphones
(20240107, 9, 9, 2, 6999.00, 0.00, 13998.00),       -- Arjun buys sunglasses
(20240107, 12, 10, 10, 650.00, 500.00, 6000.00),    -- Meera buys rice

-- Mid-January weekdays
(20240108, 4, 11, 1, 18999.00, 1500.00, 17499.00),  -- Suresh buys monitor
(20240109, 10, 12, 4, 999.00, 0.00, 3996.00),       -- Lakshmi buys shorts
(20240110, 15, 1, 2, 750.00, 0.00, 1500.00),        -- Rahul buys dry fruits

-- Mid-January weekend (high volume)
(20240113, 1, 4, 1, 69999.00, 7000.00, 62999.00),   -- Sneha buys Samsung
(20240113, 2, 7, 1, 89999.00, 8000.00, 81999.00),   -- Karthik buys MacBook
(20240113, 6, 2, 2, 3499.00, 0.00, 6998.00),        -- Priya buys jeans
(20240114, 7, 3, 1, 8999.00, 500.00, 8499.00),      -- Amit buys sneakers
(20240114, 8, 5, 5, 1499.00, 500.00, 6995.00),      -- Vikram buys t-shirts
(20240114, 13, 6, 3, 899.00, 0.00, 2697.00),        -- Anjali buys olive oil

-- Late January
(20240115, 3, 10, 1, 24999.00, 3000.00, 21999.00),  -- Meera buys headphones
(20240118, 5, 8, 3, 2999.00, 0.00, 8997.00),        -- Deepa buys mice
(20240120, 4, 9, 2, 18999.00, 2000.00, 35998.00),   -- Arjun buys monitors (weekend)
(20240120, 9, 11, 1, 6999.00, 0.00, 6999.00),       -- Suresh buys sunglasses
(20240121, 11, 12, 8, 450.00, 200.00, 3400.00),     -- Lakshmi buys honey
(20240121, 12, 1, 5, 650.00, 0.00, 3250.00),        -- Rahul buys rice
(20240125, 14, 2, 6, 350.00, 0.00, 2100.00),        -- Priya buys green tea
(20240127, 1, 10, 1, 69999.00, 5000.00, 64999.00),  -- Meera buys Samsung (weekend)
(20240127, 6, 4, 2, 3499.00, 300.00, 6698.00),      -- Sneha buys jeans
(20240128, 7, 7, 2, 8999.00, 800.00, 17198.00),     -- Karthik buys sneakers
(20240130, 15, 3, 3, 750.00, 0.00, 2250.00),        -- Amit buys dry fruits

-- February 2024
(20240201, 2, 4, 1, 89999.00, 9000.00, 80999.00),   -- Sneha buys MacBook
(20240202, 10, 5, 3, 999.00, 0.00, 2997.00),        -- Vikram buys shorts
(20240203, 3, 6, 1, 24999.00, 2500.00, 22499.00),   -- Anjali buys headphones (weekend)
(20240203, 8, 8, 4, 1499.00, 400.00, 5596.00),      -- Deepa buys t-shirts
(20240204, 4, 9, 1, 18999.00, 1000.00, 17999.00),   -- Arjun buys monitor
(20240204, 13, 10, 4, 899.00, 0.00, 3596.00),       -- Meera buys olive oil
(20240205, 5, 11, 2, 2999.00, 0.00, 5998.00),       -- Suresh buys mice
(20240208, 11, 12, 6, 450.00, 100.00, 2600.00),     -- Lakshmi buys honey
(20240210, 1, 7, 1, 69999.00, 6000.00, 63999.00);   -- Karthik buys Samsung (weekend)


-- ============================================================================
-- Verify data loaded
-- ============================================================================

SELECT 'dim_date' AS table_name, COUNT(*) AS record_count FROM dim_date
UNION ALL
SELECT 'dim_product', COUNT(*) FROM dim_product
UNION ALL
SELECT 'dim_customer', COUNT(*) FROM dim_customer
UNION ALL
SELECT 'fact_sales', COUNT(*) FROM fact_sales;

SELECT 'Data warehouse populated successfully!' AS Status;
