
import json
import random
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from faker import Faker
from confluent_kafka import Producer

# Generate fictional German customer names
fake = Faker("de_DE")

# Connect to Kafka running in Docker
producer = Producer({
    "bootstrap.servers": "localhost:9092",
    "enable.idempotence": True
})

topic = "ecommerce_orders"

# German e-commerce data
products = [
    "Laptop",
    "Smartphone",
    "Tablet",
    "Kopfhörer",
    "Kaffeemaschine",
    "Monitor",
    "Smartwatch",
    "Staubsauger"
]

cities = [
    "Berlin",
    "Hamburg",
    "München",
    "Köln",
    "Frankfurt am Main",
    "Stuttgart",
    "Karlsruhe",
    "Düsseldorf",
    "Leipzig",
    "Dresden"
]

payments = [
    "PayPal",
    "Kreditkarte",
    "SEPA-Lastschrift",
    "Rechnung",
    "Girocard"
]


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(
            f"Delivered: Partition {msg.partition()}, "
            f"Offset {msg.offset()}"
        )


print("Starting German e-commerce order simulation...")
print("Press Ctrl+C to stop.\n")

try:
    while True:

        order = {
            "order_id": int(time.time() * 1000),
            "customer_name": fake.name(),
            "city": random.choice(cities),
            "product": random.choice(products),
            "amount": round(random.uniform(15, 3000), 2),
            "payment_mode": random.choice(payments),
            "order_time": datetime.now(
                ZoneInfo("Europe/Berlin")
            ).strftime("%Y-%m-%d %H:%M:%S")
        }

        message = json.dumps(order, ensure_ascii=False)

        producer.produce(
            topic=topic,
            key=str(order["order_id"]),
            value=message.encode("utf-8"),
            callback=delivery_report
        )

        remaining = producer.flush(timeout=10)

        if remaining == 0:
            print("Generated order:", message)
        else:
            print("Warning: Message delivery not confirmed")

        time.sleep(2)

except KeyboardInterrupt:
    print("\nStopping German order simulation...")

finally:
    producer.flush()
    print("Producer closed.")
