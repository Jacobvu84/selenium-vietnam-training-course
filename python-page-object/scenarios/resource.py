import os, inspect


class UserDir(object):
    pass


# project root
user_dir = os.path.dirname(os.path.abspath(inspect.getsourcefile(UserDir)))

"""
Open Data Test Connectivity (ODTC) 
"""

TEMP_DIR_WIN = "C:\\tempdir\\"


class ODTC(object):
    def get_log_data(self, file_log):
        data = []
        try:
            log_file = TEMP_DIR_WIN + "bin\\" + file_log
            with open(log_file) as f:
                for line in f:
                    data.append(line)
            return data
        except Exception as e:
            print type(e)
            print e.args
            print e
            print file_log + " not found"

    # On-Duty
    def get_cep_room(self):
        """
        Gets the list of room in .\bin\room.log
        :return: ArrayList
        """
        return self.get_log_data("room.log")

    def get_cep_patient(self):
        """
        Gets the list of patient in .\bin\eligibility.log
        :return: ArrayList
        """
        return self.get_log_data("eligibility.log")

    def get_snf_patient(self):
        """
        Gets the list of patient in .\bin\snf_eligibility.log
        :return: ArrayList
        """
        return self.get_log_data("snf_eligibility.log")

    def get_tele_patient(self):
        """
        Gets the list of patient in .\bin\tele_eligibility.log
        :return: ArrayList
        """
        return self.get_log_data("tele_eligibility.log")

    def get_cep_provider(self):
        """
        Gets the list of doctor in .\bin\provider.log
        :return: ArrayList
        """
        return self.get_log_data("provider.log")

    # SNF
    def get_snf_provider(self):
        """
        Gets the list of doctor in .\bin\snf_provider.log
        :return: ArrayList
        """
        return self.get_log_data("snf_provider.log")

    def get_neuro_provider(self):
        return self.get_log_data("neuro_provider.log")

    def get_snf_nurse(self):
        """
        Gets the list of doctor in .\bin\snf_nurse.log
        :return: ArrayList
        """
        return self.get_log_data("snf_nurse.log")

    def get_snf_room(self):
        """
        Gets the list of room in .\bin\snf_room.log
        :return: ArrayList
        """
        return self.get_log_data("snf_room.log")

    def get_neuro_room(self):
        """
        Gets the list of room in .\bin\snf_room.log
        :return: ArrayList
        """
        return self.get_log_data("neuro_room.log")

    # TelepSych
    def get_tele_provider(self):
        """
        Gets the list of doctor in .\bin\tele_provider.log
        :return: ArrayList
        """
        return self.get_log_data("tele_provider.log")

    def get_tele_nurse(self):
        """
        Gets the list of doctor in .\bin\tele_nurse.log
        :return: ArrayList
        """
        return self.get_log_data("tele_nurse.log")

    def get_tele_room(self):
        """
        Gets the list of room in .\bin\tele_room.log
        :return: ArrayList
        """
        return self.get_log_data("tele_room.log")

    def get_room_by(self, env, index):
        _rooms = []
        rooms = []
        if env == "snf":
            rooms = self.get_snf_room()
        elif env == "tele":
            rooms = self.get_tele_room()
        else:
            rooms = self.get_cep_room()

        for room in rooms:
            room_url = room.split(",")[0]
            _rooms.append(room_url)
        return _rooms[index]

    def get_room_name_by(self, env, index=0):
        _names = []
        names = []
        if env == "snf":
            names = self.get_snf_room()
        elif env == "tele":
            names = self.get_tele_room()
        elif env == "neu":
            names = self.get_neuro_room()
        else:
            names = self.get_cep_room()

        for name in names:
            room_name = name.split(",")[3]
            _names.append(room_name)
        return _names[index]

    def get_nurse_by(self, env, index):
        _nurse = []
        nurses = []
        if env == "snf":
            nurses = self.get_snf_nurse()
        elif env == "tele":
            nurses = self.get_tele_nurse()
        else:
            pass

        for nurse in nurses:
            email = nurse.split(",")[0]
            _nurse.append(email)
        return _nurse[index]

    def get_fullname_provider(self, env='cep', index=0):
        if env == 'cep':
            provider = self.get_cep_provider()
        elif env == "snf":
            provider = self.get_snf_provider()
        elif env == "neu":
            provider = self.get_neuro_provider()
        else:
            provider = self.get_tele_provider()

        fname = provider[index].split(",")[1]
        lname = provider[index].split(",")[2]
        return fname + " " + lname

    def get_email_provider(self, env='cep', index=0):
        if env == 'cep':
            provider = self.get_cep_provider()
        elif env == "snf":
            provider = self.get_snf_provider()
        elif env == "neu":
            provider = self.get_neuro_provider()
        else:
            provider = self.get_tele_provider()
        return provider[index].split(",")[0]

    def get_fullname_patient(self, env='cep', index=0):
        if env == 'cep':
            patient = self.get_cep_patient()
        elif env == 'tele':
            patient = self.get_tele_patient()
        else:
            patient = self.get_snf_patient()
        fname = patient[index].split(",")[1]
        lname = patient[index].split(",")[2]
        return fname + " " + lname

    def get_email_patient(self, env='cep', index=0):
        if env == 'cep':
            patient = self.get_cep_patient()
            return patient[index].split(",")[0]

    def get_nurse_username(self, env='snf', index=0):
        if env == "snf":
            nurse = self.get_snf_nurse()
        else:
            nurse = self.get_tele_nurse()
        return nurse[index].split(",")[1]

    def get_nurse_full_name(self, env='snf', index=0):
        if env == "snf":
            nurse = self.get_snf_nurse()
        else:
            nurse = self.get_tele_nurse()
        fname = nurse[index].split(",")[3]
        lname = nurse[index].split(",")[4]
        return fname + " " + lname

