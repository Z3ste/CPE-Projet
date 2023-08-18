'''
Eliot BADINGA - Rami MESSEOUDI _ 5/06/2023
III-A Exercice : Course Hippique

Toutes les constantes utilisés par notre programme
'''
#################### Consts ##########################
PRONO = ""
# Quelques codes d'échappement (tous ne sont pas utilisés)
CLEARSCR="\x1B[2J\x1B[;H"          #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"             #  effacer après la position du curseur
CRLF  = "\r\n"                     #  Retour à la ligne

# Nov 2021
# Course Hippique (version élèves)
# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné

BK_GREEN = "\x1B[42m"
BK_BLACK = "\x1B[40m"
BK_RESET = "\x1B[49m"
# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc


CHEVAL = "🏇"
MEDAILLE_1 = "🥇"
MEDAILLE_2 ="🥈"
MEDAILLE_3 = "🥉"

# Une liste de couleurs à affecter aléatoirement aux chevaux
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
             CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN,  CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]



END_MSG = """
            ___________                  .__                     
            \\__    ___/__________  _____ |__| ____   ___________ 
               |    |_/ __ \\_  __ \\/     \\|  |/    \\_/ __ \\_  __ \\
               |    |\\  ___/|  | \\/  Y Y  \\  |   |  \\  ___/|  | \\/
               |____| \\___  >__|  |__|_|  /__|___|  /\\___  >__|   
                        \\/            \\/        \\/     \\/                    
"""

WELCOME_MSG = """
  ______        _                     _   _                              
 |  ____|      | |                   | | | |                             
 | |__ __ _ ___| |_    __ _ _ __   __| | | |__   ___  _ __ ___  ___  ___ 
 |  __/ _` / __| __|  / _` | '_ \ / _` | | '_ \ / _ \| '__/ __|/ _ \/ __|
 | | | (_| \__ \ |_  | (_| | | | | (_| | | | | | (_) | |  \__ \  __/\__ \\
 |_|  \__,_|___/\__|  \__,_|_| |_|\__,_| |_| |_|\___/|_|  |___/\___||___/
                                                                         
"""