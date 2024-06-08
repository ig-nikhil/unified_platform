import mysql.connector

def check_db_connection():
    try:
        # Connect to MySQL database
        db = mysql.connector.connect(
            host="sql12.freemysqlhosting.net",
            user="u212553073_nikhil_pro1",
            password="l!LWR!R@p8",
            database="u212553073_nikhil_pro1"
        )
        
        # If connection is successful, print success message
        print("Database connection established successfully.")
        # Close the connection
        db.close()
    except mysql.connector.Error as err:
        # If connection fails, print the error message
        print("Error connecting to database:", err)

if __name__ == "__main__":
    check_db_connection()
