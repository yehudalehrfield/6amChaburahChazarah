#!/usr/bin/env python3
"""
Create a chazarah schedule for the 6am Chaburah Limud
TODO: Define exact paramaters and logic if chazarah schedule
"""

__author__ = "Yehuda"
__version__ = "0.1.0"
__license__ = "MIT"

import datetime
import copy

def main():
  """ Main entry point of the app """

  class DailyLimud:
    def __init__(self, date, daf, amud):
      self.date = date
      self.daf = daf
      self.amud = amud

    def incrementDaf(self):
      self.daf += 1

    def incrementAmud(self):
      self.amud = "a" if (self.amud == "b") else "b"

    def setDate(self, date):
      self.date = date

    def getDafAmud(self):
      return str(self.daf) + self.amud

    def getDailyLimud(self):
      return "Date: " + self.date.strftime("%m/%d/%Y") + ", Limud: " + str(self.daf) + self.amud

    def getDailyLimudWithDay(self):
      week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sha']
      return "Date: " + self.date.strftime("%m/%d/%Y") + ", \tDay: " + week[self.date.weekday()] + ", \tLimud: " + str(self.daf) + self.amud

  class ChazarahLimud:
    def __init__(self,date,daf,amud,portion):
      self.date = date
      self.daf = daf
      self.amud = amud
      self.portion = portion

    def getDafAmud(self):
      return str(self.daf) + self.amud

    def getDateWithDay(self):
      week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sha']
      self.date.strftime("Date: %m/%d/%Y") + ", \tDay: " + week[self.date.weekday()]

    def incrementDaf(self):
      self.daf += 1

    def incrementAmud(self):
      self.amud = "a" if (self.amud == "b") else "b"

    def incrementPortion(self):
      self.portion = "Top" if (self.portion == "Bottom") else "Bottom"

    def setDate(self, date):
      self.date = date

    def reset(self):
      self.daf = 2
      self.amud = "a"
      self.portion = "Top"

    def getDailyLimud(self):
      limud = str(self.daf) + self.amud + self.portion
      return "Date: " + self.date.strftime("%m/%d/%Y") + ", Limud: " + limud

    def getDailyLimudWithDay(self):
      limud = str(self.daf) + self.amud + self.portion
      week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sha']
      return "Date: " + self.date.strftime("%m/%d/%Y") + ", \tDay: " + week[self.date.weekday()] + ", \tLimud: " + limud

  startDate = datetime.datetime(2023,11,27)
  # endDate = datetime.datetime(2024,3,2)
  startDaf = 6
  startAmud = "a"

  days = 60
  
  # tempDate = startDate
  # while tempDate <= endDate:
  #   print(tempDate)
  #   tempDate += datetime.timedelta(days=1)

  index = 0
  daf = startDaf

  # initial limud 
  limud = DailyLimud(datetime.datetime(2023,11,26),startDaf,startAmud)
  dailyLimudList = []

  # iterate and add limud for n days
  for date in (startDate + datetime.timedelta(n) for n in range(days)):
    limud.setDate(date)
    if (index % 7 == 0 and index != 0):
      limud.incrementAmud()
    if (index % 14 == 0 and index != 0):
      limud.incrementDaf()

    # print(limud.getDailyLimudWithDay())
    newLimud = copy.copy(limud)
    dailyLimudList.append(newLimud)

    index += 1

  # initial chazarah
  chazarahStartDaf = 2
  chazarahStartAmud = "a"
  chazarahStartPortion = "Top"

  chazarahLimud = ChazarahLimud(startDate,chazarahStartDaf,chazarahStartAmud,chazarahStartPortion)
  # TODO: fix this so that the first element is correct; however simple fix breaks stuff
  initialChazarahLimud = copy.copy(chazarahLimud)
  chazarahLimudList = []
  resetFlag = False

  chazarahIndex = 0
  # iterate and add chazarah limud with logic following the weekly/daily limud
  for pos,limud in enumerate(dailyLimudList):
    if (limud.getDafAmud() == chazarahLimud.getDafAmud()):
      print("~~~~ CHAZARAH CAUGHT UP - NEED TO RESET ~~~~")
      chazarahLimud.reset()
      resetFlag = True
      chazarahIndex = 0
    if (pos == 0):
      chazarahLimud = initialChazarahLimud
      chazarahLimud.setDate(date)
    else:
      if (resetFlag == False and chazarahIndex > 0):
        chazarahLimud.incrementPortion()
        thisAmud = chazarahLimudList[chazarahIndex-1].amud 
        lastAmud = chazarahLimudList[chazarahIndex-2].amud 

        # print("pos: " + str(pos) + " | This: " + thisAmud + " | Last: " + lastAmud)

        if (thisAmud == lastAmud and chazarahIndex > 1):
          chazarahLimud.incrementAmud()

        if ((chazarahIndex) % 4 == 0):
          chazarahLimud.incrementDaf()
    
    chazarahLimud.setDate(limud.date)
    newChazarahLimud = copy.copy(chazarahLimud)
    chazarahLimudList.append(newChazarahLimud)
    print("LIMUD: " + limud.getDailyLimud() + " \t\t" + "CHAZARAH: " + chazarahLimud.getDailyLimud())
    resetFlag = False
    chazarahIndex += 1
  
  # for limud in dailyLimudList: print(limud.getDailyLimud())
  # for limud in chazarahLimudList: print(limud.getDailyLimud())
  

//TODO: 
def getDailyLimudAndChazarah(limud, chazarah):
  return null

if __name__ == "__main__":
  """ This is executed when run from the command line """
  main()

