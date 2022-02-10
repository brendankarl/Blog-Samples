# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

import requests
import datetime
PAT = "Insert PAT"
url = "https://api.starlingbank.com/api/v2/"
headers = {"Authorization": "Bearer " + PAT}

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from ask_sdk_model import ui

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_account():
    r = requests.get(url + "accounts", headers=headers)
    return r.json()["accounts"][0]["accountUid"]

def get_default_category():
    r = requests.get(url + "accounts", headers=headers)
    return r.json()["accounts"][0]["defaultCategory"]

def get_balance():
    balance = requests.get(url + "accounts/" + (get_account()) + "/balance", headers=headers)
    return (str(balance.json()["effectiveBalance"]["minorUnits"] / 100)).split(".")[0]

def get_transactions(days):
    datefrom = (datetime.datetime.now()-datetime.timedelta(days=days)).strftime("%Y-%m-%d") + "T00:00:00Z"
    feeditems = requests.get(url + "feed/account/" + (get_account()) + "/category/" + (get_default_category()) + "?changesSince=" + datefrom, headers=headers)
    return "Amount: " + "£" + (str(feeditems.json()["feedItems"][0]["amount"]["minorUnits"] / 100)).split(".")[0] + "\n" + "Source: " + str(feeditems.json()["feedItems"][0]["source"])

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        balance = get_balance()
        speak_output = "Your balance is " + "£" + balance + "\n \n What would you like to do next?" 

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_card(ui.StandardCard(title="Brendans Bank Account",text=speak_output,image=ui.Image(small_image_url="https://minetteriordan.com/wp-content/uploads/2015/03/showmethemoney-1024x553.png",large_image_url="https://minetteriordan.com/wp-content/uploads/2015/03/showmethemoney-1024x553.png")))
                .response
        )


class LastTransaction(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("LastTransaction")(handler_input)

    def handle(self, handler_input):
        speak_output = get_transactions(30)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_card(ui.StandardCard(title="Brendans Bank Account",text=speak_output,image=ui.Image(small_image_url="https://minetteriordan.com/wp-content/uploads/2015/03/showmethemoney-1024x553.png",large_image_url="https://minetteriordan.com/wp-content/uploads/2015/03/showmethemoney-1024x553.png")))
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


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

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

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

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(LastTransaction())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
