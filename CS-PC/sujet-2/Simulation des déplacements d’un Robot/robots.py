"""
Eliot BADINGA _ 8/06/2023
Exercice : Simulation des déplacements d’un Robot

Défini le process robot et les fonctions qu'il va utiliser.
"""
from utils import unpack_botmap, pack_botmap, print_map
from Consts import *
import time
from multiprocessing import managers
import random


#################################################################
#
# Processus robot
#
#################################################################

def robot(pos : list,shared_botmap : managers.ValueProxy,direction : list,shared_rotation : managers.ValueProxy):
    while True:
        time.sleep(2)
        print("\x1B[2J\x1B[;H")
        botmap = unpack_botmap(shared_botmap.value)
        old_pos = pos
        print("[-]Mouvement: " + control(pos,botmap,direction))
        if control(pos,botmap,direction) == "avancer":
            pos = avancer(pos,direction)
        elif control(pos,botmap,direction) == "tourner_gauche":
            direction = tourner_gauche(direction)
            shared_rotation.value = "gauche"
        elif control(pos,botmap,direction) == "tourner_droite":
            direction = tourner_droite(direction)
            shared_rotation.value = "droite"
        elif control(pos,botmap,direction) == "reculer":
            pos = reculer(pos,direction)
        else:
            print("[-] Bloqué " + control(pos,botmap,direction))
            break
        botmap[old_pos[0]][old_pos[1]] = "*"
        botmap[pos[0]][pos[1]] = "W"
        print_map(botmap)
        shared_botmap.value = pack_botmap(botmap)

def control(pos : list,botmap : list,direction : list) -> str:
    if not capteur_Top(pos,botmap,direction):
        return "avancer"
    elif not capteur_Left(pos,botmap,direction) and not capteur_Right(pos,botmap,direction):
        if random.randrange(0,2) == 0:
            return "tourner_gauche"
        else:
            return "tourner_droite"
    elif not capteur_Left(pos,botmap,direction):
        return "tourner_gauche"
    elif not capteur_Right(pos,botmap,direction):
        return "tourner_droite"
    elif not capteur_Bottom(pos,botmap,direction):
        return "reculer"

#################################################################
#
# Deplacement / Rotation du robot
#
##################################################################

def avancer(pos : list,direction : list) -> list:
    """
    Genere les nouvelles positions du robots si il avance tout droit (en tenant compte de son orientation)
    """
    if direction[1] == -1:
        new_pos = [ pos[0],pos[1]-1 ]
    elif direction[1] == 1:
        new_pos = [ pos[0],pos[1] + 1 ]
    elif direction[0] == 1:
        new_pos = [ pos[0] +1,pos[1] ]
    elif direction[0] == -1:
        new_pos = [ pos[0] -1,pos[1] ]
    return new_pos

def tourner_gauche(direction : list) -> list:
    """
    Genere la nouvelle orientation du robot si il tourne à gauche (en tenant compte de son orientation)
    """
    if direction[0] == 1:
        new_direction = [0,-1]
    elif direction[0] == -1:
        new_direction = [0,1]
    elif direction[1] == 1:
        new_direction = [1,0]
    elif direction[1] == -1:
        new_direction = [-1,0]
    return new_direction

def tourner_droite(direction : list) -> list:
    """
    Genere la nouvelle orientation du robot si il tourne à droite (en tenant compte de son orientation)
    """
    if direction[0] == 1:
        new_direction = [0,1]
    elif direction[0] == -1:
        new_direction = [0,-1]
    elif direction[1] == 1:
        new_direction = [-1,0]
    elif direction[1] == -1:
        new_direction = [1,0]
    return new_direction

def reculer(pos : list,direction : list) -> list:
    """
    Genere les nouvelles positions du robots si il recule (en tenant compte de son orientation)
    """
    if direction[1] == -1:
        new_pos = [ pos[0],pos[1]+1 ]
    elif direction[1] == 1:
        new_pos = [ pos[0],pos[1] -1 ]
    elif direction[0] == 1:
        new_pos = [ pos[0] -1,pos[1] ]
    elif direction[0] == -1:
        new_pos = [ pos[0] +1,pos[1] ]
    return new_pos

#################################################################
#
# Capteurs du robots
#
##################################################################



def capteur_Left(pos : list,botmap : list,direction : list) -> bool:
    """
    Retourne True si il y a un obstacle ou une bordure de map à gauche du robot.
    """
    if direction[1] == -1:
        new_pos = [ pos[0]-1,pos[1] ]
    elif direction[1] == 1:
        new_pos = [ pos[0]+1,pos[1] ]
    elif direction[0] == 1:
        new_pos = [ pos[0],pos[1]+1 ]
    elif direction[0] == -1:
        new_pos = [ pos[0],pos[1]-1 ]
    if new_pos[0]<0 or new_pos[1]<0 or new_pos[0] >= SIZE or new_pos[1]>= SIZE: # Sortie de la map
        return True      
    if botmap[new_pos[0]][new_pos[1]] == OBSTACLE_CHAR: # obstacle
        return True
    return False

def capteur_Right(pos : list,botmap : list,direction : list) -> bool:
    """
    Retourne True si il y a un obstacle ou une bordure de map à droite du robot.
    """
    if direction[1] == -1:
        new_pos = [ pos[0]+1,pos[1] ]
    elif direction[1] == 1:
        new_pos = [ pos[0]-1,pos[1] ]
    elif direction[0] == 1:
        new_pos = [ pos[0],pos[1]-1 ]
    elif direction[0] == -1:
        new_pos = [ pos[0],pos[1]+1 ]
    if new_pos[0]<0 or new_pos[1]<0 or new_pos[0] >= SIZE or new_pos[1]>= SIZE: # Sortie de la map
        return True      
    if botmap[new_pos[0]][new_pos[1]] == OBSTACLE_CHAR: # obstacle
        return True
    return False

def capteur_Top(pos : list,botmap : list,direction : list) -> bool:
    """
    Retourne True si il y a un obstacle ou une bordure de map en haut du robot.
    """
    new_pos = avancer(pos,direction)
    if new_pos[0]<0 or new_pos[1]<0 or new_pos[0] >= SIZE or new_pos[1]>= SIZE: # Sortie de la map
        return True      
    if botmap[new_pos[0]][new_pos[1]] == OBSTACLE_CHAR: # obstacle
        return True
    return False

def capteur_Bottom(pos : list,botmap : list,direction : list) -> bool:
    """
    Retourne True si il y a un obstacle ou une bordure de map en bas du robot.
    """
    new_pos = reculer(pos,direction)
    if new_pos[0]<0 or new_pos[1]<0 or new_pos[0] >= SIZE or new_pos[1]>= SIZE: # Sortie de la map
        return True      
    if botmap[new_pos[0]][new_pos[1]] == OBSTACLE_CHAR: # obstacle
        return True
    return False
