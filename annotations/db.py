import sqlite3
from typing import Optional

class Sentence:
    def __init__(self, database_file="sentences.db"):
        self.database_file = database_file
        self.conn = sqlite3.connect(self.database_file)
        self.table_name = "sentences"

    def _make_cursor(self):
        return self.conn.cursor()

    def create_table(self):
        cursor = self._make_cursor()
        cursor.execute(f"""
                       CREATE TABLE IF NOT EXISTS {self.table_name} (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           original_sentence TEXT NOT NULL,
                           revised_sentence TEXT,
                           commentary TEXT
                           ) 
                       """)
        self.conn.commit()
        cursor.close()

    def _insert(self, 
                cursor: sqlite3.Cursor, 
                original_sentence: Optional[str]=None, 
                revised_sentence: Optional[str]=None, 
                commentary: Optional[str]=None):
        cursor.execute(f"""
                        INSERT INTO {self.table_name} (original_sentence, revised_sentence, commentary)
                       VALUES (?, ?, ?)
                       """, (original_sentence, revised_sentence, commentary))
        self.conn.commit()

    def insert(self, 
                original_sentence: Optional[str]=None, 
                revised_sentence: Optional[str]=None, 
                commentary: Optional[str]=None):
        cursor = self._make_cursor()
        self._insert(cursor, original_sentence, revised_sentence, commentary)
        cursor.close()

    def insert_many(self, objs: list[dict[str, str]]):
        cursor = self._make_cursor()
        cursor.executemany(f"""INSERT INTO {self.table_name} (original_sentence, revised_sentence, commentary)
                            VALUES (?, ?, ?)""", [(i['original_sentence'], i['revised_sentence'], i['commentary']) for i in objs]
                           )
        self.conn.commit()
        cursor.close()


    def _fetch(self, cursor: sqlite3.Cursor, _id: int):
        cursor.execute(f"""
                       SELECT * FROM {self.table_name} WHERE id={_id} 
                       """)
        return cursor.fetchone()

    def fetch(self, _id: int):
        cursor = self._make_cursor()
        return self._fetch(cursor, _id)

    def list(self, page=1):
        initial_item = (10*page)-10
        cursor = self._make_cursor()
        cursor.execute(f"""SELECT * FROM {self.table_name} ORDER BY id ASC LIMIT 10 OFFSET {initial_item}""")
        return cursor.fetchall()

    def list_ids(self, random=False):
        cursor = self._make_cursor()
        query = f"""SELECT id FROM {self.table_name}"""
        if random:
            query += " ORDER BY RANDOM()"
        cursor.execute(query)
        ids = cursor.fetchall()
        return [i[0] for i in ids]

    def update(self, _id: int, revised_sentence: Optional[str] = None, commentary: Optional[str] = None):
        cursor = self._make_cursor()
        
        # Fetch the current record
        current_record = self._fetch(cursor, _id)
        if not current_record:
            cursor.close()
            raise ValueError(f"No record found with id {_id}")

        # Prepare the update query and parameters
        update_fields = []
        update_values = []
        if revised_sentence is not None:
            update_fields.append("revised_sentence = ?")
            update_values.append(revised_sentence)
        if commentary is not None:
            update_fields.append("commentary = ?")
            update_values.append(commentary)

        if not update_fields:
            cursor.close()
            return  # No fields to update

        # Construct and execute the update query
        update_query = f"""
            UPDATE {self.table_name}
            SET {', '.join(update_fields)}
            WHERE id = ?
        """
        update_values.append(_id)
        
        cursor.execute(update_query, update_values)
        self.conn.commit()
        cursor.close()

        return self.fetch(_id)
    
    def count_rows_w_annotations(self):
        cursor = self._make_cursor()
        cursor.execute(f"""SELECT count(*) FROM {self.table_name} WHERE revised_sentence IS NOT NULL""")
        return cursor.fetchone()[0]
