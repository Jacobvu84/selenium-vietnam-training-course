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
from steps.font_end.patient.patient_health import PatientMedicationSteps

testID = sys.argv[1]  # test case ID


def edit_medication():
    # Objects
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _patient = PatientHealthSteps()
    _medication = PatientMedicationSteps()

    try:
        _actor.access_waiting_room().signin_as_patient()
        _navigate.goto_health()
        _patient.select_medications_tab()
        _medication.should_see_the_current_medications("Metoprolol,Hypertension,Amoxicillin,Paracetamol") \
            .remove_medications("Amoxicillin,Paracetamol") \
            .add_medications("Valium") \
            .should_see_the_current_medications("Metoprolol,Hypertension,Valium")

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
    edit_medication()


main()
