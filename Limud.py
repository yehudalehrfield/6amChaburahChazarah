class Limud:
  def __init__(self, date, daf, amud):
      self.date = date
      self.daf = daf
      self.amud = amud
    
  weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
  weekdaysHebrewBackwards = ['׳א םוי', '׳ב םוי', '׳ג םוי', '׳ד םוי', '׳ה םוי', '׳ו םוי', 'שדק תבש']
  weekdaysHebrew = ['יום א׳', 'יום ב׳', 'יום ג׳', 'יום ד׳', 'יום ה׳', 'יום ו׳', 'שבת קדש']
  
  

  def incrementDaf(self):
    self.daf += 1

  def incrementAmud(self):
    self.amud = "a" if (self.amud == "b") else "b"

  def getDateString(self):
    return self.date.strftime("%m/%d/%Y")

  def setDate(self, date):
    self.date = date

  def getDay(self):
    return self.weekdays[self.date.weekday()]

  def getHebrewDay(self):
    return self.weekdaysHebrew[self.date.weekday()]
    
  def getDafAmud(self):
    return str(self.daf) + self.amud

  def getDateAndDayString(self):
    return self.date.strftime("Date: %m/%d/%Y") + ", \tDay: " + self.weekdays[self.date.weekday()]
    

  def getDailyLimud(self):
    return "Date: " + self.date.strftime("%m/%d/%Y") + ", Limud: " + str(self.daf) + self.amud

  def getDailyLimudWithDay(self):
    return "Date: " + self.date.strftime("%m/%d/%Y") + ", \tDay: " + self.weekdays[self.date.weekday()] + ", \tLimud: " + st
    