# -*- coding: utf-8 -*-
#
"""
Richard Franke,
Obtaining cubatures for rectangles and other planar regions by using orthogonal
polynomials,
Math. Comp. 25 (1971), 803-817,
<https://doi.org/10.1090/S0025-5718-1971-0300440-5>.
"""
from __future__ import division

import warnings

import numpy
import sympy

from .helpers import (
    pm,
    pm2,
    concat,
    zero,
    QuadrilateralScheme,
    symm_r0,
    symm_s,
    symm_s_t,
)
from .rabinowitz_richter import rabinowitz_richter_1


def franke_1(lmbda, symbolic=False):
    frac = sympy.Rational if symbolic else lambda x, y: x / y
    sqrt = sympy.sqrt if symbolic else numpy.sqrt

    assert -frac(9, 5) <= lmbda <= frac(9, 4)

    a = sqrt(frac(9 + 5 * lmbda, 15))
    b = sqrt(frac(9 - 4 * lmbda, 15))
    c = sqrt(frac(3, 5))

    weights, points = concat(
        zero(frac(16 * (4 + 5 * lmbda), 9 * (9 + 5 * lmbda))),
        pm2([frac(25, 9 * (9 - 4 * lmbda)), b, c]),
        pm(
            [frac(40, 9 * (9 + 5 * lmbda)), a, 0],
            [frac(40 * (1 - lmbda), 9 * (9 - 4 * lmbda)), 0, c],
        ),
    )
    return QuadrilateralScheme("Franke(1, {})".format(lmbda), 5, weights, points)


def franke_2a(symbolic=False):
    frac = sympy.Rational if symbolic else lambda x, y: x / y
    sqrt = sympy.sqrt if symbolic else numpy.sqrt

    a = sqrt(frac(15 + 2 * sqrt(30), 35))
    b = sqrt(frac(15 - 2 * sqrt(30), 35))

    weights, points = concat(
        pm2(
            [0.437841520872291e-1, 0.105784012371275e1, a],
            [0.362302863812526, 0.774596669241483, b],
            [0.304070693050225, 0.469253522127911, a],
        ),
        pm([0.579684582100041, 0, b]),
    )
    return QuadrilateralScheme("Franke 2a", 7, weights, points)


def franke_2b(symbolic=False):
    frac = sympy.Rational if symbolic else lambda x, y: x / y
    sqrt = sympy.sqrt if symbolic else numpy.sqrt

    a = sqrt(frac(15 + 2 * sqrt(30), 35))
    b = sqrt(frac(15 - 2 * sqrt(30), 35))

    weights, points = concat(
        pm2(
            [0.193252691743030, 0.774596669241483, a],
            [0.169049921219002, 0.915060523380880, b],
            [0.483095233643544, 0.396191039748320, b],
        ),
        pm([0.309204306788848, 0, a]),
    )
    return QuadrilateralScheme("Franke 2b", 7, weights, points)


def franke_3a(symbolic=False):
    frac = sympy.Rational if symbolic else lambda x, y: x / y
    sqrt = sympy.sqrt if symbolic else numpy.sqrt

    a = sqrt(frac(5, 9) + frac(2, 63) * sqrt(70))
    b = sqrt(frac(5, 9) - frac(2, 63) * sqrt(70))

    weights, points = concat(
        pm2(
            [0.705065140564012e-1, 0.845927799771709, a],
            [0.721121511007611e-1, 0.628901636732253, a],
            [0.971492736037507e-1, 0.959681421214621, b],
            [0.368549048677049, 0.436030596273468, b],
        ),
        pm(
            [0.316049382716049, 0.774596669241483, 0],
            [0.188616439798053, 0, a],
            [0.258606964371341e-1, 0, b],
        ),
        zero(0.505679012345679),
    )
    return QuadrilateralScheme("Franke 3a", 9, weights, points)


def franke_3b(symbolic=False):
    frac = sympy.Rational if symbolic else lambda x, y: x / y
    sqrt = sympy.sqrt if symbolic else numpy.sqrt

    a = sqrt(frac(5, 9) + frac(2, 63) * sqrt(70))
    b = sqrt(frac(5, 9) - frac(2, 63) * sqrt(70))

    weights, points = concat(
        pm2(
            [0.499290623065150e-1, 0.945813739519925, a],
            [0.158445182284802, 0.465346624836203, a],
            [0.183383788151247, 0.804253925742002, b],
            [0.881476523665422e-1, 0.681385892163677, b],
        ),
        pm(
            [0.114456375561331, 0.963018409085396, 0.0],
            [0.454432513327558, 0.428610143223121, 0.0],
            [0.571052809297435e-1, 0.0, a],
            [0.414194459963155, 0.0, b],
        ),
    )
    return QuadrilateralScheme("Franke 3b", 9, weights, points)


def franke_3c(symbolic=False):
    frac = sympy.Rational if symbolic else lambda x, y: x / y
    sqrt = sympy.sqrt if symbolic else numpy.sqrt

    a = sqrt(frac(5, 9) + frac(2, 63) * sqrt(70))
    b = sqrt(frac(5, 9) - frac(2, 63) * sqrt(70))

    weights, points = concat(
        pm2(
            [0.494522019130682e-1, 0.949307350001342, a],
            [0.163914731881061, 0.458177548931134, a],
            [0.265904816944092, 0.774596669241483, b],
        ),
        pm(
            [0.113041839046410, 0.967776908976724, 0.0],
            [0.479922229600720, 0.417754671502987, 0.0],
            [0.471199025241204e-1, 0.0, a],
            [0.425447707110548, 0.0, b],
        ),
        zero(-0.481503595164821e-1),
    )
    return QuadrilateralScheme("Franke 3c", 9, weights, points)


def franke_5(symbolic=False):
    frac = sympy.Rational if symbolic else lambda x, y: x / y
    sqrt = sympy.sqrt if symbolic else numpy.sqrt

    r = sqrt(frac(6, 7))
    s = sqrt(frac(114 - 3 * sqrt(583), 287))
    t = sqrt(frac(114 + 3 * sqrt(583), 287))

    weights, points = concat(
        symm_r0([frac(98, 405), r]),
        symm_s(
            [frac(178981 + 2769 * sqrt(583), 472230), s],
            [frac(178981 - 2769 * sqrt(583), 472230), t],
        ),
    )
    return QuadrilateralScheme("Franke 5", 7, weights, points)


def franke_6(symbolic=False):
    frac = sympy.Rational if symbolic else lambda x, y: x / y
    sqrt = sympy.sqrt if symbolic else numpy.sqrt

    a = sqrt(frac(3, 2))
    b = sqrt(frac(3, 7) * (1 + sqrt(frac(10, 31))))
    c = sqrt(frac(3, 7) * (1 - sqrt(frac(10, 31))))

    weights, points = concat(
        zero(frac(392, 405)),
        symm_s([frac(16, 2025), a]),
        symm_s_t([frac(1519, 4050), b, c]),
    )
    return QuadrilateralScheme("Franke 6", 7, weights, points)


def franke_8():
    # TODO find error in franke_8
    warnings.warn("Franke(8) only has degree 1.")

    a = 0.488926856974369
    b = 0.690880550486344
    c = 0.939565258096838
    r = 0.918620441056722
    s = 0.344872025364404

    weights, points = concat(
        symm_r0([0.454163960686749, a]),
        symm_s([0.214200360926862, b], [0.427312318657758e-1, c]),
        symm_s_t([0.144452223260307, r, s]),
    )
    return QuadrilateralScheme("Franke 8", 1, weights, points)


Franke = {
    "1": franke_1,
    "2a": franke_2a,
    "2b": franke_2b,
    "3a": franke_3a,
    "3b": franke_3b,
    "3c": franke_3c,
    "5": franke_5,
    "6": franke_6,
    "7": rabinowitz_richter_1,
    "8": franke_8,
}