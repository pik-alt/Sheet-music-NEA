#pip install MIDIUtil

from tkinter import *
from tkinter import messagebox
import TAOAT
from midiutil import *
from noteclass import Note
from sorts import mergeSort
import subprocess, os, platform
import math


class SheetMusic:

    def __init__(self):
    
        self.window = Tk()
        self.window.title("Test")
        self.window.geometry("1000x500")
        self.window.resizable (False,False)
        self.window.config(background="darkgray")

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
        optionsCanvas.config(bg="lightgray")
        optionsCanvas.pack()

        self.staveCanvas = Canvas(staveFrame, width = 900, height = 200)
        self.staveCanvas.config(bg="white")


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

        #sets up ClefID and has a treble clef placed down by default
        self.clefID = self.staveCanvas.create_image(50, 85, image=self.treble)


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


        #buttonGenerateMusic = Button(optionsCanvas, text="Generate\nMIDI file")
        buttonGenerateMusic = Button(optionsCanvas, text="Generate\nMIDI file",command=self.createMIDI)
        buttonGenerateMusic.grid(column = 9, row = 0, padx = 100, pady = 5)


        buttonDeleteAll = Button(optionsCanvas, text = "Delete all\n notes", command=self.deleteAll)

        #Dictionary to translate from the note pointers generated by TKInter to their value in 4/4
        self.notesDict = {
            self.quarter : 1,
            self.half    : 2,
            self.eighth  : 0.5,
            self.full    : 4,
            self.rest    : 1 
        }


        #Dictionary to convert from note Y values to their midi note number
        #because the midi specification includes sharps while my software does not,
        #there is no function to go from one to the other so I have to use a dictionary
        self.trebleYposDict = {
            135: 50, #D
            125: 52, #E
            110: 53, #F
            95 : 55, #G
            80 : 57, #A
            65 : 59, #B
            50 : 60, #C
            35 : 62, #D
            20 : 64, #E
            5  : 65, #F
            -4 : 67  #G
        }

        self.bassYposDict = {
            135: 29, #F
            125: 31, #G
            110: 33, #A
            95 : 35, #B
            80 : 36, #C
            65 : 38, #D
            50 : 40, #E
            35 : 41, #F
            20 : 43, #G
            5  : 45, #A
            -4 : 47  #B
        }


        #binds left mouse click to execute the 'leftClickEvent' function
        self.staveCanvas.bind('<1>', self.leftClickEvent)

        #binds right mouse click to execute the 'rightClickEvent' function
        self.staveCanvas.bind('<3>', self.rightClickEvent)


    def deleteAll(self):
        objectList = self.staveCanvas.find_all()
        for i in range(0, len(objectList)):

            try:
                ID = objectList[i].outputID()
                self.staveCanvas.delete(ID)
            except:
                continue

    #Takes n as the name of the note to change
    #n is the parameter of the lambda function which we change for every button
    def changeNote(self,n):
        self.currentNote = n
        print(self.currentNote)

    #Function name: placeClef
    #input: none, activated by pressing the "place clef" button
    #purpose: deletes the current clef (if there is one) and places down the new one
    def placeClef(self):

        deleted = False
        index = 0
        objectList = self.staveCanvas.find_all() #returns every object within the canvas

        #linear search to sort through the canvas to find the object which matches the clefID and deletes it
        while not deleted:
            if objectList[index] == self.clefID:
                self.staveCanvas.delete(objectList[index])
                deleted = True
            else:
                index += 1
             
        #draws the current clef based on the value in the textbox
        if self.currentClef.get() == "Treble":
            self.clefID = self.staveCanvas.create_image(50, 85, image=self.treble)
        else:
            self.clefID = self.staveCanvas.create_image(60, 72, image=self.bass)


   #Function name: leftClickEvent
   #input: current mouse position
   #purpose: places a note at the x position of the mouse and to the closest stave line in the y direction
    def leftClickEvent(self,event):

        #Because the full note and the rest are so much smaller, they need to be displaced less when being placed
        displacement = 25
        if self.currentNote == self.full or self.currentNote == self.rest: displacement = 0
        yPos = self.closestStave(event) - displacement
        xPos = self.closestX(event)

        print(xPos)
        noteID = self.staveCanvas.create_image(xPos, yPos, image=self.currentNote)

        #Note(ID, x position, y position, isRest, duration)
        #use a dictionary to convert the note type to a duration
        newNote = Note(noteID, xPos, yPos, self.currentNote == self.rest, self.notesDict[self.currentNote])
        self.notesList.append(newNote)






    #Function name: linearSearch
    #input: the item you are looking for, the list that contains the item
    #parameter: item is in the list, item is an object with the .outputID() function
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
        while not stop and overlapping and index < len(overlapping):
            item = overlapping[index]

            if item > 8 and item != self.clefID: #8 is the last ID of the stave, any object after 8 is user placed
                self.staveCanvas.delete(item)    #we also don't want to delete the clefs

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


        topMiddle = 30*(mouseY // 30)

        #Finds whether the mouse is closest to the top stave line, in between the stave lines or the bottom stave line and returns the closest one
        if mouseY - topMiddle <= 10:
            return topMiddle
        elif mouseY - topMiddle > 10 and mouseY - topMiddle < 20:
            return topMiddle + 15
        else:
            return topMiddle + 30



    #Function name: closestX
    #Input: mouse position
    #output: the nearest valid x position to the mouse
    #purpose: used to snap the note to certain x positions
    def closestX(self, event):
        mouseX = (event.x)
        
        #checks if the mouse is too far to the left or right
        if mouseX < 80: return 80
        elif mouseX > 840: return 840


        middleLeft = 40*(mouseX // 40)

        if mouseX - middleLeft <= 20: return middleLeft
        else: return middleLeft + 40




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
        

    def totalElements(self, list):
        return sum(len(l) for l in list)


    #fuck this algorithm oh my god this sucks so much why the fuck do i have to finish this jesus christ
    #this is the worst thing i've ever written nothing here makes sense oh my god
    #how the hell am i even gonna write about this on my nea
    def notesXtoSameList(self, notesList):
        listOfGroupedNotes = []
        
        #runs while there's still notes to be added onto the new list
        while len(notesList[0])!= 0:
            stop = False

            tempIndex = 0
            while not stop and tempIndex < len(notesList[0])-1: 

                #checks if two notes next to eachother in the list share the x position
                if notesList[0][tempIndex].outputX_POS() == notesList[0][tempIndex+1].outputX_POS():
                    tempIndex += 1

                else:
                    stop = True

            #tempIndex should finally be 1 more than the last shared xPos item in the list for the loop coming up
            tempIndex += 1
                    
            
            tempNotesList = []

            for j in range(0, tempIndex):
                tempNotesList.append(notesList[0][0])
                del notesList[0][0]

            listOfGroupedNotes.append(tempNotesList)

        return listOfGroupedNotes

    #Function name: createMIDI
    #input: none, activated by pressing the associated button
    #output: creates a file called "SHEET_MUSIC.midi" that then plays automatically
    def createMIDI(self):

        #sets up time to be 0 so that the track plays from the beginning 
        #and also to have something to innumerate upon
        time = 0
        tempo = self.validateBPM()
        if tempo:

            #taken from the midiutils example code
            myMIDI = MIDIFile(11)
            myMIDI.addTempo(0, time, tempo)

            #sorts the note objects stored in notesList by their x position
            sortedNotesList = mergeSort(self.notesList)
            sortedNotesList = self.notesXtoSameList(sortedNotesList)


            #changes which dictionary and by extension what notes to play based on the current clef
            if self.currentClef.get() == "Treble":
                pitchDict = self.trebleYposDict
            else:
                pitchDict = self.bassYposDict

            totalJump = 0

            for i in range(0, len(sortedNotesList)):

                for j in range(0,len(sortedNotesList[i])):
                    
                    #converts the notes Y position to MIDI pitch using the dictionary
                    activeNote = sortedNotesList[i][j]


                    #undos the Y position displacement of the full note and rest, caused by them being so much smaller
                    displacementKey = 0

                    if activeNote.outputDURATION() == 4 or activeNote.outputIsRest():
                        displacementKey = 25

                    pitch = pitchDict[activeNote.outputY_POS() - displacementKey]
                    

                    duration = activeNote.outputDURATION()

                    volume = 100

                    #makes the volume of the note 0 if it's a rest
                    if activeNote.outputIsRest(): volume = 0

                    #MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)
                    myMIDI.addNote(j, 0, pitch, time + i + totalJump, 2*duration, volume)

                    #makes it so that if you place down a note of length n, the next n times on the midi file
                    #are filled with silence as to let the note play out to its full extent, this pushes all the
                    #other notes forward, and so we add totalJump to the addNote function always, to keep in sync with all the other notes
                totalJump = totalJump + math.floor(activeNote.outputDURATION())


            with open("SHEET_MUSIC.midi", "wb") as output_file:
                    myMIDI.writeFile(output_file)

            messagebox.showinfo(title="Success!",
                                    message="Created the midi file successfully")
            

            #plays the generated file automatically based on your OS
            if platform.system() == 'Windows':
                os.startfile("SHEET_MUSIC.midi")
            else:
                subprocess.run("SHEET_MUSIC.midi", check=True)



    #creates the run function so that 'main.py' has something to call to execute
    def run(self):
        self.window.mainloop()

