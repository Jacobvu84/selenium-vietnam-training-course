__author__ = 'jacob@vsee.com'

import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps

from steps.backend.provider.provider_steps import ProviderSteps
from steps.backend.provider.provider_steps import SubTypeSteps
from steps.backend.provider.provider_steps import DemographicsSteps
from steps.backend.provider.provider_steps import LicenseSteps
from steps.backend.provider.provider_steps import ProfileSteps
from steps.backend.provider.provider_steps import AssignmentSteps
from steps.mail_box import MailBoxSteps

from model.provider import snf_nurses
from model.provider import main_email
from model.provider import email_pwd
from model.provider import new_pass

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.mailbox import MailBox
from util.logger import setup_logger
from util.console import start_test
from util.support import mkdir
from util.support import TEMP_DIR_WIN
from util.support import create_gif

testID = sys.argv[1]  # test case ID

# Steps
_actor = LoginSteps()
_admin = NavigateSteps()
_provider = ProviderSteps()
_subtype = SubTypeSteps()
_demographics = DemographicsSteps()
_license = LicenseSteps()
_profile = ProfileSteps()
_assignment = AssignmentSteps()
_mailbox = MailBoxSteps()


def create_snf_nurse(snf_nurse):
    _provider.create_new()
    _subtype.select_sub_type(snf_nurse)
    _demographics.enter_demographics_information(snf_nurse)
    _license.enter_license_information(snf_nurse)
    _profile.enter_profile_information(snf_nurse)
    _assignment.enter_assignment_information(snf_nurse)


def test_create_provider():
    with MailBox(main_email, email_pwd) as mbox:
        mbox.delete_all()

    mkdir("bin")
    setup_logger('provider', TEMP_DIR_WIN + 'bin\\snf_nurse.log', level=logging.DEBUG)
    log = logging.getLogger('provider')
    try:

        _actor.visit_snf().login_as(username="admin", password="Evc0nnect=")
        _admin.goto_provider_screen()

        for snf_nurse in snf_nurses[0:3]:
            log.info(snf_nurse.demographics.email + ","
                     + snf_nurse.demographics.username + ","
                     + new_pass + ","
                     + snf_nurse.demographics.firstname + ","
                     + snf_nurse.demographics.lastname + ",[end]")

            """[TEST] CREATE NEW PROVIDERS """
            create_snf_nurse(snf_nurse)

            with MailBox(main_email, email_pwd) as inbox:
                _mailbox.get_content_in_email(mail_title=_mailbox.welcome_snf, mbox=inbox)

        print "[PASSED]: TEST PASSED"
    except Exception as e:
        print type(e)
        print e.args
        print e
        print "[FAILED]: TEST FAILED"

    finally:
        with MailBox(main_email, email_pwd) as mbox:
            mbox.delete_all()
        _actor.quit()
        create_gif()


def main():
    start_test()
    test_create_provider()


main()
