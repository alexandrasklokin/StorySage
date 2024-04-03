import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from api_utils_google import getBookDescription, getBookRating, getBooksByAuthor, getBooksByGenre # CUSTOM API HANDLING FUNCTIONS
#from api_utils_wikipedia import getBooksByBookGenre
from helpers import getBookTitleResolution, getAuthorNameResolution, getGenreResolution # SLOT RESOLUTION HELPERS

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


########################################################################################################################################################
## ______________________________________________________________________________________________________________________________________ BOOK INTENTS 
########################################################################################################################################################

## ____________________________________________________________________________________________________________________Books_ByAuthor_Intent
class Books_ByAuthor_IntentHandler(AbstractRequestHandler):
    """Handler for Request of Book by Author Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Books_ByAuthor_Intent")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        (flag_author, author_name) = getAuthorNameResolution(slots)
        
        if flag_author:
            (flag_books, books) = getBooksByAuthor(author_name)
            string_books = ', '.join(books)
            
            if flag_books and string_books!=None:
                speak_output = 'Some of the books by "'+author_name.title()+'" are: '+string_books+'.'
            else:
                speak_output = "Sorry, I could not find the author you mentioned. Ask me about another one!"
                
        else:
            speak_output = "Sorry, I don't believe that you included the name of the author. Try asking me again!"
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
    
## ____________________________________________________________________________________________________________________Books_ByGenre_Intent
class Books_ByGenre_IntentHandler(AbstractRequestHandler):
    """Handler for Request of Book by Genre Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Books_ByGenre_Intent")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        (flag_genre, genre) = getGenreResolution(slots)
        
        if flag_genre:
            (flag_books, books) = getBooksByGenre(genre)
            string_books = ', '.join(books)
            
            if flag_books and string_books!=None:
                speak_output = 'Some of the books in the genre of "'+genre.title()+'" are: '+string_books+'.'
            else:
                speak_output = "Sorry, I couldn't recognize that genre. Ask me about another one!"
                
        else:
            speak_output = "Sorry, I don't believe that you included the name of the author. Try asking me again!"
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

## ____________________________________________________________________________________________________________________BookRating_Intent
class BookRating_IntentHandler(AbstractRequestHandler):
    """Handler for Request of Book Rating Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("BookRating_Intent")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        (flag_title, book_title) = getBookTitleResolution(slots)
        
        if flag_title:
            (flag_rating, rating) = getBookRating(book_title)
            
            if flag_rating and rating!=None:
                speak_output = 'The average rating for "'+book_title.title()+'" is '+str(rating)+'.'
            else:
                speak_output = "Sorry, I could not find the book you mentioned. Ask me about another one!"
                
        else:
            speak_output = "Sorry, I don't believe that you included the name of the book. Try asking me again!"
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

## ____________________________________________________________________________________________________________________BookDescription_Intent
class BookDescription_IntentHandler(AbstractRequestHandler):
    """Handler for Request of Book Description Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("BookDescription_Intent")(handler_input)
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        slots = handler_input.request_envelope.request.intent.slots
        (flag_title, book_title) = getBookTitleResolution(slots)
        
        if flag_title:
            
            (flag_description, description) = getBookDescription(book_title)
            
            # Shorten the description
            sentences = description.split('.')
            if len(sentences) >= 3:
                short_description = '.'.join(sentences[:3]) + '.'
            else:
                short_description = description
            
            if flag_description:
                speak_output = 'Sure! Here is the description for the book "'+book_title.title()+'": '+short_description
            else:
                speak_output = "Sorry, I could not find the book you mentioned. Ask me about another one!"
        
        else:
            speak_output = "Sorry, I don't believe that you included the name of the book. Try asking me again!"
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )