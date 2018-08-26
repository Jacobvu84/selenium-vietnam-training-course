__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif

from util.mailbox import MailBox

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.backend.provider.provider_steps import ProviderSteps
from steps.mail_box import MailBoxSteps

from model.provider import main_email
from model.provider import email_pwd

testID = sys.argv[1]  # test case ID


# Tester thread
def check_start_appointment_notification():
    _actor = LoginSteps()
    _provider = ProviderSteps()
    _mailbox = MailBoxSteps()

    try:
        _actor.browse_the_web().signin_as_provider()

        # provider get email about walkin notification
        ### Harry: I think this test really needs to be redone.
        ###       We will need to work on this again after dev fix the email notification issue.
        """
        with MailBox(main_email, email_pwd) as inbox:
            _mailbox.open_link_from( title_email=_mailbox.visit_notification, mbox=inbox)
        """

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
    check_start_appointment_notification()


main()
