
"""
Eliot BADINGA _ 8/06/2023
Exercice : Game of Life

Défini toutes les fonctions concernant la génération et l'affichage de la map.
"""
import random
from colorama import Fore

def is_alive() -> bool:
    """
    Renvoie True avec une probabilité d'une chance sur 2, False sinon
    """
    if random.randrange(0,2) == 0: return True
    else: return False

def gen_mat(size) -> list:
    """
    Genere une carte sous forme de liste dans une liste avec des cellules vivantes (=1) et des 
    cellules mortes (=0)
    """
    map  = []
    for x in range(0,size):
        tmp_map = []
        for y in range(0,size):
            obstacle = 1 if is_alive() else 0
            tmp_map.append(obstacle)
        map.append(tmp_map)
    return map

def print_map(map : list):
    """
    Affiche le carte dans le terminal
    """
    size = len(map)
    print(f"{Fore.CYAN}▁{Fore.WHITE}"*(size*4+2))
    for y in range(0,size):
        print("▐",end='')
        for x in range(0,size):
            if map[x][y] == 1:
                print(" ✅ ",end='')
            else:
                print(" ❌ ",end='')
        print(f"{Fore.CYAN}▌{Fore.WHITE}")
    print(f"{Fore.CYAN}▔{Fore.WHITE}"*(size*4+2))