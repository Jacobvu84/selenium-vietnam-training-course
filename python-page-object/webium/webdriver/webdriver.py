__author__ = 'jacob@vsee.com'


from abc import ABCMeta, abstractmethod

class AbsWebdriver(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def init_driver(self):
        """ init driver """
