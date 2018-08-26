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
dst = sys.argv[6]  # Remote VM ID
is_install = int(sys.argv[7])  # Install VSee client if equal to 1


# Tester thread
def walkin_to_room_with_consultation_type():
    # Objects
    _actor = LoginSteps()
    _patient = PatientHomeSteps()
    _install = InstallSteps()

    try:
        _actor.access_waiting_room(index=1) \
            .signin_as_patient()

        _patient.see_a_doctor_in_room_quickly(visit_option="45-min Consultation")

        # VM is installed the first time
        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)
        _install.accept_privacy_and_term_GDPR()

        # Launch VM if already installed
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
    walkin_to_room_with_consultation_type()


main()
