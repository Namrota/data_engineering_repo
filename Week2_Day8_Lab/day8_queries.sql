create database week2_day8;
use week2_day8;

DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS order_item;

CREATE table customers(customer_id VARCHAR(50) PRIMARY key, name VARCHAR(50), city VARCHAR(50));
CREATE table orders(order_id VARCHAR(20) PRIMARY KEY, customer_id VARCHAR(50) NOT NULL, order_date DATE, status VARCHAR(12),
FOREIGN KEY (customer_id) references customers(customer_id));
CREATE table products(product_id VARCHAR(20) PRIMARY KEY, product_name VARCHAR(50));
CREATE table order_item(order_id VARCHAR(20) NOT NULL, product_id VARCHAR(20) NOT NULL, quantity integer, unit_price_gbp float,
FOREIGN KEY (order_id) REFERENCES orders(order_id),
FOREIGN KEY (product_id) REFERENCES products(product_id));