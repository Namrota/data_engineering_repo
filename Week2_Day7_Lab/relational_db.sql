CREATE database week2_db;

use week2_db;

# creating Relational table:

CREATE TABLE customers
(
	customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(50),
    city VARCHAR(50)
    
);
CREATE TABLE orders
(
	order_id VARCHAR(50) PRIMARY KEY,
    customer_id varchar(50) NOT NULL,
    amount_gbp DECIMAL(10,2),
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY(customer_id)
    REFERENCES customers(customer_id)
);

# Insert values into customers and orders:

INSERT INTO customers
(customer_id, customer_name, city)
VALUES
(1, 'Amelia Clarke', 'London'),
(2, 'Oliver Bennett', 'Manchester'),
(3, 'Aisha Khan', 'Leeds');
 
INSERT INTO orders
(order_id, customer_id, amount_gbp, status)
VALUES
(101, 1, 45.50, 'complete'),
(102, 2, 18.00, 'cancelled'),
(103, 1, 62.25, 'complete'),
(104, 3, 30.00, 'complete');
 
# Validate:
SELECT * FROM customers;
SELECT * FROM orders;

# Write a join that shows:
/*
order_id
customer_name
city
amount_gbp
status
*/

SELECT o.order_id, c.customer_name, c.city, o.amount_gbp, o.status
FROM orders as o
INNER JOIN customers as c
WHERE o.customer_id= c.customer_id;


