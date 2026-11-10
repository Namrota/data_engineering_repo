-- Run after registering the three temp views: customers, products, orders.
-- Revenue definition: quantity * unit_price * (1 - coalesce(discount_pct, 0))

-- 1. First 10 orders
SELECT * FROM orders LIMIT 10;

-- 2. Row counts
SELECT 'customers' AS dataset, COUNT(*) AS rows FROM customers
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'orders', COUNT(*) FROM orders;

-- 3. Delivered orders
SELECT * FROM orders WHERE order_status = 'Delivered';

-- 4. Orders placed in 2025
SELECT * FROM orders WHERE YEAR(TO_DATE(order_date)) = 2025;

-- 5. Distinct statuses
SELECT DISTINCT order_status FROM orders ORDER BY order_status;

-- 6. Missing shipping date
SELECT * FROM orders WHERE shipping_date IS NULL;

-- 7. Orders by status
SELECT order_status, COUNT(*) AS order_count
FROM orders GROUP BY order_status ORDER BY order_count DESC;

-- 8. Quantity sold by product
SELECT p.product_name, SUM(o.quantity) AS units_sold
FROM orders o JOIN products p USING (product_id)
GROUP BY p.product_name ORDER BY units_sold DESC;

-- 9. Revenue by payment method
SELECT payment_method,
       ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))), 2) AS revenue
FROM orders GROUP BY payment_method ORDER BY revenue DESC;

-- 10. Monthly revenue in 2025
SELECT DATE_FORMAT(TO_DATE(order_date), 'yyyy-MM') AS order_month,
       ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))), 2) AS revenue
FROM orders
WHERE YEAR(TO_DATE(order_date)) = 2025
GROUP BY DATE_FORMAT(TO_DATE(order_date), 'yyyy-MM')
ORDER BY order_month;

-- 11. Top 5 customers by order value
SELECT c.customer_id, c.customer_name,
       ROUND(SUM(o.quantity * o.unit_price * (1 - COALESCE(o.discount_pct, 0))), 2) AS total_value
FROM orders o JOIN customers c USING (customer_id)
GROUP BY c.customer_id, c.customer_name
ORDER BY total_value DESC LIMIT 5;

-- 12. Average order value by customer segment
WITH order_values AS (
  SELECT o.order_id, c.customer_segment,
         SUM(o.quantity * o.unit_price * (1 - COALESCE(o.discount_pct, 0))) AS order_value
  FROM orders o JOIN customers c USING (customer_id)
  GROUP BY o.order_id, c.customer_segment
)
SELECT customer_segment, ROUND(AVG(order_value), 2) AS avg_order_value
FROM order_values GROUP BY customer_segment;

-- 13. Orders with customer details
SELECT o.order_id, c.customer_name, c.city, c.region
FROM orders o JOIN customers c USING (customer_id);

-- 14. Revenue by product category
SELECT p.category,
       ROUND(SUM(o.quantity * o.unit_price * (1 - COALESCE(o.discount_pct, 0))), 2) AS revenue
FROM orders o JOIN products p USING (product_id)
GROUP BY p.category ORDER BY revenue DESC;

-- 15. Customers without orders
SELECT c.*
FROM customers c LEFT ANTI JOIN orders o ON c.customer_id = o.customer_id;

-- 16. Duplicate order IDs
SELECT order_id, COUNT(*) AS occurrences
FROM orders GROUP BY order_id HAVING COUNT(*) > 1;

-- 17. Missing discounts after replacement
SELECT COUNT(*) AS null_discount_count
FROM (SELECT COALESCE(discount_pct, 0) AS discount_pct FROM orders)
WHERE discount_pct IS NULL;

-- 18. Percentage of orders by status
SELECT order_status, COUNT(*) AS order_count,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_orders
FROM orders GROUP BY order_status ORDER BY pct_of_orders DESC;

-- 19. Rank products by revenue within category
WITH product_revenue AS (
  SELECT p.category, p.product_id, p.product_name,
         SUM(o.quantity * o.unit_price * (1 - COALESCE(o.discount_pct, 0))) AS revenue
  FROM products p JOIN orders o USING (product_id)
  GROUP BY p.category, p.product_id, p.product_name
)
SELECT *, DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS category_rank
FROM product_revenue;

-- 20. Most recent order per customer
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY TO_DATE(order_date) DESC, order_id DESC) AS rn
  FROM orders
)
SELECT * FROM ranked WHERE rn = 1;

-- 21. Gold aggregate: monthly revenue by region
CREATE OR REPLACE TABLE monthly_revenue_by_region AS
SELECT DATE_FORMAT(TO_DATE(o.order_date), 'yyyy-MM') AS order_month,
       c.region,
       ROUND(SUM(o.quantity * o.unit_price * (1 - COALESCE(o.discount_pct, 0))), 2) AS revenue
FROM orders o JOIN customers c USING (customer_id)
GROUP BY DATE_FORMAT(TO_DATE(o.order_date), 'yyyy-MM'), c.region;

-- 22. Write/read Parquet (PySpark cell)
-- spark.table("monthly_revenue_by_region").write.mode("overwrite").parquet(
--     f"/Volumes/{catalog}/{schema}/parquet/monthly_revenue_by_region")
-- spark.read.parquet(f"/Volumes/{catalog}/{schema}/parquet/monthly_revenue_by_region").show()

-- 23. Cleaned Delta table (PySpark cell)
-- cleaned_orders = orders_parquet.fillna({"discount_pct": 0})
-- cleaned_orders.write.format("delta").mode("overwrite").saveAsTable("retail_lab.cleaned_orders")
