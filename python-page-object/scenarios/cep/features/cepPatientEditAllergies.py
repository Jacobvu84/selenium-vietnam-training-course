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
from steps.font_end.patient.patient_health import PatientAllergiesSteps

testID = sys.argv[1]  # test case ID


def edit_allergies():
    # Objects
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _patient = PatientHealthSteps()
    _allergies = PatientAllergiesSteps()

    try:
        _actor.access_waiting_room().signin_as_patient()
        _navigate.goto_health()
        _patient.select_allergies_tab()
        _allergies.should_see_the_allergies("Moxifloxacin,Apresoline,5HT1 agonist,12 Hour Nasal") \
            .remove_allergies("5HT1 agonist,Moxifloxacin") \
            .add_allergies("5HT3 inhibitor,Abilify Maintena") \
            .should_see_the_allergies("5HT3 inhibitor,Abilify Maintena,12 Hour Nasal,Apresoline")

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
    edit_allergies()


main()
