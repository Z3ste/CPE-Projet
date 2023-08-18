import multiprocessing as mp
import sys , time, random
from colorama import Fore, Back, Style
import random, string

N = 4
RESSOURCES = (4, 3, 5, 2)
N_RESSOURCE_MAX = 8
PROCS = []

COLOR = [Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.BLUE, Fore.YELLOW]

def proc(index,ressource, sem, sem_ressource) -> None:
    # demander k ressources
    print(f"{COLOR[index]}[-] Processus n°{index}{Fore.WHITE} demande {ressource} ressource(s)")
    # utiliser ressources
    demander(sem,ressource,sem_ressource)
    print(f"{COLOR[index]}[-] Processus n°{index}{Fore.WHITE} utilise {ressource} ressource(s)")
    time.sleep(0.3)
    # rendre k ressources
    print(f"{COLOR[index]}[-] Processus n°{index}{Fore.WHITE} rend {ressource} ressource(s)")
    for i in range(ressource):
        sem_ressource.release()
    sem.release()
    return None

def demander(sem,ressource,sem_ressource) -> bool:
    sem.acquire()
    for i in range(ressource):
        sem_ressource.acquire()
    

def controlleur(sem_ressource,sem, n_ressource_max):
    while True:
        if not (0 <= sem_ressource.get_value() <= n_ressource_max):
            print(f"{Fore.RED}[-] Controlleur {Fore.WHITE} Probleme au niveau des ressources :{sem_ressource._Semaphore__value}")
            sem.aquire()
            time.sleep(0.2)

if __name__ == "__main__" :
    sem = mp.Semaphore(1)
    sem_ressource = mp.Semaphore(N_RESSOURCE_MAX)
    for i in range(N):
        PROCS.append(mp.Process(target = proc , args = (i,RESSOURCES[i],sem,sem_ressource,)))
        PROCS[i].start()
    controller= mp.Process(target = controlleur , args = (sem_ressource,sem,N_RESSOURCE_MAX,))
    controller.start()