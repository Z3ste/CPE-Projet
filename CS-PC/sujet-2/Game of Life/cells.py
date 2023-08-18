"""
Eliot BADINGA _ 8/06/2023
Exercice : Game of Life

Défini le process cell et les fonctions qu'il va utiliser
"""
import time
import multiprocessing as mp
from utils import unpack_botmap

def get_number_voisin_alive(map : list, pos : list) -> int:
    """
    Fourni le nombre de cellule en vie à coté d'une cellule de position `pos`
    """
    n = 0
    for x in range(-1,2):
        for y in range(-1,2):
            if pos[0] +x < 0 or pos[1] +y < 0 or pos[0] +x > len(map)-1 or pos[1] +y > len(map)-1: pass
            elif x == 0 and y == 0: pass
            elif map[pos[0]+x][pos[1]+y] == 1: n+=1
    return n

def cell(shared_map : mp.Manager, pos : list, operations : mp.Queue, sem : mp.Semaphore, lock : mp.Lock):
    """
    Chaque cellule a son propre processus cellule. Ce dernier récupère le nombre de cellule en vie à coté d'elle,
    en conclue si elle est en vie à la génération t+1, envoie son résultat dans la queue operation sous la forme
    `<x>-<y>-<en_vie>`, libere une ressource dans sem et attend que le mutex lock soit déverouillé.
    """
    while True:
        map =  unpack_botmap(shared_map.value)
        n = get_number_voisin_alive(map,pos)
        isAlive = map[pos[0]][pos[1]] == 1
        if n < 2 and isAlive:
            # Any live cell with fewer than two live neighbours dies, as if caused by under-population
            map[pos[0]][pos[1]] = 0
        elif (n ==2 or n == 3) and isAlive:
            # Any live cell with two or three live neighbours lives on to the next generation.
            map[pos[0]][pos[1]] = 1
        elif (n > 3 and n != 8) and isAlive:
            # Any live cell with more than three live neighbours dies, as if by overcrowding
            map[pos[0]][pos[1]] = 0
        elif n == 3 and not isAlive:
            # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            map[pos[0]][pos[1]] = 1
        operations.put(f"{pos[0]}-{pos[1]}-{map[pos[0]][pos[1]]}")

        sem.release()
        time.sleep(2)
        lock.acquire()
        lock.release()
