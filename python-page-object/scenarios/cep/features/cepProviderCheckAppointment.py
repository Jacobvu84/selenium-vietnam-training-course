__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.mailbox import MailBox
from util.console import start_test
from util.support import create_gif
from resource import ODTC


sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.provider.dashboard import DashBoardSteps
from steps.mail_box import MailBoxSteps

from model.provider import main_email
from model.provider import email_pwd

testID = sys.argv[1]  # test case ID


def provider_checks_appointment():
    # Objects
    _actor = LoginSteps()
    _doctor = DashBoardSteps()
    _mailbox = MailBoxSteps()
    odtc = ODTC()

    provider = odtc.get_cep_provider()
    email = provider[0].split(",")[0]
    pwd = provider[0].split(",")[3]

    patient = odtc.get_cep_patient()

    try:
        with MailBox(main_email, email_pwd) as inbox:
            _mailbox.open_link_from_email(mail_title=_mailbox.appointment_schedule, mbox=inbox, time_out=3600)

        _actor.login_as(email, pwd)
        _doctor.should_see_the_schedule(patient, 1)

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
    provider_checks_appointment()


main()
