def getBookTitleResolution(slots):
    if "Book" in slots:
        #book_title = slots["Book"].value.lower()
        book_title = slots["Book"].resolutions.resolutions_per_authority[0].values[0].value.name.lower()
        return (True, book_title)
    else:
        return (False, None)
    
def getAuthorNameResolution(slots):
    if "Author" in slots:
        author_name = slots["Author"].resolutions.resolutions_per_authority[0].values[0].value.name
        return (True, author_name)
    else:
        return (False, None)

def getGenreResolution(slots):
    if "Genre" in slots:
        genre = slots["Genre"].value.lower()
        return (True, genre)
    else:
        return (False, None)
