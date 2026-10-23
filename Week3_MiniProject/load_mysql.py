import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# Find the .env file in the same directory as this script
env_path = Path(__file__).resolve().parent / ".env"

# Load environment variables
load_dotenv(dotenv_path=env_path)


url = URL.create(
    "mysql+pymysql",
    username="root",
    password=os.environ["MYSQL_PASSWORD"],
    host="localhost",
    port=3306,
    database="quickcart_db"
)

engine = create_engine(url)

with engine.connect() as conn:
    result = conn.execute(text("SELECT VERSION()"))
    print("Connected to MySQL:", result.scalar())
    conn.close()