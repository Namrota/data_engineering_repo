# PySpark answer snippets. Assumes customers, products, orders are DataFrames.
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Basic counts and delivered orders
for name, df in [("customers", customers), ("products", products), ("orders", orders)]:
    print(name, df.count())
orders.filter(F.col("order_status") == "Delivered").show()

# Create a reusable revenue column; null discount is treated as zero
orders_clean = orders.fillna({"discount_pct": 0.0})
orders_clean = orders_clean.withColumn(
    "revenue",
    F.col("quantity") * F.col("unit_price") * (1 - F.col("discount_pct"))
)

# Revenue by payment method
orders_clean.groupBy("payment_method").agg(
    F.round(F.sum("revenue"), 2).alias("revenue")
).orderBy(F.desc("revenue")).show()

# Join orders with customers
orders_with_customers = orders_clean.join(customers, "customer_id", "inner")
orders_with_customers.select("order_id", "customer_name", "city", "region").show()

# Revenue by product category
orders_with_products = orders_clean.join(products, "product_id", "inner")
orders_with_products.groupBy("category").agg(
    F.round(F.sum("revenue"), 2).alias("revenue")
).orderBy(F.desc("revenue")).show()

# Customers who have never ordered
customers.join(
    orders.select("customer_id").distinct(),
    "customer_id",
    "left_anti"
).show()

# Most recent order per customer
w = Window.partitionBy("customer_id").orderBy(
    F.to_date("order_date").desc(), F.col("order_id").desc()
)
latest_orders = orders.withColumn("rn", F.row_number().over(w)).filter("rn = 1")
latest_orders.show()

# Monthly revenue by region
monthly_gold = (
    orders_clean.join(customers, "customer_id")
    .withColumn("order_month", F.date_format(F.to_date("order_date"), "yyyy-MM"))
    .groupBy("order_month", "region")
    .agg(F.round(F.sum("revenue"), 2).alias("revenue"))
)
monthly_gold.write.mode("overwrite").parquet(
    f"{parquet_base}/monthly_revenue_by_region"
)

# Write cleaned data as a managed Delta table
orders_clean.write.format("delta").mode("overwrite").saveAsTable(
    "retail_lab.cleaned_orders"
)
