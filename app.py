from flask import Flask, jsonify
import pyodbc
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Flask app
app = Flask(__name__)

# Database connection string
def get_db_connection():
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_HOST')},{os.getenv('DB_PORT')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')}"
    )
    return pyodbc.connect(connection_string)

@app.route('/employees', methods=['GET'])
def get_employees():
    """Fetch employees from the database."""
    employee_id = request.args.get('EmployeeID')  # Get query parameter

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch all employees or a specific employee based on the query parameter
        if employee_id:
            query = "SELECT EmployeeID, EmployeeName FROM dbo.Employee WHERE EmployeeID = ?"
            cursor.execute(query, employee_id)
        else:
            query = "SELECT EmployeeID, EmployeeName FROM dbo.Employee"
            cursor.execute(query)

        rows = cursor.fetchall()

        # Transform query result to a list of dictionaries
        employees = [
            {"EmployeeID": row.EmployeeID, "EmployeeName": row.EmployeeName}
            for row in rows
        ]

        # If employee_id is provided but no result found
        if employee_id and not employees:
            return jsonify({"error": f"No employee found with EmployeeID {employee_id}"}), 404

        return jsonify(employees), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    app.run(debug=True)
