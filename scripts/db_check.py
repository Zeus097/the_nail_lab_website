import os
import psycopg2
from urllib.parse import urlparse

database_url = os.getenv("DATABASE_URL")

print("📦 DATABASE_URL:", database_url)

try:
    print("⏳ Опит за свързване към базата...")
    result = urlparse(database_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=hostname,
        port=port,
        sslmode='require'
    )
    print("✅ Успешна връзка с базата данни.")
    conn.close()

except Exception as e:
    print("❌ Грешка при свързване:")
    print(e)
