weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
weekdaysHebrewBackwards = ['׳א םוי', '׳ב םוי', '׳ג םוי', '׳ד םוי', '׳ה םוי', '׳ו םוי', 'שדק תבש']
weekdaysHebrew = ['יום ב׳', 'יום ג׳', 'יום ד׳', 'יום ה׳', 'יום ו׳', 'שבת קדש', 'יום א׳']
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

hebrewCount = ["","א","ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט", "י",
 "י״א", "י״ב", "י״ג", "י״ד", "ט״ו", "ט״ז", "י״ז", "י״ח", "י״ט", "כ",
 "כ״א", "כ״ב", "כ״ג", "כ״ד", "כ״ה", "כ״ו", "כ״ז", "כ״ח", "כ״ט", "ל",
 "ל״א", "ל״ב", "ל״ג", "ל״ד", "ל״ה", "ל״ו", "ל״ז", "ל״ח", "ל״ט", "מ",
 "מ״א", "מ״ב", "מ״ג", "מ״ד", "מ״ה", "מ״ו", "מ״ז", "מ״ח", "מ״ט", "נ",
 "נ״א", "נ״ב", "נ״ג", "נ״ד", "נ״ה", "נ״ו", "נ״ז", "נ״ח", "נ״ט", "ס",
 "ס״א", "ס״ב", "ס״ג", "ס״ד", "ס״ה", "ס״ו", "ס״ז", "ס״ח", "ס״ט", "ע",
 "ע״א", "ע״ב", "ע״ג", "ע״ד", "ע״ה", "ע״ו", "ע״ז", "ע״ח", "ע״ט", "פ",
 "פ״א", "פ״ב", "פ״ג", "פ״ד", "פ״ה", "פ״ו", "פ״ז", "פ״ח", "פ״ט", "צ",
 "צ״א", "צ״ב", "צ״ג", "צ״ד", "צ״ה", "צ״ו", "צ״ז", "צ״ח", "צ״ט", "ק"]

hebrewCountNoTics = [num.replace("״","") for num in hebrewCount]

amudim = {"a":".", "b":":"}

def convertToHebDaf(num, tics):
  return hebrewCount[num] if tics else hebrewCountNoTics[num]

def convertAmudToDots(amud):
  return amudim.get(amud)

# TODO: check why this is failing to add dots
def convertDafAmudToHeb(dafNum, amud, tics):
  return amudim.get(amud) + hebrewCount[dafNum] if tics else hebrewCountNoTics[dafNum]