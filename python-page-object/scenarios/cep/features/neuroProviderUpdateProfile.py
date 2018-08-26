__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.provider.my_patient import MyPatientSteps
from steps.font_end.provider.my_patient import AllVisitSteps
from steps.navigate_steps import NavigateSteps
from steps.document import DocumentSteps
from steps.account_steps import ProviderProfileSteps
from steps.font_end.provider.visit_note import VisitNoteSteps

testID = sys.argv[1]  # test case ID


def provider_update_profile():
    # Objects
    _actor = LoginSteps()
    _all_visit = AllVisitSteps()
    _navigate = NavigateSteps()
    _my_patient = MyPatientSteps()
    _document = DocumentSteps()
    _profile = ProviderProfileSteps()
    _visit_detail = VisitNoteSteps()
    doc_file = 'my_doc.png'


    try:
        _actor \
            .visit_neuro() \
            .signin_as_provider(env='neu')
        _navigate\
            .goto_patient_page()
        _my_patient \
            .select_tab("All Visits")
        _all_visit \
            .search_history_visit_by(value='Guest Neuro 02') \
            .should_see_the_status_visit("Deleted")\
            .view()
        _visit_detail \
            .has_tab("Documents")
        _document\
            .upload_document(doc_file)\
            .should_see_the_document(doc_file)\
            .delete_document("Are you sure you want to delete this file?")\
            .should_see_the_message("You have not uploaded any Health Records.")

        odtc = ODTC()
        index = 0

        provider = odtc.get_neuro_provider()
        email = provider[index].split(",")[0]
        f_name = provider[index].split(",")[1]
        l_name = provider[index].split(",")[2]
        full_name = odtc.get_fullname_provider(env='neu')

        _actor\
            .open_profile(full_name)
        _profile.should_see_profile_information(email=email,
                                                first_name=f_name,
                                                last_name=l_name,
                                                short_bio="evisitqa06+test{last_name}@gmail.com",
                                                street_address="514 S. Magnolia St.",
                                                city="Orlando",
                                                state="Florida",
                                                zipcode="32806",
                                                phone_number="650.390.6970",
                                                timezone="UTC-07:00 Pacific Time (US & Canada)",
                                                DEA="none",
                                                NPI="none",
                                                educational_training="".ljust(1),
                                                professional_interests="".ljust(1),
                                                personal_interests="".ljust(1))
        _profile.edit_profile(first_name=l_name,
                              last_name=f_name,
                              short_bio="The life is not real",
                              street_address="7500 Security Boulevard",
                              city="Baltimore",
                              state="Maryland",
                              zipcode="21244",
                              phone_number="650.390.9999",
                              timezone="UTC-08:00 Alaska",
                              DEA="none",
                              NPI="none",
                              educational_training="Master's Degree in Healthcare Informatics",
                              professional_interests="Exploring the relationship between social media",
                              personal_interests="traveling and long walks on the beach",
                              photo="no")
        _profile.should_see_profile_information(email=email,
                                                first_name=l_name,
                                                last_name=f_name,
                                                short_bio="The life is not real",
                                                street_address="7500 Security Boulevard",
                                                city="Baltimore",
                                                state="Maryland",
                                                zipcode="21244",
                                                phone_number="650.390.9999",
                                                timezone="UTC-08:00 Alaska",
                                                DEA="none",
                                                NPI="none",
                                                educational_training="Master's Degree in Healthcare Informatics",
                                                professional_interests="Exploring the relationship between social media",
                                                personal_interests="traveling and long walks on the beach")
        print "[PASSED]: TEST PASSED"
    except Exception as e:
        print type(e)
        print e.args
        print e
        print "[INFO]: TEST FAILED"
    finally:
        _actor.quit()
        create_gif()

def main():
    start_test()
    provider_update_profile()


main()
