import sqlite3


class DatabaseService:

    def __init__(self, db_path):

        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False
        )

        self.create_table()

    def create_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS violations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            violation_type TEXT,
            vehicle_number TEXT,
            confidence REAL,
            evidence_path TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """

        self.conn.execute(query)
        self.conn.commit()

    def insert_violation(
        self,
        violation_type,
        vehicle_number,
        confidence,
        evidence_path
    ):

        query = """
        INSERT INTO violations(
            violation_type,
            vehicle_number,
            confidence,
            evidence_path
        )
        VALUES(?,?,?,?)
        """

        self.conn.execute(
            query,
            (
                violation_type,
                vehicle_number,
                confidence,
                evidence_path
            )
        )

        self.conn.commit()

    def get_all_violations(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM violations
            ORDER BY id DESC
            """
        )

        return cursor.fetchall()

    def get_total_violations(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM violations
            """
        )

        return cursor.fetchone()[0]

    def get_violation_count(
        self,
        violation_type
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM violations
            WHERE violation_type = ?
            """,
            (violation_type,)
        )

        return cursor.fetchone()[0]