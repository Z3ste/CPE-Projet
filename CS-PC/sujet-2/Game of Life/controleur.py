"""
Eliot BADINGA _ 8/06/2023
Exercice : Game of Life

Défini le process controleur
"""

import time
import multiprocessing as mp
from utils import unpack_botmap, pack_botmap
from map import print_map

def controleur(shared_map : mp.Manager, operations : mp.Queue, sem : mp.Semaphore, size :int, lock : mp.Lock):
    """
    Le controleur attend que les cellules aient effectué leurs opérations (via le semaphore sem), affiche la map,
    verouille le mutex lock et actualise les données de la carte. Il deverouille ensuite le mutex lock, ce qui permet
    aux cellules de faire leurs calculs.
    """
    counter = 0
    while True:
        counter += 1
        for i in range(size**2-1):
            sem.acquire()
        print("\x1B[2J\x1B[;H")
        print(f"[-]Generation {counter} is ok")  
        map =  unpack_botmap(shared_map.value)
        print_map(map)
        lock.acquire()
        while not operations.empty():
            op = operations.get()
            x = int(op.split("-")[0])
            y = int(op.split("-")[1])
            v = int(op.split("-")[2])
            map[x][y] = v
        shared_map.value = pack_botmap(map)

        lock.release()
        time.sleep(1)
     