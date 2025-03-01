import pyodbc

server = "hackusudatafreaks.database.windows.net"
database = "HackUSU25"
username = "dataFreak"
password = "datathon2004!"
driver = "{ODBC Driver 17 for SQL Server}"

conn = pyodbc.connect(
    f"DRIVER={driver};SERVER={server},1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"
)

cursor = conn.cursor()
cursor.execute("SELECT @@VERSION")
row = cursor.fetchone()
print("Connected to:", row[0])

conn.close()
