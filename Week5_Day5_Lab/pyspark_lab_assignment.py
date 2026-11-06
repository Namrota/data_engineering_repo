
'''
 **Q. 3 — Create a Local Spark Application**

Create a local Spark application named:

<aside>
💡

britmart_foundations

</aside>

Create a DataFrame from:

<aside>
💡

[
(101, "London", 45.50),
(102, "Manchester", 18.00),
(103, "Leeds", 30.00),
]

</aside>

Display the rows and stop the session.


Expected Output:

+--------+----------+------+
|order_id|      city|amount|
+--------+----------+------+
|     101|    London|  45.5|
|     102|Manchester|  18.0|
|     103|     Leeds|  30.0|
+--------+----------+------+

root
 |-- order_id: long (nullable = true)
 |-- city: string (nullable = true)
 |-- amount: double (nullable = true)

'''



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

# Creating the psark session and context

from pyspark.sql import SparkSession

# SparkSession is the main entry point to Spark functionality.
# SparkSession.builder: Starts configuring a SparkSession
# .appNamne("MyFirstPySparkPropject"): Assigns a mname to the Saprk application
# .master("local[2]"): runs Spark locally with two worker threads.
# .getOrCreate(): creates a new SparkSession if one does not exist, or returns the existing one.

spark = (
    SparkSession.builder
    .appName("britmart_foundations")
    .master("local[2]")
    .getOrCreate()
)


# reduces Spark log messages to only show errors, making the output more cleaner and readable.
sc= spark.sparkContext
sc.setLogLevel("ERROR")

data= [
    (101, "London", 45.50),
    (102, "Manchester", 18.00),
    (103, "Leeds", 30.00),
]

df= spark.createDataFrame(data, ["order_id", "city", "amount"])
df.show() # displays the contents of the DataFrane in a tabular format
df.printSchema() # prints the schema of the DataFrame, column names and their data types
spark.stop()