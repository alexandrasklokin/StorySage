import requests
import re

CLEANR = re.compile('<.*?>')

def makeRequestMultiResponse(url, search_param, search_result):
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract book genres from the API response
        data = response.json()
        temp_list = []
        pages = data['query'][search_param]
        for page in pages:
            temp_list.append(page[search_result])
        return (True, temp_list)
        
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}, {response.reason}")
        return (False, f"An error occurred. Please try again.")
    
def getGenreByBook(book_title):
    url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&titles={book_title}'
    (flag, books) = makeRequestMultiResponse(url, 'title', 'categories')
    return (flag, books)

def getBooksByGenre(genre):
    url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:{genre}'
    (flag, books) = makeRequestMultiResponse(url, 'categorymembers', 'title')
    return (flag, books)

def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

def getAuthorDescription(author_name):
    url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=true&titles={author_name}'
    response = requests.get(url)
    data = response.json()

    # Extract the description from the API response
    pages = data['query']['pages']
    for page_id in pages:
        page = pages[page_id]
        if 'extract' in page:
            description = cleanhtml(page['extract'])
            return (True, description.strip())

    return (False, None)