import sqlite3


class MyDB:

    def __init__(self) -> None:
        pass

    def initialize_database(self, db_name, table_name):
        # Establish connection with database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # Declare table name
        t_name = table_name
        # Create table
        cursor.execute(
                f'''CREATE TABLE IF NOT EXISTS {t_name}
                (id INTEGER PRIMARY KEY, input TEXT, output TEXT)''')
        
        # Check if database is connected/created
        if conn:
            print('Databse initialized.\n')

    def add_entry(self, i, o, db_name, t_name):
        # Establish connection
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if conn:
            print('Connection established\n')

        # Add database entry
        cursor.execute(f"INSERT INTO {t_name} (input, output) VALUES (?, ?)", (i, o))
        print("Entry added\n")
        conn.commit()
    
    def delete_entry(self, entry_id, db_name, t_name):
        # Establish connection
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if conn:
            print('Connection established\n')

        # Delete database entry
        cursor.execute(f"DELETE FROM {t_name} WHERE id = (?)", (entry_id,))
        print("Entry deleted\n")
        conn.commit()

    def query_db(self, db_name, t_name):
        # Establish connection
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if conn:
            print('Connection established\n')

        # Query database and return rows to view all entries
        conn.commit()
        cursor.execute(f"SELECT * FROM {t_name}")
        rows = cursor.fetchall()
        # Print success message
        print('Database query successfull\n')
        return rows 
        # for row in rows:
        #     print(f"{row[0]}\n")

    def close_db(self, db_name, t_name):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Close connection
        conn.commit()
        conn.close()
        print("Connection closed.")


