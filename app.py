from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql
from pymysql.err import InterfaceError

app = Flask(__name__)

User_Email = ""

def get_db_connection():
    try:
        connection = pymysql.connect(
            host="149.100.151.103",
            user="u212553073_nikhil_pro1",
            password="l!LWR!R@p8",
            database="u212553073_nikhil_pro1"
        )
        return connection
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

db = get_db_connection()
cursor = db.cursor() if db else None

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    global User_Email
    email = request.form['email']
    password = request.form['password']

    # Check if connection is still open, otherwise reconnect
    global db, cursor
    try:
        cursor.execute("SELECT 1")
    except (InterfaceError, AttributeError):
        db = get_db_connection()
        cursor = db.cursor() if db else None

    if cursor:
        # Check if user exists and credentials are correct
        query = "SELECT Position FROM Employees WHERE Email = %s AND Password = %s"
        cursor.execute(query, (email, password))
        position = cursor.fetchone()

        if position:
            User_Email = email
            if position[0] == 'Manager':
                return redirect(url_for('manager_dashboard'))
            elif position[0] == 'employee':
                return redirect(url_for('employee_dashboard'))
        else:
            return render_template('login.html', message="Invalid credentials")
    else:
        return render_template('login.html', message="Database connection error")

@app.route('/signout')
def signout():
    global User_Email
    User_Email = ""
    return redirect(url_for('login'))

@app.route('/manager/dashboard')
def manager_dashboard():
    if User_Email:
        user_query = "SELECT FirstName, LastName, Position FROM Employees WHERE Email = %s"
        cursor.execute(user_query, (User_Email,))
        user_data = cursor.fetchone()

        if user_data:
            user_name = f"{user_data[0]} {user_data[1]}"
            position = f"{user_data[2]}"
            # Fetching data for the dashboard
            cursor.execute("SELECT * FROM customers")
            dataCustomers = cursor.fetchall()
            cursor.execute("SELECT * FROM employees")
            dataEmployees = cursor.fetchall()
            cursor.execute("SELECT * FROM transactions")
            dataTransactions = cursor.fetchall()
            cursor.execute("SELECT * FROM products")
            dataProducts = cursor.fetchall()
            cursor.execute("SELECT * FROM suppliers")
            dataSuppliers = cursor.fetchall()
            cursor.execute("SELECT SUM(TotalAmount) FROM orders")
            totalsales = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM employees")
            totalemployees = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM customers")
            totalcustomers = cursor.fetchone()[0]
            cursor.execute("""SELECT c.CustomerName, p.ProductName, o.OrderDate 
                              FROM orders o 
                              JOIN customers c ON o.CustomerID = c.CustomerID 
                              JOIN products p ON o.ProductID = p.ProductID 
                              ORDER BY o.OrderDate DESC LIMIT 3""")
            recentorders = cursor.fetchall()

            return render_template('manager_dashboard.html', user_name=user_name, position=position, dataCustomers=dataCustomers,
                                   dataEmployees=dataEmployees, dataProducts=dataProducts, dataTransactions=dataTransactions,
                                   dataSuppliers=dataSuppliers, totalsales=totalsales, recentorders=recentorders,
                                   totalemployees=totalemployees, totalcustomers=totalcustomers)
    return render_template('login.html')

@app.route('/employee/dashboard')
def employee_dashboard():
    if User_Email:
        user_query = "SELECT FirstName, LastName, Department FROM employees WHERE Email = %s"
        cursor.execute(user_query, (User_Email,))
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

@app.route('/production/dashboard')
def production_dashboard():
    user_query = "SELECT FirstName, LastName, Position FROM Employees WHERE Email = %s"
    cursor.execute(user_query, (User_Email,))
    user_data = cursor.fetchone()
    user_name = f"{user_data[0]} {user_data[1]}"
    position = f"{user_data[2]}"
    cursor.execute('SELECT COUNT(ProductID) FROM products')
    daysales = cursor.fetchone()
    cursor.execute('SELECT SUM(Quantity), SUM(TotalAmount) FROM orders WHERE YEAR(OrderDate) = YEAR(CURDATE()) AND MONTH(OrderDate) = MONTH(CURDATE())')
    monthsales = cursor.fetchone()
    cursor.execute('SELECT SUM(Quantity), SUM(TotalAmount) FROM orders WHERE YEAR(OrderDate) = YEAR(CURDATE())')
    yearsales = cursor.fetchone()

    return render_template('production_dashboard.html', user_name=user_name, position=position, daysales=daysales, monthsales=monthsales, yearsales=yearsales)

@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['productName']
        product_category = request.form['productCategory']
        product_quantity = int(request.form['productQuantity'])
        product_price = float(request.form['productPrice'])

        cursor.execute("INSERT INTO products (ProductName, Category, QuantityInStock, UnitPrice) VALUES (%s, %s, %s, %s)", 
                       (product_name, product_category, product_quantity, product_price))
        db.commit()

        return redirect(url_for('production_dashboard'))

@app.route('/get_product_details', methods=['POST'])
def get_product_details():
    if request.method == 'POST':
        product_id = request.form['productIdToShow']

        cursor.execute("SELECT * FROM products WHERE ProductID = %s", (product_id,))
        product_details = cursor.fetchone()

        if product_details:
            return render_template('product_details.html', product_details=product_details)
        else:
            return render_template('product_details.html', error_message="Product not found")

@app.route('/finance/dashboard')
def finance_dashboard():
    return render_template('finance_dashboard.html')

@app.route('/sales/dashboard')
def sales_dashboard():
    user_query = "SELECT FirstName, LastName, Position FROM Employees WHERE Email = %s"
    cursor.execute(user_query, (User_Email,))
    user_data = cursor.fetchone()
    user_name = f"{user_data[0]} {user_data[1]}"
    position = f"{user_data[2]}"
    cursor.execute('SELECT SUM(Quantity), SUM(TotalAmount) FROM orders WHERE OrderDate = CURDATE()')
    daysales = cursor.fetchone()
    cursor.execute('SELECT SUM(Quantity), SUM(TotalAmount) FROM orders WHERE YEAR(OrderDate) = YEAR(CURDATE()) AND MONTH(OrderDate) = MONTH(CURDATE())')
    monthsales = cursor.fetchone()
    cursor.execute('SELECT SUM(Quantity), SUM(TotalAmount) FROM orders WHERE YEAR(OrderDate) = YEAR(CURDATE())')
    yearsales = cursor.fetchone()
    cursor.execute('SELECT * FROM orders')
    dataOrders = cursor.fetchall()
    cursor.execute('SELECT * FROM customers')
    dataCustomers = cursor.fetchall()

    return render_template('sales_dashboard.html', user_name=user_name, position=position, daysales=daysales, monthsales=monthsales, yearsales=yearsales, dataOrders=dataOrders, dataCustomers=dataCustomers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    if request.method == 'POST':
        customer_name = request.form['customerName']
        customer_email = request.form['customerEmail']
        customer_phone = request.form['customerPhone']
        customer_address = request.form['customerAddress']

        cursor.execute("INSERT INTO customers (CustomerName, ContactNumber, Email, Address) VALUES (%s, %s, %s, %s)", 
                       (customer_name, customer_phone, customer_email, customer_address))
        db.commit()

        return redirect(url_for('sales_dashboard'))

@app.route('/add_order', methods=['POST'])
def add_order():
    if request.method == 'POST':
        order_date = request.form['orderDate']
        customer_id = request.form['customerId']
        product_id = request.form['productId']
        quantity = int(request.form['quantity'])
        total_amount = float(request.form['totalAmount'])

        cursor.execute("INSERT INTO orders (OrderDate, CustomerID, ProductID, Quantity, TotalAmount) VALUES (%s, %s, %s, %s, %s)", 
                       (order_date, customer_id, product_id, quantity, total_amount))
        db.commit()

        return redirect(url_for('sales_dashboard'))

@app.route('/hr/dashboard')
def hr_dashboard():
    user_query = "SELECT FirstName, LastName, Position FROM Employees WHERE Email = %s"
    cursor.execute(user_query, (User_Email,))
    user_data = cursor.fetchone()
    user_name = f"{user_data[0]} {user_data[1]}"
    position = f"{user_data[2]}"
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    return render_template('hr_dashboard.html', user_name=user_name, position=position, employees=employees)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        phone = request.form['phone']
        position = request.form['position']
        department = request.form['department']

        cursor.execute("INSERT INTO employees (FirstName, LastName, Email, ContactNumber, Position, Department) VALUES (%s, %s, %s, %s, %s, %s)", 
                       (first_name, last_name, email, phone, position, department))
        db.commit()

        return redirect(url_for('hr_dashboard'))

@app.route('/get_employee_details', methods=['POST'])
def get_employee_details():
    if request.method == 'POST':
        employee_id = request.form['employeeIdToShow']

        cursor.execute("SELECT * FROM employees WHERE EmployeeID = %s", (employee_id,))
        employee_details = cursor.fetchone()

        if employee_details:
            return render_template('employee_details.html', employee_details=employee_details)
        else:
            return render_template('employee_details.html', error_message="Employee not found")

@app.route('/suppliers/dashboard')
def suppliers_dashboard():
    user_query = "SELECT FirstName, LastName, Position FROM Employees WHERE Email = %s"
    cursor.execute(user_query, (User_Email,))
    user_data = cursor.fetchone()
    user_name = f"{user_data[0]} {user_data[1]}"
    position = f"{user_data[2]}"
    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()

    return render_template('suppliers_dashboard.html', user_name=user_name, position=position, suppliers=suppliers)

@app.route('/add_supplier', methods=['POST'])
def add_supplier():
    if request.method == 'POST':
        supplier_name = request.form['supplierName']
        contact_number = request.form['contactNumber']
        email = request.form['email']
        address = request.form['address']

        cursor.execute("INSERT INTO suppliers (SupplierName, ContactNumber, Email, Address) VALUES (%s, %s, %s, %s)", 
                       (supplier_name, contact_number, email, address))
        db.commit()

        return redirect(url_for('suppliers_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
