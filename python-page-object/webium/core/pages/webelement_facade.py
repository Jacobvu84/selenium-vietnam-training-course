__author__ = 'jacob@vsee.com'

import os,sys, time
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.remote.webelement import WebElement

from abc import ABCMeta, abstractmethod

class WebElementFacade(WebElement):
    __metaclass__ = ABCMeta

    # Implemented
    @abstractmethod
    def waitUntilClickable(self):
        raise NotImplementedError('users must define waitUntilClickable to use this base class')

    @abstractmethod
    def waitUntilVisible(self):
        raise NotImplementedError('users must define waitUntilVisible to use this base class')

    @abstractmethod
    def waitUntilPresent(self):
        raise NotImplementedError('users must define waitUntilPresent to use this base class')

    @abstractmethod
    def type(self, value):
        raise NotImplementedError('users must define type to use this base class')

    # None
    @abstractmethod
    def typeAndEnter(self, value):
        raise NotImplementedError('users must define typeAndEnter to use this base class')

    @abstractmethod
    def typeAndTab(self, value):
        raise NotImplementedError('users must define typeAndTab to use this base class')

    @abstractmethod
    def getAttribute(self, name):
        raise NotImplementedError('users must define getAttribute to use this base class')

    @abstractmethod
    def selectByVisibleText(self, label):
        raise NotImplementedError('users must define selectByVisibleText to use this base class')

    @abstractmethod
    def selectByValue(self, value):
        raise NotImplementedError('users must define selectByValue to use this base class')

    @abstractmethod
    def selectByIndex(self, indexValue):
        raise NotImplementedError('users must define selectByIndex to use this base class')

    @abstractmethod
    def getValue(self):
        raise NotImplementedError('users must define getValue to use this base class')

    @abstractmethod
    def getText(self):
        raise NotImplementedError('users must define getText to use this base class')

    @abstractmethod
    def waitUntilNotVisible(self):
        raise NotImplementedError('users must define waitUntilNotVisible to use this base class')

    @abstractmethod
    def waitUntilEnabled(self):
        raise NotImplementedError('users must define waitUntilEnabled to use this base class')

    @abstractmethod
    def waitUntilDisabled(self):
        raise NotImplementedError('users must define waitUntilDisabled to use this base class')

    @abstractmethod
    def waitForCondition(self, driver):
        raise NotImplementedError('return Wait')

    @abstractmethod
    def click(self):
        raise NotImplementedError('users must define click to use this base class')

    @abstractmethod
    def clear(self):
        raise NotImplementedError('users must define clear to use this base class')
