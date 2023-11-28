import calendar
import util

""" Daily Limud - Amud Weekly"""


class Limud:
    def __init__(self, date, daf, amud):
        self.date = date
        self.daf = daf
        self.amud = amud

    def incrementDaf(self):
        self.daf += 1

    def incrementAmud(self):
        self.amud = "a" if (self.amud == "b") else "b"

    def getDateString(self):
        weekday = util.weekdays[self.date.weekday()]
        month = util.months[self.date.month - 1]
        day = str(self.date.day)
        year = str(self.date.year)
        return "{0}, {1} {2}, {3}".format(weekday, month, day, year)

    def setDate(self, date):
        self.date = date

    def getDay(self):
        return util.weekdays[self.date.weekday()]

    def getHebrewDay(self):
        return util.weekdaysHebrew[self.date.weekday()]

    def getDafAmud(self):
        return str(self.daf) + self.amud

    def getDafAmudHeb(self, tics):
        return util.convertAmudToDots(self.amud) + util.convertToHebDaf(self.daf, tics)
        # return util.convertDafAmudToHeb(self.daf, self.amud, tics)

    def getDateAndDayString(self):
        return (
            self.date.strftime("Date: %m/%d/%Y")
            + ", \tDay: "
            + util.weekdays[self.date.weekday()]
        )

    def getDailyLimud(self):
        return (
            "Date: "
            + self.date.strftime("%m/%d/%Y")
            + ", Limud: "
            + str(self.daf)
            + self.amud
        )
