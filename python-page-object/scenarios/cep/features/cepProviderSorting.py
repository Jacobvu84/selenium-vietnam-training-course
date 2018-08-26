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
from steps.font_end.provider.my_patient import AllVisitSteps

testID = sys.argv[1]  # test case ID


# Tester thread
def sorting():
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _patient = MyPatientSteps()
    _all_visit = AllVisitSteps()

    try:
        _actor.browse_the_web().signin_as_provider()
        _navigate.goto_patient_page()

        # provider do sorting - Visits History
        _patient.select_tab("All Visits")
        _all_visit.show_entries("10") \
            .default_sorting_by(column="Visit Time", sort_by="descending") \
            .should_see_sorting(column="Visit Time", label="Visit Time: activate to sort column ascending") \
            .should_see_sorting(column="Patient", label="Patient: activate to sort column ascending") \
            .should_see_sorting(column="Waiting Room", label="Waiting Room: activate to sort column ascending") \
            .should_see_sorting(column="Provider", label="Provider: activate to sort column ascending") \
            .should_see_sorting(column="Email", label="Email: activate to sort column ascending") \
            .should_see_sorting(column="Visit Status", label="Visit Status: activate to sort column ascending") \
        .change_sorting_by(column="Visit Time") \
            .default_sorting_by(column="Visit Time", sort_by="ascending") \
            .should_see_sorting(column="Visit Time", label="Visit Time: activate to sort column descending") \
            .should_see_sorting(column="Patient", label="Patient: activate to sort column ascending") \
            .should_see_sorting(column="Waiting Room", label="Waiting Room: activate to sort column ascending") \
            .should_see_sorting(column="Provider", label="Provider: activate to sort column ascending") \
            .should_see_sorting(column="Email", label="Email: activate to sort column ascending") \
            .should_see_sorting(column="Visit Status", label="Visit Status: activate to sort column ascending") \
        .change_sorting_by(column="Patient") \
            .default_sorting_by(column="Patient", sort_by="ascending") \
            .should_see_sorting(column="Visit Time", label="Visit Time: activate to sort column ascending") \
            .should_see_sorting(column="Patient", label="Patient: activate to sort column descending") \
            .should_see_sorting(column="Waiting Room", label="Waiting Room: activate to sort column ascending") \
            .should_see_sorting(column="Provider", label="Provider: activate to sort column ascending") \
            .should_see_sorting(column="Email", label="Email: activate to sort column ascending") \
            .should_see_sorting(column="Visit Status", label="Visit Status: activate to sort column ascending") \
        .change_sorting_by(column="Waiting Room") \
            .default_sorting_by(column="Waiting Room", sort_by="ascending") \
            .should_see_sorting(column="Waiting Room", label="Waiting Room: activate to sort column descending") \
            .change_sorting_by(column="Provider") \
            .default_sorting_by(column="Provider", sort_by="ascending") \
            .should_see_sorting(column="Provider", label="Provider: activate to sort column descending") \
        .change_sorting_by(column="Email") \
            .default_sorting_by(column="Email", sort_by="ascending") \
            .should_see_sorting(column="Email", label="Email: activate to sort column descending") \
            .change_sorting_by(column="Visit Status") \
            .default_sorting_by(column="Visit Status", sort_by="ascending") \
            .should_see_sorting(column="Visit Status", label="Visit Status: activate to sort column descending")
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
    sorting()


main()
