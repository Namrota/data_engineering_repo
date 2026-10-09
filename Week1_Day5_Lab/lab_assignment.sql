-- DDL : CREATE, DROP, ALTER, TRUNCATE
-- DML : INSERT, UPDATE, DELETE

-- Create and use database
CREATE DATABASE IF NOT EXISTS week1_db;
USE week1_db;

-- Drop tables if they already exist (clean setup)
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- Create customers table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    city VARCHAR(50),
    signup_date DATE
);

-- Create products table
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    unit_price DECIMAL(8,2)
);

-- Create orders table (contains 22 rows)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(8,2),
    order_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create payments table
CREATE TABLE payments (
    payment_id INT PRIMARY KEY,
    order_id INT,
    paid_amount DECIMAL(10,2),
    payment_date DATETIME,
    payment_method VARCHAR(20),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- ------------------------------------------------------------------------ --

-- Insert customers (10 rows)
INSERT INTO customers (customer_id, customer_name, email, city, signup_date) VALUES
(1, 'Asha Mehta', 'asha@example.com', 'Pune', '2021-02-15'),
(2, 'Rahul Sharma', 'rahul@example.com', 'Mumbai', '2020-11-20'),
(3, 'Simran Kaur', 'simran@example.com', 'Delhi', '2022-01-05'),
(4, 'Vikram Singh', 'vikram@example.com', 'Bengaluru', '2019-06-10'),
(5, 'Nisha Patel', 'nisha@example.com', 'Ahmedabad', '2021-09-30'),
(6, 'Karan Verma', 'karan@example.com', 'Chennai', '2020-03-22'),
(7, 'Priya Rao', 'priya@example.com', 'Hyderabad', '2022-05-11'),
(8, 'Manish Gupta', 'manish@example.com', 'Pune', '2021-12-01'),
(9, 'Leena Joshi', 'leena@example.com', NULL, '2020-07-07'),
(10, 'Suresh Nair', 'suresh@example.com', 'Kochi', '2018-10-18');


-- Insert products (6 rows)
INSERT INTO products (product_id, product_name, category, unit_price) VALUES
(101, 'Wireless Mouse', 'Accessories', 599.00),
(102, 'Mechanical Keyboard', 'Accessories', 2499.00),
(103, '27-inch Monitor', 'Display', 12999.00),
(104, 'USB-C Adapter', 'Accessories', 499.00),
(105, 'Laptop 14-inch', 'Computers', 54999.00),
(106, 'External SSD 1TB', 'Storage', 7999.00);


-- Insert orders (22 rows)
INSERT INTO orders (order_id, customer_id, product_id, quantity, unit_price, order_date, status) VALUES
(1001, 1, 101, 1, 599.00, '2022-01-10', 'delivered'),
(1002, 2, 102, 1, 2499.00, '2022-02-15', 'delivered'),
(1003, 3, 104, 2, 499.00, '2022-03-05', 'delivered'),
(1004, 1, 103, 1, 12999.00, '2022-03-20', 'cancelled'),
(1005, 4, 105, 1, 54999.00, '2022-04-02', 'delivered'),
(1006, 5, 101, 2, 599.00, '2022-04-18', 'pending'),
(1007, 6, 106, 1, 7999.00, '2022-05-06', 'delivered'),
(1008, 7, 102, 1, 2499.00, '2022-05-25', 'delivered'),
(1009, 8, 104, 3, 499.00, '2022-06-10', 'delivered'),
(1010, 9, 101, 1, 599.00, '2022-06-21', 'returned'),
(1011, 10, 105, 1, 54999.00, '2022-07-02', 'delivered'),
(1012, 2, 106, 2, 7999.00, '2022-07-18', 'delivered'),
(1013, 3, 101, 4, 599.00, '2022-08-05', 'delivered'),
(1014, 4, 104, 1, 499.00, '2022-08-20', 'delivered'),
(1015, 5, 102, 1, 2499.00, '2022-09-01', 'pending'),
(1016, 6, 103, 1, 12999.00, '2022-09-15', 'delivered'),
(1017, 7, 105, 1, 54999.00, '2022-10-03', 'delivered'),
(1018, 8, 106, 1, 7999.00, '2022-10-25', 'pending'),
(1019, 9, 101, 2, 599.00, '2022-11-11', 'delivered'),
(1020, 10, 104, 5, 499.00, '2022-11-29', 'delivered'),
(1021, 1, 102, 1, 2499.00, '2022-12-05', 'delivered'),
(1022, 2, 101, 3, 599.00, '2022-12-20', 'delivered');


-- Insert payments (8 rows)
INSERT INTO payments (payment_id, order_id, paid_amount, payment_date, payment_method) VALUES
(5001, 1001, 599.00, '2022-01-11 10:10:00', 'card'),
(5002, 1002, 2499.00, '2022-02-16 11:15:00', 'card'),
(5003, 1005, 54999.00, '2022-04-03 09:05:00', 'bank_transfer'),
(5004, 1007, 7999.00, '2022-05-07 14:00:00', 'card'),
(5005, 1011, 54999.00, '2022-07-03 12:20:00', 'bank_transfer'),
(5006, 1012, 15998.00, '2022-07-19 16:45:00', 'card'),
(5007, 1016, 12999.00, '2022-09-16 10:00:00', 'card'),
(5008, 1017, 54999.00, '2022-10-04 18:30:00', 'bank_transfer');

-- ----------------------------------------------------------------------

-- Verification:

SELECT DATABASE() AS current_database; -- week1_db
SELECT COUNT(*) AS total_customers FROM customers; -- 10
SELECT COUNT(*) AS total_products FROM products; -- 6
SELECT COUNT(*) AS total_orders FROM orders; -- 22

-- ------------------------------------------------------------------------

-- Lab 1: Select all orders
SELECT * FROM orders;

-- Lab 2: Select specific columns with WHERE
-- Find order_id, customer_id, quantity, and order_date for orders where quantity > 2.

SELECT order_id, customer_id, quantity, order_date
FROM orders
WHERE quantity > 2;

-- Lab 3: Use IN and BETWEEN
-- Problem Statement
-- A. List orders placed by customer_id 1, 2, or 3.
-- B. List orders placed between '2022-07-01' and '2022-12-31' (inclusive).

SELECT * FROM orders
WHERE customer_id IN (1,2,3);

SELECT * FROM orders
WHERE order_date BETWEEN '2022-07-01' and '2022-12-31';

-- Combining both the conditions:
SELECT * FROM orders
WHERE customer_id IN (1,2,3) AND order_date BETWEEN '2022-07-01' and '2022-12-31';

-- Lab 4: DISTINCT values — cities of customers
-- List distinct cities where customers live.

SELECT distinct(city) FROM customers;

-- Lab 5: ORDER BY and LIMIT
-- Find the 5 most recent orders (order_date descending). Show order_id, customer_id, order_date.
SELECT * FROM orders
ORDER BY order_date DESC
LIMIT 5; 

-- Lab 6: Pattern matching with LIKE
-- Find products whose name contains 'USB' or 'USB-C' using LIKE. Show product_id and product_name.

SELECT product_id, product_name FROM products 
WHERE product_name LIKE '%USB%';

-- Lab 7: IS NULL and IS NOT NULL
-- Find customers whose city is NULL. Then count customers with non-null city.

SELECT * FROM customers
WHERE city IS NULL;

-- COUNT() when passed with a column will count only non-null values
SELECT COUNT(city) FROM customers;


-- Lab 8: INSERT a new order (Create CRUD)
-- Add a new order for customer_id 3 buying product_id 106 with quantity 1 on '2023-01-05' 
-- status 'pending'. 
-- Use order_id 1100.
INSERT INTO orders (order_id, customer_id, product_id, quantity, unit_price, order_date, `status`)
VALUES (1100, 3, 106, 1, 7999.00, '2023-01-05', 'pending');

SELECT * FROM orders;

-- Lab 9: UPDATE with safe practices
-- Change the status of order_id 1006 from 'pending' to 'delivered'. 
-- Show the row before and after the update.

SELECT * FROM orders
WHERE order_id= 1100;

-- Update status to `delivered`
UPDATE orders SET `status`= 'delivered'
WHERE order_id= 1100;

-- Lab 10: DELETE with safe practices
-- Delete order with order_id 1004 (it was cancelled). 
-- Verify the deletion by attempting to SELECT it and by counting remaining rows.

SELECT * FROM orders
WHERE order_id= 1004;

DELETE FROM orders
WHERE order_id= 1004;

-- Lab 11: Aggregation functions
/*
Problem Statement
A. Find total number of orders.
B. Find total quantity ordered across all orders.
C. Find average unit_price across orders.
D. Find minimum and maximum unit_price recorded in orders.
*/

SELECT COUNT(*) as total_orders FROM orders ;

SELECT SUM(quantity) as total_quantity_ordered FROM orders;

SELECT AVG(unit_price) as avg_unit_price FROM orders;

SELECT MAX(unit_price) as max_unit_price FROM orders;

SELECT MIN(unit_price) as min_unit_price FROM orders;


-- Lab 12: GROUP BY and HAVING
/* Find total spent per customer (sum of quantity * unit_price) 
and list customers who spent more than 20000. Show customer_id and total_spent.
*/

SELECT customer_id, SUM(quantity * unit_price) as total_spent
FROM orders
GROUP BY customer_id
HAVING SUM(quantity * unit_price) > 20000;


-- Lab 13: INNER JOIN — orders with customer names
/*
List order_id, customer_name, product_id, quantity, order_date for all delivered orders. Use INNER JOIN.
*/

SELECT o.order_id, c.customer_name, p.product_id, o.quantity, o.order_date
FROM customers as c
INNER JOIN orders as o
ON c.customer_id= o.customer_id
INNER JOIN products as p
ON p.product_id= o.product_id
WHERE o.status= 'delivered';

-- Lab 14: LEFT JOIN — find orders without payments
/*
Find orders that do not have an entry in payments (left join payments and filter where payment_id 
IS NULL). 
Show order_id, customer_id, order_date.
*/

SELECT o.order_id, o.customer_id, o.order_date, p.paid_amount, p.payment_method
FROM orders as o
LEFT JOIN payments as p
ON o.order_id= p.order_id
WHERE p.payment_id IS NULL;

-- Lab 15: Multi-table join with aggregation
/*
For each product category, calculate total revenue = SUM(quantity * unit_price)
and total_units_sold = SUM(quantity). 
Show category, total_units_sold, total_revenue. Order by total_revenue DESC.
*/

SELECT p.category, 
SUM(o.quantity * o.unit_price) as total_revenue, 
SUM(o.quantity) as total_units_sold
FROM orders as o
INNER JOIN products as p
ON p.product_id = o.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- Lab 16: Final Integrated Lab — Business report
/*
Create a business report showing top 5 customers 
by total spending (total_spent = SUM(quantity * unit_price)). For each top customer, show:
customer_id
customer_name
city
total_spent
total_orders (number of orders)
first_order_date
last_order_date
Consider only orders with status IN ('delivered', 'returned') 
and order_date in 2022. Order the result by total_spent DESC and limit to 5.
*/


SELECT c.customer_id,
c.customer_name,
c.city,
SUM(o.quantity * o.unit_price) as total_spent,
COUNT(o.order_id) as total_orders,
min(o.order_date) as min_order_date,
max(o.order_date) as max_order_date
FROM customers as c
INNER JOIN orders as o
on c.customer_id= o.customer_id
WHERE o.status IN('delivered', 'returned') AND
o.order_date>= '2022-01-01' AND
o.order_date < '2023-01-01'
GROUP BY c.customer_id,
c.customer_name,
c.city
ORDER BY total_spent DESC
LIMIT 5;
 



































