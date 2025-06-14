import psycopg2

try:
    conn = psycopg2.connect(
        dbname="mydb",
        user="postgres",
        password="Dipak4646",
        host="127.0.0.1",
        port="5432"
    )
    print("Successfully connected to the database!")
    conn.close()
except Exception as e:
    print(f"Error connecting to database: {str(e)}") 