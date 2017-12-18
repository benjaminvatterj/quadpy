# -*- coding: utf-8 -*-
#
from sympy import Rational as fr

from .helpers import untangle2


class HammerStroud(object):
    '''
    Preston C. Hammer and Arthur H. Stroud,
    Numerical Evaluation of Multiple Integrals II,
    Math. Comp. 12 (1958), 272-280,
    <https://doi.org/10.1090/S0025-5718-1958-0102176-6>.
    '''
    def __init__(self, degree):
        self.degree = degree
        if degree == 2:
            data = {
                's2': [
                    [fr(1, 3), fr(1, 6)],
                    ]
                }
        else:
            assert degree == 3
            data = {
                's3': [
                    [-fr(27, 48)],
                    ],
                's2': [
                    [+fr(25, 48), fr(1, 5)],
                    ]
                }

        self.bary, self.weights = untangle2(data)
        self.points = self.bary[:, 1:]
        return