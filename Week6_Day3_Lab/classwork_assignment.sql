//Q1. Show the first 10 bookings.
SELECT * FROM travel_bookings LIMIT 10;

//Q2. How many bookings are there in total?
SELECT COUNT(*) as total_bookings FROM travel_bookings;

//Q3. List all bookings to Spain.
SELECT booking_id, customer_id, customer_name, home_city
FROM travel_bookings
WHERE LOWER(destination_country) = 'spain';

//Q4. Find all Cancelled bookings.
SELECT * 
FROM travel_bookings
WHERE lower(status)= 'cancelled';

//Q5. Which bookings have no discount recorded (NULL)?
SELECT booking_id, booking_date, customer_name, discount_pct, destination_country
FROM travel_bookings
WHERE discount_pct is null;

//Level 2: Aggregations

//Q6. Calculate the revenue for every booking.
SELECT booking_id, round(sum(travellers * PRICE_PER_PERSON_GBP * (1- ifnull(discount_pct, 0)/100)),2) as revenue_per_booking_gbp
FROM travel_bookings
GROUP BY booking_id
ORDER BY revenue_per_booking_gbp desc;

//Q7. Total revenue by package type for non-cancelled bookings, highest first.
SELECT package_type,  round(sum(travellers * PRICE_PER_PERSON_GBP * (1- ifnull(discount_pct, 0)/100)),2) as revenue_per_package
FROM travel_bookings
WHERE lower(status) <> 'cancelled'
GROUP BY package_type
ORDER BY revenue_per_package desc;

//Q8. Which destination country is booked most often?
SELECT destination_country, count(destination_country) as booking_count
FROM travel_bookings
GROUP BY destination_country
ORDER BY booking_count desc
LIMIT 1;

//Q9. Share of bookings by payment mode.
SELECT payment_mode,
       COUNT(*) AS bookings,
       ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_share
FROM travel_bookings
GROUP BY payment_mode
ORDER BY bookings DESC;

//Q10. Customers with more than 2 bookings.
SELECT customer_id, count(customer_id) as bookings_done
FROM travel_bookings
WHERE lower(status) <> 'cancelled'
GROUP BY customer_id
HAVING bookings_done >= 2
ORDER BY bookings_done desc;


//Q11. Average rating per destination country (ignore NULL ratings), with at least 2 rated trips.
SELECT destination_country, round(avg(rating)) as avg_rating, count(rating) as rated_trip
FROM travel_bookings
GROUP BY destination_country
HAVING rated_trip >= 2
ORDER BY rated_trip desc;

//Q12. Work out each trip's return date and how far in advance it was booked.
SELECT booking_id, travel_start_date, dateadd('day', nights, travel_start_date) as return_date, datediff('day', booking_date, travel_start_date) as advance_booking_date
FROM travel_bookings
WHERE lower(status) <> 'cancelled';

//Q13. Monthly bookings count and revenue by travel month.
SELECT MONTH(travel_start_date) as travel_month, count(booking_id) as booking_count, ROUND(SUM(travellers * price_per_person_gbp * (1 - COALESCE(discount_pct,0)/100)), 2) AS revenue_gbp
FROM travel_bookings
GROUP BY travel_month
ORDER BY revenue_gbp desc;

//Q14. Rank customers by total spend within each home city.
with customer_spend as(
    SELECT customer_id, home_city, ROUND(SUM(travellers * price_per_person_gbp * (1-            COALESCE(discount_pct,0)/100)), 2) as total_spend
    FROM travel_bookings
    GROUP BY customer_id, home_city
)
SELECT customer_id, home_city, total_spend, dense_rank() over (
    partition by home_city
    order by total_spend desc) as rank_customers
FROM customer_spend
ORDER BY home_city, rank_customers, customer_id;

//Q15. For repeat customers, show the gap in days between consecutive bookings.
SELECT customer_id, booking_date, ifnull(datediff('day', LAG(booking_date) OVER (partition by customer_id order by booking_date), booking_date),0) as last_booking_date
FROM travel_bookings
QUALIFY COUNT(*) OVER(PARTITION BY customer_id) > 1
ORDER BY customer_name, booking_date;

//Q16. Top 2 destinations by revenue within each package type (use QUALIFY).
SELECT destination_country, package_type, round(sum(travellers * price_per_person_gbp),2) as revenue_gbp
FROM travel_bookings
WHERE lower(status) <> 'cancelled'
GROUP BY destination_country, package_type
QUALIFY RANK() OVER(PARTITION BY package_type order by revenue_gbp desc) <=2
ORDER BY revenue_gbp desc;

//Q17. Cancellation rate by package type.
SELECT package_type, count(*) as total_bookings, round(100 * (sum(iff(lower(status)='cancelled', 1, 0))/ count(*)), 2) as cancel_rate_pct
FROM travel_bookings
GROUP BY package_type;

//Q18. Segment bookings into Budget, Mid-range and Premium using CASE
SELECT booking_id, destination_city, price_per_person_gbp,
       CASE
         WHEN price_per_person_gbp < 400 THEN 'Budget'
         WHEN price_per_person_gbp < 900 THEN 'Mid-range'
         ELSE 'Premium'
       END AS price_band
FROM travel_bookings;
