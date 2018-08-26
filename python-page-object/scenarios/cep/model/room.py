__author__ = 'jacob@vsee.com'

import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.rand import generate

from util.setting import _domain
from util.setting import _version

from util.setting import _snf_domain
from util.setting import _snf_version

from util.setting import _telesych_domain
from util.setting import _telesych_version

from util.setting import _neuro_domain
from util.setting import _neuro_version

from resource import ODTC


class ConnectProviderData(object):
    odtc = ODTC()

    def get_cep_providers(self):
        emails = []
        providers = self.odtc.get_cep_provider()
        for provider in providers:
            email = provider.split(",")[0]
            emails.append(email)
        return emails

    def get_tele_providers(self):
        emails = []
        providers = self.odtc.get_tele_provider()
        for provider in providers:
            email = provider.split(",")[0]
            emails.append(email)
        return emails

    def get_snf_providers(self):
        emails = []
        providers = self.odtc.get_snf_provider()
        for provider in providers:
            email = provider.split(",")[0]
            emails.append(email)
        return emails

    def get_neuro_providers(self):
        emails = []
        providers = self.odtc.get_neuro_provider()
        for provider in providers:
            email = provider.split(",")[0]
            emails.append(email)
        return emails


class Room(object):
    def __init__(self, slug, code, name, assignments, domain, version):
        self.slug = "cepqa1_" + slug
        self.code = "cepqa1_" + code
        self.name = "CEP Automation QA Room 1_" + name
        self.assignments = assignments
        self.domain = domain
        self.url = 'https://' + domain + '/cep/' + version + '/u/' + self.slug + ''


class RoomData(object):
    connect = ConnectProviderData()

    def get_cep_room(self):
        # On-Duty
        clinical = Room(generate(30), generate(31), generate(32), self.connect.get_cep_providers(), _domain, _version)
        conference = Room(generate(40), generate(41), generate(42), self.connect.get_cep_providers(), _domain, _version)
        emergency = Room(generate(50), generate(51), generate(52), self.connect.get_cep_providers(), _domain, _version)

        rooms = [clinical, conference, emergency]
        return rooms

    # Data Test
    # - clinical:    for adding
    # - conference:  for deleting
    # - emergency:   for editing

    def get_snf_rooms(self):
        # SNF
        snf_clinical = Room(generate(10), generate(11), generate(12), self.connect.get_snf_providers(), _snf_domain, _snf_version)
        snf_conference = Room(generate(20), generate(21), generate(22), self.connect.get_snf_providers(), _snf_domain, _snf_version)

        snf_rooms = [snf_clinical, snf_conference]
        return snf_rooms

    def get_tele_rooms(self):
        # TelePsych
        tele_clinical = Room(generate(13), generate(14), generate(15), self.connect.get_tele_providers(),
                             _telesych_domain, _telesych_version)
        tele_conference = Room(generate(23), generate(24), generate(25), self.connect.get_tele_providers(),
                               _telesych_domain, _telesych_version)

        tele_rooms = [tele_clinical, tele_conference]

        return tele_rooms

    def get_neuro_rooms(self):
        # Neuro
        neuro_clinical = Room(generate(16), generate(17), generate(18), self.connect.get_neuro_providers(),
                             _neuro_domain, _neuro_version)
        neuroconference = Room(generate(26), generate(27), generate(28), self.connect.get_neuro_providers(),
                               _neuro_domain, _neuro_version)

        neuro_rooms = [neuro_clinical, neuroconference]
        return neuro_rooms
