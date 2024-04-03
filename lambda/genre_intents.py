import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from api_utils_dictionary import getGenreDescription
from helpers import getBookTitleResolution, getAuthorNameResolution, getGenreResolution # SLOT RESOLUTION HELPERS

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


########################################################################################################################################################
## ______________________________________________________________________________________________________________________________________ GENRE INTENTS 
########################################################################################################################################################

## ____________________________________________________________________________________________________________________GenreDescription_Intent
class GenreDescription_IntentHandler(AbstractRequestHandler):
    """Handler for Request of Genre Description Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GenreDescription_Intent")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        (flag_genre, genre) = getGenreResolution(slots)
        
        if flag_genre:
            (flag_description, description) = getGenreDescription(genre)

            if flag_description:
                speak_output = 'Here is a definition of the genre '+genre.title()+': '+description
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