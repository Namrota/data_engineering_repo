------------------- Role -----------------------------
USE ROLE ACCOUNTADMIN;
------------------- Grant warehouse permissions -------
GRANT USAGE ON WAREHOUSE SNOWFLAKE_LEARNING_WH TO ROLE ACCOUNTADMIN;
------------------- Create a database -----------------
CREATE DATABASE IF NOT EXISTS BREWBEATS_DB;
USE DATABASE BREWBEATS_DB;
------------------- Create SCHEMA ---------------------
CREATE SCHEMA IF NOT EXISTS BREWBEATS_DB.BRONZE;
USE SCHEMA BRONZE;

-------- At this point I have uploaded the file as a table
SELECT *
FROM RAW_COFFEE_SALES
LIMIT 10;

-------- Verifying the snowflake table
DESC TABLE RAW_COFFEE_SALES;
SELECT COUNT(*) FROM RAW_COFFEE_SALES;


-- Q1. Write the SQL to create a stage and load coffee_sales.csv into a Snowflake table.
-- Steps to create a STAGE and load the .csv file in it:
-- Create internal stage
CREATE STAGE IF NOT EXISTS brewbeats_stg
FILE_FORMAT = (
TYPE = CSV
SKIP_HEADER = 1
FIELD_DELIMITER = ','
FIELD_OPTIONALLY_ENCLOSED_BY = '"');

--Ingestion -> Add Data -> Load Files to STAGE -> Select the coffee_sales.csv file
-- Enter Upload.
-- Verify if the file got uploaded successfully

LIST @BREWBEATS_DB.BRONZE.BREWBEATS_STG;

-- Since the file uploaded in the Staging area is a raw CSV file, $1, $2 and so on are positional number for the columns with as alias. Snowflake reads the positional fields from the CSV.
-- $<file_col_num>
-- @<stage_name>: used to reference a stage where the files are stored

SELECT
    $1 AS DATE,
    $2 AS DATETIME,
    $3 AS CASH_TYPE,
    $4 AS CARD,
    $5 AS MONEY,
    $6 AS COFFEE_NAME
FROM @BREWBEATS_STG
LIMIT 5;

-- Q2. Write a query to find the top 3 coffee types by revenue.

SELECT coffee_name, SUM(money)
FROM raw_coffee_sales
GROUP BY 1
ORDER BY 2 DESC
LIMIT 3;

-- Q3.Write the SQL to create a stage and load spotify.csv into a Snowflake table.
-- Create internal stage
CREATE STAGE IF NOT EXISTS spotify_stg
FILE_FORMAT = (
TYPE = CSV
SKIP_HEADER = 1
FIELD_DELIMITER = ','
FIELD_OPTIONALLY_ENCLOSED_BY = '"');

LIST @SPOTIFY_STG;

SELECT 
    $1 AS acousticness,
    $2 AS danceability,
    $3 AS duration_ms,
    $4 AS energy,
    $5 AS instrumentalness,
    $6 AS key,
    $7 AS liveness,
    $8 AS loudness
FROM @SPOTIFY_STG
LIMIT 5;

DESC TABLE spotify;

ALTER TABLE spotify RENAME TO raw_spotify;

-- Q4. Write a query to find the top 3 songs by Drake.
SELECT song_title, danceability
FROM raw_spotify
WHERE artist ILIKE '%drake%' and danceability > 0.80
ORDER BY 2 DESC
LIMIT 3;

----------------------- For DBT---------------------------------

SELECT CURRENT_ORGANIZATION_NAME(), CURRENT_ACCOUNT_NAME();

DESC USER "namrotag.stocks";

----------- Grant ACCESS:
USE ROLE ACCOUNTADMIN;

GRANT CREATE SCHEMA
ON DATABASE BREWBEATS_DB
TO ROLE DBT_ROLE;

----------- Verify Silver stage--------------------
USE SCHEMA BREWBEATS_DB.DBT_DEV_SILVER;
-- 3636 rows
SELECT COUNT(*) FROM stg_coffee_sales;
DESC VIEW stg_coffee_sales;
SELECT * FROM stg_coffee_sales
LIMIT 10;

------------- Verify Gold stage -------------------
USE SCHEMA BREWBEATS_DB.DBT_DEV_GOLD;

SELECT * FROM fct_daily_revenue
LIMIT 20;

------------ Validate if there are any null values
SELECT
    COUNT_IF(SALE_DATE IS NULL) AS NULL_SALE_DATE,
    COUNT_IF(TOTAL_SALES IS NULL) AS NULL_TOTAL_SALES,
    COUNT_IF(TOTAL_REVENUE_PER_DAY IS NULL) AS NULL_TOTAL_REVENUE_PER_DAY,
    COUNT_IF(AVG_SALES_VAL IS NULL) AS NULL_AVG_SALES_VAL
FROM FCT_DAILY_REVENUE;

----------- Verifying actual date ransge:
SELECT
    MIN(SALE_DATE) AS FIRST_SALE_DATE,
    MAX(SALE_DATE) AS LAST_SALE_DATE,
    COUNT(*) AS DAYS_WITH_SALES
FROM FCT_DAILY_REVENUE;

---------- Verify if there are records for the last available SALE_DATE:
SELECT
    SALE_DATE,
    TOTAL_SALES,
    TOTAL_REVENUE_PER_DAY,
    AVG_SALES_VAL
FROM FCT_DAILY_REVENUE
WHERE SALE_DATE = (
    SELECT MAX(SALE_DATE)
    FROM FCT_DAILY_REVENUE
);

--------------------------------------------------------------------------------------