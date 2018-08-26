# cepProviderViewMedicalInfo

__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.patient.patient_health import PatientHealthSteps
from steps.font_end.patient.patient_visit import PatientVisitSteps

testID = sys.argv[1]  # test case ID


def patient_my_health():
    # Objects
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _health = PatientHealthSteps()
    _patient_visit = PatientVisitSteps()

    try:

        _actor.access_waiting_room().signin_as_patient()
        _navigate.goto_health()
        _health.has_tab("Medical History") \
            .has_tab("Allergies") \
            .has_tab("Medications") \
            .has_tab("Documents") 

        # My Appointments ( Patient) = Visit Note (provider)
        _navigate.goto_visit_page()
        _patient_visit.should_see_the_upcoming_visits_table_with_columns("Visit Time,Type,Provider,Action") \
            .should_see_the_past_visit_table_with_columns("Visit Time,Type,Provider,Visit Status,Action") \

        # update search late

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
    patient_my_health()


main()
