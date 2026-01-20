class Note:
    def __init__(self,ID,X_POS,Y_POS,isRest,DURATION,accent):
        self.ID = ID #int
        self.X_POS = X_POS #int
        self.Y_POS = Y_POS #int
        self.isRest = isRest #bool
        self.DURATION = DURATION #int
        self.accent = accent #int, -1 for no accent

    def outputID(self):
        return self.ID
    
    def outputX_POS(self):
        return self.X_POS
    
    def outputY_POS(self):
        return self.Y_POS
    
    def outputIsRest(self):
        return self.isRest
    
    def outputDURATION(self):
        return self.DURATION
    
    def outputAccent(self):
        return self.accent
    
    def setAccent(self, newAccent):
        self.accent = newAccent
    