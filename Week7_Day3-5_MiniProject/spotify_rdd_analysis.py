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

# Create a spark session and context
spark = (
    SparkSession.builder
    .appName("spotify_analysis")
    .getOrCreate()
)

sc= spark.sparkContext
sc.setLogLevel("ERROR")

file_path= Path("spotify_data.csv").resolve()
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
df= (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(file_path))
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
coffee_df.describe().show()
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


spark.stop()