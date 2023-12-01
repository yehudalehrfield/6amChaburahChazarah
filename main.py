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

EXPORTS_DIR = "./exports/"
FILE_PREFIX = "6amChabura"
DEFAULT_DAY_COUNT = 180
CSV_HEADERS = ["Date", "Hebrew Date", "לימוד", "חזרה"]
EXCLUDED_DATES = [
    datetime.date(2023, 12, 31),
    datetime.date(2024, 2, 18),
    datetime.date(2024, 4, 14),
    datetime.date(2024, 6, 2),
    datetime.date(2024, 8, 4),
    datetime.date(2024, 9, 22),
]


def main():
    """Main entry point of the app"""

    # ╔════════════════════════════════════╗
    # ║   Initial Limud Values and Set Up  ║
    # ╚════════════════════════════════════╝
    startDate = datetime.date(2023, 12, 4)
    # endDate = datetime.date(2024,3,2)
    startDaf = 6
    startAmud = "a"

    # Number of Days to Generate Chazarah Schedule
    # If argument is given in the command line, use that value
    days = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DAY_COUNT

    # initial limud
    dailyLimud = limud.Limud(datetime.date(2023, 11, 26), startDaf, startAmud)
    dailyLimudList = []

    # iterate and add limud for n days
    index = 0
    for date in (startDate + datetime.timedelta(n) for n in range(days)):
        dailyLimud.setDate(date)
        if index % 7 == 0 and index != 0:
            dailyLimud.incrementAmud()
        if index % 14 == 0 and index != 0:
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

    chazarahLimud = limud.ChazarahLimud(
        startDate, chazarahStartDaf, chazarahStartAmud, chazarahStartSection
    )
    chazarahLimudList = []

    chazarahLimudDict = {}

    chazarahCycleIndex = 0  # repeats for each chazarah cycle (until reset)
    chazarahRunningIndex = 0  # only increments on days that are not off days

    chazarahScheduleCSV = (
        EXPORTS_DIR
        + FILE_PREFIX
        + "_start="
        + startDate.strftime("%m%d%Y")
        + "_days="
        + str(days)
        + ".csv"
    )

    # ╔════════════════════╗
    # ║   Chazarah Logic   ║
    # ╚════════════════════╝
    with open(
        chazarahScheduleCSV,
        "w",
    ) as file:
        writer = csv.writer(file, dialect="excel")

        # Header Row for the CSV
        writer.writerow(CSV_HEADERS)

        # iterate and add chazarah limud with logic following the weekly/daily limud
        for pos, dailyLimud in enumerate(dailyLimudList):
            # On first iteration, chazarah will be 2aTop
            if pos == 0:
                chazarahLimud = limud.ChazarahLimud(
                    startDate, chazarahStartDaf, chazarahStartAmud, chazarahStartSection
                )
                chazarahLimud.setDate(date)
                chazarahRunningIndex += 1
            elif dailyLimud.date in EXCLUDED_DATES:
                print("**** BREAK TIME - SKIP THE DAY's CHAZARAH LIMUD ****")
                writeOffDayRowToCSV(writer, dailyLimud)
                continue
            else:
                lastAmudSection = chazarahLimud.amud + chazarahLimud.section
                lastSection = chazarahLimud.section

                chazarahLimud.incrementSection()

                # TODO: can this logic be improved?
                if chazarahRunningIndex == 0:
                    thisAmud = "a"
                    lastamud = null
                elif chazarahRunningIndex == 1:
                    thisAmud = lastAmud = "a"
                else:
                    thisAmud = chazarahLimudList[chazarahRunningIndex - 1].amud
                    lastAmud = chazarahLimudList[chazarahRunningIndex - 2].amud

                # if amud is complete (top then bottom), increment to the next
                # TODO: can we do this without chazarahCycleIndex?
                if lastSection == "Full":
                    chazarahLimud.incrementAmud()
                elif thisAmud == lastAmud and chazarahCycleIndex > 1:
                    chazarahLimud.incrementAmud()

                if lastAmudSection == "bBottom" or lastAmudSection == "bFull":
                    chazarahLimud.incrementDaf()

                chazarahRunningIndex += 1

            # reset chazarah if chazarah caught up with limud
            if dailyLimud.getDafAmud() == chazarahLimud.getDafAmud():
                print("~~~~ CHAZARAH CAUGHT UP - NEED TO RESET ~~~~")
                chazarahLimud.reset()
                chazarahCycleIndex = 0

            # chazarah date will match limud date
            chazarahLimud.setDate(dailyLimud.date)

            # check if this is 3x
            transitionToFull = isChazara3x(chazarahLimud, chazarahLimudDict)

            if transitionToFull:
                chazarahCount = chazarahLimudDict.get(chazarahLimud.getDafAmudSection())
                chazarahLimud.section = "Full"
                # If the full amud had already been a chazara, increment that dict entry
                if chazarahLimud.getDafAmudSection() in chazarahLimudDict:
                    chazarahLimudDict[chazarahLimud.getDafAmudSection()] = (
                        chazarahLimudDict[chazarahLimud.getDafAmudSection()] + 1
                    )
                # if this is the first time doing the amud, set the intial value as what was previously the value for the section
                else:
                    chazarahLimudDict[chazarahLimud.getDafAmudSection()] = chazarahCount

            # we technically do not need a list here...
            chazarahLimudList.append(copy.copy(chazarahLimud))

            # testing dict functionality
            if not transitionToFull:
                chazarahLimudDict[chazarahLimud.getDafAmudSection()] = (
                    1
                    if not chazarahLimudDict.get(chazarahLimud.getDafAmudSection())
                    else chazarahLimudDict[chazarahLimud.getDafAmudSection()] + 1
                )

            # Add Row to CSV
            writeRowToCSV(writer, dailyLimud, chazarahLimud)

            print(
                pos,
                getDailyLimudAndChazarah(
                    dailyLimud,
                    chazarahLimud,
                    chazarahLimudDict.get(chazarahLimud.getDafAmudSection()),
                    transitionToFull,
                ),
            )

            chazarahCycleIndex += 1


def getDailyLimudAndChazarah(dailyLimud, chazarah, chazarahCount, isFullAmud3x):
    return (
        dailyLimud.getDateString()
        + "\tLimud: "
        + dailyLimud.getDafAmud()
        + "\tChazarah: "
        + chazarah.getDafAmudSection()
        + "\t Chazarah Count: "
        + str(chazarahCount)
        + "\t Amud Transition: "
        + str(isFullAmud3x)
    )


def writeRowToCSV(writer, dailyLimud, chazarahLimud):
    writer.writerow(
        [
            dailyLimud.getDateString(),
            convertGregToHebrew(dailyLimud.date),
            dailyLimud.getDafAmudHeb(False) if not dailyLimud.date.weekday() else "",
            chazarahLimud.getDafAmudSectionHeb(False),
        ]
    )


def writeOffDayRowToCSV(writer, dailyLimud):
    writer.writerow(
        [
            dailyLimud.getDateString(),
            convertGregToHebrew(dailyLimud.date),
            dailyLimud.getDafAmudHeb(False) if not dailyLimud.date.weekday() else "",
            "OFF",
        ]
    )


def convertGregToHebrew(date):
    pyLuachGregDate = dates.GregorianDate(date.year, date.month, date.day)
    pyLuachHebDate = pyLuachGregDate.to_heb()
    return pyLuachHebDate.hebrew_date_string(True).replace("ה׳", "")


def isChazara3x(chazarahLimud, chazarahLimudDict):
    if chazarahLimud.getDafAmudSection() not in chazarahLimudDict:
        return False
    return chazarahLimudDict.get(chazarahLimud.getDafAmudSection()) >= 3


if __name__ == "__main__":
    """This is executed when run from the command line"""
    main()
