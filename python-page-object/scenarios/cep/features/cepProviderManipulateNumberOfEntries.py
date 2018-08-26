__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_patient import MyPatientSteps

testID = sys.argv[1]  # test case ID


# Tester thread
def paging():
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _my_patient = MyPatientSteps()

    try:
        _actor.browse_the_web().signin_as_provider()
        _navigate.goto_patient_page()

        all_options = ['10', '25', '50', '100', '200']

        _my_patient.select_tab("My Patients") \
            .should_see_default_number_rows_is_shown("25") \
            .should_see_all_options(all_options)

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
    paging()


main()
