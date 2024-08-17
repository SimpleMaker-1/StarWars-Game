import requests
import random
from PIL import Image, ImageTk
from io import BytesIO
from customtkinter import *
import csv
import os
from pygame import mixer

abspath = os.path.abspath(__file__) #stupid python directory bullcrap, im angry
dname = os.path.dirname(abspath)
os.chdir(dname)

mixer.init() #MUSIC
mixer.music.load(os.path.join("Music.mp3"))
mixer.music.play(loops=-1)

# Star Wars episodes and other initial variables
episodes = ["The Phantom Menace","Attack of the Clones","Revenge of the Sith","A New Hope","The Empire Strikes Back","Return of the Jedi"]
listOfStarShips = []
starShipImg = []
numbers = list(range(4))  # List of unique random numbers
random.shuffle(numbers)
randomIndex = None
app = CTk()
app.geometry("1280x720")
won = False

def fillLists():
    with open("starship.csv", mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            listOfStarShips.append(tuple(row))
            response = requests.get(row[0])
            imgData = BytesIO(response.content)
            pilImg = Image.open(imgData)
            starShipImg.append(ImageTk.PhotoImage(pilImg))

def getNextNum():
    global randomIndex
    if numbers.__len__() != 0:
        randomIndex = numbers.pop()

def CheckAnswer():
    if dropdownbox.get() == listOfStarShips[randomIndex][1] and not won:
        getNextNum()
        CorrectGuess()

def CorrectGuess():
    print(numbers)
    if numbers.__len__() != 0:
        image_label.configure(image=starShipImg[randomIndex])  # Update the displayed image
        image_label.image = starShipImg[randomIndex]  # Keep a reference to the new image
    else:
        print("hello")
        global won
        won = True
        victory_label.configure(text="You Win!", font=("Comic Sans MS", 100))
        image_label.destroy()
        dropdownbox.destroy()
        btn.destroy()

fillLists()
getNextNum()

victory_label = CTkLabel(master=app, text="", font=("Comic Sans MS", 100))
victory_label.place(relx=0.5, rely=0.5, anchor="center")

image_label = CTkLabel(master=app, text="", image=starShipImg[randomIndex])
image_label.place(relx=0.5, rely=0.5, anchor="center")

dropdownbox = CTkComboBox(master=app, values=episodes, state="readonly")
dropdownbox.place(relx=0.5, rely=0.8, anchor="center")

btn = CTkButton(master=app, text="Submit", command=CheckAnswer)
btn.place(relx=0.5, rely=0.84, anchor="center")

app.mainloop()
