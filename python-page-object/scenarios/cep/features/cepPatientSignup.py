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
from steps.font_end.patient.create_account import CreateAccountSteps
from steps.font_end.patient.create_account import RegisterSteps
from steps.mail_box import MailBoxSteps

from model.patient import patient_gmail
from model.patient import password_gmail
from model.patient import patient_pwd

testID = sys.argv[1]  # test case ID


def patient_sign_up():
    # Objects
    _actor = LoginSteps()
    _patient = CreateAccountSteps()
    _register = RegisterSteps()
    _mailbox = MailBoxSteps()

    with MailBox(patient_gmail, password_gmail) as mbox:
        mbox.delete_all()

    try:

        """
        [TEST] CREATE ACCOUNT:
        eligibility[x].split(",")[y]
          - x: number of row/records of room (from 0)
          - y: 0 - email 
               1 - first name
               2 - last name
               
        mail_title="Activate your CEP OnDuty account"
        """
        odtc = ODTC()
        patients = odtc.get_cep_patient()
        for patient in patients:
            email = patient.split(",")[0]
            f_name = patient.split(",")[1]
            l_name = patient.split(",")[2]

            _actor.access_waiting_room() \
                .sign_up()
            _patient.create_an_account(patient)

            with MailBox(patient_gmail, password_gmail) as inbox:
                _mailbox.open_link_from_email(mail_title=_mailbox.active_account, mbox=inbox)

            _register.should_see_default_account_information(patient) \
                .set_up_password(patient_pwd) \
                .complete_patient_information()

            _actor.should_see_full_name(f_name + " " + l_name) \
                .logout()
            _actor.access_waiting_room() \
                .login_as(email, patient_pwd) \
                .should_see_full_name(f_name + " " + l_name)\
                .logout()

        print "[PASSED]: TEST PASSED"
    except Exception as e:
        print type(e)
        print e.args
        print e
        print "[FAILED]: TEST FAILED"
    finally:
        with MailBox(patient_gmail, password_gmail) as mbox:
            mbox.delete_all()
        _actor.quit()
        create_gif()


def main():
    start_test()
    patient_sign_up()


main()
