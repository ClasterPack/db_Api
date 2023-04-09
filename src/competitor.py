from datetime import timedelta


class Competitor:

    def __init__(self, name, surname, tryout_number, record):
        self.firstname = name
        self.surname = surname
        self.tryout_number = tryout_number
        self.record = timedelta(seconds=record)

    def __repr__(self):
        return repr((self.tryout_number, self.firstname, self.surname, self.record))
