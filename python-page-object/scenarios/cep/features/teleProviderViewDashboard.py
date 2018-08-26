__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.provider.dashboard import DashBoardSteps
from steps.font_end.nurse.nurse_steps import NurseSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_patient import AllVisitSteps
from steps.font_end.provider.my_patient import MyPatientSteps

testID = sys.argv[1]  # test case ID


def provider_observe_bashboard():
    # Objects
    _actor = LoginSteps()
    _dashboard = DashBoardSteps()
    _menu = NurseSteps()
    _navigate = NavigateSteps()
    _all_visit = AllVisitSteps()
    _my_patient = MyPatientSteps()

    odtc = ODTC()

    try:
        _actor \
            .visit_telepsych() \
            .signin_as_provider(env='tele')

        _menu\
            .should_see_menu_bar('Dashboard, Patients, Calendar') \
            .should_contains_menu_item('Dashboard, Patients, Calendar')\
            .should_see_menu_item_default('Dashboard')

        _dashboard\
            .should_see_section("Currently in the Waiting Room")\
            .should_see_today_schedule_section()\
            .should_see_create_new_visit_option()

        _navigate.goto_patient_page()
        _my_patient\
            .select_tab("All Visits")

        # provider can see visits of others Provider
        _all_visit \
            .search_history_visit_by(value='Patient Tele 04') \
            .should_see_the_provider_name('Provider Telep 01') \
            .search_history_visit_by(value='Patient Tele 03') \
            .should_see_the_provider_name('Super Admin Telep') \
            .search_history_visit_by(value='Patient Tele 02') \
            .should_see_the_provider_name('Provider Telep 02') \
            .search_history_visit_by(value='Patient Tele 01') \
            .should_see_the_provider_name('Clinic Admin Telep')

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
    provider_observe_bashboard()


main()
