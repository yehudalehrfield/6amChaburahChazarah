import limud

""" Chazarah Limud - Half Amud Daily (To Start)"""
class ChazarahLimud(limud.Limud):
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