__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.nurse.nurse_steps import NurseSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_patient import MyPatientSteps
from steps.font_end.provider.my_patient import AllVisitSteps

testID = sys.argv[1]  # test case ID


def nurse_observe_menu_bar():
    # Objects
    _actor = LoginSteps()
    _nurse = NurseSteps()
    _navigate = NavigateSteps()
    _my_patient = MyPatientSteps()
    _all_visit = AllVisitSteps()

    odtc = ODTC()

    try:
        # WHEN: Nurse creates the visit
        _actor \
            .visit_telepsych() \
            .signin_as_nurse(env='tele')

        _nurse\
            .should_see_menu_bar('Dashboard,My Patients') \
            .should_contains_menu_item('Dashboard,My Patients')\
            .should_see_menu_item_default('Dashboard')

        _navigate\
            .goto_my_patients()\
            .re_type_password()

        _my_patient\
            .select_tab("All Visits")

        for index in range(0,4):
            name = odtc.get_fullname_patient(env='tele', index=index)
            _all_visit \
                .search_history_visit_by(value=name) \
                .should_see_the_patient_name(name)

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
    nurse_observe_menu_bar()


main()
