__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_patient import MyPatientSteps
from steps.font_end.provider.visit_note import VisitNoteSteps

testID = sys.argv[1]  # test case ID

# Tester thread
def provider_edit_visit_note():
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _my_patient = MyPatientSteps()
    _visit_note = VisitNoteSteps()
    odtc = ODTC()
    patients = odtc.get_cep_patient()
    email = patients[0].split(",")[0]
    full_name = odtc.get_fullname_patient()

    try:
        _actor.browse_the_web().signin_as_provider()
        _navigate.goto_patient_page()
        _my_patient \
            .search_patient_by(email) \
            .go_to_visit_note(full_name)

        _visit_note.scroll_down_bottom_page().search_visit_history_by_date().edit_visit_note()

        """
        
        Verify before edit
        
        _visit_note.should_see_the_reason_for_visit_in_my_patient("Chest pain,Rash,Fever") \
                   .should_see_the_past_medical_history_in_my_patient("Depression,Heart burn (GERD),Headaches (Migraines),Irregular heart beat,Asthma") \
                   .should_see_the_allergies_in_my_patient("5HT1 agonist,12 Hour Nasal,Apresoline,Moxifloxacin") \
                   .should_see_the_medications_in_my_patient("Amoxicillin,Paracetamol,Hypertension,Metoprolol") \
        """
        _visit_note.provider_edit_chief_complaint("Asthma,Constipation") \
            .provider_edit_past_medical_history("Thyroid problem") \
            .provider_edit_allergies("Dandrex") \
            .provider_edit_medications("Abciximab")

        _visit_note.provider_edit_comment_plan_or_discharge_instructions("Do exercise in the morning") \
            .complete__and_sent_visit_to_patient()

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
    provider_edit_visit_note()


main()
