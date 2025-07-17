from ctypes import alignment
import tkinter as Tk
from tkinter import ttk
from turtle import bgcolor
import string
import requests
from io import BytesIO
from PIL import Image, ImageTk



class GUI_CMP:
    myRoot = None
    MonsterImageCanvas = None
    MonsterUrl = "https://www.dnd5eapi.co/api/2014/monsters"
    headers = {'Accept': 'application/json'}
    monsterListEntry = None
    def __init__(self, parent=None):
        self.myRoot = Tk.Tk()
        self.myRoot.geometry("800x800")
        self.MonsterImageCanvas = Tk.Canvas(self.myRoot, width=402, height=402, 
                   highlightthickness=2, highlightbackground="black",
                   bg=self.myRoot.cget("bg"))
        self.MonsterImageCanvas.place(x=0, y=0)
        monsterNames = []
        button = Tk.Button(self.myRoot, text='Load', width=25, command=self.buttonClickFunc)
        button.place(x=0,y=405)
        response = requests.get(self.MonsterUrl, self.headers)
        if response.status_code == 200:
            theResults = response.json()["results"]
            monsterNames = [monster['index'] for monster in theResults]
        self.monsterListEntry = ttk.Combobox(self.myRoot, values=monsterNames, width=26)
        self.monsterListEntry.place(x=0, y=430)
        self.monsterListEntry.set("pick a monster")

        self.myRoot.mainloop()
    
    def buttonClickFunc(self):
        response = requests.get(self.MonsterUrl, self.headers)
        if response.status_code == 200:
            theMonsters = response.json()["results"]
            theOrc = [monster for monster in theMonsters if monster['index'] == self.monsterListEntry.get()][0]

            orcUrl = "https://www.dnd5eapi.co" + theOrc["url"]
            response = requests.get(orcUrl, self.headers)
            if response.status_code == 200:
                theOrc = response.json()
                print(theOrc)
                orcImage = "https://www.dnd5eapi.co" + theOrc["image"]
                response = requests.get(orcImage)
                if response.status_code == 200:
                    print("got image!")
                    coverImage = Image.open(BytesIO(response.content)).resize(size=[400, 400])
                    self.monster_image = ImageTk.PhotoImage(coverImage)
                    pictureLabel = Tk.Label(self.myRoot, image=self.monster_image)
                    pictureLabel.place(x=0,y=0)
            print("got here")
   

        
if __name__ == "__main__":
    myGui_Cmp = GUI_CMP()
