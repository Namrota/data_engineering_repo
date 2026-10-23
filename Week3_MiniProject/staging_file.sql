USE quickcart_db;

CREATE TABLE IF NOT EXISTS stg_customers (
    batch_id VARCHAR(50) NOT NULL,
    source_row_number INT NOT NULL,
    customer_id TEXT,
    customer_name TEXT,
    email TEXT,
    city TEXT,
    signup_date TEXT,
    PRIMARY KEY (batch_id, source_row_number)
);

CREATE TABLE IF NOT EXISTS stg_products (
    batch_id VARCHAR(50) NOT NULL,
    source_row_number INT NOT NULL,
    product_id TEXT,
    product_name TEXT,
    category TEXT,
    supplier_id TEXT,
    cost_price TEXT,
    selling_price TEXT,
    PRIMARY KEY (batch_id, source_row_number)
);

CREATE TABLE IF NOT EXISTS stg_orders (
    batch_id VARCHAR(50) NOT NULL,
    source_row_number INT NOT NULL,
    order_id TEXT,
    customer_id TEXT,
    product_id TEXT,
    order_date TEXT,
    quantity TEXT,
    unit_price TEXT,
    payment_status TEXT,
    PRIMARY KEY (batch_id, source_row_number)
);

CREATE TABLE IF NOT EXISTS stg_clickstream (
    batch_id VARCHAR(50) NOT NULL,
    source_row_number INT NOT NULL,
    event_id TEXT,
    customer_id TEXT,
    event_type TEXT,
    page_url TEXT,
    event_timestamp TEXT,
    device_type TEXT,
    PRIMARY KEY (batch_id, source_row_number)
);


CREATE TABLE IF NOT EXISTS daily_sales_summary (
    sales_date DATE PRIMARY KEY,
    total_orders INT NOT NULL,
    total_revenue DECIMAL(14,2) NOT NULL
);

SHOW TABLES LIKE 'stg_%';

SELECT 'customers' AS source, COUNT(*) AS row_count
FROM stg_customers
WHERE batch_id = '2026-10-23'

UNION ALL

SELECT 'products', COUNT(*)
FROM stg_products
WHERE batch_id = '2026-10-23'

UNION ALL

SELECT 'orders', COUNT(*)
FROM stg_orders
WHERE batch_id = '2026-10-23'

UNION ALL

SELECT 'clickstream', COUNT(*)
FROM stg_clickstream
WHERE batch_id = '2026-10-23';

# Count orders by payment status
SELECT
    LOWER(TRIM(payment_status)) AS payment_status,
    COUNT(*) AS order_count
FROM stg_orders
WHERE batch_id = '2026-10-23'
GROUP BY LOWER(TRIM(payment_status))
ORDER BY order_count DESC;

# Calculate the percentage of orders by payment status
SELECT
    LOWER(TRIM(payment_status)) AS payment_status,
    COUNT(*) AS order_count,
    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM stg_orders
WHERE batch_id = '2026-10-23'
GROUP BY LOWER(TRIM(payment_status))
ORDER BY order_count DESC;

SELECT * FROM daily_sales_summary;
