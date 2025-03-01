import pyodbc
class SQL:
    def __init__(self):
        self.server = "hackusudatafreaks.database.windows.net"
        self.database = "HackUSU25"
        self.username = "dataFreak"
        self.password = "datathon2004!"
        self.driver = "{ODBC Driver 17 for SQL Server}"
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = pyodbc.connect(
            f"DRIVER={self.driver};SERVER={self.server},1433;DATABASE={self.database};UID={self.username};PWD={self.password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT @@VERSION")
        row = self.cursor.fetchone()
        print("Connected to:", row[0])

    def query(self, offset, batch_size):
        query = f"""
        SELECT * FROM RpoPlan ORDER BY (select Null) OFFSET {offset} ROWS FETCH NEXT {batch_size} ROWS ONLY;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()
