from tkinter import * 
from multiprocessing import Process, Manager
import ctypes

from Consts import *
from robots import robot
from utils import gen_map, pack_botmap
from map import Map, refresh_map






    
    
if __name__ == "__main__" :
    # Generation d'une map aléatoire
    BOTMAP = gen_map()

    # Position de départ du robot
    botmap_print = BOTMAP.copy()
    direction = [0,-1]
    pos = [SIZE-1,SIZE-1]
    botmap_print[pos[0]][pos[1]] = "W"

    # Création des variables partagées
    manager = Manager()
    shared_botmap = manager.Value(ctypes.c_char_p, pack_botmap(BOTMAP))
    shared_rotation = manager.Value(ctypes.c_char_p, "none")

    # Création du processus robot
    robotProcess = Process(target=robot, args=(pos,shared_botmap,direction,shared_rotation,))
    robotProcess.start()

    # Création de la carte avec tkinter
    WINDOW = Map()
    WINDOW.show(botmap_print)
    WINDOW.after(1000, refresh_map, WINDOW,shared_botmap,shared_rotation)
    WINDOW.mainloop()

