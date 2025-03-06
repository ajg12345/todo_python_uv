import pathlib
import sqlite3

DATABASE_PATH = pathlib.Path(__file__).parent / "todo.db"

class Database:
    def __init__(self, db_path=DATABASE_PATH):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self.create_table()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS todo(
                item_id INTEGER PRIMARY KEY,
                item TEXT,
                done INTEGER
            );
        """
        self._run_query(query)

    def _run_query(self, query):
        result = self.cursor.execute(query)
        self.db.commit()
        return result
    
    def add_todo_item(self, item):
        query_string = f"INSERT INTO todo VALUES (NULL, '{item}', 0);"
        print(query_string)
        self._run_query(query_string)
    
    def delete_todo_item(self, item_id):
        self._run_query(
            f"DELETE FROM todo WHERE item_id={item_id};",
        )

    def mark_as_done(self, item_id):
        self._run_query(
            f"UPDATE todo SET done=1 WHERE item_id={item_id};",
        )

    def retrieve_all_items(self):
        result = self._run_query("SELECT * FROM todo;")
        returned_items = result.fetchall()
        return returned_items