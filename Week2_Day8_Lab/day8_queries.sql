create database week2_day8;
use week2_day8;

DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS order_item;

CREATE table customers(customer_id VARCHAR(50) PRIMARY key, name VARCHAR(50), city VARCHAR(50));
CREATE table orders(order_id VARCHAR(20) PRIMARY KEY, customer_id VARCHAR(50) NOT NULL, order_date DATE, status VARCHAR(12),
FOREIGN KEY (customer_id) references customers(customer_id));
CREATE table products(product_id VARCHAR(20) PRIMARY KEY, product_name VARCHAR(50), unit_price_gbp float);
CREATE table order_item(order_id VARCHAR(20) NOT NULL, product_id VARCHAR(20) NOT NULL, quantity integer,
FOREIGN KEY (order_id) REFERENCES orders(order_id),
FOREIGN KEY (product_id) REFERENCES products(product_id));

/* Q. 9 — Insert a Small Normalized Dataset*/

INSERT INTO customers VALUES
(1, 'Amelia Clarke', 'London'),
(2, 'Oliver Bennett', 'Manchester');
 
INSERT INTO products VALUES
(10, 'Desk Lamp', 25.00),
(11, 'Office Chair', 80.00),
(12, 'Notebook Set', 10.00);
 
INSERT INTO orders VALUES
(1001, 1, '2026-08-01', 'Completed'),
(1002, 2, '2026-08-01', 'Cancelled'),
(1003, 1, '2026-08-02', 'Completed');
 
INSERT INTO order_item VALUES
(1001, 10, 2),
(1001, 12, 1),
(1002, 11, 1),
(1003, 12, 3);

Select * FROM customers;
SELECT * FROM products;


 

