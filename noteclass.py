class Note:
    def __init__(self,ID,X_POS,Y_POS,isRest,DURATION):
        self.ID = ID
        self.X_POS = X_POS
        self.Y_POS = Y_POS
        self.isRest = isRest
        self.DURATION = DURATION

    def outputID(self):
        return self.ID
    