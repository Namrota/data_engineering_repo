CREATE DATABASE IF NOT EXISTS quickcart_db;

USE quickcart_db;

CREATE TABLE customers(
customer_id int PRIMARY KEY,
customer_name VARCHAR(80),
email VARCHAR(80),
city VARCHAR(80),
signup_date DATE
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(150),
    category VARCHAR(100),
    supplier_id INT,
    cost_price DECIMAL(12,2),
    selling_price DECIMAL(12,2)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    order_date DATE,
    quantity INT,
    unit_price DECIMAL(12,2),
    payment_status VARCHAR(30),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

CREATE TABLE clickstream (
    event_id INT PRIMARY KEY,
    customer_id INT NULL,
    event_type VARCHAR(50),
    page_url VARCHAR(500),
    event_timestamp DATETIME,
    device_type VARCHAR(30),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

/*--------------------------------------------------------------------------*/
# Investigate the rows inserted into the tables:
SELECT * FROM customers;
SELECT * FROM orders;
SELECT * FROM products;
SELECT * FROM clickstream;
/*--------------------------------------------------------------------------*/
# 1. Find top 10 customers by revenue.  
SELECT o.customer_id, o.order_id, c.customer_name, SUM(o.quantity * o.unit_price) as total_revenue
FROM orders as o
INNER JOIN customers as c
ON o.customer_id= c.customer_id
GROUP BY o.order_id, o.customer_id, c.customer_name
order by total_revenue desc
LIMIT 10;

#2. Find month-over-month sales growth. 
with monthly_sales as (
	SELECT date_format(order_date, '%Y-%m-01') as sales_month,
    SUM(quantity*unit_price) as monthly_revenue
	FROM orders
	GROUP BY date_format(order_date, '%Y-%m-01')
),
sales_comparison AS(
	SELECT sales_month,
    monthly_revenue,
    LAG(monthly_revenue) OVER(
		ORDER BY sales_month
    ) as previous_month_sales
    FROM monthly_sales
)
SELECT 
	sales_month,
    monthly_revenue,
    previous_month_sales,
    ROUND(
		((monthly_revenue-previous_month_sales)/NULLIF(previous_month_sales, 0)) * 100, 2
        ) as mom_sales_pct
FROM sales_comparison
ORDER BY sales_month;

#3. Find customers who ordered in consecutive months.  

with customer_months as (
	SELECT DISTINCT customer_id,
	date_format(order_date, '%Y-%m-01') as purchase_month
    FROM orders
),
previous_purchases as(SELECT
	customer_id,
    purchase_month,
    LAG(purchase_month)OVER
		(PARTITION BY customer_id
		ORDER BY purchase_month
		) as previous_month
FROM customer_months
)
SELECT DISTINCT
	p.customer_id, c.customer_name
FROM previous_purchases as p
INNER JOIN customers as c
ON p.customer_id= c.customer_id
WHERE
timestampdiff(month, p.previous_month, p.purchase_month)= 1;

# 4. Find products never ordered.  
SELECT *
FROM products
WHERE product_id NOT IN (SELECT product_id FROM orders);

# 5. Find revenue contribution percentage by category.  
SELECT p.category, 
SUM(o.quantity * o.unit_price) as total_revenue,
ROUND(
	(
		SUM(o.quantity * o.unit_price)/NULLIF(SUM(SUM(o.quantity * o.unit_price)) OVER(), 0)
    ) * 100,
    2
) as revenue_contribution_pct
FROM orders as o
INNER JOIN products as p
ON o.product_id= p.product_id
GROUP BY p.category
ORDER BY revenue_contribution_pct desc;

/*---------------------------------------------------------------------------*/

# Q2. Advanced SQL
# 1. Rank customers based on total revenue.  
with total_revenue_calc as(
	SELECT 
		o.customer_id as cust_id, 
		c.customer_name as cust_nam, 
		SUM(o.quantity * o.unit_price) as total_revenue
	FROM orders as o
	INNER JOIN customers as c
		ON o.customer_id= c.customer_id
	GROUP BY 
		o.customer_id, 
        c.customer_name
)
SELECT 
	cust_id, cust_nam, total_revenue,
    RANK() OVER(order by total_revenue desc) as customer_rank
FROM total_revenue_calc
order by  customer_rank;

# 2. Find running total sales by month.
SELECT 
	YEAR(order_date) as order_year, 
    MONTH(order_date) as order_month, 
    SUM(quantity * unit_price) as sales,
    SUM(SUM(quantity * unit_price)) OVER(order by YEAR(order_date), MONTH(order_date)) as running_total
FROM orders
GROUP BY order_year, order_month
order by order_year, order_month;

#3. Find the highest selling product per category.  
with revenue_sales as (
	SELECT o.product_id, p.category, p.product_name, SUM(o.unit_price * o.quantity) as total_revenue
	FROM orders as o
	INNER JOIN products as p
		ON o.product_id= p.product_id
	GROUP BY o.product_id, p.category, p.product_name
),
ranked_product as(
	SELECT *,  RANK() OVER(PARTITION BY category
				ORDER BY total_revenue DESC) as product_rank
	FROM revenue_sales
)

SELECT 
	product_id,
    category,
    product_name,
    total_revenue
FROM ranked_product
WHERE product_rank= 1;

# 4. Find 7-day rolling average sales.

WITH daily_sales AS (
    SELECT
        order_date,
        SUM(unit_price * quantity) AS total_sales
    FROM orders
    GROUP BY order_date
)
SELECT
    order_date,
    total_sales,
    ROUND(
        AVG(total_sales) OVER (
            ORDER BY order_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS rolling_avg_7_days
FROM daily_sales
ORDER BY order_date;

/*---------------------------------------------------------------------------*/

/* Q3. SQL Optimization Scenario 
The following query takes 18 minutes: 
SELECT c.customer_name, 
 SUM(o.quantity * o.unit_price) 
FROM orders o 
JOIN customers c 
ON o.customer_id = c.customer_id
WHERE order_date >= '2025-01-01' 
GROUP BY c.customer_name; 
Tasks 
1. Identify possible bottlenecks.  
2. Suggest indexes.  


Solution: 
1. a.MySQL scams for the entire `orders` table to find the qualifying dates
   b.Computing such large data can be expensive
   c.Matching orders with suitable customers can be expensive, s the join processes many rows

2. Creating an index for the `order_date` makes it easier because the analysis needs to be done often. It
helps to locate qualifying date ranges. 

*/

# 3. Explain execution plan analysis.  
/*
MySQL's EXPLAIN ANALYZE command provides detailed information about query execution plans,
including specifics about the optimizer's decisions, access methods, and estimated costs. 
Unlike the EXPLAIN statement, which outlines the execution plan without running the query, 
EXPLAIN ANALYZE actually executes the query and provides runtime statistics. 
This makes it an invaluable tool for analyzing query performance and identifying areas
for improvement.

*/
EXPLAIN ANALYZE
SELECT c.customer_name, 
 SUM(o.quantity * o.unit_price) 
FROM orders o 
JOIN customers c 
ON o.customer_id = c.customer_id
WHERE order_date >= '2025-01-01' 
GROUP BY c.customer_name; 

/*

Filter: ((o.order_date >= DATE\'2025-01-01\') and (o.customer_id is not null))
(cost=51 rows=167) (actual time=0.049..0.224 rows=491 loops=1)
491 loops means 491 times the lookup operation was executed.

Out of 500 rows, 491 rows were qualified by the filtering condition.
*/














































