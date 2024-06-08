








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
    cursor.execute(query, (email, password))
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
# Manager dashboard route
@app.route('/manager/dashboard')
def manager_dashboard():
    if User_Email:
        # Fetch user data from the Employees table
        user_query = "SELECT FirstName, LastName,Position FROM employees WHERE Email = %s"
        cursor.execute(user_query, (User_Email,))
        user_data = cursor.fetchone()
        cursor.execute("SELECT * FROM customers")
        dataCustomers = cursor.fetchall()
        cursor.execute("Select * from employees")
        dataEmployees = cursor.fetchall()
        cursor.execute("Select * from transactions")
        dataTransactions = cursor.fetchall()
        cursor.execute("Select * from products")
        dataProducts = cursor.fetchall()
        cursor.execute("Select * from suppliers")
        dataSuppliers = cursor.fetchall()
        cursor.execute("select sum(TotalAmount)  from orders")
        totalsales = cursor.fetchone()[0]
        cursor.execute(" select count(*) from employees")
        totalemployees = cursor.fetchone()[0]
        cursor.execute(" select count(*) from customers")
        totalcustomers = cursor.fetchone()[0]
        cursor.execute("SELECT c.CustomerName, p.ProductName, o.OrderDate FROM orders o JOIN customers c ON o.CustomerID = c.CustomerID JOIN products p ON o.ProductID = p.ProductID ORDER BY o.OrderDate DESC LIMIT 3 ")
        recentorders =cursor.fetchall()
        # cursor.execute("Select * from inventory")
        # dataEmployees = cursor.fetchall()



        if user_data:
            user_name = f"{user_data[0]} {user_data[1]} "
            position = f"{user_data[2]}"
            return render_template('manager_dashboard.html', user_name=user_name,position=position,dataCustomers=dataCustomers,
                                   dataEmployees=dataEmployees,dataProducts=dataProducts,dataTransactions=dataTransactions,
                                   dataSuppliers=dataSuppliers,totalsales=totalsales,recentorders=recentorders,
                                   totalemployees=totalemployees,totalcustomers=totalcustomers)
    
    return render_template('login.html')


# Employee dashboard route
@app.route('/employee/dashboard')
def employee_dashboard():
    if User_Email:
        # Fetch user data from the Employees table
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

# Production department dashboard route
@app.route('/production/dashboard')
def production_dashboard():
    user_query = "SELECT FirstName, LastName,Position FROM employees WHERE Email = %s"
    cursor.execute(user_query, (User_Email,))
    user_data = cursor.fetchone()
    user_name = f"{user_data[0]} {user_data[1]} "
    position = f"{user_data[2]}"
    cursor.execute('SELECT count(ProductID) FROM products')
    daysales = cursor.fetchone()
    cursor.execute('SELECT sum(Quantity),sum(TotalAmount) FROM orders WHERE YEAR(OrderDate) = YEAR(CURDATE()) AND MONTH(OrderDate) = MONTH(CURDATE()) ')
    monthsales = cursor.fetchone()
    cursor.execute('SELECT sum(Quantity),sum(TotalAmount) FROM orders  WHERE YEAR(OrderDate) = YEAR(CURDATE()) ')
    yearsales = cursor.fetchone()
   # cursor.execute('Select * from orders')
   # dataOrders=cursor.fetchall()
   # cursor.execute('Select * from customers')
   # dataCustomers = cursor.fetchall()
    
    return render_template('production_dashboard.html',user_name=user_name,position=position,daysales=daysales,monthsales=monthsales,yearsales=yearsales)

from flask import request, redirect, url_for

@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        # Extract form data
        product_name = request.form['productName']  # Corrected key to match the form
        product_category = request.form['productCategory']  # Corrected key to match the form
        product_quantity = int(request.form['productQuantity'])  # Ensure conversion to integer
        product_price = float(request.form['productPrice'])  # Ensure conversion to float

        # Insert data into the products table
        cursor.execute("INSERT INTO products (ProductName, Category, QuantityInStock, UnitPrice) VALUES (%s, %s, %s, %s)", 
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
        cursor.execute("SELECT * FROM products WHERE ProductID = %s", (product_id,))
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
    cursor.execute(user_query, (User_Email,))
    user_data = cursor.fetchone()
    user_name = f"{user_data[0]} {user_data[1]} "
    position = f"{user_data[2]}"
    cursor.execute('SELECT sum(Quantity),sum(TotalAmount) FROM orders WHERE OrderDate = CURDATE()')
    daysales = cursor.fetchone()
    cursor.execute('SELECT sum(Quantity),sum(TotalAmount) FROM orders WHERE YEAR(OrderDate) = YEAR(CURDATE()) AND MONTH(OrderDate) = MONTH(CURDATE()) ')
    monthsales = cursor.fetchone()
    cursor.execute('SELECT sum(Quantity),sum(TotalAmount) FROM orders  WHERE YEAR(OrderDate) = YEAR(CURDATE()) ')
    yearsales = cursor.fetchone()
    cursor.execute('Select * from orders')
    dataOrders=cursor.fetchall()
    cursor.execute('Select * from customers')
    dataCustomers = cursor.fetchall()
    
    return render_template('sales_dashboard.html',user_name=user_name,position=position,daysales=daysales,monthsales=monthsales,yearsales=yearsales,
                           dataOrders=dataOrders,dataCustomers=dataCustomers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    if request.method == 'POST':
        # Extract form data
        customer_name = request.form['customerName']
        customer_email = request.form['customerEmail']
        customer_phone = request.form['customerPhone']
        customer_address = request.form['customerAddress']

        # Insert data into the customers table
        cursor.execute("INSERT INTO customers (CustomerName, ContactNumber, Email, Address) VALUES (%s, %s, %s, %s)", (customer_name, customer_phone, customer_email, customer_address))
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
            cursor.execute("INSERT INTO orders (OrderDate, CustomerID, ProductID, Quantity, TotalAmount) VALUES (%s, %s, %s, %s, %s)", (order_date, customer_id, product_id, quantity, total_amount))
            db.commit()
            return "Order added successfully!", 200
        except Exception as e:
            print("Error:", e)
            db.rollback()
            return "Failed to add order.",


# HR department dashboard route
@app.route('/hr/dashboard')
def hr_dashboard():
    cursor.execute("Select * from employees")
    dataEmployees = cursor.fetchall()
    user_query = "SELECT FirstName, LastName,Position FROM employees WHERE Email = %s"
    cursor.execute(user_query, (User_Email,))
    user_data = cursor.fetchone()
    user_name = f"{user_data[0]} {user_data[1]} "
    position = f"{user_data[2]}"
    cursor.execute('SELECT count(*) FROM employees ')
    totalEmployees = cursor.fetchone()
    cursor.execute('SELECT count(*) FROM employees where position="Manager" ')
    totalManagers = cursor.fetchone()
    cursor.execute('SELECT count(*) FROM employees where Gender="Female" ')
    totalFemales = cursor.fetchone()

    return render_template('hr_dashboard.html',dataEmployees=dataEmployees,user_name=user_name,
                           position=position,totalEmployees=totalEmployees,totalManagers=totalManagers,totalFemales=totalFemales
                           )

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
        cursor.execute("INSERT INTO employees (FirstName, LastName, DateOfBirth, Gender, Department, Position, Salary, Password, Email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (employee_first_name, employee_last_name, employee_date_of_birth, employee_gender, employee_department, employee_position, employee_salary, employee_password, employee_email))
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
        cursor.execute(delete_query, (employee_id,))
        db.commit()

        # Optionally, you can return a response to indicate success
        return 'Employee deleted successfully'

if __name__ == '__main__':
    app.run(debug=True)