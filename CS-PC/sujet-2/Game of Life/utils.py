"""
Eliot BADINGA _ 8/06/2023
Exercice : Game of Life

Défini des fonctions diverses utilisées par le programme.
"""
import pickle
import base64


def pack_botmap(botmap : list) -> str:
    """
    Permet de transformer une liste en une chaine de caractere
    """
    return base64.b64encode(pickle.dumps(botmap)).decode()

def unpack_botmap(botmap: str) -> list:
    """
    Permet de transformer une chaine de caractère en une liste
    """
    return pickle.loads(base64.b64decode(botmap))