# FlexiMart Data Architecture Project

**Student Name:** Dhwani Jain
**Student ID:** bitsom_ba_25071053
**Email:** dhwanijain85@gmail.com
**Date:** January 2026

## Project Overview

This project implements a complete data architecture solution for FlexiMart, an e-commerce company. It includes an ETL pipeline to ingest and clean raw CSV data into a MySQL relational database, a NoSQL analysis using MongoDB for flexible product catalogs, and a star schema data warehouse for OLAP analytics. The project demonstrates practical skills in data engineering, database design, and business intelligence.

## Repository Structure

```
├── data/
│   ├── customers_raw.csv
│   ├── products_raw.csv
│   └── sales_raw.csv
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── create_database.sql
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   ├── business_queries_results.txt
│   ├── data_quality_report.txt
│   └── requirements.txt
├── part2-nosql/
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   └── products_catalog.json
├── part3-datawarehouse/
│   ├── star_schema_design.md
│   ├── warehouse_schema.sql
│   ├── warehouse_data.sql
│   ├── analytics_queries.sql
│   └── analytics_queries_results.txt
├── SETUP_GUIDE.md
└── README.md
```

## Technologies Used

- **Python 3.x** - ETL pipeline development
- **pandas** - Data manipulation and cleaning
- **mysql-connector-python** - MySQL database connectivity
- **MySQL 8.0** - Relational database for OLTP and data warehouse
- **MongoDB 6.0** - NoSQL database for flexible product catalog

## Setup Instructions

### Prerequisites

1. Python 3.8 or higher
2. MySQL Server installed and running
3. MongoDB installed (for Part 2)

### Database Setup

```bash
# Set MySQL password (used throughout project)
# Password: fleximart123

# Create OLTP database and run ETL
cd part1-database-etl
mysql -u root -pfleximart123 < create_database.sql
python3 etl_pipeline.py

# Run Business Queries
mysql -u root -pfleximart123 fleximart < business_queries.sql

# Create Data Warehouse
cd ../part3-datawarehouse
mysql -u root -pfleximart123 < warehouse_schema.sql
mysql -u root -pfleximart123 < warehouse_data.sql

# Run Analytics Queries
mysql -u root -pfleximart123 fleximart_dw < analytics_queries.sql
```

### MongoDB Setup

```bash
# Import product catalog
cd part2-nosql
mongoimport --db fleximart --collection products --file products_catalog.json --jsonArray

# Run operations in MongoDB shell
mongosh < mongodb_operations.js
```

## Project Components

### Part 1: Database and ETL (30 marks)

- **ETL Pipeline**: Extracts data from 3 CSV files, transforms (cleans duplicates, handles missing values, standardizes formats), and loads into MySQL
- **Schema Documentation**: Entity-Relationship descriptions, 3NF normalization explanation
- **Business Queries**: 3 SQL queries with JOINs, GROUP BY, HAVING, and window functions

### Part 2: NoSQL Analysis (20 marks)

- **NoSQL Justification**: Analysis of RDBMS limitations vs MongoDB benefits
- **MongoDB Operations**: 5 operations including queries, aggregations, and updates

### Part 3: Data Warehouse (35 marks)

- **Star Schema Design**: Fact table (fact_sales) with 3 dimension tables (dim_date, dim_product, dim_customer)
- **Sample Data**: 30 dates, 15 products, 12 customers, 40 transactions
- **Analytics Queries**: Drill-down analysis, top-N products, customer segmentation

## Key Learnings

Through this project, I learned how different database paradigms serve different purposes - relational databases excel at transactional integrity while NoSQL provides flexibility for varied data structures. Building the ETL pipeline taught me the importance of data quality and standardization before loading into production systems. The star schema design demonstrated how denormalization improves query performance for analytical workloads compared to normalized OLTP schemas.

## Challenges Faced

1. **Phone Number Standardization**: Raw data had multiple formats (with/without country code, leading zeros). Solved by using regex to extract digits and applying consistent +91-XXXXXXXXXX format.

2. **Foreign Key Integrity in Sales Data**: Some sales referenced customers/products that were dropped during cleaning. Implemented ID mapping system to link CSV IDs to database auto-increment IDs and skip invalid references.

3. **Date Format Parsing**: CSV files contained 7 different date formats (YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY, etc.). Created a function that tries multiple format patterns until one succeeds.

4. **MongoDB vs SQL Mindset**: Shifting from relational thinking to document-oriented design required understanding when to embed vs reference data, and how aggregation pipelines differ from SQL JOINs.
