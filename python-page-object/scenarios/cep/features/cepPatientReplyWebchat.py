__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.patient_steps import PatientHomeSteps
from steps.install_steps import InstallSteps
from steps.web_chat import WebChatSteps

testID = sys.argv[1]  # test case ID
bType = sys.argv[2]  # type of browser
osType = sys.argv[3]  # type of platform
userID = int(sys.argv[4])  # userID
src = sys.argv[5]  # Local VM ID
dst = sys.argv[6]  # Remote VM ID
is_install = int(sys.argv[7])  # Install VSee client if equal to 1


def patient_reply_web_chat():
    # Objects
    _actor = LoginSteps()
    _patient = PatientHomeSteps()
    _install = InstallSteps()
    _webchat = WebChatSteps()

    odtc = ODTC()
    provider_full_name = odtc.get_fullname_provider(index=2)
    patient_full_name = odtc.get_fullname_patient()

    try:
        _actor.access_waiting_room() \
            .signin_as_patient()

        _patient.see_a_doctor_in_room_quickly(visit_option="no")

        # VM is installed the first time
        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)

        # Launch VM if already installed
        _webchat.wait_for_message_from_sender("Dear, Mr. " + patient_full_name) \
            .reply_message("Dear, " + provider_full_name) \
            .wait_for_message_from_sender("How are you going?") \
            .reply_message("Thanks Doctor, I am doing well") \
            .wait_for_message_from_sender("Do you exercise everyday?") \
            .reply_message("Yes, Walking and Running 7km everyday") \
            .wait_for_message_from_sender("That sounds great. Keep moving!") \
            .wait_for_message_from_sender("Please, Should not eat fish, meat, butter") \
            .reply_message("Absolutely, Yes") \
            .reply_message("Thank you for your advices.") \
            .close_web_chat() \
            .should_not_see_web_chat_of(provider_full_name)

        _patient.wait_doctor_visit(testID, src, dst) \
            .wait_doctor_complete_visit(testID, src) \
            .patient_rate_and_end_visit()

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
    patient_reply_web_chat()


main()
