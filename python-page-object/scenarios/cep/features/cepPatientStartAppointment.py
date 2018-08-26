__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.patient_steps import PatientHomeSteps
from steps.install_steps import InstallSteps

testID = sys.argv[1]  # test case ID
bType = sys.argv[2]  # type of browser
osType = sys.argv[3]  # type of platform
userID = int(sys.argv[4])  # userID
src = sys.argv[5]  # Local VM ID
is_install = int(sys.argv[6])  # Install VSee client if equal to 1


def start_appointment():
    # Objects
    _actor = LoginSteps()
    _patient = PatientHomeSteps()
    _install = InstallSteps()

    try:
        _actor.access_waiting_room() \
            .signin_as_patient(1)

        _patient.start_his_appointment()

        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)
        _install.accept_privacy_and_term_GDPR()

        _patient.just_exit_appointment().should_see_end_call(testID, src)

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
    start_appointment()


main()
