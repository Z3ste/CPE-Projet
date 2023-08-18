"""
Eliot BADINGA _ 8/06/2023
Exercice : Simulation des déplacements d’un Robot

Défini tout ce qui concerne l'affichage graphique du programme dans tkinter.
"""
from tkinter import * 
from Consts import *
from utils import unpack_botmap
from multiprocessing import managers
class Map(Tk):
    def __init__(self):
        super().__init__()
        self.title("BotMap")
        self.obstacle_img   = PhotoImage(master=self,file="img/pneu-50x50.png")
        self.step_img       = PhotoImage(master=self,file="img/wall-500x500.png")
        self.bot_img       = PhotoImage(master=self,file="img/wall-e-50x50_y_-1.png")
        self.geometry("800x800")
        self.frame = Frame(self,bg="black")
        self.orientation = "y_-1"
        self.robot = None
    def show(self, botmap : list):
        """
        Affiche la carte / obstacles
        """
        self.botmap= botmap
        for x in range(SIZE):
            for y in range(SIZE):
                item_canv = Canvas(self.frame, width = 50, height = 50, bg = 'black')
                if self.botmap[x][y] == "*":
                    img = self.step_img
                elif self.botmap[x][y] == OBSTACLE_CHAR:
                    img = self.obstacle_img
                elif self.botmap[x][y] == "W":
                    img = self.bot_img 
                item_canv.create_image(25, 25,image = img)
                item_canv.image = img
                
                if self.botmap[x][y] == "W":
                    self.robot = item_canv
                    self.robot.grid(column=x, row=y)
                else:
                    item_canv.grid(column=x, row=y)
        self.frame.pack(side="top", expand=True, fill="both")
    
    def refresh(self,pos : list):
        """
        Change l'emplacement du robot sur la carte
        """
        self.robot.grid(column=pos[0], row=pos[1])
        
    def rotate(self,rotation : str):
        """
        Effectue une rotation du robot
        """
        self.robot.delete('all')
        if self.orientation == "y_-1" and rotation =="gauche":
            self.orientation = "x_-1"
        elif self.orientation == "y_-1" and rotation =="droite":
            self.orientation = "x_+1"
        elif self.orientation == "y_+1" and rotation =="gauche":
            self.orientation = "x_+1"
        elif self.orientation == "y_+1" and rotation =="droite":
            self.orientation = "x_-1"
        elif self.orientation == "x_-1" and rotation =="gauche":
            self.orientation = "y_+1"
        elif self.orientation == "x_-1" and rotation =="droite":
            self.orientation = "y_-1"
        elif self.orientation == "x_+1" and rotation =="gauche":
            self.orientation = "y_-1"
        elif self.orientation == "x_+1" and rotation =="droite":
            self.orientation = "y_+1"
        self.bot_img = PhotoImage(master=self,file=f"img/wall-e-50x50_{self.orientation}.png")
        self.robot = Canvas(self.frame, width = 50, height = 50, bg = 'black')
        self.robot.create_image(25, 25,image = self.bot_img)
        self.robot.img = self.bot_img


    def reset(self):
        """
        Detruit la frame
        """
        # destroy all widgets from frameshared_rotation
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.pack_forget()

def refresh_map(window : Map,shared_botmap : managers.ValueProxy,shared_rotation : managers.ValueProxy):
    botmap = unpack_botmap(shared_botmap.value)
    if shared_rotation.value != "none":
        window.rotate(shared_rotation.value)
        shared_rotation.value = "none"
    for x in range(SIZE):
        for y in range(SIZE):
            if botmap[x][y] == "W":
                window.refresh([x,y])
    window.after(1000, refresh_map, window,shared_botmap,shared_rotation)