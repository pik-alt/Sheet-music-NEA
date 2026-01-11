from tkinter import *
from tkinter import messagebox
import TAOAT
from midiutil import *
from noteclass import Note
from sorts import merge,mergeSort


class SheetMusic:

    def __init__(self):
    
        self.window = Tk()
        self.window.title("Test")
        self.window.geometry("1000x500")
        self.window.resizable (False,False)
        self.window.config(background="blue")

        #checks if its 6
        if TAOAT.is_six(6):
            print(6)

        self.notesList = []

        #Setting up the two main frames for the UI, one for the top bar (optionsFrame) and one for the main stave (staveFrame)
        optionsFrame = Frame(self.window)
        optionsFrame.grid(row = 0, column = 0, padx = 50, pady = 30, columnspan = 2)

        staveFrame = Frame(self.window)
        staveFrame.grid(row = 1, column = 0, padx = 50, pady = 30, columnspan = 2)


        #Creates the two canvasas to be able to import images onto them
        #Currently very different colours just so I can see what I'm doing
        optionsCanvas = Canvas(optionsFrame, width = 930, height = 100)
        optionsCanvas.config(bg="green")
        optionsCanvas.pack()

        self.staveCanvas = Canvas(staveFrame, width = 900, height = 200)
        self.staveCanvas.config(bg="red")


        #List of clefs for the dropdown menu
        self.listClef = ["Treble","Bass"]


        #loads in images of all the notes and clefs
        self.quarter = PhotoImage(file="images/quarter.png")
        self.half = PhotoImage(file="images/half.png")
        self.eighth = PhotoImage(file="images/eighth.png")
        self.full = PhotoImage(file="images/full.png") 
        self.rest = PhotoImage(file="images/rest.png") 
            #full and rest need to self.full and self.rest as I need to compare them later and so they need to exist as objects

        self.treble = PhotoImage(file="images/treble.png")
        self.bass = PhotoImage(file="images/bass.png")


        #initialises the variable 'currentNote' and has it be set to the default of a quarter note
        self.currentNote = self.quarter

        #initialises the variable 'currentClef' and sets it to the default of treble
        self.currentClef = StringVar(value="Treble")

        #initialises the constant STAVE_GAP, being the distance between stave lines
        self.STAVE_GAP = 30

        #draw stave lines
        for i in range(0, 5):
            self.staveCanvas.create_line(20, 30 + (self.STAVE_GAP * i), 880, 30 + (self.STAVE_GAP * i), width = 3)
            self.staveCanvas.pack()

        #Draws the one vertical line at the beginning and the two at the end
        self.staveCanvas.create_line(20, 29, 20, 152, width = 3)
        self.staveCanvas.create_line(880, 29, 880, 152, width = 3)
        self.staveCanvas.create_line(870, 29, 870, 152, width = 3)


        #Create buttons for the top options bar
        #Uses the lambda function because it doesn't work if we just call changeNote(quarter) for instance
        buttonQuarter = Button(optionsCanvas, image=self.quarter, command=lambda n=self.quarter: self.changeNote(n))
        buttonQuarter.grid(column=0, row = 0, padx = 5, pady = 5)

        buttonHalf = Button(optionsCanvas, image=self.half, command=lambda n=self.half: self.changeNote(n))
        buttonHalf.grid(column = 1, row = 0 , padx = 5, pady = 5)

        buttonEighth = Button(optionsCanvas, image=self.eighth, command=lambda n=self.eighth: self.changeNote(n))
        buttonEighth.grid(column = 3, row = 0, padx = 5, pady = 5)

        buttonFull = Button(optionsCanvas, image=self.full, command=lambda n=self.full: self.changeNote(n))
        buttonFull.grid(column = 4, row = 0, padx = 5, pady = 5)

        buttonRest = Button(optionsCanvas, image=self.rest, command=lambda n=self.rest: self.changeNote(n))
        buttonRest.grid(column = 5, row = 0, padx = 5, pady = 5)


        #Creates the clef selection drop down menu and the label 
        clefDropDown = OptionMenu(optionsCanvas, self.currentClef, *self.listClef)
        clefDropDown.grid(column = 6, row = 0, padx = (50,0), pady = (10,0))

        textClefDropDown = Label(optionsCanvas, text="Select Clef", font=("Arial", 10))
        textClefDropDown.grid(column = 6, row = 0, padx = (50,0), pady = (10,0),sticky=N)


        #Creates button for placing the clef
        #Currently the user has to delete the old clef manually, that should be fixed in the future ideally
        buttonPlaceClef = Button(optionsCanvas, text="Place\nclef", command = self.placeClef)
        buttonPlaceClef.grid(column = 7, row = 0, padx = (15,20), pady = 0)

        

        self.BPMtextBox = Text(optionsCanvas, height = 1, width = 3, bg="lightgray", font=("Arial",15))
        self.BPMtextBox.grid(column = 8, row = 0, padx = (30,0), pady = (10,0))

        BPMtextBoxLabel = Label(optionsCanvas, text = "Select Tempo", font=("Arial", 10))
        BPMtextBoxLabel.grid(column = 8, row = 0, padx = (30,0), pady=(10,20), sticky = N)

        #Inserting initial BPM of 120
        self.BPMtextBox.insert("1.0", "120")


        buttonGenerateMusic = Button(optionsCanvas, text="Generate\nMIDI file",command=self.validateBPM)
        buttonGenerateMusic.grid(column = 9, row = 0, padx = 100, pady = 5)


        #Dictionary to translate from the note pointers generated by TKInter to their value in 4/4
        self.notesDict = {
            self.quarter : 1,
            self.half    : 2,
            self.eighth  : 0.5,
            self.full    : 4,
            self.rest    : 1 
        }


        #binds left mouse click to execute the 'leftClickEvent' function
        self.staveCanvas.bind('<1>', self.leftClickEvent)

        #binds right mouse click to execute the 'rightClickEvent' function
        self.staveCanvas.bind('<3>', self.rightClickEvent)


    #Takes n as the name of the note to change
    #n is the parameter of the lambda function which we change for every button
    def changeNote(self,n):
        self.currentNote = n
        print(self.currentNote)


    #Function for the 'buttonPlaceClef' to call, checks which clef is selected and places it down
    def placeClef(self):
        if self.currentClef.get() == "Treble":
            self.staveCanvas.create_image(50, 85, image=self.treble)
        else:
            self.staveCanvas.create_image(60, 72, image=self.bass)


   #Function name: leftClickEvent
   #input: current mouse position
   #purpose: places a note at the x position of the mouse and to the closest stave line in the y direction
    def leftClickEvent(self,event):

        #Because the full note and the rest are so much smaller, they need to be displaced less when being placed
        displacement = 25
        if self.currentNote == self.full or self.currentNote == self.rest: displacement = 0

        yPos = self.closestStave(event) - displacement
        
        noteID = self.staveCanvas.create_image((event.x), yPos, image=self.currentNote)

        #Have to check whether the note is a rest or not in order to be able to pitch the notes correctly i.e. the rests are silent

        #Note(ID, x position, y position, isRest, duration)
        #use a dictionary to convert the note type to a duration
        newNote = Note(noteID, event.x, yPos, self.currentNote == self.rest, self.notesDict[self.currentNote])
        self.notesList.append(newNote)
        print(self.notesList)



    #Function name: linearSearch
    #input: the item you are looking for, the list that contains the item
    #parameter: item is in the list, ID is the first item in each array item
    #purpose: searches through the list and returns the item's index
    def linearSearch(self, wantedItem, list):
        found = False
        index = 0
        #Item will always be in the array, we don't need a condition if index > len(list)
        while found != True:
            if list[index].outputID() == wantedItem:
                found = True
                return index
            else: index += 1


    #Function name: rightClickEvent
    #input: current mouse position
    #purpose: deletes whatever object the mouse is currently overlapping with
    def rightClickEvent(self,event):
        overlapping = self.staveCanvas.find_overlapping(event.x, event.y, event.x + 1, event.y + 1)
        stop = False
        index = 0

        #we reverse the list so that it deletes the newest of multiple notes if they overlap
        overlapping = overlapping[::-1]

        #we check if the mouse is overlapping with something and then delete the first user placed note
        while not stop and overlapping:
            item = overlapping[index]

            if item > 8: #8 is the last ID of the stave, any object after 8 is user placed
                self.staveCanvas.delete(item)

                index = self.linearSearch(item, self.notesList)
                del self.notesList[index]
                stop = True
            index += 1


    #Function name: closestStave
    #input: current mouse position (event in this case)
    #output: Y coordinate of the closest stave to the mouse
    def closestStave(self,event):
        mouseY=(event.y)

        #checks if the mouse is above or below the stave
        if mouseY >= 160:
            return 160
            
        elif mouseY <= 20:
            return 21
        
        #Finds the first multiple of 30 that the mouse's y position is below
        #we multiply it by 30 to get the y position of the stave line, topMiddle being the first stave line the mouse is below
        else:

            topMiddle = 30*(mouseY // 30)

            #Finds whether the mouse is closest to the top stave line, in between the stave lines or the bottom stave line and returns the closest one
            if mouseY - topMiddle <= 10:
                return topMiddle
            elif mouseY - topMiddle > 10 and mouseY - topMiddle < 20:
                return topMiddle + 15
            else:
                return topMiddle + 30



    #Function name: validateBPM
    #input: Text stored in the BPM text box
    #output: returns the tempo only if it's a valid integer
    def validateBPM(self):
        tempo = self.BPMtextBox.get("1.0",END)

        try:
            tempo = int(tempo)
            print(tempo)

            if tempo <= 0 or tempo > 300:
                messagebox.showwarning(title="Error",
                                       message="Please enter a number between 0 and 300")
            else: return tempo



        except:
            messagebox.showinfo(title="Error", 
                                message="Please enter an integer for the tempo")
        
    
    #def convertYposToPitch(Ypos):


    def createMIDI(self):
        tempo = self.validateBPM()
        if tempo:
            #taken from the midiutils example code
            MyMIDI = MIDIFile(1)
            MyMIDI.addTempo(0, 0, tempo)

            self.notesList = mergeSort(self.notesList)



            



    #creates the run function so that 'main.py' has something to call to execute
    def run(self):
        self.window.mainloop()

