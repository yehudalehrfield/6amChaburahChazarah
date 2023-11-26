#!/usr/bin/env python3
"""
Create a chazarah schedule for the 6am Chaburah 
TODO: Define exact paramaters and logic if chazarah schedule
"""

__author__ = "Yehuda"
__version__ = "0.1.0"
__license__ = "MIT"

import sys
import datetime
import copy
import Limud
import csv
from pyluach import dates, hebrewcal

def main():
  """ Main entry point of the app """

  """ Daily Limud - Amud Weekly"""
  class DailyLimud(Limud.Limud):
    def __init__(self, date, daf, amud):
      super().__init__(date, daf, amud)
  
  """ Chazarah Limud - Half Amud Daily (To Start)"""
  class ChazarahLimud(Limud.Limud):
    def __init__(self,date,daf,amud,section):
      self.date = date
      self.daf = daf
      self.amud = amud
      self.section = section

    def getDafAmudSection(self):
      return self.getDafAmud() + " " +  self.section

    def getDafAmudSectionHeb(self, tics):
      return self.getDafAmudHeb(tics) + " " +  self.section

    def incrementSection(self):
      self.section = "Top" if (self.section == "Bottom") else "Bottom"

    def reset(self):
      self.daf = 2
      self.amud = "a"
      self.section = "Top"

  # Initial Limud Values
  startDate = datetime.datetime(2023,11,27)
  # endDate = datetime.datetime(2024,3,2)
  startDaf = 6
  startAmud = "a"

  # Number of Days to Calculate Chazarah Schedule
  # If argument is given in the command line, use that value
  defaultDays = 60
  days = int(sys.argv[1]) if len(sys.argv) > 1 else defaultDays

  # initial limud 
  limud = DailyLimud(datetime.datetime(2023,11,26),startDaf,startAmud)
  dailyLimudList = []

  # iterate and add limud for n days
  index = 0
  for date in (startDate + datetime.timedelta(n) for n in range(days)):
    limud.setDate(date)
    if (index % 7 == 0 and index != 0):
      limud.incrementAmud()
    if (index % 14 == 0 and index != 0):
      limud.incrementDaf()

    # print(limud.getDailyLimudWithDay())
    dailyLimudList.append(copy.copy(limud))

    index += 1

  # Initial Chazarah Values
  chazarahStartDaf = 2
  chazarahStartAmud = "a"
  chazarahStartSection = "Top"

  chazarahLimud = ChazarahLimud(startDate,chazarahStartDaf,chazarahStartAmud,chazarahStartSection)
  chazarahLimudList = []

  chazarahIndex = 0

  EXPORTS_DIR = './exports/'
  FILE_PREFIX = '6amChabura'
  
  with open(EXPORTS_DIR + FILE_PREFIX + '_start=' + startDate.strftime("%m%d%Y") + '_days=' + str(days) + '.csv','w') as file:
    writer = csv.writer(file, dialect='excel')

    # Header Row for the CSV
    writer.writerow(["Date","Hebrew Date","Limud","Chazarah"])

    # iterate and add chazarah limud with logic following the weekly/daily limud
    for pos,limud in enumerate(dailyLimudList):
      # On first iteration, chazarah will be 2aTop
      if (pos == 0):
        chazarahLimud = ChazarahLimud(startDate,chazarahStartDaf,chazarahStartAmud,chazarahStartSection)
        chazarahLimud.setDate(date)
      else:
        # if we are not resetting, increment section and amud/daf if applicable
        chazarahLimud.incrementSection()
        
        thisAmud = chazarahLimudList[chazarahIndex-1].amud 
        lastAmud = chazarahLimudList[chazarahIndex-2].amud 

        # print("pos: " + str(pos) + " | This: " + thisAmud + " | Last: " + lastAmud)

        if (thisAmud == lastAmud and chazarahIndex > 1):
          chazarahLimud.incrementAmud()

        if (chazarahIndex % 4 == 0):
          chazarahLimud.incrementDaf()

      # reset chazarah if chazarah caught up with limud
      if (limud.getDafAmud() == chazarahLimud.getDafAmud()):
        print("~~~~ CHAZARAH CAUGHT UP - NEED TO RESET ~~~~")
        chazarahLimud.reset()
        chazarahIndex = 0

      # chazarah date will match limud date
      chazarahLimud.setDate(limud.date)

      chazarahLimudList.append(copy.copy(chazarahLimud))
      
      # Add to CSV
      writer.writerow([limud.getDateString(), convertGregToHebrew(limud.date), limud.getDafAmudHeb(False) if not limud.date.weekday() else "", chazarahLimud.getDafAmudSectionHeb(False)])
      
      print(getDailyLimudAndChazarah(limud,chazarahLimud))

      chazarahIndex += 1
  

def getDailyLimudAndChazarah(limud, chazarah):
  # return limud.getDateAndDayString() + ", \tLimud: " + limud.getDafAmud() + ", \tChazarah: " + chazarah.getDafAmudSection()
  return limud.getDateString() + ", \tLimud: " + limud.getDafAmud() + ", \tChazarah: " + chazarah.getDafAmudSection()

# TODO:
def writeLineToCSV(writer, limud, chazarah):
  return null

def convertGregToHebrew(date):
  pyLuachGregDate = dates.GregorianDate(date.year, date.month, date.day)
  pyLuachHebDate = pyLuachGregDate.to_heb()
  return pyLuachHebDate.hebrew_date_string(True)

if __name__ == "__main__":
  """ This is executed when run from the command line """
  main()

