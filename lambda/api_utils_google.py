import requests

API_KEY = "AIzaSyDyKmIDHPgjacF9BKHFmPYiLJNwaK13e4U"

def makeRequest(url, search_param):
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract book description from the API response
        data = response.json()
        if 'items' in data:
            book_info = data['items'][0]['volumeInfo']
            book_description = book_info.get(search_param, None)
            
            return (True, book_description)
        else:
            return (False, f"Book '{BOOK_TITLE}' not found.")
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}, {response.reason}")
        return (False, f"An error occured. Please try again.")

def makeRequestMultiResponse(url, search_param):
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract book description from the API response
        data = response.json()
        temp_list = []
        if 'items' in data:
            for item in data['items']:
                book_info = item['volumeInfo']
                book_search_value = book_info.get(search_param, None)
                temp_list.append(book_search_value)
            
            return (True, temp_list)
        else:
            return (False, None)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}, {response.reason}")
        return (False, f"An error occured. Please try again.")

def getBookDescription(book_title):
    url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{book_title}&key={API_KEY}'
    (flag, description) = makeRequest(url, 'description')
    return (flag, description)

def getBookRating(book_title):
    url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{book_title}&key={API_KEY}'
    (flag, rating) = makeRequest(url, 'averageRating')
    return (flag, rating)

def getBookGenres(book_title):
    url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{book_title}&key={API_KEY}'
    (flag, categories) = makeRequest(url, 'categories')
    return (flag, categories)

def getBooksByBookGenre(book_title):
    (flag_genre, genres) = getBookGenres(book_title)
    if flag_genre:
        main_genre = genres[0]
        url = f'https://www.googleapis.com/books/v1/volumes?q=subject:{main_genre}&key={API_KEY}'
        (flag, books) = makeRequest(url, 'title')
    return (flag, main_genre, books)

def getBooksByAuthor(author_name):
    url = f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{author_name}&key={API_KEY}'
    (flag, books) = makeRequestMultiResponse(url, 'title')
    return (flag, books)

def getBooksByGenre(genre):
    url = f'https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&key={API_KEY}'
    (flag, books) = makeRequestMultiResponse(url, 'title')
    return (flag, books)

def getAuthorsByBook(book_title):
    url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{book_title}&key={API_KEY}'
    (flag, authors) = makeRequest(url, 'authors')
    return (flag, authors)

def getAuthorsByGenre(genre):
    url = f'https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&key={API_KEY}'
    (flag, authors) = makeRequestMultiResponse(url, 'authors')
    authors = [elem[0] for elem in authors]
    return (flag, authors)