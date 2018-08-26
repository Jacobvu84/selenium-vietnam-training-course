__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_patient import MyPatientSteps

testID = sys.argv[1]  # test case ID




# Tester thread
def view_visit_note():
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _my_patient = MyPatientSteps()
    odtc = ODTC()
    full_name = odtc.get_fullname_patient()

    # cepProviderStartVisit also check UI in the Medical History, allergies
    try:
        _actor.browse_the_web().signin_as_provider()
        _navigate.goto_patient_page()
        _my_patient \
            .select_tab("My Patients") \
            .go_to_visit_note(full_name) \
            .has_tab("Medical History")\
            .should_see_the_headings("Past Medical History,Past Surgeries,"
                                     "Family Medical History,Social History,Health Habits")
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
    view_visit_note()


main()
