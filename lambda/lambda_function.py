# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

########################################################################################################################################################
## ______________________________________________________________________________________________________________________________________ BOOK INTENTS 
########################################################################################################################################################
from book_intents import Books_ByAuthor_IntentHandler, Books_ByGenre_IntentHandler, BookRating_IntentHandler, BookDescription_IntentHandler #, Books_ByBookGenre_IntentHandler

########################################################################################################################################################
## ______________________________________________________________________________________________________________________________________ AUTHOR INTENTS 
########################################################################################################################################################
from author_intents import Author_ByBook_IntentHandler, Authors_ByGenre_IntentHandler, AuthorDescription_IntentHandler

########################################################################################################################################################
## ______________________________________________________________________________________________________________________________________ AUTHOR INTENTS 
########################################################################################################################################################
from genre_intents import GenreDescription_IntentHandler # Genre_ByBookAndAuthor_IntentHandler, Genre_ByAuthor_Intent, Genre_ByBook_Intent

########################################################################################################################################################
## ______________________________________________________________________________________________________________________________________ BASIC INTENTS 
########################################################################################################################################################

class HelloIntentHandler(AbstractRequestHandler):
    """Handler for Hello Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello from StorySage!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I don't think I can answer that question. I might not know about every book out there! Try asking me about something else!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(HelloIntentHandler()) #1
# ______________________________________________________________ BOOK
sb.add_request_handler(Books_ByAuthor_IntentHandler()) #2
#sb.add_request_handler(Books_ByBookGenre_IntentHandler()) #3
sb.add_request_handler(Books_ByGenre_IntentHandler()) #4
sb.add_request_handler(BookDescription_IntentHandler()) #5
sb.add_request_handler(BookRating_IntentHandler()) #6
# ______________________________________________________________ AUTHOR
sb.add_request_handler(Author_ByBook_IntentHandler()) #7
sb.add_request_handler(Authors_ByGenre_IntentHandler()) #8
sb.add_request_handler(AuthorDescription_IntentHandler()) #9
# ______________________________________________________________ GENRE
#sb.add_request_handler(Genre_ByBookAndAuthor_IntentHandler()) #10
#sb.add_request_handler(Genre_ByAuthor_Intent()) #11
#sb.add_request_handler(Genre_ByBook_Intent()) #12
sb.add_request_handler(GenreDescription_IntentHandler()) #13


sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()