import sqlite3


class MyDB:

    def __init__(self, db_name: str, table_name: str) -> None:
        # Establish connection with database
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # Declare table name
        self.t_name = table_name
        # Create table
        self.cursor.execute(
                f'''CREATE TABLE IF NOT EXISTS {self.t_name}
                (id INTEGER PRIMARY KEY, input TEXT, output TEXT)''')
        
        # Check if database is connected/created
        if self.conn:
            print('Databse initialized.\n')

    def add_entry(self, i, o):
        # Add database entry
        self.cursor.execute(f"INSERT INTO {self.t_name} (input, output) VALUES (?, ?)", (i, o))
        print("Entry added")
        self.conn.commit()
    
    def delete_entry(self, entry_id):
        # Delete database entry
        self.cursor.execute(f"DELETE FROM {self.t_name} WHERE id = (?)", (entry_id,))
        print("Entry deleted")
        self.conn.commit()

    def query_db(self):
        # Query database and return rows to view all entries
        self.conn.commit()
        self.cursor.execute(f"SELECT * FROM {self.t_name}")
        rows = self.cursor.fetchall()
        return rows 
        # for row in rows:
        #     print(f"{row[0]}\n")

    def close_db(self):
        # Close connection
        self.conn.commit()
        self.conn.close()
        print("Connection closed.")


