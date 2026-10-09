use order_db;

CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100) NOT NULL,
  city VARCHAR(50)
);
 
CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  customer_id INT,
  order_date DATE,
  amount_gbp DECIMAL(10,2),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
  product_id INT PRIMARY KEY,
  sku VARCHAR(50) UNIQUE,
  price DECIMAL(10,2) NOT NULL,
  quantity INT
);
 
INSERT INTO products (product_id, sku, price, quantity) VALUES
(2, 'SKU-002', 1234567890.99, 5.3);
 -- Throws an error out of range value for column 'price'
 
SELECT * FROM products;

SELECT DATABASE() AS current_database;

DROP TABLE IF EXISTS customers_demo;
CREATE TABLE customers_demo (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  city VARCHAR(50)
);
 
INSERT INTO customers_demo (customer_id, customer_name, city) VALUES
(1, 'Sana Patil', 'Leeds'),
(2, 'Mohit Rao', 'London'),
(3, '', ''),
(4, 'Riri', '');
 
SELECT * FROM customers_demo ORDER BY customer_id;

-- Adding another row performing CRUD operations:
-- Create
INSERT INTO customers_demo (customer_id, customer_name, city) VALUES (5, 'Asha Nair', 'Chennai');
 
-- Read
SELECT * FROM customers_demo;
 
-- Update
UPDATE customers_demo SET city = 'Bengaluru' WHERE customer_id = 5;
 
-- Delete
DELETE FROM customers_demo WHERE customer_id = 5;

-- Update multiple rows:
UPDATE customers_demo c
JOIN (
    SELECT 1 as id, 5 as new_score1, 8 as new_score2
    UNION ALL
    SELECT 2, 10, 8
    UNION ALL
    SELECT 3, 8, 3
    UNION ALL
    SELECT 4, 10, 7
) vals ON s.id = vals.id
SET score1 = new_score1, score2 = new_score2;
 
SELECT COUNT(*) AS remaining_count FROM customers_demo;

SELECT * FROM orders;

INSERT INTO customers (customer_id, customer_name, city) VALUES
(1, 'Sana Patil', 'Leeds'),
(2, 'Mohit Rao', 'London'),
(3, 'Alex', 'Hamburg'),
(4, 'Riri', 'New Jersey');
 

INSERT INTO orders (order_id, customer_id, order_date, amount_gbp) VALUES
(101, 4, '2006-10-01', 56.90),
(102, 1, '2006-09-10', 80.00),
(103, 2, '2006-06-21', 120.51);

INSERT INTO orders (order_id, customer_id, order_date, amount_gbp) VALUES
(104, 2, '2006-09-03', 80.90),
(105, 1, '2006-04-10', 170.00);

SELECT customer_id, COUNT(*) AS orders_count, SUM(amount_gbp) AS total_amount
FROM orders
GROUP BY customer_id
HAVING SUM(amount_gbp) > 200
ORDER BY total_amount DESC;
 

-- Joins

DROP TABLE IF EXISTS customer_one;
DROP TABLE IF EXISTS customer_two;

CREATE TABLE customer_one (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100) NOT NULL,
  age INT NOT NULL
);

CREATE TABLE customer_two (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100) NOT NULL,
  age INT NOT NULL,
  city VARCHAR(50) NOT NULL
);


INSERT INTO customer_one (customer_id, customer_name, age) VALUES
(1, 'Ana', 23),
(2, 'Bob', 21),
(3, 'Charlie', 24);

INSERT INTO customer_two (customer_id, customer_name, age, city) VALUES
(1, 'Ana', 23, 'Madrid'),
(2, 'Bobby', 21, 'Barcelona'),
(3, 'Max', 24, 'Berlin'),
(4, 'Andrew', 26, 'London');

-- All the rows from the right tbale and the matching rows from the left table are displayed
SELECT * FROM customer_one as co
RIGHT JOIN  customer_two as ct
ON co.customer_id= ct.customer_id;






