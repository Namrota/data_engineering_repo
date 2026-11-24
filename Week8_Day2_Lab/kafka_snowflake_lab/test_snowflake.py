
import os
import getpass
import snowflake.connector

# Snowflake connection configuration
config = {
    "account": os.environ["SNOWFLAKE_ACCOUNT"],
    "user": os.environ["SNOWFLAKE_USER"],
    "warehouse": os.environ["SNOWFLAKE_WAREHOUSE"],
    "role": os.environ["SNOWFLAKE_ROLE"],
    "database": "KAFKA_DEMO",
    "schema": "REALTIME",
}

# Password authentication
config["password"] = getpass.getpass(
    "Enter Snowflake password: "
)

try:
    # Establish connection
    conn = snowflake.connector.connect(**config)

    print("Successfully connected to Snowflake!")

    cursor = conn.cursor()

    # Verify connection and context
    cursor.execute("""
        SELECT
            CURRENT_USER(),
            CURRENT_DATABASE(),
            CURRENT_SCHEMA(),
            CURRENT_WAREHOUSE()
    """)

    print("Connection details:", cursor.fetchone())

    # Check destination table
    cursor.execute("SELECT COUNT(*) FROM ORDERS")

    print("Current order count:", cursor.fetchone()[0])

except Exception as e:
    print("Snowflake connection failed:", e)

finally:
    if "cursor" in locals():
        cursor.close()

    if "conn" in locals():
        conn.close()
