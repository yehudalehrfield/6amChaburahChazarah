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
  chazarahLimudList = [chazarahLimud]
  resetFlag = False

  chazarahIndex = 0
  # iterate and add chazarah limud with logic following the weekly/daily limud
  for limud in dailyLimudList:
    chazarahLimud.setDate(limud.date)
    if (limud.getDafAmud() == chazarahLimud.getDafAmud()):
      print("~~~~ CHAZARAH CAUGHT UP - NEED TO RESET ~~~~")
      # TODO: reset the chazarahLimud obj and also the pos to 0 --> will need to use an index
      chazarahLimud.reset()
      resetFlag = True
    
    print("LIMUD: " + limud.getDailyLimud() + " \t\t" + "CHAZARAH: " + chazarahLimud.getDailyLimud())
    
    if (resetFlag == False):
      chazarahLimud.incrementPortion()
      thisAmud = chazarahLimudList[chazarahIndex].amud 
      lastAmud = chazarahLimudList[chazarahIndex-1].amud 

      # print("pos: " + str(pos) + " | This: " + thisAmud + " | Last: " + lastAmud)

      if ((chazarahIndex > 0) and (thisAmud == lastAmud)):
        chazarahLimud.incrementAmud()

      if ((chazarahIndex+1) % 4 == 0):
        chazarahLimud.incrementDaf()
    
    newChazarahLimud = copy.copy(chazarahLimud)
    chazarahLimudList.append(newChazarahLimud)
    resetFlag = False
    chazarahIndex += 1
  
  # for limud in dailyLimudList: print(limud.getDailyLimud())
  # for limud in chazarahLimudList: print(limud.getDailyLimud())
  


if __name__ == "__main__":
  """ This is executed when run from the command line """
  main()

