__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.mailbox import MailBox
from util.console import start_test
from util.support import create_gif

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.patient.visit_summary import PatientVisitSummarySteps
from steps.mail_box import MailBoxSteps

from model.patient import patient_gmail
from model.patient import password_gmail

testID = sys.argv[1]  # test case ID


def view_visit_summary():
    # Objects
    _actor = LoginSteps()
    _patient_visit_summary = PatientVisitSummarySteps()
    _mailbox = MailBoxSteps()

    try:
        _actor.access_waiting_room() \
            .signin_as_patient()

        with MailBox(patient_gmail, password_gmail) as inbox:
            _mailbox.open_link_from_email(mail_title=_mailbox.visit_summary, mbox=inbox)

        # data test to verify is fixed at cepProviderStartVisit.py. Don't change
        _patient_visit_summary.view_visit_summary() \
            .should_see_reason_for_visit("Chest pain,Chest pain") \
            .should_see_plan_or_discharge_instructions("NOT eat meat, fish, milk, egg") \
            .finish_view()

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
    view_visit_summary()


main()
