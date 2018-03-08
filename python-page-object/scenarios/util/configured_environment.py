"""
Handling of multi-module projects

@author jacob
"""

import ConfigParser

class EnvironmentVariables():

    global _config

    def __init__(self, properties="D:\\vsee-space\\eVisitRegression\\selenium\\scenarios\\oneclick\\vsee.properties"):
        self. _config = ConfigParser.RawConfigParser()
        self. _config.read(properties)


    def _property(self, session, option):
        return self._config.get(session, option)


    # Webdriver properties

    def base_url(self):
        return self._property('webdriver', 'webdriver.base.url')

    def webdriver_driver(self):
        return self._property('webdriver', 'webdriver.driver')


    def firefox_driver(self):
        return self._property('webdriver', 'webdriver.firefox.driver')


    def chrome_driver(self):
        return self._property('webdriver', 'webdriver.chrome.driver')

    # Provider Account properties
    def provider_user(self):
        return self._property('provider', 'username')


    def provider_password(self):
        return self._property('provider', 'password')


    # Patients Account properties
    def patient_username(self):
        return self._property('patients', 'username')

    def patient_password(self):
        return self._property('patients', 'password')
