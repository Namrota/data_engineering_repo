SELECT sale_date,
COUNT(*) as total_sales,
ROUND(SUM(amount), 2) as total_revenue_per_day,
ROUND(AVG(amount), 2) as avg_sales_val

FROM {{ ref('stg_coffee_sales') }}

WHERE sale_date is not null and amount is not null

GROUP BY 1
ORDER BY 1