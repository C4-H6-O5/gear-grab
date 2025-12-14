import sqlite3
import os

def setup_database():
    db_filename = 'geargrab.db'
    schema_filename = 'schema.sql'

    # Check if schema file exists
    if not os.path.exists(schema_filename):
        print(f"Error: '{schema_filename}' not found. Please create it first.")
        return

    try:
        # Connect to database
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        print(f"Connected to {db_filename}...")

        # Read the SQL instructions from the external file
        with open(schema_filename, 'r') as file:
            sql_script = file.read()

        # Execute the script
        cursor.executescript(sql_script)
        conn.commit()
        
        print(f"Success! Database created using instructions from {schema_filename}")
        print("Tables created and sample data inserted.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database()