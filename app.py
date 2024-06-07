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
    global db
    while True:
        try:
            db.ping(reconnect=True)
            print("Reconnected to the database.")
            return
        except pymysql.Error as e:
            print(f"Error reconnecting to MySQL database: {e}")
            time.sleep(5)  # Wait for 5 seconds before attempting reconnection

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = connect_to_database()
        if db:
            try:
                with db.cursor() as cursor:
                    query = "SELECT Position FROM employees WHERE Email = %s AND Password = %s"
                    cursor.execute(query, (email, password))
                    position = cursor.fetchone()

                    if position:
                        session['email'] = email
                        if position[0] == 'Manager':
                            return redirect(url_for('manager_dashboard'))
                        elif position[0] == 'employee':
                            return redirect(url_for('employee_dashboard'))
                    else:
                        flash('Invalid email or password', 'error')
            except pymysql.Error as e:
                print(f"Error executing SQL query: {e}")
                flash('An error occurred, please try again later', 'error')
                reconnect_to_database()  # Attempt to reconnect to the database
        else:
            flash('Failed to connect to database', 'error')
    return render_template('login.html')

# Manager dashboard route
@app.route('/manager/dashboard')
def manager_dashboard():
    if 'email' in session:
        # Retrieve data from the database
        # Make sure to use session['email'] to prevent SQL injection
        return render_template('manager_dashboard.html')
    else:
        return redirect(url_for('login'))

# Employee dashboard route
@app.route('/employee/dashboard')
def employee_dashboard():
    if 'email' in session:
        # Retrieve data from the database
        # Make sure to use session['email'] to prevent SQL injection
        return render_template('employee_dashboard.html')
    else:
        return redirect(url_for('login'))

# Production dashboard route
@app.route('/production/dashboard')
def production_dashboard():
    if 'email' in session:
        # Retrieve data from the database
        # Make sure to use session['email'] to prevent SQL injection
        return render_template('production_dashboard.html')
    else:
        return redirect(url_for('login'))

# Sign out route
@app.route('/signout')
def signout():
    session.pop('email', None)
    return redirect(url_for('login'))

# Add product route
@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['productName']
        product_category = request.form['productCategory']
        product_quantity = int(request.form['productQuantity'])
        product_price = float(request.form['productPrice'])

        db = connect_to_database()
        if db:
            try:
                with db.cursor() as cursor:
                    cursor.execute("INSERT INTO products (ProductName, Category, QuantityInStock, UnitPrice) VALUES (%s, %s, %s, %s)", 
                                   (product_name, product_category, product_quantity, product_price))
                    db.commit()
                    flash('Product added successfully', 'success')
            except pymysql.Error as e:
                print(f"Error executing SQL query: {e}")
                flash('An error occurred while adding the product', 'error')
                reconnect_to_database()  # Attempt to reconnect to the database
        else:
            flash('Failed to connect to database', 'error')
        return redirect(url_for('production_dashboard'))

# Get product details route
@app.route('/get_product_details', methods=['POST'])
def get_product_details():
    if request.method == 'POST':
        product_id = request.form['productIdToShow']

        db = connect_to_database()
        if db:
            try:
                with db.cursor() as cursor:
                    cursor.execute("SELECT * FROM products WHERE ProductID = %s", (product_id,))
                    product_details = cursor.fetchone()

                    if product_details:
                        return render_template('product_details.html', product_details=product_details)
                    else:
                        return render_template('product_details.html', error_message="Product not found")
            except pymysql.Error as e:
                print(f"Error executing SQL query: {e}")
                flash('An error occurred while retrieving product details', 'error')
                reconnect_to_database()  # Attempt to reconnect to the database
        else:
            flash('Failed to connect to database', 'error')
    return render_template('product_details.html')

# Finance dashboard route
@app.route('/finance/dashboard')
def finance_dashboard():
    return render_template('finance_dashboard.html')

# Sales dashboard route
@app.route('/sales/dashboard')
def sales_dashboard():
    if 'email' in session:
        # Retrieve data from the database
        # Make sure to use session['email'] to prevent SQL injection
        return render_template('sales_dashboard.html')
    else:
        return redirect(url_for('login'))

# Add customer route
@app.route('/add_customer', methods=['POST'])
def add_customer():
    if request.method == 'POST':
        customer_name = request.form['customerName']
        customer_email = request.form['customerEmail']
        customer_phone = request.form['customerPhone']
        customer_address = request.form['customerAddress']

        db = connect_to_database()
        if db:
            try:
                with db.cursor() as cursor:
                    cursor.execute("INSERT INTO customers (CustomerName, ContactNumber, Email, Address) VALUES (%s, %s, %s, %s)", 
                                   (customer_name, customer_phone, customer_email, customer_address))
                    db.commit()
                    flash('Customer added successfully', 'success')
            except pymysql.Error as e:
                print(f"Error executing SQL query: {e}")
                flash('An error occurred while adding the customer', 'error')
                reconnect_to_database()  # Attempt to reconnect to the database
        else:
            flash('Failed to connect to database', 'error')
        return redirect(url_for('sales_dashboard'))

# Add order route
@app.route('/add_order', methods=['POST'])
def add_order():
    if request.method == 'POST':
        order_date = request.form['orderDate']
        customer_id = request.form['customerId']
        product_id = request.form['productId']
        quantity = int(request.form['quantity'])
        total_amount = float(request.form['totalAmount'])

        db = connect_to_database()
        if db:
            try:
                with db.cursor() as cursor:
                    cursor.execute("INSERT INTO orders (OrderDate, CustomerID, ProductID, Quantity, TotalAmount) VALUES (%s, %s, %s, %s, %s)", 
                                   (order_date, customer_id, product_id, quantity, total_amount))
                    db.commit()
                    flash('Order added successfully', 'success')
            except pymysql.Error as e:
                print(f"Error executing SQL query: {e}")
                flash('An error occurred while adding the order', 'error')
                reconnect_to_database()  # Attempt to reconnect to the database
        else:
            flash('Failed to connect to database', 'error')
        return redirect(url_for('sales_dashboard'))

# HR dashboard route
@app.route('/hr/dashboard')
def hr_dashboard():
    if 'email' in session:
        # Retrieve data from the database
        # Make sure to use session['email'] to prevent SQL injection
        return render_template('hr_dashboard.html')
    else:
        return redirect(url_for('login'))

# Add employee route
@app.route('/add_employee', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        department = request.form['department']
        position = request.form['position']
        gender = request.form['gender']
        dob = request.form['dob']
        password = request.form['password']

        db = connect_to_database()
        if db:
            try:
                with db.cursor() as cursor:
                    cursor.execute("INSERT INTO employees (FirstName, LastName, Email, Phone, Address, Department, Position, Gender, DOB, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                                   (first_name, last_name, email, phone, address, department, position, gender, dob, password))
                    db.commit()
                    flash('Employee added successfully', 'success')
            except pymysql.Error as e:
                print(f"Error executing SQL query: {e}")
                flash('An error occurred while adding the employee', 'error')
                reconnect_to_database()  # Attempt to reconnect to the database
        else:
            flash('Failed to connect to database', 'error')
        return redirect(url_for('hr_dashboard'))

# Get employee details route
@app.route('/get_employee_details', methods=['POST'])
def get_employee_details():
    if request.method == 'POST':
        employee_id = request.form['employeeIdToShow']

        db = connect_to_database()
        if db:
            try:
                with db.cursor() as cursor:
                    cursor.execute("SELECT * FROM employees WHERE EmployeeID = %s", (employee_id,))
                    employee_details = cursor.fetchone()

                    if employee_details:
                        return render_template('employee_details.html', employee_details=employee_details)
                    else:
                        return render_template('employee_details.html', error_message="Employee not found")
            except pymysql.Error as e:
                print(f"Error executing SQL query: {e}")
                flash('An error occurred while retrieving employee details', 'error')
                reconnect_to_database()  # Attempt to reconnect to the database
        else:
            flash('Failed to connect to database', 'error')
    return render_template('employee_details.html')

if __name__ == '__main__':
    app.run(debug=False)

