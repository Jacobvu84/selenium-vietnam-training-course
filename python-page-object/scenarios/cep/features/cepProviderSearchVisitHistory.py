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
from steps.font_end.provider.my_patient import AllVisitSteps

testID = sys.argv[1]  # test case ID


# Tester thread
def view_patient():
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _patient = MyPatientSteps()
    _all_visit = AllVisitSteps()
    odtc = ODTC()

    patients = odtc.get_cep_patient()
    email = patients[1].split(",")[0]
    f_name = patients[1].split(",")[1]
    l_name = patients[1].split(",")[2]

    full_name = f_name + " " + l_name

    try:
        _actor.browse_the_web().signin_as_provider()
        _navigate.goto_patient_page()

        _patient.select_tab("All Visits")
        _all_visit.search_history_visit_by("^0^") \
            .should_see_no_matching_records_found() \
            .search_history_visit_by(f_name) \
            .should_see_appointment_information(1) \
            .search_history_visit_by(l_name) \
            .should_see_appointment_information(1) \
            .search_history_visit_by(full_name) \
            .should_see_appointment_information(1) \
            .search_history_visit_by(email) \
            .should_see_appointment_information(1) \
            .search_history_visit_by("Male") \
            .should_see_appointment_information(1)

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
    view_patient()


main()
