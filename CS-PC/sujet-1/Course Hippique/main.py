'''
Eliot BADINGA - Rami MESSEOUDI _ 5/06/2023
III-A Exercice : Course Hippique

'''
Nb_process=20 # Nombre de processus

from Consts import *
from Affichages import *

import multiprocessing as mp
from colorama import Fore
import os, time,math, random, sys, ctypes



def un_cheval(ma_ligne : int, keep_running : mp.Value, pos : mp.Array) :
    '''
    Responsable du processus d'un cheval. Le fait avancer a une vitesse aléatoire sur le circuit
    :param ma_ligne:        ligne occupé par le cheval
    :param keep_running:    le cheval doit-il courrir ?
    :param pos:             positions des chevaux
    '''
    col=1

    while col < LONGEUR_COURSE and keep_running.value :
        move_to(ma_ligne+1,col)         # pour effacer toute ma ligne
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print(BK_GREEN + '('+chr(ord('A')+ma_ligne)+f')➞ {CHEVAL}' + BK_GREEN)

        col+=1
        pos[ma_ligne] = col
        time.sleep(0.1 * random.randint(1,5))


def arbitre(ligne : int, pos : mp.Array):
    '''
    Responsable du processsus arbitre. Affichage des informations sur l'évolution de la course.
    :param ligne:   ligne à partir de laquelle on affiche les informations d'arbitrages
    :param pos:     la positios des chevaux
    '''

    # un beau champs vert
    for lig in range(2,ligne):
        for col in range(0, LONGEUR_COURSE+2):
            print_ligne(lig,BK_GREEN+ " ",col)
    print_ligne(ligne-3,BK_BLACK,0)
    


    isFinished= False
    classment = []
    time.sleep(0.5) 
    while not isFinished:
        ## Affichage d'un jolie menue
        print_ligne(ligne, (BK_BLACK + "▔")*(LONGEUR_COURSE+1))
        print_ligne(0, (BK_BLACK + "▁")*(LONGEUR_COURSE+1))       
        print_ligne(ligne+1,f"{BK_BLACK}{UNDERLINE}{BOLD}Classement{NORMAL}",col=int(LONGEUR_COURSE/8))
        print_ligne(ligne+1,f"{BK_BLACK}{UNDERLINE}{BOLD}Pronostic{NORMAL}",col=int(LONGEUR_COURSE/4+4))
        print_ligne(ligne+5,f"{BK_BLACK}Vous avez misez sur{NORMAL}",col=int(LONGEUR_COURSE/4+4))
        print_ligne(ligne+6,f"{BK_BLACK}{BOLD}{PRONO}{NORMAL}",col=int(LONGEUR_COURSE/4+8))
        for i in range(15):
            print_ligne(ligne+2+i,BK_BLACK + "▎",col=int(LONGEUR_COURSE/4))
        for i in range(15):
            print_ligne(ligne+2+i,BK_BLACK + "▎",col=int(LONGEUR_COURSE/2))
        
        ## Affichage du score (col < 25%)
       
        tmp_pos = list(pos)
        if tmp_pos == ([LONGEUR_COURSE]*20): isFinished = True
        
        # Verifier que un nouveau cheval a atteint la ligne d'arrivé
        for i in range(0,len(tmp_pos)-1):
            if tmp_pos[i] == LONGEUR_COURSE and not i in classment:
                classment.append(i)
        tmp_classement = list(classment)
        
        # On calcul la suite du classement avec 
        # uniquement les chevaux qui concourt encore
        # On calcul les 10 premiers chevaux qui court encore
        while len(tmp_classement) < 10:
            id_best = tmp_pos.index(max(tmp_pos))
            if not id_best in tmp_classement:
                tmp_classement.append(id_best)
            tmp_pos[id_best] = 0
            
        # On affiche le score
        for i in range(10):
            if i == 0: color = BK_BLACK + CL_YELLOW + MEDAILLE_1
            elif i == 1: color = BK_BLACK + CL_GRAY + MEDAILLE_2
            elif i == 2: color = BK_BLACK + CL_BROWN + MEDAILLE_3
            else: color = BK_BLACK + CL_WHITE
            

            best_horse = "(" + chr(ord('A')+tmp_classement[i]) + ">"
            print_ligne(ligne+3+i, f"{color}n°{i+1}: {best_horse}", col=10)
            

    # Suppression du champs vert
    for lig in range(2,ligne):
        for col in range(0, LONGEUR_COURSE+2):
            print_ligne(lig,BK_BLACK+ " ",col)
    print_ligne(ligne-3,BK_BLACK,0)
    print_ligne(3,CL_GREEN + END_MSG, col=int(LONGEUR_COURSE/2))

# ---------------------------------------------------
# La partie principale :
if __name__ == "__main__" :
    try:

        print(f"{Fore.CYAN}{WELCOME_MSG}{Fore.WHITE}")
        
        print("[-] Votre pronostic (A-%s)" % (chr(Nb_process+65-1)))
        
        while PRONO not in [chr(i+65) for i in range(Nb_process)]:
            if PRONO != "": print("[x] Choix incorrect")
            PRONO = input("?>")

        os.system("clear")
        import platform
        print(BK_BLACK)
        if platform.system() == "Darwin" :
            mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
            
        LONGEUR_COURSE = 100 # Tout le monde aura la même copie (donc no need to have a 'value')
        keep_running=mp.Value(ctypes.c_bool, True)

        # course_hippique(keep_running)
        
        
        mes_process = [0 for i in range(Nb_process)]
        
        

        effacer_ecran()
        curseur_invisible()


        pos = mp.Array('i', [0]*Nb_process)
        mon_arbitre = mp.Process(target=arbitre, args=(Nb_process+3, pos,))
        mon_arbitre.start()

            
        for i in range(Nb_process):  # Lancer   Nb_process  processus
            mes_process[i] = mp.Process(target=un_cheval, args= (i,keep_running,pos,))
            mes_process[i].start()
        
        move_to(Nb_process+10, 1)


        for i in range(Nb_process): mes_process[i].join()
        mon_arbitre.join()

        move_to(24, 1)
        curseur_visible()
        print("Fini")
        print(BK_RESET + CL_WHITE)
        time.sleep(30)
    except KeyboardInterrupt:
        print(Fore.RESET + BK_RESET)