__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.guest_steps import GuestSteps
from steps.font_end.provider.dashboard import DashBoardSteps
from steps.install_steps import InstallSteps
from steps.web_chat import WebChatSteps
from steps.font_end.nurse.nurse_steps import NurseSteps

testID = sys.argv[1]  # test case ID
bType = sys.argv[2]  # type of browser
osType = sys.argv[3]  # type of platform
userID = int(sys.argv[4])  # userID
src = sys.argv[5]  # Local VM ID
dst = sys.argv[6]  # Remote VM ID
is_install = int(sys.argv[7])  # Install VSee client if equal to 1


def guest_observe_bashboard():
    # Objects
    _actor = LoginSteps()
    _dashboard = DashBoardSteps()
    _guest = GuestSteps()
    _nurse = NurseSteps()
    _install = InstallSteps()
    _webchat = WebChatSteps()

    odtc = ODTC()
    provider_name = odtc.get_fullname_provider(env='neu')
    vsee_id = odtc.get_email_provider(env='neu')

    try:
        _actor \
            .enter_waiting_room(env='neu') \

        _dashboard\
            .should_not_see_login_button()\
            .should_see_see_a_doctor_now_button()\
            .should_see_current_number_of_patients_waiting('0')\
            .should_see_room_description('Hello, I am Baymax, your personal healthcare companion')
        _dashboard \
            .see_a_doctor_now()

        _guest.provides_intake_information(first_name='Guest Neuro 01',
                                           last_name='641984',
                                           reason='Headache')

        # VM is installed the first time
        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)
        _install.accept_privacy_and_term_GDPR()

        _nurse \
            .should_see_the_chat_button(vsee_id, provider_name) \
            .should_see_the_exit_button() \
            .should_see_notify('Your provider will be with you shortly.') \
            .start_to_chat_with(vsee_id, provider_name)

        _webchat\
            .send_a_message("Dear, Mr. " + provider_name) \
            .send_a_message("How are you going?") \
            .wait_for_message_from_sender("Thanks, I am doing well") \
            .send_a_message("I sent the intake attachment file") \
            .send_a_message("Please, Review it!") \
            .send_a_message("Can you please give me a call ?") \
            .wait_for_message_from_sender("I am calling...") \
            .close_web_chat().should_not_see_web_chat_of(provider_name)

        # Launch VM if already installed
        _nurse\
            .wait_doctor_visit(testID, src, dst) \
            .should_see_visit_status('Visit with Dr. ' + provider_name + ', Ph.D is in progress') \
            .wait_doctor_complete_visit(testID, src) \
            .end_visit()
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
    guest_observe_bashboard()


main()
