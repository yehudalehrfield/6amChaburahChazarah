class Limud:
  def __init__(self, date, daf, amud):
      self.date = date
      self.daf = daf
      self.amud = amud
    
  weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sha']
  weekHebrew = ['׳א םוי', '׳ב םוי', '׳ג םוי', '׳ד םוי', '׳ה םוי', '׳ו םוי', 'שדק תבש']

  def incrementDaf(self):
    self.daf += 1

  def incrementAmud(self):
    self.amud = "a" if (self.amud == "b") else "b"

  def setDate(self, date):
    self.date = date

  def getDafAmud(self):
    return str(self.daf) + self.amud

  def getDateAndDayString(self):
    return self.date.strftime("Date: %m/%d/%Y") + ", \tDay: " + self.weekHebrew[self.date.weekday()]

  def getDailyLimud(self):
    return "Date: " + self.date.strftime("%m/%d/%Y") + ", Limud: " + str(self.daf) + self.amud

  def getDailyLimudWithDay(self):
    return "Date: " + self.date.strftime("%m/%d/%Y") + ", \tDay: " + self.weekHebrew[self.date.weekday()] + ", \tLimud: " + st