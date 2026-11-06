
'''
Create a Text Analysis application using PySpark.

- the application will read a text file, process the text and count top 5 most frequent words
- exclude NLTK stop words from the count
- display top 5 words with their counts in descending order

--PySpark: to process the text data and perform analysis on it
- SparkSession: main entry point to Spark application
- SparkContext: entry point to Spark functionality, provides low-level functionality to work with RDDs

This section now reads the saved article from the text file using PySaprk.
Processes the text and count the top most frequent words, excluding the
NLTK stop words from the count.
Finally, it displays top 5 words with their counts in descending order.
'''
# gives information about the Python interpreter and its environment
import sys
import os
import requests

# fetch stop words from the URL and store them in set for efficient lookup
stopwords_url= "https://raw.githubusercontent.com/stopwords-iso/stopwords-en/master/stopwords-en.txt"
stopwords_list = requests.get(stopwords_url, timeout= 15).content
stopwords = set(stopwords_list.decode().splitlines())
#print(stopwords)


# Use the same Python for the driver and workers
#We store that interpreter path in a variable
python_exe = sys.executable
# This tells Spark which Python executable to use for worker processes that execute Python transformations
os.environ["PYSPARK_PYTHON"] = python_exe
# This tells Spark which Python executable to use for the driver process
os.environ["PYSPARK_DRIVER_PYTHON"] = python_exe
# Path to the article text file:
file_path= "Week5_Day5_Lab/article.txt"

# Creating the pysark session and context
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

# fetch article from .txt file:
extracted_file= sc.textFile(file_path)

# display just a few rows of the extracted file
print(extracted_file.take(5))

# split the text into words, and covert them into lowercase
words= extracted_file.flatMap(lambda line: line.lower().split())
print("First 20 words: ", words.take(20))

#filter out non-alphabtic words and stop words from the list of words
clean_words= words.filter(lambda word: word.isalpha() and word not in stopwords)
print("First 20 clean words: ", clean_words.take(20))

# count the frequency of each word using map and reduceByKey
word_counts= clean_words.map(lambda word: (word,1)).reduceByKey(lambda a,b: a+b)
print("Top 5 words with their counts in descending order: ", word_counts.takeOrdered(5, key= lambda x: -x[1]))

spark.stop()