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

    patients = odtc.get_cep_patient()
    email = odtc.get_email_patient()
    full_name = odtc.get_fullname_patient()

    # cepProviderViewPatientsVisitHistory also check UI in the Visit note page
    try:
        _actor.browse_the_web().signin_as_provider()
        _navigate.goto_patient_page()
        _my_patient \
            .select_tab("My Patients") \
            .go_to_visit_note(full_name) \
            .should_see_avatar_with_size(width=120.0, height=120.0) \
            .should_see_full_name(full_name) \
            .should_see_the_email(email)\
            .should_see_the_upcoming_visits_table_with_columns("Visit Time,Type,Provider,Action") \
            .should_see_the_visit_history_table_with_columns("Visit Time,Visit Info,Provider,Visit Status,Action") \
            .back_to_my_patient() \
            .has_tab("All Visits")\
            .should_see_the_all_visit_history_table_with_columns("Visit Time,Patient,Waiting Room,Provider,"
                                                                 "Gender,Age,Email,Visit Status,Action")

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
