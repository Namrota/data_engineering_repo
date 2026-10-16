create database week2_day10;
use week2_day10;

 /* Q1 */
CREATE TABLE orders_perf (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    city VARCHAR(50) NOT NULL,
    amount_gbp DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL
);
 
INSERT INTO orders_perf VALUES
(1, 101, '2026-08-01', 'London', 45.50, 'complete'),
(2, 102, '2026-08-01', 'Manchester', 18.00, 'cancelled'),
(3, 101, '2026-08-02', 'London', 62.25, 'complete'),
(4, 103, '2026-08-02', 'Leeds', 30.00, 'complete'),
(5, 104, '2026-08-03', 'Bristol', 55.50, 'complete'),
(6, 102, '2026-08-03', 'Manchester', 12.00, 'pending'),
(7, 101, '2026-08-04', 'London', 80.00, 'complete'),
(8, 105, '2026-08-04', 'Leeds', 20.00, 'complete'),
(9, 106, '2026-08-05', 'Bristol', 100.00, 'complete'),
(10, 102, '2026-08-05', 'Manchester', 40.00, 'complete');


/*Q2*/
EXPLAIN
SELECT
order_id,
order_date,
amount_gbp
FROM orders_perf
WHERE customer_id = 101;

/*Q3*/

CREATE INDEX idx_orders_customers on orders_perf(customer_id);

EXPLAIN
SELECT
order_id,
order_date,
amount_gbp
FROM orders_perf
WHERE customer_id = 101;

/*Q5*/

SELECT *
FROM orders_perf
WHERE status = 'complete';

SELECT
    order_id,
    order_date,
    amount_gbp
FROM orders_perf
WHERE status = 'complete';

/*Q6*/
SELECT
    order_id,
    customer_id,
    city
FROM orders_perf
WHERE order_date >= '2026-08-03' and amount_gbp >= 40 and status= 'complete';

/*Q7*/
CREATE TABLE customers_perf (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL
);
 
INSERT INTO customers_perf VALUES
(101, 'Amelia Clarke', 'London'),
(102, 'Oliver Bennett', 'Manchester'),
(103, 'Aisha Khan', 'Leeds'),
(104, 'Harry Thompson', 'Bristol'),
(105, 'Emily Wilson', 'Leeds'),
(106, 'Noah Davies', 'Bristol');

SELECT o.order_id, c.customer_id, o.order_date, o.amount_gbp
FROM orders_perf as o
INNER JOIN
customers_perf as c
ON o.customer_id= c.customer_id;