__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.provider.dashboard import DashBoardSteps

testID = sys.argv[1]  # test case ID


# Tester thread
def start_visit():
    _actor = LoginSteps()
    _dashboard = DashBoardSteps()

    try:
        _actor.browse_the_web().signin_as_provider()

        # provider checks patient online
        _dashboard.should_not_see_patient_in_waiting_room()

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
    start_visit()


main()
