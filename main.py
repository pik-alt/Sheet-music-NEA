from tkinter import *
window = Tk()
window.title("Test")
window.geometry("1000x500")
window.resizable (True,True)
window.config(background="blue")

#Setting up the two main frames for the UI, one for the top bar (optionsFrame) and one for the main stave (staveFrame)
optionsFrame = Frame(window)
optionsFrame.grid(row = 0, column = 0, padx = 50, pady = 30, columnspan = 2)

staveFrame = Frame(window)
staveFrame.grid(row = 1, column = 0, padx = 50, pady = 30, columnspan = 2)


#Creates the two canvasas to be able to import images onto them
#Currently very different colours just so I can see what I'm doing
optionsCanvas = Canvas(optionsFrame, width = 930, height = 100)
optionsCanvas.config(bg="green")
optionsCanvas.pack()

staveCanvas = Canvas(staveFrame, width = 900, height = 200)
staveCanvas.config(bg="red")


#load in image of the quarter note
quarter = PhotoImage(file="quarter2.png")


#draw stave lines
for i in range(0, 5):
    staveCanvas.create_line(20, 30 + (30 * i), 880, 30 + (30 * i), width = 3)
    staveCanvas.pack()
    
#Draws the one vertical line at the beginning and the two at the end
staveCanvas.create_line(20, 29, 20, 152, width = 3)
staveCanvas.create_line(880, 29, 880, 152, width = 3)
staveCanvas.create_line(870, 29, 870, 152, width = 3)


optionsCanvas.create_rectangle(30, 50, 60, 100, fill="green")
optionsCanvas.create_image(30, 50, image=quarter)


def optionsClick(event):
    overlapping = optionsCanvas.find_overlapping(event.x, event.y, event.x + 1, event.y + 1)
    optionsCanvas.itemconfig(overlapping, fill="red")



def leftClickEvent(event):
    staveCanvas.create_image((event.x),closestStave(event)-25,image=quarter)
    print(event.y)


def closestStave(event):
    mouseY=(event.y)

    #checks if the mouse is above or below the stave
    if mouseY > 150:
        return 150
    elif mouseY < 30:
        return 30
    
    #cycles through the stave lines to check which ones it's inbetween, topMiddle being the first line that the mouse is under
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


staveCanvas.bind('<1>', leftClickEvent)
optionsCanvas.bind('<1>', optionsClick)
window.mainloop()

