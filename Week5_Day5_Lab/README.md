### Text Analysis using PySpark:

#### Extract:
For this project an article is extracted from Wikipedia page. Function `extract_article` in `extract_article.py` successfully extracts an article using BeautifulSoup and further lightly transforms the raw data to filter out citation subscrioted numbers from the article (source).

#### Load:
The extracted article is then saved as a .txt file using the function `save_article_to_file` in `extract_article.py`

#### Transform:
Once the file is loaded into a given path, I will be using pySpark to:
- read the text file from the local dirctory: `sc.textFile()`
- split the lines of the article into words and convert them all into lower case: `flatMap(lambda line: line.lower().split())`
- filter out non-alphabets or stop words from the list: ` words.filter(lambda word: word.isalpha() and word not in stopwords)`
- finally use reduceByKey inorder to get the frequency of words: `clean_words.map(lambda word: (word,1)).reduceByKey(lambda a,b: a+b)`
- lastly, to get the top 5 words, sort by values in descending order: `word_counts.takeOrdered(5, key= lambda x: -x[1])`

where, pyspark.RDD.takeOrdered ---> Get the N elements from an RDD ordered in ascending order or as specified by the optional key function.