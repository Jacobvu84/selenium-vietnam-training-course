__author__ = 'jacob@vsee.com'

import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps

from steps.backend.provider.provider_steps import ProviderSteps
from steps.mail_box import MailBoxSteps

from model.provider import telepsych_providers
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

_mailbox = MailBoxSteps()


def create_provider(provider):
    _actor\
        .visit_telepsych()\
        .login_as(username="admin", password="Evc0nnect=")

    _admin\
        .goto_provider_screen()

    _provider\
        .create_new() \
        .select_sub_type(provider) \
        .enter_demographics_information(provider) \
        .enter_license_information(provider) \
        .enter_profile_information(provider) \
        .enter_assignment_information(provider)

    _admin\
        .goto_all_user_screen()

    _provider \
        .search_user(provider) \
        .should_see_provider_information(provider) \
        .assign_role(provider)\

    _actor.logout()


def test_create_provider():
    with MailBox(main_email, email_pwd) as mbox:
        mbox.delete_all()

    mkdir("bin")
    setup_logger('provider', TEMP_DIR_WIN + 'bin\\tele_provider.log', level=logging.DEBUG)
    log = logging.getLogger('provider')
    try:

        for provider in telepsych_providers[0:5]:
            log.info(
                provider.demographics.email + "," +
                provider.demographics.firstname + "," +
                provider.demographics.lastname + "," +
                new_pass + "," + provider.role + ",[end]")

            """[TEST] CREATE NEW PROVIDERS """
            create_provider(provider)

            with MailBox(main_email, email_pwd) as inbox:
                _mailbox.open_link_from_email(mail_title=_mailbox.welcome_telepsych, mbox=inbox)

            _provider.set_password(new_pass) \
                .should_see_alert_message("Password changed. You can now login with your new password.")

            _actor.login_as(provider.demographics.email, new_pass) \
                .should_see_full_name(provider.demographics.firstname + " " + provider.demographics.lastname) \
                .logout()

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
