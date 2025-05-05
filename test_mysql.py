import os
import traceback
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

print("→ test_mysql:", os.getcwd(), " | USER:", os.getenv("DB_USER"))
load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

try:
    print("🔌 Attempting connection...")
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user=user,
        password=password,
        database="postdb",
        connection_timeout=5,  # force error if hangs
        auth_plugin="caching_sha2_password",
        use_pure=True
    )
    print("test_mysql: connected!")
    conn.close()
except Error as e:
    print("❌ MySQL Error:", e)
    traceback.print_exc()
except Exception as e:
    print("❌ Other Error:", e)
    traceback.print_exc()

print("🏁 Script end")