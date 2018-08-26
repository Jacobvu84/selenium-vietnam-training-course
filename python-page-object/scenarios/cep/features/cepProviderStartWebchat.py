__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC


sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.provider.dashboard import DashBoardSteps
from steps.web_chat import WebChatSteps
from steps.font_end.provider.control_panel import ControlPanelSteps
from steps.font_end.provider.visit_note import VisitNoteSteps

testID = sys.argv[1]  # test case ID


# Tester thread
def provider_start_web_chat():
    _actor = LoginSteps()
    _dashboard = DashBoardSteps()
    _webchat = WebChatSteps()
    _control_panel = ControlPanelSteps()
    _visit_note = VisitNoteSteps()

    odtc = ODTC()
    provider_full_name = odtc.get_fullname_provider(index=2)
    patient_full_name = odtc.get_fullname_patient()

    try:
        _actor.browse_the_web().signin_as_provider(index=2)

        # provider start Visit
        _dashboard.select_patient_in_lounge()
        _control_panel.open_webchat()

        _webchat.send_a_message("Dear, Mr. " + patient_full_name) \
            .wait_for_message_from_sender("Dear, " + provider_full_name) \
            .send_a_message("How are you going?") \
            .wait_for_message_from_sender("Thanks Doctor, I am doing well") \
            .send_a_message("Do you exercise everyday?") \
            .wait_for_message_from_sender("Yes, Walking and Running 7km everyday") \
            .send_a_message("That sounds great. Keep moving!") \
            .send_a_message("Please, Should not eat fish, meat, butter") \
            .wait_for_message_from_sender("Thank you for your advices.") \
            .close_web_chat().should_not_see_web_chat_of(patient_full_name)

        _visit_note.complete__and_sent_visit_to_patient() \
            .feedback_on_patient().submit().should_see_back_to_lounge()

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
    provider_start_web_chat()


main()
