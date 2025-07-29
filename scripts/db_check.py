import psycopg2
import os
from dotenv import load_dotenv

# Зарежда .env директно
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("📦 DATABASE_URL:", DATABASE_URL)

try:
    print("⏳ Опит за свързване към базата...")
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Успешна връзка към базата данни!")
    conn.close()
except Exception as e:
    print("❌ Грешка при свързване:")
    print(e)
