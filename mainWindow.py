from tkinter import *
import time
import TAOAT

class MainWindow:

    def __init__(self):
    
        self.window = Tk()
        self.window.title("Test")
        self.window.geometry("1000x500")
        self.window.resizable (False,False)
        self.window.config(background="blue")

        if TAOAT.is_six(6):
            print(6)

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


        #List of clefs for the dropdown box
        listClef = ["Treble","Bass"]

        #loads in images of all the notes
        quarter = PhotoImage(file="images/quarter.png")
        half = PhotoImage(file="images/half.png")
        eighth = PhotoImage(file="images/eighth.png")
        full = PhotoImage(file="images/full.png")
        rest = PhotoImage(file="images/rest.png")

        #initialises the variable 'currentNote' and has it be set to the default of a quarter note
        self.currentNote = quarter

        #initialises the variable 'currentClef' and sets it to the default of treble
        currentClef = StringVar(value="Treble")

        #draw stave lines
        for i in range(0, 5):
            self.staveCanvas.create_line(20, 30 + (30 * i), 880, 30 + (30 * i), width = 3)
            self.staveCanvas.pack()

        #Draws the one vertical line at the beginning and the two at the end
        self.staveCanvas.create_line(20, 29, 20, 152, width = 3)
        self.staveCanvas.create_line(880, 29, 880, 152, width = 3)
        self.staveCanvas.create_line(870, 29, 870, 152, width = 3)


        #Create buttons for the top options bar
        #Uses the lambda function because it doesn't work if we just call changeNote(quarter) for instance
        buttonQuarter = Button(optionsCanvas, image=quarter, command=lambda n=quarter: self.changeNote(n))
        buttonQuarter.grid(column=0, row = 0, padx = 5, pady = 5)

        buttonHalf = Button(optionsCanvas, image=half, command=lambda n=half: self.changeNote(n))
        buttonHalf.grid(column = 1, row = 0 , padx = 5, pady = 5)

        buttonEighth = Button(optionsCanvas, image=eighth, command=lambda n=eighth: self.changeNote(n))
        buttonEighth.grid(column = 3, row = 0, padx = 5, pady = 5)

        buttonFull = Button(optionsCanvas, image=full, command=lambda n=full: self.changeNote(n))
        buttonFull.grid(column = 4, row = 0, padx = 5, pady = 5)

        buttonRest = Button(optionsCanvas, image=rest, command=lambda n=rest: self.changeNote(n))
        buttonRest.grid(column = 5, row = 0, padx = 5, pady = 5)


        #Creates the clef selection drop down menu
        clefDropDown = OptionMenu(optionsCanvas, currentClef, *listClef)
        clefDropDown.grid(column = 6, row = 0, padx = 20, pady = 5, sticky=E)


        #binds left mouse click to execute the 'leftClickEvent' function
        self.staveCanvas.bind('<1>', self.leftClickEvent)

        self.staveCanvas.bind('<3>', self.rightClickEvent)


    #Takes n as the name of the note to change
    #n is the parameter of the lambda function which we change for every button
    def changeNote(self,n):
        self.currentNote = n
        print(self.currentNote)




    #Places a note down evey time you click the mouse on the stave
    #x position is the mouses x position, y position is the output from closest stave to snap it
    def leftClickEvent(self,event):
        self.staveCanvas.create_image((event.x),self.closestStave(event)-25,image=self.currentNote)
        print(event.y)

    
    def rightClickEvent(self,event):
        overlapping = self.staveCanvas.find_overlapping(event.x, event.y, event.x + 1, event.y + 1)
        for item in overlapping:
            if item > 8: #8 is the last ID of the stave, any object after 8 is user placed
                self.staveCanvas.delete(item)


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
        
        #cycles through the stave lines to check which ones it's inbetween, topMiddle being the first line that the mouse is under
        #I stopped using break just to appease Sinfield
        else:
            stop = False
            currentStave = 30
            while not stop:
                if mouseY < currentStave:
                    topMiddle = currentStave - 30
                    stop = True
                else:
                    currentStave += 30

            #Finds whether the mouse is closest to the top stave line, in between the stave lines or the bottom stave line and returns the closest one
            if mouseY - topMiddle <= 10:
                return topMiddle
            elif mouseY - topMiddle > 10 and mouseY - topMiddle < 20:
                return topMiddle + 15
            else:
                return topMiddle + 30




    #creates the run function so that 'main.py' has something to call to execute
    def run(self):
        self.window.mainloop()

