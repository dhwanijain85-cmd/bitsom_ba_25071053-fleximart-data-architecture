# FlexiMart ETL Pipeline - Setup Guide

## FOR MAC USERS - Complete Steps

### 1. Install Python Packages
```bash
pip3 install --break-system-packages pandas mysql-connector-python
```

### 2. Setup MySQL
```bash
# Kill any MySQL processes and restart
pkill -9 mysqld
brew services restart mysql
sleep 3

# Set password to fleximart123
mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'fleximart123';"
```

If that gives an error, run this instead:
```bash
# Stop MySQL
brew services stop mysql

# Start without password
mysqld_safe --skip-grant-tables &
sleep 3

# Set password
mysql -u root -e "FLUSH PRIVILEGES; ALTER USER 'root'@'localhost' IDENTIFIED BY 'fleximart123';"

# Restart MySQL
pkill mysqld
sleep 2
brew services start mysql
sleep 3
```

### 3. Navigate to Part 1 Directory
```bash
cd part1-database-etl
```

### 4. Create Database
```bash
mysql -u root -pfleximart123 < create_database.sql
```

### 5. Run the Pipeline
```bash
python3 etl_pipeline.py
```

### 6. Check Results
```bash
cat data_quality_report.txt
```

---

## FOR WINDOWS USERS - Complete Steps

### 1. Install Python Packages
Open Command Prompt or PowerShell:
```cmd
pip install pandas mysql-connector-python
```

### 2. Setup MySQL

**If MySQL is not installed:**
1. Download from: https://dev.mysql.com/downloads/installer/
2. Install MySQL Server
3. During installation, set root password to: `fleximart123`
4. Complete installation

**If MySQL is already installed:**

Open Command Prompt as Administrator:
```cmd
net stop MySQL
net start MySQL
```

Then set the password:
```cmd
mysql -u root -p
```
(Enter current password, then run):
```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'fleximart123';
exit;
```

### 3. Navigate to Part 1 Directory
```cmd
cd part1-database-etl
```

### 4. Create Database
```cmd
mysql -u root -pfleximart123 < create_database.sql
```

### 5. Run the Pipeline
```cmd
python etl_pipeline.py
```

### 6. Check Results
```cmd
type data_quality_report.txt
```

---

## Troubleshooting

**Error: "Access denied"**
- Make sure password in etl_pipeline.py line 24 is `fleximart123`
- Re-run the MySQL password setup commands

**Error: "Unknown database"**
- Navigate to part1-database-etl folder first: `cd part1-database-etl`
- Run: `mysql -u root -pfleximart123 < create_database.sql`

**Error: "command not found: mysql" (Mac)**
- Install MySQL: `brew install mysql`
- Start it: `brew services start mysql`

**Error: "MySQL service not found" (Windows)**
- Reinstall MySQL from the official website
- Make sure to check "MySQL Server" during installation

## Quick One-Liner (Mac)
```bash
cd part1-database-etl && mysql -u root -pfleximart123 -e "DROP DATABASE IF EXISTS fleximart; CREATE DATABASE fleximart;" && mysql -u root -pfleximart123 fleximart < create_database.sql && python3 etl_pipeline.py
```