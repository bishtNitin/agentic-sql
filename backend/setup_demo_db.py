"""
Demo Database Setup Script
Creates sample tables and populates them with demo data
"""
import sqlite3
from datetime import datetime, timedelta
import random
import os

# Database file path
DB_PATH = "demo.db"


def create_tables(conn):
    """Create demo tables"""
    cursor = conn.cursor()
    
    # Employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            department VARCHAR(50),
            salary INTEGER,
            hire_date DATE
        )
    """)
    
    # Departments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL UNIQUE,
            budget INTEGER,
            manager_id INTEGER
        )
    """)
    
    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(50),
            price DECIMAL(10, 2),
            stock INTEGER
        )
    """)
    
    # Customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE,
            city VARCHAR(50),
            registration_date DATE
        )
    """)
    
    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            customer_name VARCHAR(100),
            quantity INTEGER,
            order_date DATE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    
    conn.commit()
    print("Tables created successfully")


def populate_departments(conn):
    """Populate departments table"""
    cursor = conn.cursor()
    
    departments = [
        ("Engineering", 500000, None),
        ("Sales", 300000, None),
        ("Marketing", 250000, None),
        ("Human Resources", 200000, None),
        ("Finance", 350000, None),
    ]
    
    cursor.executemany(
        "INSERT INTO departments (name, budget, manager_id) VALUES (?, ?, ?)",
        departments
    )
    
    conn.commit()
    print(f"Inserted {len(departments)} departments")


def populate_employees(conn):
    """Populate employees table"""
    cursor = conn.cursor()
    
    first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Lisa", 
                   "William", "Jennifer", "James", "Mary", "Richard", "Patricia", "Thomas"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
                  "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez"]
    departments = ["Engineering", "Sales", "Marketing", "Human Resources", "Finance"]
    
    employees = []
    base_date = datetime.now() - timedelta(days=1825)  # 5 years ago
    
    for i in range(50):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        department = random.choice(departments)
        salary = random.randint(40000, 150000)
        hire_date = base_date + timedelta(days=random.randint(0, 1825))
        
        employees.append((name, department, salary, hire_date.strftime("%Y-%m-%d")))
    
    cursor.executemany(
        "INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)",
        employees
    )
    
    conn.commit()
    print(f"Inserted {len(employees)} employees")


def populate_products(conn):
    """Populate products table"""
    cursor = conn.cursor()
    
    products = [
        ("Laptop Pro 15", "Electronics", 1299.99, 45),
        ("Wireless Mouse", "Electronics", 29.99, 150),
        ("USB-C Hub", "Electronics", 49.99, 80),
        ("Desk Chair", "Furniture", 249.99, 30),
        ("Standing Desk", "Furniture", 599.99, 15),
        ("Monitor 27\"", "Electronics", 399.99, 60),
        ("Keyboard Mechanical", "Electronics", 149.99, 90),
        ("Desk Lamp", "Furniture", 79.99, 50),
        ("Notebook Set", "Office Supplies", 19.99, 200),
        ("Pen Pack", "Office Supplies", 9.99, 300),
        ("Webcam HD", "Electronics", 89.99, 70),
        ("Headphones", "Electronics", 199.99, 100),
        ("Office Desk", "Furniture", 449.99, 20),
        ("Filing Cabinet", "Furniture", 179.99, 25),
        ("Whiteboard", "Office Supplies", 89.99, 40),
    ]
    
    cursor.executemany(
        "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
        products
    )
    
    conn.commit()
    print(f"Inserted {len(products)} products")


def populate_customers(conn):
    """Populate customers table"""
    cursor = conn.cursor()
    
    first_names = ["Alex", "Sam", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Avery"]
    last_names = ["Anderson", "Thompson", "White", "Harris", "Martin", "Jackson", "Lee", "Walker"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", 
              "San Antonio", "San Diego", "Dallas", "San Jose"]
    
    customers = []
    base_date = datetime.now() - timedelta(days=730)  # 2 years ago
    
    for i in range(30):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"{name.lower().replace(' ', '.')}.{i}@email.com"  # Add index to ensure uniqueness
        city = random.choice(cities)
        reg_date = base_date + timedelta(days=random.randint(0, 730))
        
        customers.append((name, email, city, reg_date.strftime("%Y-%m-%d")))
    
    cursor.executemany(
        "INSERT INTO customers (name, email, city, registration_date) VALUES (?, ?, ?, ?)",
        customers
    )
    
    conn.commit()
    print(f"Inserted {len(customers)} customers")


def populate_orders(conn):
    """Populate orders table"""
    cursor = conn.cursor()
    
    # Get product IDs and customer names
    cursor.execute("SELECT id FROM products")
    product_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT name FROM customers")
    customer_names = [row[0] for row in cursor.fetchall()]
    
    orders = []
    base_date = datetime.now() - timedelta(days=365)  # 1 year ago
    
    for i in range(100):
        product_id = random.choice(product_ids)
        customer_name = random.choice(customer_names)
        quantity = random.randint(1, 5)
        order_date = base_date + timedelta(days=random.randint(0, 365))
        
        orders.append((product_id, customer_name, quantity, order_date.strftime("%Y-%m-%d")))
    
    cursor.executemany(
        "INSERT INTO orders (product_id, customer_name, quantity, order_date) VALUES (?, ?, ?, ?)",
        orders
    )
    
    conn.commit()
    print(f"Inserted {len(orders)} orders")


def main():
    """Main setup function"""
    print(f"Setting up demo database: {DB_PATH}")
    
    # Remove existing database if it exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Removed existing database")
    
    # Create connection
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Create tables
        create_tables(conn)
        
        # Populate tables
        populate_departments(conn)
        populate_employees(conn)
        populate_products(conn)
        populate_customers(conn)
        populate_orders(conn)
        
        print("\n✓ Demo database setup completed successfully!")
        print(f"  Location: {os.path.abspath(DB_PATH)}")
        print("\nTables created:")
        print("  - employees (50 rows)")
        print("  - departments (5 rows)")
        print("  - products (15 rows)")
        print("  - customers (30 rows)")
        print("  - orders (100 rows)")
        
    except Exception as e:
        print(f"\n✗ Error setting up database: {e}")
        raise
    
    finally:
        conn.close()


if __name__ == "__main__":
    main()
