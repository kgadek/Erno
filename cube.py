#!/usr/bin/env python
# -*- coding: utf-8

import subprocess

class Repr:
    """ Reprezentacja kostki + konwersja do formatu
    czytelnego dla solvera"""

    F_TOP = 0
    F_LEFT = 1
    F_FRONT = 2
    F_RIGHT = 3
    F_BACK = 4
    F_BOTTOM = 5

    C_WHITE = 0
    C_GREEN = 1
    C_ORANGE = 2
    C_BLUE = 3
    C_RED = 4
    C_YELLOW = 5

    n_dict = {0: 'W', 1: 'G', 2: 'O',
              3: 'B', 4: 'R', 5: 'Y'}

    def __init__(self):
        self.state = [[[-1 for _ in range(6)] for _ in range(4)] for _ in range(4)]
    def __str__(self):
        lst = []
        for i in state:
            for j in state:
                for k in state:
                    lst.append(n_dict[k])
        return ''.join(lst)
        

class Solver:
    """ Wywoływanie solvera """
    def run(cubeRepr):
        resAll = subprocess.check_output(["./mcube", str(cubeRepr)])
        res = resAll.split('\n')[-4].split(', ')
        return res

class Steering:
    """ Sterowanie kostką, przechowywanie stanu
    robota """
    pass

class Cube:
    """ Główny program """
    pass
