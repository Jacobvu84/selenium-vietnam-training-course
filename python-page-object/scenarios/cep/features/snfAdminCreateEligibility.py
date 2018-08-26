__author__ = 'jacob@vsee.com'

import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps
from steps.backend.clinic.clinic_steps import EligibilitySteps
from steps.backend.clinic.clinic_steps import ClinicSteps

from model.patient import snf_eligibilities

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import setup_logger
from util.console import start_test
from util.support import mkdir
from util.support import TEMP_DIR_WIN
from util.support import create_gif
from util.setting import _snf_domain

testID = sys.argv[1]  # test case ID

# Steps
_actor = LoginSteps()
_navigate = NavigateSteps()
_clinic = ClinicSteps()
_eligibility = EligibilitySteps()


def test_eligibility():
    try:

        mkdir("bin")
        setup_logger('eligibility', TEMP_DIR_WIN + 'bin\\snf_eligibility.log', level=logging.DEBUG)
        log = logging.getLogger('eligibility')

        """[TEST] CREATE A ELIGIBILITY"""
        _actor.visit_snf().login_as(username="admin", password="Evc0nnect=")

        for eligibility in snf_eligibilities[0:2]:
            log.debug(
                eligibility.firstname + "," + eligibility.lastname + "," + eligibility.DOB + "," +
                eligibility.SSN + "," + eligibility.account_code + ",[end]")

            _navigate.goto_clinic_screen()
            _clinic.view_eligibility(domain=_snf_domain)
            _eligibility.creat_new_eligibility(eligibility) \
                .should_see_success_alert_message() \
                .should_see_eligibility_in_table()

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
