
import os
import json
import getpass

import snowflake.connector
from confluent_kafka import Consumer


# 1. Connect to Snowflake
config = {
    "account": os.environ["SNOWFLAKE_ACCOUNT"],
    "user": os.environ["SNOWFLAKE_USER"],
    "warehouse": os.environ["SNOWFLAKE_WAREHOUSE"],
    "role": os.environ["SNOWFLAKE_ROLE"],
    "database": "KAFKA_DEMO",
    "schema": "REALTIME",
    "autocommit": False,
}

if os.getenv("SNOWFLAKE_AUTHENTICATOR") == "externalbrowser":
    config["authenticator"] = "externalbrowser"
else:
    config["password"] = getpass.getpass("Snowflake password: ")

conn = snowflake.connector.connect(**config)
cursor = conn.cursor()

print("Connected to Snowflake!")


# 2. Configure Kafka consumer
consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "snowflake-orders-v1",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
})

consumer.subscribe(["ecommerce_orders"])

# 3. Parameterized, duplicate-resistant insertion
merge_sql = """
MERGE INTO KAFKA_DEMO.REALTIME.ORDERS AS target
USING (
    SELECT
        %s AS ORDER_ID,
        %s AS CUSTOMER_NAME,
        %s AS CITY,
        %s AS PRODUCT,
        %s AS AMOUNT,
        %s AS PAYMENT_MODE,
        TO_TIMESTAMP_NTZ(%s, 'YYYY-MM-DD HH24:MI:SS') AS ORDER_TIME
) AS source

ON target.ORDER_ID = source.ORDER_ID

WHEN NOT MATCHED THEN
    INSERT (
        ORDER_ID,
        CUSTOMER_NAME,
        CITY,
        PRODUCT,
        AMOUNT,
        PAYMENT_MODE,
        ORDER_TIME
    )
    VALUES (
        source.ORDER_ID,
        source.CUSTOMER_NAME,
        source.CITY,
        source.PRODUCT,
        source.AMOUNT,
        source.PAYMENT_MODE,
        source.ORDER_TIME
    )
"""

processed = 0

print("Listening for Kafka orders. Press Ctrl+C to stop.")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print("Kafka error:", msg.error())
            continue

        try:
            # Decode Kafka JSON
            order = json.loads(msg.value().decode("utf-8"))

            values = (
                order["order_id"],
                order["customer_name"],
                order["city"],
                order["product"],
                order["amount"],
                order["payment_mode"],
                order["order_time"],
            )

            # Write to Snowflake
            cursor.execute(merge_sql, values)
            conn.commit()

            # Commit Kafka offset after successful write
            consumer.commit(message=msg, asynchronous=False)

            processed += 1
            print(
                f"Processed order {order['order_id']} "
                f"| Kafka offset {msg.offset()}"
            )

        except Exception as e:
            conn.rollback()
            print("Processing failed:", e)
            print("Stopping to avoid skipping the failed record.")
            break

except KeyboardInterrupt:
    print("\nConsumer stopped.")

finally:
    consumer.close()
    cursor.close()
    conn.close()
    print(f"Orders processed in this run: {processed}")
