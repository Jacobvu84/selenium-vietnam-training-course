__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC
from util.date_time import get_current_datetime

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_patient import MyPatientSteps

testID = sys.argv[1]  # test case ID

# Tester thread
def view_patient():
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _my_patient = MyPatientSteps()

    odtc = ODTC()
    index = 0
    patients = odtc.get_cep_patient()
    email = patients[index].split(",")[0]
    full_name = odtc.get_fullname_patient()

    try:
        _actor.browse_the_web().signin_as_provider()
        _navigate.goto_patient_page()

        _my_patient.has_tab("All Visits")
        _my_patient.has_tab("My Patients")

        _my_patient \
            .select_tab("My Patients") \
            .search_patient_by(full_name) \
            .should_see_name_patient(full_name) \
            .should_see_gender_patient("Male") \
            .should_see_age_patient("35")\
            .should_see_email_patient(email)\
            .should_see_last_visit_patient(get_current_datetime())

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
