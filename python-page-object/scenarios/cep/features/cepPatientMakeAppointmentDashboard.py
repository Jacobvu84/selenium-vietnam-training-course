__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from util.mailbox import MailBox

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.patient_steps import PatientHomeSteps
from steps.mail_box import MailBoxSteps

from model.patient import patient_gmail
from model.patient import password_gmail
from model.provider import main_email
from model.provider import email_pwd

testID = sys.argv[1]  # test case ID


def patient_make_appoinment():
    # Objects
    _actor = LoginSteps()
    _he = PatientHomeSteps()
    _mailbox = MailBoxSteps()

    try:
        with MailBox(main_email, email_pwd) as mbox:
            mbox.delete_all()

        _actor.access_waiting_room().signin_as_patient(1)
        _he.schedule_appointment(1)

        # Check mail
        with MailBox(patient_gmail, password_gmail) as inbox:
            _mailbox.open_link_from_email(mail_title=_mailbox.make_appointment, mbox=inbox)
        _he.should_see_start_appointment_in_dashboard("Today")

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
    patient_make_appoinment()


main()
