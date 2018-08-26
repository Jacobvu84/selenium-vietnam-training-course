__author__ = 'jacob@vsee.com'

import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps
from steps.backend.clinic.clinic_steps import EligibilitySteps
from steps.backend.clinic.clinic_steps import ClinicSteps

from model.patient import eligibilities
from model.patient import patient_pwd

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import setup_logger
from util.console import start_test
from util.support import mkdir
from util.support import TEMP_DIR_WIN
from util.support import create_gif

testID = sys.argv[1]  # test case ID

# Steps
_actor = LoginSteps()
_navigate = NavigateSteps()
_clinic = ClinicSteps()
_eligibility = EligibilitySteps()


def test_eligibility():
    try:

        mkdir("bin")
        setup_logger('eligibility', TEMP_DIR_WIN + 'bin\\eligibility.log', level=logging.DEBUG)
        log = logging.getLogger('eligibility')

        """[TEST] CREATE A ELIGIBILITY"""
        _actor.browse_the_web().login_as(username="admin", password="Evc0nnect=")

        for eligibility in eligibilities[0:3]:
            log.debug(
                eligibility.email + "," + eligibility.firstname + "," + eligibility.lastname + "," + eligibility.DOB + "," +
                eligibility.SSN + "," + eligibility.account_code + "," + patient_pwd + ",[end]")

            _navigate.goto_clinic_screen()
            _clinic.view_eligibility()
            _eligibility.creat_new_eligibility(eligibility) \
                .should_see_success_alert_message() \
                .should_see_eligibility_in_table()

        """
        [TEST] DELETE A ELIGIBILITY:
        eligibility[x].split(",")[y]
          - x: number of row/records of room (from 0)
          - y: 1 - first name
               2 - last name
               3 - DOB
               4 - SSN
               5 - Account Code
        
        eligibility = get_patient()
        ssn = eligibility[2].split(",")[4]
        _eligibility.delete_eligibility(ssn).should_see('No matching records found')
        """
        print "[PASSED]: TEST PASSED"
    # Catch any exception from test failure
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
    test_eligibility()


main()
