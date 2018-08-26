__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import get_provider


sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps

testID = sys.argv[1]  # test case ID

def patient_sign_up():
    # Objects
    _actor = LoginSteps()

    try:
        providers = get_provider()

        _actor.enter_waiting_room() \
            .should_see_providers(providers) \
            .access_waiting_room() \
            .signin_as_patient() \
            .should_see_providers(providers) \
            .logout()

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
    patient_sign_up()


main()
