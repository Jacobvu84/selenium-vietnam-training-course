__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.guest_steps import GuestSteps
from steps.font_end.provider.dashboard import DashBoardSteps
from steps.install_steps import InstallSteps
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
    _install = InstallSteps()
    _nurse = NurseSteps()

    try:
        _actor \
            .enter_waiting_room(env='neu')
        _dashboard \
            .see_a_doctor_now()
        _guest.provides_intake_information(first_name='Guest Neuro 02',
                                           last_name='641985',
                                           reason='Headache')
        # VM is installed the first time
        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)
        _install.accept_privacy_and_term_GDPR()

        _nurse \
            .should_see_the_exit_button() \
            .should_see_notify('Your provider will be with you shortly.')

        _install\
            .close_the_video_conference(testID, src)\
            .relaunch_video()\
            .should_see_the_video_relaunch(testID, src)

        _nurse\
            .exit_the_appointment()

        _dashboard\
            .should_not_see_login_button()\
            .should_see_see_a_doctor_now_button()\
            .should_see_current_number_of_patients_waiting('0')\
            .should_see_room_description('Hello, I am Baymax, your personal healthcare companion')

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
