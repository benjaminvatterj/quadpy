# -*- coding: utf-8 -*-
#

import warnings

import numpy
import sympy

from ..helpers import article, fsd, pm, pm_roll, untangle
from ._helpers import E3rScheme

citation = article(
    authors=["A.H. Stroud", "D. Secrest"],
    title="Approximate integration formulas for certain spherically symmetric regions",
    journal="Math. Comp.",
    volume="17",
    year="1963",
    pages="105-135",
    url="https://doi.org/10.1090/S0025-5718-1963-0161473-0",
)


def stroud_secrest_vii(symbolic=False):
    frac = sympy.Rational if symbolic else lambda x, y: x / y
    sqrt = numpy.vectorize(sympy.sqrt) if symbolic else numpy.sqrt

    nu, xi = [sqrt(15 - p_m * 3 * sqrt(5)) for p_m in [+1, -1]]
    A = frac(3, 5)
    B = frac(1, 30)

    data = [(A, numpy.array([[0, 0, 0]])), (B, pm_roll(3, [xi, nu]))]

    points, weights = untangle(data)
    pi = sympy.pi if symbolic else numpy.pi
    weights *= 8 * pi
    return E3rScheme("Stroud-Secrest VII", weights, points, 5, citation)


def stroud_secrest_viii(symbolic=False):
    frac = sympy.Rational if symbolic else lambda x, y: x / y
    sqrt = numpy.vectorize(sympy.sqrt) if symbolic else numpy.sqrt

    nu = sqrt(30)
    eta = sqrt(10)
    A = frac(3, 5)
    B = frac(2, 75)
    C = frac(3, 100)

    data = [(A, numpy.array([[0, 0, 0]])), (B, fsd(3, (nu, 1))), (C, pm(3, eta))]
    points, weights = untangle(data)
    pi = sympy.pi if symbolic else numpy.pi
    weights *= 8 * pi
    return E3rScheme("Stroud-Secrest VIII", weights, points, 5, citation)


def stroud_secrest_ix(symbolic=False):
    frac = sympy.Rational if symbolic else lambda x, y: x / y
    sqrt = numpy.vectorize(sympy.sqrt) if symbolic else numpy.sqrt

    eta = sqrt(10)
    xi, nu = [sqrt(15 - p_m * 5 * sqrt(5)) for p_m in [+1, -1]]
    A = frac(3, 5)
    B = frac(1, 50)

    data = [(A, numpy.array([[0, 0, 0]])), (B, pm(3, eta)), (B, pm_roll(3, [xi, nu]))]
    points, weights = untangle(data)
    pi = sympy.pi if symbolic else numpy.pi
    weights *= 8 * pi
    return E3rScheme("Stroud-Secrest IX", weights, points, 5, citation)


def stroud_secrest_x(symbolic=False):
    sqrt = numpy.vectorize(sympy.sqrt) if symbolic else numpy.sqrt

    sqrt130 = sqrt(130)

    nu = sqrt((720 - 24 * sqrt130) / 11)
    xi = sqrt(288 + 24 * sqrt130)
    eta = sqrt((-216 + 24 * sqrt130) / 7)
    A = (5175 - 13 * sqrt130) / 8820
    B = (3870 + 283 * sqrt130) / 493920
    C = (3204 - 281 * sqrt130) / 197568
    # ERR in Stroud's book: 917568 vs. 197568
    D = (4239 + 373 * sqrt130) / 197568

    data = [
        (A, numpy.array([[0, 0, 0]])),
        (B, fsd(3, (nu, 1))),
        (C, fsd(3, (xi, 2))),
        (D, pm(3, eta)),
    ]

    points, weights = untangle(data)
    pi = sympy.pi if symbolic else numpy.pi
    weights *= 8 * pi

    # TODO ERR find out what's wrong
    warnings.warn("Stroud-Secrest X for E_3^r has degree 3, not 7.")
    return E3rScheme("Stroud-Secrest X", weights, points, 4, citation)


def stroud_secrest_xi(symbolic=False):
    sqrt = numpy.vectorize(sympy.sqrt) if symbolic else numpy.sqrt

    sqrt5 = sqrt(5)
    sqrt39 = sqrt(39)
    sqrt195 = sqrt(195)

    nu, xi = [
        sqrt(-50 + p_m * 10 * sqrt5 + 10 * sqrt39 - p_m * 2 * sqrt195)
        for p_m in [+1, -1]
    ]
    eta = sqrt(36 + 4 * sqrt39)
    mu, lmbda = [
        sqrt(54 + p_m * 18 * sqrt5 + 6 * sqrt39 + p_m * 2 * sqrt195) for p_m in [+1, -1]
    ]
    A = (1725 - 26 * sqrt39) / 2940
    B = (1065 + 171 * sqrt39) / 54880
    C = (297 - 47 * sqrt39) / 32928

    data = [
        (A, numpy.array([[0, 0, 0]])),
        (B, pm_roll(3, [xi, nu])),
        (C, pm(3, eta)),
        (C, pm_roll(3, [lmbda, mu])),
    ]

    points, weights = untangle(data)
    pi = sympy.pi if symbolic else numpy.pi
    weights *= 8 * pi
    return E3rScheme("Stroud-Secrest XI", weights, points, 7, citation)
