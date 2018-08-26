__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.web_chat import WebChatSteps

testID = sys.argv[1]  # test case ID


def nurse_chat_with_provider_from_dashbroad():
    # Objects
    _actor = LoginSteps()
    _webchat = WebChatSteps()

    odtc = ODTC()
    index = 0
    provider_name = odtc.get_fullname_provider(env='tele', index=index)
    vsee_id = odtc.get_email_provider(env='tele', index=index)

    try:
        # WHEN: Nurse creates the visit
        _actor \
            .visit_telepsych() \
            .signin_as_nurse(env='tele')

        _webchat.open_web_chat_from_dashboard(vsee_id, provider_name)\
            .send_a_message("Dear, Mr. " + provider_name) \
            .send_a_message("Can you please visit in 30 mins?") \
            .wait_for_message_from_sender("I will call you with VSee Messenger") \
            .close_web_chat().should_not_see_web_chat_of(provider_name)

        print "[PASSED]: TEST PASSED"

    except Exception as e:
        print type(e)
        print e.args
        print e
        print "[INFO]: TEST FAILED"
    finally:
        _actor.quit()
        create_gif()

def main():
    start_test()
    nurse_chat_with_provider_from_dashbroad()


main()
