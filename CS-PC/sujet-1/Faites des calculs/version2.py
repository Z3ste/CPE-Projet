'''
Eliot BADINGA _ 5/06/2023
Exercice : faites des calcul

Version 2: M demandeurs, N calculateurs
            M queue de demande, M queue de réponse (2*M queue au total)
'''
import multiprocessing as mp
import sys , time, random
from colorama import Fore, Back, Style
import random, string


N = 2 # nombre de calculateur
M = 3 # nombre de demandeur

def get_random_operation() -> str:
    """
    Genere une operation aléatoire (parfois invalide)
    """
    op = random.choice(["-","+","/","*","$$"])  # le $$ pour simuler une opération invalide
    n1 = random.randrange(1,200)
    n2 = random.randrange(1,200)
    return f"{n1} {op} {n2}"


def demandeur(index: int, asks : mp.Queue, answers: mp.Queue) -> None:
    """
    Genere des opérations aléatoires toutes les secondes et les envoies dans la queue `asks[index]`

    """
    while True:
        time.sleep(random.randrange(0,10)/10)
        op = get_random_operation()
        print(f"{Fore.CYAN}[-]{Fore.WHITE} : Demandeur n°{index} '{op}'")
        asks[index].put(op)
        while answers[index].empty(): pass # attend la réponse
        res = answers[index].get()
        print(f"{Fore.CYAN}[-]{Fore.WHITE} : Demandeur n°{index}: resultat '{op}={res}'")
    
def receveur(index, asks : list ,answsers : list) -> None:
    """
    Reçoit des opérations dans les queue stocké dans la liste `asks`, 
    les évalue (check si elles sont valides), et envoie le résultat dans la queue associé `answsers[index]`
    """
    while True:
        for i in range(0,len(asks)):
            if not asks[i].empty():
                op = asks[i].get()
                try:                # Traitement des calculs incorrect
                    res = eval(op)
                    print(f"{Fore.GREEN}[-]{Fore.WHITE} : Receveur n°{index} '{op}={res}'")
                except:             # Si le calcul est incorrect, le resultat est None
                    print(f"{Fore.GREEN}[-]{Fore.WHITE} : Receveur n°{index} {Fore.RED}Is invalid operation '{op}'{Fore.WHITE}")
                    res = None
                answsers[i].put(res)
            
if __name__ == "__main__" :
    asks = []
    answers = []
    demandeur_procs, receveur_procs = [], []
    for i in range(M):
        asks.append(mp.Queue()); answers.append(mp.Queue())

    for i in range(M):
        demandeur_procs.append(mp.Process(target = demandeur , args = (i,asks,answers,)))

    for i in range(N):
        receveur_procs.append(mp.Process(target = receveur , args = (i,asks,answers,)))

    for proc in demandeur_procs: proc.start()
    for proc in receveur_procs: proc.start()