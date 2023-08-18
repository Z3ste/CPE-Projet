"""
Eliot BADINGA _ 8/06/2023
Exercice : Simulation des déplacements d’un Robot

Défini des fonctions diverses utilisées par le programme.
"""
import pickle
import base64
import random
from Consts import *


def pack_botmap(botmap : list) -> str:
    """
    Permet de transformer une liste en une chaine de caractere
    """
    return base64.b64encode(pickle.dumps(botmap)).decode()

def unpack_botmap(botmap: str) -> list:
    """
    Permet de transformer une chaine de caractère en une liste
    """
    return pickle.loads(base64.b64decode(botmap))

def get_obstacle() -> bool:
    """
    Renvoie True avec une probabilité d'une chance sur 10, False sinon
    """
    if random.randrange(0,10) == 0: return True
    else: return False
def gen_map() -> list:
    """
    Genere une carte sous forme de liste dans une liste avec des obstacles disposés aléatoirement.
    Un '*' est une case vide, un '@' est une case avec un obstacle
    """
    map  = []
    for x in range(0,SIZE):
        tmp_map = []
        for y in range(0,SIZE):
            obstacle = OBSTACLE_CHAR if get_obstacle() else "*"
            tmp_map.append(obstacle)
        map.append(tmp_map)
    return map

def print_map(map : list):
    """
    Affiche le carte dans le terminal
    """
    print("▁"*SIZE*3)
    for y in range(0,SIZE):
        print("▐",end='')
        for x in range(0,SIZE):
            print(" " + map[x][y] + " ",end='')
        print("▌")
    print("▁"*SIZE*3)