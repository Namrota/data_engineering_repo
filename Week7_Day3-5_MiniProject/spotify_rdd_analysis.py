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

file_path= Path("spotify_data.csv").resolve()

'''
Troubleshooting:

print("File exists:", file_path.exists())
print("File size:", file_path.stat().st_size)
print("Spark master:", sc.master)

# Test 1: Python-created RDD
print("Test 1:")
print(sc.parallelize(["hello", "spotify"]).take(2))

# Test 2: Read the file using standard Python
print("Test 2:")
with open(file_path, "r", encoding="utf-8-sig") as f:
    for _ in range(3):
        print(repr(f.readline()[:200]))

# Test 3: Read the file using Spark DataFrame API
print("Test 3:")
df = spark.read.option("header", True).csv(str(file_path))
df.show(5, truncate=False)



'''

spark.stop()