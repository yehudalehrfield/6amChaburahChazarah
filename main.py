#!/usr/bin/env python3
"""
Create a chazarah schedule for the 6am Chaburah 
TODO: Define exact paramaters and logic for chazarah schedule (notably transitioning from half-amud)
"""

__author__ = "Yehuda"
__version__ = "0.1.0"
__license__ = "MIT"

import sys
import datetime
import copy
import limud
import csv
from pyluach import dates, hebrewcal

EXPORTS_DIR = './exports/'
FILE_PREFIX = '6amChabura'
DEFAULT_DAY_COUNT = 60
CSV_HEADERS = ["Date","Hebrew Date","לימוד","חזרה"]

def main():
  """ Main entry point of the app """

  # ╔════════════════════════════════════╗
  # ║   Initial Limud Values and Set Up  ║
  # ╚════════════════════════════════════╝ 
  startDate = datetime.datetime(2023,11,27)
  # endDate = datetime.datetime(2024,3,2)
  startDaf = 6
  startAmud = "a"

  # Number of Days to Generate Chazarah Schedule
  # If argument is given in the command line, use that value
  days = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DAY_COUNT

  # initial limud 
  dailyLimud = limud.Limud(datetime.datetime(2023,11,26),startDaf,startAmud)
  dailyLimudList = []

  # iterate and add limud for n days
  index = 0
  for date in (startDate + datetime.timedelta(n) for n in range(days)):
    dailyLimud.setDate(date)
    if (index % 7 == 0 and index != 0):
      dailyLimud.incrementAmud()
    if (index % 14 == 0 and index != 0):
      dailyLimud.incrementDaf()

    # print(limud.getDailyLimudWithDay())
    dailyLimudList.append(copy.copy(dailyLimud))

    index += 1

  # ╔═══════════════════════════════════════╗
  # ║   Initial Chazarah Values and Set Up  ║
  # ╚═══════════════════════════════════════╝ 
  chazarahStartDaf = 2
  chazarahStartAmud = "a"
  chazarahStartSection = "Top"

  chazarahLimud = limud.ChazarahLimud(startDate,chazarahStartDaf,chazarahStartAmud,chazarahStartSection)
  chazarahLimudList = [] # we technically do not need a list here since we are writing to csv...

  chazarahIndex = 0
  
  # ╔════════════════════╗
  # ║   Chazarah Logic   ║
  # ╚════════════════════╝
  with open(EXPORTS_DIR + FILE_PREFIX + '_start=' + startDate.strftime("%m%d%Y") + '_days=' + str(days) + '.csv','w') as file:
    writer = csv.writer(file, dialect='excel')

    # Header Row for the CSV
    writer.writerow(CSV_HEADERS)

    # iterate and add chazarah limud with logic following the weekly/daily limud
    for pos,dailyLimud in enumerate(dailyLimudList):
      # On first iteration, chazarah will be 2aTop
      if (pos == 0):
        chazarahLimud = limud.ChazarahLimud(startDate,chazarahStartDaf,chazarahStartAmud,chazarahStartSection)
        chazarahLimud.setDate(date)
      else:
        # increment section and amud/daf if applicable
        chazarahLimud.incrementSection()
        
        thisAmud = chazarahLimudList[chazarahIndex-1].amud 
        lastAmud = chazarahLimudList[chazarahIndex-2].amud 

        # if amud is complete (top then bottom), increment to the next
        if (thisAmud == lastAmud and chazarahIndex > 1):
          chazarahLimud.incrementAmud()

        # after four iterations (top, bottom, top, bottom), we move on to the next daf 
        if (chazarahIndex % 4 == 0):
          chazarahLimud.incrementDaf()

      # reset chazarah if chazarah caught up with limud
      if (dailyLimud.getDafAmud() == chazarahLimud.getDafAmud()):
        print("~~~~ CHAZARAH CAUGHT UP - NEED TO RESET ~~~~")
        chazarahLimud.reset()
        chazarahIndex = 0

      # chazarah date will match limud date
      chazarahLimud.setDate(dailyLimud.date)

      # we technically do not need a list here...
      chazarahLimudList.append(copy.copy(chazarahLimud))
      
      # Add Row to CSV
      writeRowToCSV(writer,dailyLimud,chazarahLimud)
      
      print(getDailyLimudAndChazarah(dailyLimud,chazarahLimud))

      chazarahIndex += 1
  
def getDailyLimudAndChazarah(dailyLimud, chazarah):
  return dailyLimud.getDateString() + ", \tLimud: " + dailyLimud.getDafAmud() + ", \tChazarah: " + chazarah.getDafAmudSection()

def writeRowToCSV(writer, dailyLimud, chazarahLimud):
  writer.writerow([dailyLimud.getDateString(), convertGregToHebrew(dailyLimud.date), dailyLimud.getDafAmudHeb(False) if not dailyLimud.date.weekday() else "", chazarahLimud.getDafAmudSectionHeb(False)])

def convertGregToHebrew(date):
  pyLuachGregDate = dates.GregorianDate(date.year, date.month, date.day)
  pyLuachHebDate = pyLuachGregDate.to_heb()
  return pyLuachHebDate.hebrew_date_string(True)

if __name__ == "__main__":
  """ This is executed when run from the command line """
  main()

