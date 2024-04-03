import requests

def getGenreDescription(genre):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{genre}'
    response = requests.get(url)
    data = response.json()
    meanings = data[0].get('meanings',None)[0].get('definitions',None)[0].get('definition',None)
    if meanings:
        return (True, meanings)
    else:
        return (False, None)  # Return None if no definition is found