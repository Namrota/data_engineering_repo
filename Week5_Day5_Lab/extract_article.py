'''
Create a Text Analysis application using PySpark.

- the application will read a text file, process the text and count top 5 most frequent words
- exclude NLTK stop words from the count
- display top 5 words with their counts in descending order

-- Python:
- requests: to fetch the stop words from the URL
- os: to interact with the operating system
- sys: gives information about the Python interpreter and its environment
- BeautifulSoup: to parse the HTML content of the article

'''

import requests
import os
from bs4 import BeautifulSoup

def extract_article(url):
    '''
    Fetches the article from the given URL and returns the plain text content.

    Parameters:
        url (str): The URL of the article to fetch.
    '''

    '''
    The request lib sends an HTTP GET request to the specified URL,
    and the response is stored in the `response` variable.

    headers: specifies the User-Agent header to identify the request as coming from a Python script.
    This is important because some websites block requests that do not have a valid User-Agent header.
    In this case status error code: 403 (Forbidden) was returned before implementing it.

    timeout: specifies the maximum time (in seconds) to wait for a response to the server.
    If the server does not respons within this time, a timeout exception is raised.
    '''
    response = requests.get(
        url,
        headers={"User-Agent": "PythonSparkLearning/1.0 (educational project)"},
        timeout=20
    )
    # raise an exception if the request was unsuccessful (status code 4xx or 5xx)
    response.raise_for_status()
    # parse the HTML content of the article:
    soup = BeautifulSoup(response.text, "html.parser")
    '''
    select_one(): selects the first element that matches the CSS selector "#bodyContent",
    which is the main content area of the Wikipedia article.

    decompose(): removes the selected elemeents from the parse tree, effectively deleting from the HTML
    document. In this case it removes the citation references (subscripted numbers) from the article.

    '''
    article_content = soup.select_one("#bodyContent")
    for citation in article_content.select("sup.mw-ref, sup.reference"):
        citation.decompose()
    paragraphs = article_content.find_all("p")
    # get_text(): extracts the text content from the paragraph elements,
    # " " is used as the separator between the text of the paragraphs
    # strip= True removes the leading and the trailing Whitespaces
    article_text = [
        p.get_text(" ", strip=True)
        for p in paragraphs
        if p.get_text(strip=True)      # Keeps only paragraphs containing non-whitespace text
    ]
    return '\n'.join(article_text)


def save_article_to_file(output_path):
    '''
    Saves the article text to a specified file

    '''
    # Save the article in the text file
    saved_loc= output_path if output_path else "article.txt"
    article_text= extract_article(article_URL)
    with open(saved_loc, 'w', encoding= 'utf-8') as f:
        f.write(''.join(article_text))
    print(f"Article saved to: {os.path.abspath(saved_loc)}")

# Write article from Wikipedia into a text file:
article_URL= "https://en.wikipedia.org/wiki/False_memory"
save_article_to_file("Week5_Day5_Lab/article.txt")