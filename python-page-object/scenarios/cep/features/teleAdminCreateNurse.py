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

from model.provider import telepsych_nurses
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
from resource import ODTC

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

odtc = ODTC()

provider = odtc.get_tele_provider()
email = provider[2].split(",")[0]
f_name = provider[2].split(",")[1]
l_name = provider[2].split(",")[2]
full_name = f_name + " " + l_name


def create_telepsych_nurse(nurse):
    _provider.create_new()
    _subtype.select_sub_type(nurse)
    _demographics.enter_demographics_information(nurse)
    _license.enter_license_information(nurse)
    _profile.enter_profile_information(nurse)
    _assignment.enter_assignment_information(nurse)


def test_create_telepsych_nurses():

    with MailBox(main_email, email_pwd) as mbox:
        mbox.delete_all()

    mkdir("bin")
    setup_logger('provider', TEMP_DIR_WIN + 'bin\\tele_nurse.log', level=logging.DEBUG)
    log = logging.getLogger('provider')
    try:

        _actor \
            .visit_telepsych() \
            .signin_as_provider(env='tele', index=2)\
            .access_admin_panel(env='tele', index=2)

        _admin.goto_provider_screen()

        for nurse in telepsych_nurses[0:3]:
            log.info(nurse.demographics.email + ","
                     + nurse.demographics.username + ","
                     + new_pass + ","
                     + nurse.demographics.firstname + ","
                     + nurse.demographics.lastname + ",[end]")

            """[TEST] CREATE NEW PROVIDERS """
            create_telepsych_nurse(nurse)

            with MailBox(main_email, email_pwd) as inbox:
                _mailbox.get_content_in_email(mail_title=_mailbox.welcome_telepsych, mbox=inbox)

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
    test_create_telepsych_nurses()


main()
