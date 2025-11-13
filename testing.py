import tkinter as tk
import random

root = tk.Tk()
canvas = tk.Canvas(root, background="black", width=400, height=400)
canvas.pack(fill="both", expand=True)

for i in range(20):
    x = random.randint(0,380)
    y = random.randint(0,380)
    color = random.choice(['red', 'orange', 'yellow', 'green', 'blue'])

    canvas.create_rectangle(x, y, x+20, y+20, outline=color)

def  highlight_overlapping(event):
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)

    overlapping = canvas.find_overlapping(x, y, x+1, y+1)
    for item in overlapping:
        canvas.itemconfigure(item, fill="white")

canvas.bind("<Motion>", highlight_overlapping)
root.mainloop()