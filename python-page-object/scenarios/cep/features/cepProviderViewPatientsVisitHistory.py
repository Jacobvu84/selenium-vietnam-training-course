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
    email = patients[0].split(",")[0]
    f_name = patients[0].split(",")[1]
    l_name = patients[0].split(",")[2]

    try:
        _actor.browse_the_web().signin_as_provider()
        _navigate.goto_patient_page()

        # Search visit history of test case id 9976
        # can't search datetime, status,
        _patient.select_tab("All Visits")
        _all_visit \
            .show_entries("100") \
            .search_history_visit_by(email) \
            .should_see_visit_information(0).view() \
            .has_tab("Visit Notes") \
            .has_tab("Medical History") \
            .has_tab("Allergies") \
            .has_tab("Medications") \
            .has_tab("Documents") \
            .has_tab("Demographics")

        # Need update verify information in each tab: cepProviderEditVisitInstruction.py
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
