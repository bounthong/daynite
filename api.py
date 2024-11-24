from flask import Flask, jsonify, request
import pyodbc

# Flask app
app = Flask(__name__)

# Database connection string (hardcoded for local testing)
DB_HOST = "18.234.156.9"
DB_PORT = "1433"
DB_USER = "bounthong"
DB_PASSWORD = "Idlysmaf@$24"
DB_NAME = "DayNite"

def get_db_connection():
    """Establish a connection to the MSSQL database."""
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_HOST},{DB_PORT};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD}"
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
   # app.run(debug=True)
   app.run(host='0.0.0.0', port=5000)
