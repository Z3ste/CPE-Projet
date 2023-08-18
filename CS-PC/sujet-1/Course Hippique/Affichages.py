'''
Eliot BADINGA - Rami MESSEOUDI _ 5/06/2023
III-A Exercice : Course Hippique

Toutes les fonctions d'affichages utilisées par notre programme
'''

from Consts import *


def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : 
    print(BK_GREEN + "\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig+1) + ";" + str(col) + "f",end='')

def print_ligne(lig, data, col=0): 
    print(f"\033[{lig};{col}f{data}",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='') # Un exemple !