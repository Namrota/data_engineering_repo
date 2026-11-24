# Real-Time E-Commerce Streaming Analytics Using Kafka and Snowflake

## 1. Project Overview

This project demonstrates an event-driven data pipeline using Apache Kafka, Python, and Snowflake.

The objective is to simulate e-commerce orders from German customers, stream these transactions through Apache Kafka, and ingest them into Snowflake for analytical processing.

The project will eventually integrate with Power BI to visualize revenue, product sales, customer locations, and payment-method trends.

### Project Objectives

- Simulate e-commerce transactions using Python and Faker.
- Publish JSON events to an Apache Kafka topic.
- Understand Kafka producers, consumers, topics, partitions, and offsets.
- Consume Kafka messages using Python.
- Insert the received transactions into Snowflake.
- Validate the accuracy and uniqueness of the ingested records.
- Prepare the data for Power BI reporting.

### Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Data simulation and ingestion scripts |
| Faker | Generate synthetic customer information |
| confluent-kafka | Kafka producer and consumer |
| Apache Kafka 4.x | Event streaming and message retention |
| Docker Desktop | Run the Kafka broker |
| KRaft | Kafka metadata and cluster coordination |
| Snowflake | Cloud data warehouse |
| Snowflake Python Connector | Connect Python to Snowflake |
| Power BI | Dashboard visualization (next phase) |

---

## 2. System Architecture

```text
             PYTHON DATA SIMULATOR
             producer.py + Faker
                      |
                      | JSON order events
                      v
               APACHE KAFKA
             Topic: ecommerce_orders
                1 Partition
                      |
                      | Consumer reads messages
                      v
              PYTHON CONSUMER
             consumer_snowflake.py
                      |
                      | SQL MERGE
                      v
                 SNOWFLAKE
          KAFKA_DEMO.REALTIME.ORDERS
                      |
                      v
                   POWER BI
                (Next phase)
```

### Understanding the Data Flow

1. The Python producer creates fictional e-commerce transactions.
2. The producer serializes each transaction into JSON and sends it to Kafka.
3. Kafka stores the messages in the `ecommerce_orders` topic.
4. The Python consumer subscribes to this topic and reads the stored events.
5. The consumer extracts the fields from the JSON messages.
6. The consumer performs a SQL `MERGE` to insert new records into Snowflake.
7. After a successful Snowflake transaction, the consumer commits the Kafka offset.
8. Snowflake stores the data for analytics and future Power BI visualization.

**Important:** Kafka and Snowflake have different responsibilities. Kafka temporarily retains streaming events according to its retention configuration, while Snowflake provides persistent analytical storage for the ingested records.

---

## 3. Project Directory

The project was created in Windows PowerShell:

```powershell
mkdir kafka_snowflake_lab
cd kafka_snowflake_lab
```

Project location:

```text
D:\IronHack_DE\Week8_Day2_Lab\kafka_snowflake_lab
```

### Project Files

```text
kafka_snowflake_lab/
│
├── producer.py
│     Generates fictional German e-commerce orders
│
├── test_snowflake.py
│     Verifies Python-to-Snowflake connectivity
│
├── consumer_snowflake.py
│     Consumes Kafka events and loads Snowflake
│
└── README.md
      Project documentation
```

---

## 4. Step 1 — Start Apache Kafka Using Docker

### Objective

Start the Apache Kafka broker so that Python producers and consumers can communicate with it.

The original assignment used ZooKeeper and Windows Kafka batch scripts. However, this environment uses Kafka 4.x with KRaft, running inside Docker Desktop.

Therefore, no separate ZooKeeper installation is required.

### Commands Executed

Check existing Docker containers:

```powershell
docker ps -a
```

Start Kafka if the container is stopped:

```powershell
docker start kafka
```

Verify running containers:

```powershell
docker ps
```

The Kafka container exposes port `9092`, allowing Python applications running on Windows to connect using:

```text
localhost:9092
```

### Explanation

- `docker ps -a` displays all Docker containers.
- `docker start kafka` starts the previously created Kafka container.
- `docker ps` displays currently running containers.
- Port `9092` is used for Kafka client communication.

**Observation:** The existing Docker Kafka container was running and accessible.

---

## 5. Step 2 — Create the Kafka Topic

### Objective

Create a Kafka topic to receive the simulated e-commerce transactions.

### Command

```powershell
docker exec kafka /opt/kafka/bin/kafka-topics.sh --create --if-not-exists --topic ecommerce_orders --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092
```

### Verify Topic Configuration

```powershell
docker exec kafka /opt/kafka/bin/kafka-topics.sh --describe --topic ecommerce_orders --bootstrap-server localhost:9092
```

### Observed Configuration

```text
Topic: ecommerce_orders
PartitionCount: 1
ReplicationFactor: 1

Partition: 0
Leader: 1
Replicas: 1
Isr: 1
```

### Explanation

- **Topic:** A logical stream that stores related events.
- **Partition:** An ordered log containing Kafka messages.
- **Replication factor:** Number of copies maintained across Kafka brokers.
- **Leader:** Broker responsible for reads and writes for the partition.
- **ISR (In-Sync Replicas):** Replicas currently synchronized with the leader.
- **Offset:** Position of a message inside its partition.

This lab uses one partition and one broker, which is sufficient for demonstrating the ingestion workflow but does not provide broker-level fault tolerance.

---

## 6. Step 3 — Configure the Python Environment

### Objective

Create an isolated environment for Kafka and Snowflake development.

An initial attempt to install packages in the Anaconda `base` environment produced dependency conflicts involving Streamlit, pandas, and protobuf.

To prevent further conflicts, a dedicated Conda environment was created.

### Create Environment

```powershell
conda create -n kafka_snowflake python=3.11 -y
```

Activate it:

```powershell
conda activate kafka_snowflake
```

### Install Libraries

```powershell
python -m pip install confluent-kafka snowflake-connector-python pandas faker
```

### Verify Installed Packages

```powershell
python -c "import confluent_kafka; print('Kafka OK')"
python -c "import snowflake.connector; print('Snowflake OK')"
python -c "from faker import Faker; print('Faker OK')"
python -c "import pandas; print('Pandas OK')"
```

Check dependency compatibility:

```powershell
python -m pip check
```

### Observed Output

```text
Kafka OK
Snowflake OK
Faker OK
Pandas OK

No broken requirements found.
```

### Verify Python Interpreter

```powershell
python -c "import sys; print(sys.executable)"
```

The output confirmed that Python was running from the dedicated `kafka_snowflake` Conda environment.

**Conclusion:** The environment was successfully isolated and configured for Kafka and Snowflake development.

---

## 7. Step 4 — Simulate German E-Commerce Transactions

### Objective

Develop a Python producer that generates fictional German customer orders and sends them to Apache Kafka.

### Script

`producer.py`

### Simulation Configuration

| Attribute | Configuration |
|---|---|
| Faker locale | `de_DE` |
| Customer names | Fictional German names |
| Cities | Berlin, Hamburg, München, Köln, Frankfurt am Main, Stuttgart, Karlsruhe, Düsseldorf, Leipzig, Dresden |
| Products | Laptop, Smartphone, Tablet, Kopfhörer, Kaffeemaschine, Monitor, Smartwatch, Staubsauger |
| Payment methods | PayPal, Kreditkarte, SEPA-Lastschrift, Rechnung, Girocard |
| Transaction amount | €15–€3,000 |
| Simulation interval | Approximately 2 seconds |
| Timestamp timezone | Europe/Berlin |
| Event format | JSON |

### Important Python Components

**Faker for German data:**

```python
from faker import Faker

fake = Faker("de_DE")
```

**Create Kafka producer:**

```python
from confluent_kafka import Producer

producer = Producer({
    "bootstrap.servers": "localhost:9092",
    "enable.idempotence": True
})
```

**Generate an order:**

The producer constructs a dictionary containing these fields:

```text
order_id
customer_name
city
product
amount
payment_mode
order_time
```

The `order_id` is generated using a millisecond timestamp, and `order_time` uses German local time.

**Convert data to JSON:**

```python
message = json.dumps(order, ensure_ascii=False)
```

The `ensure_ascii=False` option preserves German characters such as ä, ö, ü, and ß.

**Publish to Kafka:**

```python
producer.produce(
    topic="ecommerce_orders",
    key=str(order["order_id"]),
    value=message.encode("utf-8"),
    callback=delivery_report
)
```

A delivery callback reports whether Kafka acknowledged the message and, on success, provides its partition and offset.

### Run the Producer

```powershell
python producer.py
```

### Observations

The producer continuously generated German e-commerce transactions.

Kafka confirmed successful deliveries into Partition 0, with sequential offsets from 0 through 44.

A total of **45 messages** were generated during the test.

The producer was stopped using `Ctrl+C`.

---

## 8. Step 5 — Verify Records Using Kafka Console Consumer

### Objective

Confirm that the messages generated by Python were successfully stored in Kafka and could be retrieved by an independent consumer.

### Command

```powershell
docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic ecommerce_orders --bootstrap-server localhost:9092 --from-beginning
```

### Explanation

- `kafka-console-consumer.sh` starts a Kafka consumer through the terminal.
- `--topic ecommerce_orders` specifies the source topic.
- `--bootstrap-server localhost:9092` identifies the broker.
- `--from-beginning` requests consumption from the earliest available offset when no earlier committed group offset overrides it.

### Observed Results

```text
Processed a total of 45 messages
```

All 45 generated records were displayed by the Kafka console consumer.

The records contained the expected seven JSON fields, and German characters appeared correctly.

The consumed sequence matched the successfully published messages.

### Key Learning

A Kafka producer and consumer are independent applications.

The producer publishes events to Kafka, while the consumer retrieves those events from the topic.

Kafka retains the records according to its retention policy, even when the producer has stopped.

---

## 9. Step 6 — Create the Snowflake Database and Table

### Objective

Prepare a Snowflake database, schema, and table to store the simulated e-commerce orders.

### Snowflake SQL

```sql
CREATE DATABASE IF NOT EXISTS KAFKA_DEMO;

CREATE SCHEMA IF NOT EXISTS KAFKA_DEMO.REALTIME;

USE DATABASE KAFKA_DEMO;
USE SCHEMA REALTIME;

CREATE TABLE IF NOT EXISTS ORDERS (
    ORDER_ID NUMBER(19,0),
    CUSTOMER_NAME VARCHAR(200),
    CITY VARCHAR(100),
    PRODUCT VARCHAR(100),
    AMOUNT NUMBER(12,2),
    PAYMENT_MODE VARCHAR(100),
    ORDER_TIME TIMESTAMP_NTZ,
    INGESTED_AT TIMESTAMP_LTZ
        DEFAULT CURRENT_TIMESTAMP()
);
```

### Schema Explanation

| Column | Purpose |
|---|---|
| `ORDER_ID` | Unique logical identifier for each generated order |
| `CUSTOMER_NAME` | Fictional customer name |
| `CITY` | German city associated with the transaction |
| `PRODUCT` | Purchased product |
| `AMOUNT` | Order amount in euros |
| `PAYMENT_MODE` | Simulated payment method |
| `ORDER_TIME` | Time of the simulated order |
| `INGESTED_AT` | Time the row was inserted into Snowflake |

`NUMBER(12,2)` was chosen instead of `FLOAT` to preserve two-decimal financial amounts.

`TIMESTAMP_NTZ` was used because the simulated `order_time` field represents German local time without an explicit timezone offset.

### Verify the Table

```sql
SELECT COUNT(*)
FROM KAFKA_DEMO.REALTIME.ORDERS;
```

**Initial result:** 0 rows.

---

## 10. Step 7 — Establish Python-to-Snowflake Connectivity

### Objective

Validate that the Python application can authenticate with Snowflake and access the destination database.

### Snowflake Configuration

The connection used:

```text
Warehouse: