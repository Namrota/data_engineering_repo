# os module to interact with the operating system
import os
# gives information about the Python interpreter and its environment
import sys
# Use the same Python for the driver and workers
#We store that interpreter path in a variable
python_exe = sys.executable
# This tells Spark which Python executable to use for worker processes that execute Python transformations
os.environ["PYSPARK_PYTHON"] = python_exe
# This tells Spark which Python executable to use for the driver process
os.environ["PYSPARK_DRIVER_PYTHON"] = python_exe
# Main entry point for the pyspark session and context
from pyspark.sql import SparkSession
from pathlib import Path
from pyspark.sql import functions as F
# Create a spark session and context
spark = (
    SparkSession.builder
    .appName("spotify_analysis")
    .getOrCreate()
)

sc= spark.sparkContext
sc.setLogLevel("ERROR")

file_path_spotify= Path("spotify_data.csv").resolve()
file_path_coffee= Path("coffee_sales.csv").resolve()

'''
Troubleshooting:

print("File exists:", file_path.exists())
print("File size:", file_path.stat().st_size)
print("Spark master:", sc.master)

#### Test 1: Python-created RDD
print("Test 1:")
print(sc.parallelize(["hello", "spotify"]).take(2))

#### Test 2: Read the file using standard Python
print("Test 2:")
with open(file_path, "r", encoding="utf-8-sig") as f:
    for _ in range(3):
        print(repr(f.readline()[:200]))

#### Test 3: Read the file using Spark DataFrame API
print("Test 3:")
df = spark.read.option("header", True).csv(str(file_path))
df.show(5, truncate=False)

Issue resolved: Creating RDD directly from CSV file led to Python worker crash when executing take(10)

Reading the CSV file as a DataFrame and converting it to RDD worked.

First 5 rows generated:

Row(acousticness=0.0102, danceability=0.833, duration_ms=204600, energy=0.434, instrumentalness=0.0219, key=2, liveness=0.165, loudness=-8.795, mode=1, speechiness=0.431, tempo=150.062, time_signature=4, valence=0.286, target=1, song_title='Mask Off', artist='Future')
Row(acousticness=0.199, danceability=0.743, duration_ms=326933, energy=0.359, instrumentalness=0.00611, key=1, liveness=0.137, loudness=-10.401, mode=1, speechiness=0.0794, tempo=160.083, time_signature=4, valence=0.588, target=1, song_title='Redbone', artist='Childish Gambino')
Row(acousticness=0.0344, danceability=0.838, duration_ms=185707, energy=0.412, instrumentalness=0.000234, key=2, liveness=0.159, loudness=-7.148, mode=1, speechiness=0.289, tempo=75.044, time_signature=4, valence=0.173, target=1, song_title='XannyFamily', artist='Future')
Row(acousticness=0.604, danceability=0.494, duration_ms=199413, energy=0.338, instrumentalness=0.51, key=5, liveness=0.0922, loudness=-15.236, mode=1, speechiness=0.0261, tempo=86.468, time_signature=4, valence=0.23, target=1, song_title='Master Of None', artist='Beach House')
Row(acousticness=0.18, danceability=0.678, duration_ms=392893, energy=0.561, instrumentalness=0.512, key=5, liveness=0.439,loudness=-11.648, mode=0, speechiness=0.0694, tempo=174.004, time_signature=4, valence=0.904, target=1, song_title='Parallel Lines', artist='Junior Boys')


### Q1. Load Spotify_data.csv into an RDD and count the number of songs per artist.

'''
# Convert the Dataframe to a RDD by using .rdd
'''
In PySpark, .option("inferSchema", "true") tells
Spark to automatically detect the data types of columns when reading a CSV file,
instead of treating every column as a string.

'''
df= (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(file_path_spotify))
    )

spotify_rdd= df.rdd

# Display records: testing
#for row in spotify_rdd.take(5):
#    print(row)

artists_rdd= spotify_rdd.map(lambda row: (row["artist"], 1))

count_songs_rdd= artists_rdd.reduceByKey(lambda a,b: a+b)

'''
Current data in count_somgs:
[('Future', 8), ('Childish Gambino', 2), ('Beach House', 6)]
Swapping key, value: [(8, 'Future'), (2, 'Childish Gambino'), (6, 'Beach House')]

'''
swapped_count_songs_rdd= count_songs_rdd.map(lambda x: (x[1], x[0]))
sort_count_rdd= swapped_count_songs_rdd.sortByKey(False)
#print("Top 5 artists:", sort_count_rdd.take(5))
'''
Output:
Top 5 artists: [(16, 'Drake'),
(13, 'Rick Ross'),
(12, 'Disclosure'),
(10, 'Backstreet Boys'),
(10, 'WALK THE MOON')]
'''

'''
### Q2. Using RDD transformations, find the average danceability across all songs.

'''

danceability_rdd= spotify_rdd.map(lambda row: row['danceability'])
danceability_avg= danceability_rdd.mean()
'''
Average danceability across all songs: 0.6184

'''
#print(f"Average danceability across all songs: {danceability_avg:.4f}")


'''
Q3. Load coffee_sales.csv into a DataFrame and find the total revenue.

'''
coffee_df= (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(file_path_coffee))
    )

# Data Validation:
# Print first 3 rows in tabular format
# print(coffee_df.show(3))
'''
+----------+--------------------+---------+-------------------+-----+-------------+
|      date|            datetime|cash_type|               card|money|  coffee_name|
+----------+--------------------+---------+-------------------+-----+-------------+
|2024-03-01|2024-03-01 10:15:...|     card|ANON-0000-0000-0001| 38.7|        Latte|
|2024-03-01|2024-03-01 12:19:...|     card|ANON-0000-0000-0002| 38.7|Hot Chocolate|
|2024-03-01|2024-03-01 12:20:...|     card|ANON-0000-0000-0002| 38.7|Hot Chocolate|
+----------+--------------------+---------+-------------------+-----+-------------+
'''

#coffee_df.printSchema()
'''
root
 |-- date: date (nullable = true)
 |-- datetime: timestamp (nullable = true)
 |-- cash_type: string (nullable = true)
 |-- card: string (nullable = true)
 |-- money: double (nullable = true)
 |-- coffee_name: string (nullable = true)
'''
# Summary of the DataFrame
#coffee_df.describe().show()
'''
+-------+---------+-------------------+------------------+-----------+
|summary|cash_type|               card|             money|coffee_name|
+-------+---------+-------------------+------------------+-----------+
|  count|     3636|               3547|              3636|       3636|
|   mean|     NULL|               NULL|31.746859185917987|       NULL|
| stddev|     NULL|               NULL| 4.919925803555432|       NULL|
|    min|     card|ANON-0000-0000-0001|             18.12|  Americano|
|    max|     cash|ANON-0000-0000-1316|              40.0|      Latte|
+-------+---------+-------------------+------------------+-----------+

As can be seen there are NULL values in the column `card`.

'''
total_revenue= coffee_df.agg(
    F.sum(
        F.col("money").cast("decimal(12,2)")
    ).alias("Total Revenue Generated")
)

#total_revenue.show()

'''
+-----------------------+
|Total Revenue Generated|
+-----------------------+
|              115431.58|
+-----------------------+


Q4. Find the number of transactions for each coffee_name using groupBy.
'''

coffee_name_grouping= (
    coffee_df
    .groupBy('coffee_name')
    .agg(
        F.sum(coffee_df["money"]
              .cast("decimal(12,2)")).alias("total_transactions"))
)
#coffee_name_grouping.show()

'''
Output:

+-------------------+------------------+
|        coffee_name|total_transactions|
+-------------------+------------------+
|           Espresso|           2814.28|
|Americano with Milk|          25269.12|
|              Latte|          27866.30|
|          Americano|          15062.26|
|      Hot Chocolate|          10172.46|
|              Cocoa|           8678.16|
|            Cortado|           7534.86|
|         Cappuccino|          18034.14|
+-------------------+------------------+


Q5. Add a new column for month from the date column, and find total revenue per month.
'''

coffee_sales_data= coffee_df.withColumn(
    'months', F.month(coffee_df.date))

grouping_by_month= (
    coffee_sales_data
    .groupBy('months')
    .agg(
        F.sum(coffee_df["money"]
              .cast("decimal(12,2)")).alias("total_transactions"))
)

ordering_by_transactions= grouping_by_month.orderBy(coffee_sales_data.months)

#ordering_by_transactions.show()

'''
Output:

+------+------------------+
|months|total_transactions|
+------+------------------+
|     1|           6398.86|
|     2|          13215.48|
|     3|          17036.64|
|     4|           6720.56|
|     5|           9063.42|
|     6|           7758.76|
|     7|           6915.94|
|     8|           7613.84|
|     9|           9988.64|
|    10|          13891.16|
|    11|           8590.54|
|    12|           8237.74|
+------+------------------+


Q7. How many times the songs had ‘love’ in them?

'''
love_songs= spotify_rdd.filter(lambda row: "love" in row["song_title"].lower()).count()
#print(f"songs with love in them: {love_songs}")

'''
Output:
songs with love in them: 88


Q8. BrewBeats wants to play some party songs for their 5th Birthday , curate a songs list for them.
'''
anniversary_songs= spotify_rdd.filter(lambda rows: rows["danceability"] >= 0.7 and rows["energy"] >= 0.7)
for song in anniversary_songs.take(10):
    print(
        "| Song_title:", song["song_title"],
        "| Artist:", song["artist"],
        "| Danceability:", song["danceability"],
        "| Energy:", song["energy"]
    )

'''
Output:

| Song_title: Donme Dolap - Baris K Edit | Artist: Modern Folk Üçlüsü | Danceability: 0.753 | Energy: 0.748
| Song_title: C O O L - Radio Edit | Artist: Le Youth | Danceability: 0.735 | Energy: 0.759
| Song_title: Percolator (Jamie Jones Vault Mix) - mixed | Artist: Cajmere | Danceability: 0.854 | Energy: 0.719
| Song_title: House of Jealous Lovers | Artist: The Rapture | Danceability: 0.747 | Energy: 0.74
| Song_title: This Ready Flesh | Artist: TR/ST | Danceability: 0.781 | Energy: 0.795
| Song_title: Poppin' My Collar | Artist: Three 6 Mafia | Danceability: 0.722 | Energy: 0.823
| Song_title: 07-Nov | Artist: Beyoncé | Danceability: 0.747 | Energy: 0.705
| Song_title: Bang That | Artist: Disclosure | Danceability: 0.731 | Energy: 0.852
| Song_title: Return Of The Mack - C & J Street Mix | Artist: Mark Morrison | Danceability: 0.715 | Energy: 0.833
| Song_title: Fantastic Man | Artist: William Onyeabor | Danceability: 0.7 | Energy: 0.756

'''

spark.stop()