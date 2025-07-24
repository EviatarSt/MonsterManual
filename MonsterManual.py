from ctypes import alignment
import tkinter as Tk
from tkinter import ttk
from tkinter import scrolledtext
from turtle import bgcolor
import json
import string
import requests
from io import BytesIO
from PIL import Image, ImageTk
import openai
from openai import OpenAI
       

class GUI_CMP:
    myRoot = None
    MonsterImageCanvas = None
    MonsterUrl = "https://www.dnd5eapi.co/api/2014/monsters"
    headers = {'Accept': 'application/json'}
    monsterListEntry = None
    monsterText = None
    encountersWidgetList = []
    manualMode = True

    def __init__(self, parent=None):
        self.myRoot = Tk.Tk()
        self.myRoot.geometry("1100x800")
        self.MonsterImageCanvas = Tk.Canvas(self.myRoot, width=402, height=402, 
                   highlightthickness=2, highlightbackground="black",
                   bg=self.myRoot.cget("bg"))
        self.MonsterImageCanvas.place(x=0, y=0)
        monsterNames = []
        button = Tk.Button(self.myRoot, text='Load', width=25, command=self.buttonClickFunc)
        button.place(x=0,y=410)
        response = requests.get(self.MonsterUrl, self.headers)
        if response.status_code == 200:
            theResults = response.json()["results"]
            monsterNames = [monster['index'] for monster in theResults]
        self.monsterListEntry = ttk.Combobox(self.myRoot, values=monsterNames, width=26,state="readonly")
        self.monsterListEntry.place(x=0, y=435)
        self.monsterListEntry.set("pick a monster")

        timesList = ["sunrise", "sunset", "night", "dusk"]
        placesList = ["in a forest", "in a dungeon", "in a corridor", "in avalley",
                      "in a desert", "on a bridge",
                      "in a cave", "on a ship", "on a mountainside", 
                      "in a graveyard", "in the snow"]


        LabelTime = Tk.Label(self.myRoot, text="time: ")
        EntryTime = ttk.Combobox(self.myRoot, values=timesList, width=8)
        LabelTime.place(x=410, y=10)
        EntryTime.place(x=450, y=10)
        EntryTime.set("irrelevant")
        self.encountersWidgetList.append({
            "widget": LabelTime,
            "place_info": LabelTime.place_info()})
        self.encountersWidgetList.append({
            "widget": EntryTime,
            "place_info": EntryTime.place_info()})

        LabelPlace = Tk.Label(self.myRoot, text="place: ")
        EntryPlace = ttk.Combobox(self.myRoot, values=placesList, width=18)
        LabelPlace.place(x=410, y=40)
        EntryPlace.place(x=450, y=40)
        self.encountersWidgetList.append({
            "widget": LabelPlace,
            "place_info": LabelPlace.place_info()})
        self.encountersWidgetList.append({
            "widget": EntryPlace,
            "place_info": EntryPlace.place_info()})

        LabelMonsterNum = Tk.Label(self.myRoot, text="Monster Num: ")
        EntryMonsterNum = ttk.Combobox(self.myRoot, values=list(range(1,6)), width=4)
        LabelMonsterNum.place(x=410, y=70)
        EntryMonsterNum.place(x=500, y=70)
        self.encountersWidgetList.append({
            "widget": LabelMonsterNum,
            "place_info": LabelMonsterNum.place_info()})
        self.encountersWidgetList.append({
            "widget": EntryMonsterNum,
            "place_info": EntryMonsterNum.place_info()})

        LabelWeapons = Tk.Label(self.myRoot, text="weapons: ")
        EntryWeapons = Tk.Entry(self.myRoot, width=20)
        LabelWeapons.place(x=410, y=100)
        EntryWeapons.place(x=470, y=100)
        EntryWeapons.insert(0, "unarmed")
        self.encountersWidgetList.append({
            "widget": LabelWeapons,
            "place_info": LabelWeapons.place_info()})
        self.encountersWidgetList.append({
            "widget": EntryWeapons,
            "place_info": EntryWeapons.place_info()})

        LabelPlaceDetails = Tk.Label(self.myRoot, text="extra details, place: ")
        EntryPlaceDetails = Tk.Text(self.myRoot, width=60, height=3)
        LabelPlaceDetails.place(x=410, y=130)
        EntryPlaceDetails.place(x=530, y=130)
        self.encountersWidgetList.append({
            "widget": LabelPlaceDetails,
            "place_info": LabelPlaceDetails.place_info()})
        self.encountersWidgetList.append({
            "widget": EntryPlaceDetails,
            "place_info": EntryPlaceDetails.place_info()})

        LabelMonsterDetails = Tk.Label(self.myRoot, text="extra details, monster: ")
        EntryMonsterDetails = Tk.Text(self.myRoot, width=60, height=3)
        LabelMonsterDetails.place(x=410, y=220)
        EntryMonsterDetails.place(x=530, y=220)
        self.encountersWidgetList.append({
            "widget": LabelMonsterDetails,
            "place_info": LabelMonsterDetails.place_info()})
        self.encountersWidgetList.append({
            "widget": EntryMonsterDetails,
            "place_info": EntryMonsterDetails.place_info()})

        self.manualModeButton = Tk.Button(self.myRoot, text='Manual Mode', width=25, command=self.ManualModeOn)
        self.manualModeButton.place(x=0, y=470)
        self.encounterModeButton = Tk.Button(self.myRoot, text='Encounter Mode', width=25, command=self.EncounterGeneratorMode)
        self.encounterModeButton.place(x=0, y=500)
        ThemonsterText = scrolledtext.ScrolledText(self.myRoot, wrap=Tk.WORD)
        ThemonsterText.place(x=410, y=10)
        self.monsterText = {
            "widget": ThemonsterText,
            "place_info": ThemonsterText.place_info()}

        with open("C:\\OAF\\Pandoras Box.txt", 'r', encoding='utf-8') as file:
            self.openAiKey = file.read()
        
        self.myRoot.mainloop()
    
    def buttonClickFunc(self):
        self.monsterText["widget"].delete('1.0', 'end')
        response = requests.get(self.MonsterUrl, self.headers)
        if response.status_code == 200:
            theMonsters = response.json()["results"]
            theMonster = [monster for monster in theMonsters if monster['index'] == self.monsterListEntry.get()][0]

            orcUrl = "https://www.dnd5eapi.co" + theMonster["url"]
            
            response = requests.get(orcUrl, self.headers)
            if response.status_code == 200:
                keys_to_exclude = {"url", "updated_at", "image", "forms", "legendary_actions", "reactions"}
                theMonster = response.json()
                orcImage = "https://www.dnd5eapi.co" + theMonster["image"]
                theMonster = {k:v for k, v in theMonster.items() if k not in keys_to_exclude}
                self.monsterText["widget"].insert(Tk.END, json.dumps(theMonster, indent=2))
                print(theMonster)
                
                client = OpenAI(api_key=self.openAiKey)

                myMessage = " ".join(["give me a 1-paragraph long description of the D&D (version 5) monster called \"",
                                    self.monsterListEntry.get(),
                "\", and another short paragraph listing natural enemies and disliked races of the monster"])
                opresponse = client.chat.completions.create(
                    model="gpt-4o",  # or "gpt-3.5-turbo"
                    messages=[
                        {"role": "user", "content": myMessage}
                        ]
                    )
                print("\n")
                print(opresponse.choices[0].message.content)
                print("\n")
                response = requests.get(orcImage)
                if response.status_code == 200:

                    coverImage = Image.open(BytesIO(response.content)).resize(size=[400, 400])
                    self.monster_image = ImageTk.PhotoImage(coverImage)
                    pictureLabel = Tk.Label(self.myRoot, image=self.monster_image)
                    pictureLabel.place(x=0,y=0)

    def ManualModeOn(self):
        for item in self.encountersWidgetList:
            item["widget"].place_forget()
        self.monsterText["widget"].place(**self.monsterText["place_info"])

    def EncounterGeneratorMode(self):
        self.monsterText["widget"].place_forget()
        for item in self.encountersWidgetList:
            item["widget"].place(**item["place_info"])

   

        
if __name__ == "__main__":
    myGui_Cmp = GUI_CMP()
