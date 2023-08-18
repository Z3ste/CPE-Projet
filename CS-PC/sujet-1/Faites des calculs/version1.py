'''
Eliot BADINGA _ 5/06/2023
Exercice : faites des calcul

Version 1 : 
    1 demandeur, N calculateur
    1 queue
'''
import multiprocessing as mp
import time, random
from colorama import Fore
import random


N = 10 # nombre de calculateur


def get_random_operation() -> str:
    """
    Genere une operation aléatoire (parfois invalide)
    """
    op = random.choice(["-","+","/","*","$$"])  # le $$ pour simuler une opération invalide
    n1 = random.randrange(1,200)
    n2 = random.randrange(1,200)
    return f"{n1} {op} {n2}"


def demandeur(ask : mp.Queue, answer : mp.Queue) -> None:
    """
    Genere des opérations aléatoires toutes les secondes et les envoies dans la queue `ask`

    """
    while True:
        time.sleep(1)
        op = get_random_operation()
        print(f"{Fore.CYAN}[-]{Fore.WHITE} : Demandeur '{op}'")
        ask.put(op)
        while answer.empty(): pass # attend la réponse
        res = answer.get()
        print(f"{Fore.CYAN}[-]{Fore.WHITE} : Demandeur: resultat '{op}={res}'\n")
        
def receveur(ask : mp.Queue ,answser : mp.Queue) -> None:
    """
    Reçoit des opérations dans la queue `ask`, les évalue (check si elles sont valides), et envoie le résultat dans la queue
    `answser`
    """
    while True:
        if not ask.empty():
            op = ask.get()
            try:                # Traitement des calculs incorrect
                res = eval(op)
                print(f"{Fore.GREEN}[-]{Fore.WHITE} : Receveur '{op}={res}'")
            except:             # Si le calcul est incorrect, le resultat est None
                print(f"{Fore.GREEN}[-]{Fore.WHITE} : Receveur {Fore.RED}Is invalid operation '{op}'{Fore.WHITE}")
                res = None
            answser.put(res)
            
if __name__ == "__main__" :
    ask, answer = mp.Queue(), mp.Queue()
    demandeur_proc = mp.Process(target = demandeur , args = (ask,answer,))
    receveur_procs = []
    for i in range(N):
        receveur_procs.append(mp.Process(target = receveur , args = (ask,answer,)))

    demandeur_proc.start()
    for i in range(N): receveur_procs[i].start()