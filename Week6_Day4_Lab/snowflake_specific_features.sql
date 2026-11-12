show tables;

//Level 4: Snowflake-Specific Features (great for live demos)

//Q19. Time Travel. Delete Cancelled bookings by mistake, then recover the

SELECT COUNT(*) from travel_bookings; -- around 30 rows in total

DELETE FROM travel_bookings WHERE status = 'Cancelled';

SELECT COUNT(*) FROM travel_bookings; -- reduced number of rows

-- Table as it was 5 minutes ago
SELECT COUNT(*) FROM travel_bookings AT(OFFSET => -60*5);

-- Restore using the query ID of the DELETE (see Query History)
INSERT INTO travel_bookings
SELECT * FROM travel_bookings BEFORE(STATEMENT => '01c85c0b-0000-bb7f-0001-49a60002f1ea')
WHERE status = 'Cancelled';

SELECT COUNT(*) FROM travel_bookings WHERE lower(status) = 'cancelled';


//Q20. Zero-copy cloning. Create a dev copy instantly and change it safely.
CREATE TABLE bookings_dev CLONE travel_bookings;
UPDATE bookings_dev SET status = 'Completed' WHERE status = 'Upcoming';

SELECT status, COUNT(*) FROM travel_bookings GROUP BY status;      -- unchanged
SELECT status, COUNT(*) FROM bookings_dev GROUP BY status;  -- changed


//Q21. UNDROP.
DROP TABLE bookings_dev;
UNDROP TABLE bookings_dev;

//Q22. Semi-structured data (VARIANT). Query JSON from a booking website's event log.
// event TABLE
// VARIANT allows Snowflake
CREATE OR REPLACE TABLE booking_events (event VARIANT);

//JSON data: parse_json()
INSERT INTO booking_events
SELECT PARSE_JSON('{"booking_id":2001,"device":"mobile","extras":[{"name":"Airport Transfer","price":35},{"name":"Travel Insurance","price":22}]}');


SELECT event:booking_id::INT AS booking_id,
       event:device::STRING AS device,
       f.value:name::STRING AS extra_name,
       f.value:price::NUMBER AS extra_price_gbp
FROM booking_events,
     LATERAL FLATTEN(input => event:extras) f;

//Q23. Secure data sharing idea. Create a view for the marketing team that hides customer names.
-- share only the required columns
CREATE OR REPLACE VIEW v_marketing_bookings AS
SELECT booking_id, home_city, destination_country, package_type,
       travel_start_date, travellers, status
FROM travel_bookings;

//Q24. Dynamic data masking (Enterprise edition). Mask customer names for non-admin roles.
CREATE OR REPLACE MASKING POLICY mask_name AS (val STRING) RETURNS STRING ->
  CASE WHEN CURRENT_ROLE() IN ('ACCOUNTADMIN') THEN val ELSE '*** MASKED ***' END;


ALTER TABLE travel_bookings MODIFY COLUMN customer_name SET MASKING POLICY mask_name;

SELECT * FROM travel_bookings;


-- check role:
SELECT
    CURRENT_ROLE() AS ACTIVE_ROLE,
    CURRENT_DATABASE() AS DATABASE_NAME,
    CURRENT_SCHEMA() AS SCHEMA_NAME;

USE ROLE SNOWFLAKE_LEARNING_ROLE;

SELECT CURRENT_ROLE();

SELECT booking_id, customer_name
FROM travel_bookings
LIMIT 5;

USE ROLE ACCOUNTADMIN;