import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from api_utils_google import getAuthorsByBook, getAuthorsByGenre # CUSTOM API HANDLING FUNCTIONS
from api_utils_wikipedia import getAuthorDescription # CUSTOM API HANDLING FUNCTIONS
from helpers import getBookTitleResolution, getAuthorNameResolution, getGenreResolution # SLOT RESOLUTION HELPERS

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


########################################################################################################################################################
## ______________________________________________________________________________________________________________________________________ AUTHOR INTENTS 
########################################################################################################################################################

## ____________________________________________________________________________________________________________________Author_ByBook_Intent
class Author_ByBook_IntentHandler(AbstractRequestHandler):
    """Handler for Request of Author by Book Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Author_ByBook_Intent")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        (flag_title, book_title) = getBookTitleResolution(slots)
        
        if flag_title:
            (flag_author, authors) = getAuthorsByBook(book_title)
            string_authors = ', '.join(authors)
            
            if flag_author and string_authors!=None:
                speak_output = '"'+book_title.title()+'" is written by '+string_authors.title()+'.'
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
    
## ____________________________________________________________________________________________________________________Authors_ByGenre_Intent
class Authors_ByGenre_IntentHandler(AbstractRequestHandler):
    """Handler for Request of Authors by Genre Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Authors_ByGenre_Intent")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        (flag_genre, genre) = getGenreResolution(slots)
        
        if flag_genre:
            (flag_author, authors) = getAuthorsByGenre(genre)
            string_authors = ', '.join(authors)
            
            if flag_author and string_authors!=None:
                speak_output = 'Here are some "'+genre.title()+'" writters: '+string_authors.title()+'.'
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
    
## ____________________________________________________________________________________________________________________AuthorDescription_Intent
class AuthorDescription_IntentHandler(AbstractRequestHandler):
    """Handler for Request of Author Description Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AuthorDescription_Intent")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        (flag_author, author_name) = getAuthorNameResolution(slots)
        
        if flag_author:
            (flag_description, description) = getAuthorDescription(author_name)
            
            if flag_description and description!=None:
                speak_output = description
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