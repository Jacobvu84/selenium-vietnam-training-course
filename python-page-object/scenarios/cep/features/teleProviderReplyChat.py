__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.web_chat import WebChatSteps

testID = sys.argv[1]  # test case ID


# Tester thread
def provider_reply_chat_message():
    _actor = LoginSteps()
    _webchat = WebChatSteps()

    index = 0

    try:
        _actor \
            .visit_telepsych() \
            .signin_as_provider(env='tele', index=index)

        _webchat \
            .wait_for_message_from_sender("Can you please visit in 30 mins?") \
            .reply_message("Yes, Of course.") \
            .reply_message("Please, Provide patient information and enter waiting room") \
            .reply_message("I will call you with VSee Messenger") \
            .close_web_chat()

        print "[PASSED]: TEST PASSED"
    except Exception as e:
        print type(e)
        print e.args
        print e
        print "[FAILED]: TEST FAILED"

    finally:
        _actor.quit()
        create_gif()


def main():
    start_test()
    provider_reply_chat_message()


main()
