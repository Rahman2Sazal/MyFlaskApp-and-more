import os
from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    # These environment variables will be handy when linking containers later
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "secretpass"),
        database=os.getenv("DB_NAME", "testdb")
    )


 
@app.route('/')
def home():
    return "CI/CD Pipeline Demo App"
    
@app.route('/version')
def version():
    return jsonify({"version": "2.0"})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


@app.route('/datetime')
def get_datetime():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Note: Using the exact query requested in the prompt
        cursor.execute("SELECT CURRENT_TIMESTAMP();")
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            "status": "success",
            "mysql_timestamp": result[0]
        })
    except Error as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)