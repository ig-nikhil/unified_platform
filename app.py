from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Establish database connection
def connect_to_database():
    try:
        db = pymysql.connect(
            host="149.100.151.103",
            user="u212553073_nikhil_pro1",
            password="l!LWR!R@p8",
            database="u212553073_nikhil_pro1"
        )
        return db
    except pymysql.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# Reconnect to the database if connection is lost
def reconnect_to_database():
    global db, cursor
    while True:
        try:
            db.ping(reconnect=True)
            print("Reconnected to the database.")
            cursor = db.cursor()
            return
        except pymysql.Error as e:
            print(f"Error reconnecting to MySQL database: {e}")
            time.sleep(5)  # Wait for 5 seconds before attempting reconnection

# Helper function to execute queries with reconnection logic
def execute_query(query, args=None):
    global db, cursor
    try:
        cursor.execute(query, args)
    except (pymysql.err.OperationalError, pymysql.err.InterfaceError):
        reconnect_to_database()
        cursor.execute(query, args)

User_Email = ""
# Initialize database connection and cursor
db = connect_to_database()
cursor = db.cursor()
reconnect_to_database()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

# Validate login credentials and redirect to appropriate dashboard
@app.route('/login', methods=['POST'])
def login():
    global User_Email
    email = request.form['email']
    password = request.form['password']

    # Check if user exists and credentials are correct
    query = "SELECT Position FROM employees WHERE Email = %s AND Password = %s"
    execute_query(query, (email, password))
    position = cursor.fetchone()

    if position:
        User_Email = email
        # Check position of the employee and redirect to the appropriate dashboard
        if position[0] == 'Manager':
            return redirect(url_for('manager_dashboard'))
        elif position[0] == 'employee':
            return redirect(url_for('employee_dashboard'))
    else:
        # If user credentials are incorrect, render the login form again
        return render_template('login.html', message="Invalid credentials")

@app.route('/signout')
def signout():
    global User_Email
    User_Email = ""
    return redirect(url_for('login'))

# Manager dashboard route
@app.route('/manager/dashboard')
def manager_dashboard():
    if User_Email:
        # Fetch user data from the Employees table
        user_query = "SELECT FirstName, LastName,Position FROM employees WHERE Email = %s"
        execute_query(user_query, (User_Email,))
        user_data = cursor.fetchone()
        execute_query("SELECT * FROM customers")
        dataCustomers = cursor.fetchall()
        execute_query("Select * from employees")
        dataEmployees = cursor.fetchall()
        execute_query("Select * from transactions")
        dataTransactions = cursor.fetchall()
        execute_query("Select * from products")
        dataProducts = cursor.fetchall()
        execute_query("Select * from suppliers")
        dataSuppliers = cursor.fetchall()
        execute_query("select sum(TotalAmount)  from orders")
        totalsales = cursor.fetchone()[0]
        execute_query(" select count(*) from employees")
        totalemployees = cursor.fetchone()[0]
        execute_query(" select count(*) from customers")
        totalcustomers = cursor.fetchone()[0]
        execute_query("SELECT c.CustomerName, p.ProductName, o.OrderDate FROM orders o JOIN customers c ON o.CustomerID = c.CustomerID JOIN products p ON o.ProductID = p.ProductID ORDER BY o.OrderDate DESC LIMIT 3 ")
        recentorders = cursor.fetchall()

        if user_data:
            user_name = f"{user_data[0]} {user_data[1]} "
            position = f"{user_data[2]}"
            return render_template('manager_dashboard.html', user_name=user_name, position=position, dataCustomers=dataCustomers,
                                   dataEmployees=dataEmployees, dataProducts=dataProducts, dataTransactions=dataTransactions,
                                   dataSuppliers=dataSuppliers, totalsales=totalsales, recentorders=recentorders,
                                   totalemployees=totalemployees, totalcustomers=totalcustomers)
    
    return render_template('login.html')

# Employee dashboard route
@app.route('/employee/dashboard')
def employee_dashboard():
    if User_Email:
        # Fetch user data from the Employees table
        user_query = "SELECT FirstName, LastName, Department FROM employees WHERE Email = %s"
        execute_query(user_query, (User_Email,))
        user_data = cursor.fetchone()

        if user_data:
            department = user_data[2]
            if department == 'Production':
                return redirect(url_for('production_dashboard'))
            elif department == 'Finance':
                return redirect(url_for('finance_dashboard'))
            elif department == 'Sales':
                return redirect(url_for('sales_dashboard'))
            elif department == 'HR':
                return redirect(url_for('hr_dashboard'))

    return render_template('login.html')

# Production department dashboard route
@app.route('/production/dashboard')
def production_dashboard():
    user_query = "SELECT FirstName, LastName,Position FROM employees WHERE Email = %s"
    execute_query(user_query, (User_Email,))
    user_data = cursor.fetchone()
    user_name = f"{user_data[0]} {user_data[1]} "
    position = f"{user_data[2]}"
    execute_query('SELECT count(ProductID) FROM products')
    daysales = cursor.fetchone()
    execute_query('SELECT sum(Quantity),sum(TotalAmount) FROM orders WHERE YEAR(OrderDate) = YEAR(CURDATE()) AND MONTH(OrderDate) = MONTH(CURDATE()) ')
    monthsales = cursor.fetchone()
    execute_query('SELECT sum(Quantity),sum(TotalAmount) FROM orders  WHERE YEAR(OrderDate) = YEAR(CURDATE()) ')
    yearsales = cursor.fetchone()

    return render_template('production_dashboard.html', user_name=user_name, position=position, daysales=daysales, monthsales=monthsales, yearsales=yearsales)

@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        # Extract form data
        product_name = request.form['productName']  # Corrected key to match the form
        product_category = request.form['productCategory']  # Corrected key to match the form
        product_quantity = int(request.form['productQuantity'])  # Ensure conversion to integer
        product_price = float(request.form['productPrice'])  # Ensure conversion to float

        # Insert data into the products table
        execute_query("INSERT INTO products (ProductName, Category, QuantityInStock, UnitPrice) VALUES (%s, %s, %s, %s)", 
                      (product_name, product_category, product_quantity, product_price))
        db.commit()

        # Redirect to the sales dashboard after adding the product
        return redirect(url_for('production_dashboard'))

@app.route('/get_product_details', methods=['POST'])
def get_product_details():
    if request.method == 'POST':
        # Extract the product ID from the form data
        product_id = request.form['productIdToShow']

        # Fetch product details from the database
        execute_query("SELECT * FROM products WHERE ProductID = %s", (product_id,))
        product_details = cursor.fetchone()

        if product_details:
            # Render the template with the product details
            return render_template('product_details.html', product_details=product_details)
        else:
            # If product not found, return an error message
            return render_template('product_details.html', error_message="Product not found")

# Finance department dashboard route
@app.route('/finance/dashboard')
def finance_dashboard():
    return render_template('finance_dashboard.html')

# Sales department dashboard route
@app.route('/sales/dashboard')
def sales_dashboard():
    user_query = "SELECT FirstName, LastName,Position FROM employees WHERE Email = %s"
    execute_query(user_query, (User_Email,))
    user_data = cursor.fetchone()
    user_name = f"{user_data[0]} {user_data[1]} "
    position = f"{user_data[2]}"
    execute_query('SELECT sum(Quantity),sum(TotalAmount) FROM orders WHERE OrderDate = CURDATE()')
    daysales = cursor.fetchone()
    execute_query('SELECT sum(Quantity),sum(TotalAmount) FROM orders WHERE YEAR(OrderDate) = YEAR(CURDATE()) AND MONTH(OrderDate) = MONTH(CURDATE()) ')
    monthsales = cursor.fetchone()
    execute_query('SELECT sum(Quantity),sum(TotalAmount) FROM orders  WHERE YEAR(OrderDate) = YEAR(CURDATE()) ')
    yearsales = cursor.fetchone()
    execute_query('Select * from orders')
    dataOrders = cursor.fetchall()
    execute_query('Select * from customers')
    dataCustomers = cursor.fetchall()

    return render_template('sales_dashboard.html', user_name=user_name, position=position, daysales=daysales, monthsales=monthsales, yearsales=yearsales,
                           dataOrders=dataOrders, dataCustomers=dataCustomers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    if request.method == 'POST':
        # Extract form data
        customer_name = request.form['customerName']
        customer_email = request.form['customerEmail']
        customer_phone = request.form['customerPhone']
        customer_address = request.form['customerAddress']

        # Insert data into the customers table
        execute_query("INSERT INTO customers (CustomerName, ContactNumber, Email, Address) VALUES (%s, %s, %s, %s)", (customer_name, customer_phone, customer_email, customer_address))
        db.commit()

        # Redirect to the sales dashboard after adding the customer
        return redirect(url_for('sales_dashboard'))

@app.route('/add_order', methods=['POST'])
def add_order():
    if request.method == 'POST':
        # Extract form data
        order_date = request.form['orderDate']
        customer_id = request.form['customerID']
        product_id = request.form['productID']
        quantity = request.form['quantity']
        total_amount = request.form['totalAmount']

        # Insert data into the orders table
        try:
            execute_query("INSERT INTO orders (OrderDate, CustomerID, ProductID, Quantity, TotalAmount) VALUES (%s, %s, %s, %s, %s)", (order_date, customer_id, product_id, quantity, total_amount))
            db.commit()
            return "Order added successfully!", 200
        except Exception as e:
            print("Error:", e)
            db.rollback()
            return "Failed to add order."

# HR department dashboard route
@app.route('/hr/dashboard')
def hr_dashboard():
    execute_query("Select * from employees")
    dataEmployees = cursor.fetchall()
    user_query = "SELECT FirstName, LastName,Position FROM employees WHERE Email = %s"
    execute_query(user_query, (User_Email,))
    user_data = cursor.fetchone()
    user_name = f"{user_data[0]} {user_data[1]} "
    position = f"{user_data[2]}"
    execute_query('SELECT count(*) FROM employees ')
    totalEmployees = cursor.fetchone()
    execute_query('SELECT count(*) FROM employees where position="Manager" ')
    totalManagers = cursor.fetchone()
    execute_query('SELECT count(*) FROM employees where Gender="Female" ')
    totalFemales = cursor.fetchone()

    return render_template('hr_dashboard.html', dataEmployees=dataEmployees, user_name=user_name,
                           position=position, totalEmployees=totalEmployees, totalManagers=totalManagers, totalFemales=totalFemales)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        # Extract form data
        employee_first_name = request.form['employeeFirstName']
        employee_last_name = None
        employee_date_of_birth = None
        employee_gender = request.form['employeeGender']
        employee_department = request.form['employeeDepartment']
        employee_position = request.form['employeePosition']
        employee_salary = request.form['employeeSalary']
        employee_password = None
        employee_email = request.form['employeeEmail']

        # Insert data into the Employees table
        execute_query("INSERT INTO employees (FirstName, LastName, DateOfBirth, Gender, Department, Position, Salary, Password, Email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (employee_first_name, employee_last_name, employee_date_of_birth, employee_gender, employee_department, employee_position, employee_salary, employee_password, employee_email))
        db.commit()

        # Redirect to the manager dashboard or any other page as needed
        return redirect(url_for('hr_dashboard'))

@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    if request.method == 'POST':
        # Get the employee ID from the request form data and parse it as an integer
        employee_id = int(request.form.get('deleteEmployeeID'))

        # Perform the deletion operation
        delete_query = "DELETE FROM employees WHERE EmployeeID = %s"
        execute_query(delete_query, (employee_id,))
        db.commit()

        # Optionally, you can return a response to indicate success
        return 'Employee deleted successfully'

if __name__ == '__main__':
    app.run(debug=False)
