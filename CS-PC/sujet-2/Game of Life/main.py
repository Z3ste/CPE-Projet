from utils import pack_botmap
from controleur import controleur
from cells import cell
from map import gen_mat
import ctypes
import multiprocessing as mp
from Consts import *





if __name__ == "__main__" :
    # On genere la map
    map = gen_mat(SIZE)

    # On créé les variables partagées qui nous interessent
    operations = mp.Queue()         # Permet de push les changements d'état des cellules au controleur
    sem = mp.Semaphore(0)           # Permet de lancer le controleur une fois que toutes les cellules ont été traités
    lock = mp.Lock()                # Permet de faire patienter les cellules le temps que le controleur effectue ses opérations

    manager = mp.Manager()          # Permet de partager avec les cells et le controlleur la map
    shared_map = manager.Value(ctypes.c_char_p, pack_botmap(map))

    # Generations des processus
    cells = []
    for x in range(SIZE):
        for y in range(SIZE):
            cells.append(mp.Process(target=cell, args=(shared_map,[x,y],operations,sem,lock,)))
    contr = mp.Process(target=controleur, args=(shared_map,operations,sem,SIZE,lock,))
    contr.start()
    for i in range(SIZE**2):
            cells[i].start()

    while True:
        pass