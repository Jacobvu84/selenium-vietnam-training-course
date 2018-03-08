__author__ = 'jacob@vsee.com'

import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps
from steps.provider_steps import ProviderSteps
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import startTest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from webium.driver import get_driver

def test_create_provider():
    startTest()

    # Given the admin logged in page
    _loginStep = LoginSteps()
    _loginStep.open_browser_on()
    _loginStep.sign_in()
    assert _loginStep.is_title_matches(), "eVisit-Dev title of vsee.io doesn't match."

    # When admin create new provider
    _navigateStep = NavigateSteps()
    _navigateStep.goto_provider_screen()

    # Then the email should see in the list provider
    _providerStep = ProviderSteps()
    _providerStep.create_new('Selenium', 'VN', 'QA Engineer', 'vuthelinh@gmail.com', True, 'Remote Medic')
    _providerStep.search_provider_by_email('vuthelinh@gmail.com')
    assert _providerStep.should_see_the_email_matches('vuthelinh@gmail.com'), "vuthelinh@gmail.com not found"


     # When admin delete the provider
    _providerStep.delete_provider_by_email()

     # Then should see the message is "No matching records found"
    assert _providerStep.should_see_no_results_found(), "Found existing the email"

    get_driver().quit()

def main():
    test_create_provider()


main()