'''
Eliot BADINGA - Rami MESSEOUDI _ 5/06/2023
III-B Exercice : faites des calcul

Version 2 : M demandeurs, N calculateurs
            1 queue de demande, 1 queue de reponse

Ajouter une variante où au lieu d’une expression, le demandeur communique une fonction
particulière à appliquer (lambda function) (2 points).
'''
import multiprocessing as mp
import sys , time, random
from colorama import Fore, Back, Style
import random, string


N = 10 # nombre de calculateur
M = 10 # nombre de demandeur

def get_random_operation() -> str:
    """
    Genere une operation aléatoire (parfois invalide)
    """
    op = random.choice(["-","+","/","*","$$"])  # le $$ pour simuler une opération invalide
    n1 = random.randrange(1,200)
    n2 = random.randrange(1,200)
    return f"lambda x: {n1} {op} {n2} + x**2"   # Fonction choisis arbitrairement 


def demandeur(index: int, ask : mp.Queue, answer: mp.Queue) -> None:
    """
    Genere des opérations aléatoires toutes les secondes et les envoies dans la queue `asks[index]`

    """
    while True:
        time.sleep(random.randrange(0,10)/10) # Genere un pause d'un temps aléatoire
        op = get_random_operation()
        print(f"{Fore.CYAN}[-]{Fore.WHITE} : Demandeur n°{index} '{op}'")
        ask.put([index,op])

        isGood = False              # Recupere le résultat de l'opération
        while not isGood:           # Recupere un resultat dans la queue
            id, res = answer.get()  # Verifie que l'index de la réponse est celle du demandeur
            if id == index:         # Si oui, sort de la boucle et affiche le résultat
                isGood = True       # Sinon, reinjecte le résultat de l'opération dans la queue
            else:                   # et lit un autre résultat
                answer.put([id,res])

        print(f"{Fore.CYAN}[-]{Fore.WHITE} : Demandeur n°{index}: resultat '{op}={res}'")

def receveur(index:int, ask : list ,answser : list) -> None:
    """
    Reçoit des opérations dans les queue stocké dans la liste `asks`, 
    les évalue (check si elles sont valides), et envoie le résultat dans la queue associé `answsers[index]`
    """
    while True:
        if not ask.empty():
            index_demandeur, op = ask.get()
            try:                # Traitement des calculs incorrect
                res = eval(f"({op})({index})")
                print(f"{Fore.GREEN}[-]{Fore.WHITE} : Receveur n°{index} '{op}={res}' avec x={index} (demandeur n°{index_demandeur})")
            except:             # Si le calcul est incorrect, le resultat est None
                print(f"{Fore.GREEN}[-]{Fore.WHITE} : Receveur n°{index} {Fore.RED}Is invalid operation '{op}'{Fore.WHITE} (demandeur n°{index_demandeur})")
                res = None
            answser.put([index_demandeur,res])
            
if __name__ == "__main__" :
    demandeur_procs, receveur_procs = [], []
    ask, answer = mp.Queue(), mp.Queue()
    for i in range(M):
        demandeur_procs.append(mp.Process(target = demandeur , args = (i,ask,answer,)))

    for i in range(N):
        receveur_procs.append(mp.Process(target = receveur , args = (i,ask,answer,)))

    for proc in demandeur_procs: proc.start()
    for proc in receveur_procs: proc.start()