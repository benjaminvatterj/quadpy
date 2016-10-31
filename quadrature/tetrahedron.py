# -*- coding: utf-8 -*-
#
import math
import numpy
import sympy

from . import helpers


def show(tet, scheme):
    '''Shows the quadrature points on a given tetrahedron. The size of the
    balls around the points coincides with their weights.
    '''
    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect('equal')

    edges = numpy.array([
        [tet[0], tet[1]],
        [tet[0], tet[2]],
        [tet[0], tet[3]],
        [tet[1], tet[2]],
        [tet[1], tet[3]],
        [tet[2], tet[3]],
        ])
    for edge in edges:
        plt.plot(edge[:, 0], edge[:, 1], edge[:, 2], '-k')

    transformed_pts = \
        + numpy.outer(
            (1.0 - scheme.points[:, 0]
                 - scheme.points[:, 1]
                 - scheme.points[:, 2]),
            tet[0]
            ) \
        + numpy.outer(scheme.points[:, 0], tet[1]) \
        + numpy.outer(scheme.points[:, 1], tet[2]) \
        + numpy.outer(scheme.points[:, 2], tet[3])

    vol = integrate(lambda x: numpy.ones(1), tet, Keast(0))
    helpers.plot_balls(
        plt, ax, transformed_pts, scheme.weights, vol,
        tet[:, 0].min(), tet[:, 0].max(),
        tet[:, 1].min(), tet[:, 1].max(),
        tet[:, 2].min(), tet[:, 2].max(),
        )
    return


def integrate(f, tetrahedron, scheme):
    xi = scheme.points.T
    x = \
        + numpy.outer(tetrahedron[0], 1.0 - xi[0] - xi[1] - xi[2]) \
        + numpy.outer(tetrahedron[1], xi[0]) \
        + numpy.outer(tetrahedron[2], xi[1]) \
        + numpy.outer(tetrahedron[3], xi[2])

    # det is the signed volume of the tetrahedron
    J0 = \
        - numpy.outer(tetrahedron[0], 1.0) \
        + numpy.outer(tetrahedron[1], 1.0)
    J1 = \
        - numpy.outer(tetrahedron[0], 1.0) \
        + numpy.outer(tetrahedron[2], 1.0)
    J2 = \
        - numpy.outer(tetrahedron[0], 1.0) \
        + numpy.outer(tetrahedron[3], 1.0)
    det = J0[0]*J1[1]*J2[2] + J1[0]*J2[1]*J0[2] + J2[0]*J0[1]*J1[2] \
        - J0[2]*J1[1]*J2[0] - J1[2]*J2[1]*J0[0] - J2[2]*J0[1]*J1[0]
    # reference volume
    det *= 1.0/6.0

    return math.fsum(scheme.weights * f(x).T * abs(det))


def _s4():
    return numpy.array([
        [0.25, 0.25, 0.25, 0.25]
        ])


def _s31(a):
    b = 1.0 - 3*a
    return numpy.array([
        [a, a, a, b],
        [a, a, b, a],
        [a, b, a, a],
        [b, a, a, a],
        ])


def _s22(a):
    b = 0.5 - a
    return numpy.array([
        [a, a, b, b],
        [a, b, a, b],
        [b, a, a, b],
        [a, b, b, a],
        [b, a, b, a],
        [b, b, a, a],
        ])


def _s211(a, b):
    c = 1.0 - 2*a - b
    return numpy.array([
        [a, a, b, c],
        [a, b, a, c],
        [b, a, a, c],
        [a, b, c, a],
        [b, a, c, a],
        [b, c, a, a],
        [a, a, c, b],
        [a, c, a, b],
        [c, a, a, b],
        [a, c, b, a],
        [c, a, b, a],
        [c, b, a, a],
        ])


def _s1111(a, b, c):
    d = 1.0 - a - b - c
    return numpy.array([
        [a, b, c, d],
        [a, b, d, c],
        [a, c, b, d],
        [a, c, d, b],
        [a, d, b, c],
        [a, d, c, b],
        [b, a, c, d],
        [b, a, d, c],
        [b, c, a, d],
        [b, c, d, a],
        [b, d, a, c],
        [b, d, c, a],
        [c, a, b, d],
        [c, a, d, b],
        [c, b, a, d],
        [c, b, d, a],
        [c, d, a, b],
        [c, d, b, a],
        [d, a, b, c],
        [d, a, c, b],
        [d, b, a, c],
        [d, b, c, a],
        [d, c, a, b],
        [d, c, b, a],
        ])


class HammerMarloweStroud(object):
    '''
    P.C. Hammer, O.J. Marlowe and A.H. Stroud,
    Numerical Integration Over Simplexes and Cones,
    Mathematical Tables and Other Aids to Computation,
    Vol. 10, No. 55, Jul. 1956, pp. 130-137,
    <https://doi.org/10.1090/S0025-5718-1956-0086389-6>.

    Abstract:
    In this paper we develop numerical integration formulas for simplexes and
    cones in n-space for n>=2. While several papers have been written on
    numerical integration in higher spaces, most of these have dealt with
    hyperrectangular regions. For certain exceptions see [3]. Hammer and Wymore
    [1] have given a first general type theory designed through systematic use
    of cartesian product regions and affine transformations to extend the
    possible usefulness of formulas for each region.

    Two of the schemes also appear in

    P.C. Hammer, Arthur H. Stroud,
    Numerical Evaluation of Multiple Integrals II,
    Mathematical Tables and Other Aids to Computation.
    Vol. 12, No. 64 (Oct., 1958), pp. 272-280,
    <http://www.jstor.org/stable/2002370>
    '''
    def __init__(self, index):
        if index == 1:
            self.weights = numpy.concatenate([
                0.25 * numpy.ones(4),
                ])
            bary = numpy.concatenate([
                self._r(1.0 / numpy.sqrt(5.0)),
                ])
            self.degree = 2
        elif index == 2:
            self.weights = numpy.concatenate([
                0.25 * numpy.ones(4),
                ])
            bary = numpy.concatenate([
                self._r(-1.0 / numpy.sqrt(5.0)),
                ])
            self.degree = 2
        elif index == 3:
            self.weights = numpy.concatenate([
                -0.8 * numpy.ones(1),
                9.0/20.0 * numpy.ones(4),
                ])
            bary = numpy.concatenate([
                _s4(),
                self._r(1.0 / 3.0),
                ])
            self.degree = 3
        else:
            raise ValueError('Illegal Hammer-Marlowe-Stroud index')

        self.points = bary[:, 1:]
        return

    def _r(self, r):
        '''Given $r$ (as appearing in the article), it returns the barycentric
        coordinates of the three points.
        '''
        a = r + (1.0-r) / 4.0
        b = (1.0 - a) / 3.0
        return numpy.array([
            [a, b, b, b],
            [b, a, b, b],
            [b, b, a, b],
            [b, b, b, a],
            ])


def _newton_cotes(n, point_fun):
    '''
    Construction after

    P. Silvester,
    Symmetric quadrature formulae for simplexes
    Math. Comp., 24, 95-100 (1970),
    <https://doi.org/10.1090/S0025-5718-1970-0258283-6>.
    '''
    degree = n

    # points
    idx = numpy.array([
        [i, j, k, n-i-j-k]
        for i in range(n + 1)
        for j in range(n + 1 - i)
        for k in range(n + 1 - i - j)
        ])
    bary = point_fun(idx, n)
    points = bary[:, [1, 2, 3]]

    # weights
    if n == 0:
        weights = numpy.ones(1)
        return points, weights, degree

    def get_poly(t, m, n):
        return sympy.prod([
            sympy.poly(
                (t - point_fun(k, n)) / (point_fun(m, n) - point_fun(k, n))
            )
            for k in range(m)
            ])
    weights = numpy.empty(len(points))
    idx = 0
    for i in range(n + 1):
        for j in range(n + 1 - i):
            for k in range(n + 1 - i - j):
                l = n - i - j - k
                # Compute weight.
                # Define the polynomial which to integrate over the
                # tetrahedron.
                t = sympy.DeferredVector('t')
                g = get_poly(t[0], i, n) \
                    * get_poly(t[1], j, n) \
                    * get_poly(t[2], k, n) \
                    * get_poly(t[3], l, n)
                # The integral of monomials over a tetrahedron are well-known,
                # see Silvester.
                weights[idx] = numpy.sum([
                     c * numpy.prod([math.factorial(k) for k in m]) * 6.0
                     / math.factorial(numpy.sum(m) + 3)
                     for m, c in zip(g.monoms(), g.coeffs())
                     ])
                idx += 1
    return points, weights, degree


class NewtonCotesClosed(object):
    def __init__(self, n):
        self.points, self.weights, self.degree = \
            _newton_cotes(n, lambda k, n: k / float(n))
        return


class NewtonCotesOpen(object):
    def __init__(self, n):
        self.points, self.weights, self.degree = \
            _newton_cotes(n, lambda k, n: (k+1) / float(n+4))
        if n == 0:
            self.degree = 1
        return


class Yu(object):
    '''
    Yu Jinyun,
    Symmetyric Gaussian quadrature formulae for tetrahedronal regions,
    Computer Methods in Applied Mechanics and Engineering, 43 (1984) 349-353,
    <https://dx.doi.org/10.1016/0045-7825(84)90072-0>.

    Abstract:
    Quadrature formulae of degrees 2 to 6 are presented for the numerical
    integration of a function over tetrahedronal regions. The formulae
    presented are of Gaussian type and fully symmetric with respect to the four
    vertices of the tetrahedron.
    '''
    def __init__(self, index):
        if index == 1:
            self.weights = 0.25 * numpy.ones(4)
            bary = _s31(0.138196601125015)
            self.degree = 2
        elif index == 2:
            self.weights = numpy.concatenate([
                -0.8 * numpy.ones(1),
                0.45 * numpy.ones(4)
                ])
            bary = numpy.concatenate([
                _s4(),
                _s31(1.0/6.0)
                ])
            self.degree = 3
        elif index == 3:
            self.weights = numpy.concatenate([
                0.5037379410012282E-01 * numpy.ones(4),
                0.6654206863329239E-01 * numpy.ones(12)
                ])
            bary = numpy.concatenate([
                _s31(0.7611903264425430E-01),
                _s211(0.4042339134672644, 0.1197005277978019)
                ])
            self.degree = 4
        elif index == 4:
            self.weights = numpy.concatenate([
                0.1884185567365411 * numpy.ones(1),
                0.6703858372604275E-01 * numpy.ones(4),
                0.4528559236327399E-01 * numpy.ones(12)
                ])
            bary = numpy.concatenate([
                _s4(),
                _s31(0.8945436401412733E-01),
                _s211(0.4214394310662522, 0.1325810999384657),
                ])
            self.degree = 5
        elif index == 5:
            self.weights = numpy.concatenate([
                0.9040129046014750E-01 * numpy.ones(1),
                0.1911983427899124E-01 * numpy.ones(4),
                0.4361493840666568E-01 * numpy.ones(12),
                0.2581167596199161E-01 * numpy.ones(12)
                ])
            bary = numpy.concatenate([
                _s4(),
                _s31(0.5742691731735682E-01),
                _s211(0.2312985436519147, 0.5135188412556341E-01),
                _s211(0.4756909881472290E-01, 0.2967538129690260),
                ])
            self.degree = 6
        else:
            raise ValueError('Illegal closed Yu index')

        self.points = bary[:, [1, 2, 3]]
        return


class Keast(object):
    '''
    P. Keast,
    Moderate degree tetrahedral quadrature formulas,
    CMAME 55: 339-348
    1986,
    <http://dx.doi.org/10.1016/0045-7825(86)90059-9>.

    Abstract:
    Quadrature formulas of degrees 4 to 8 for numerical integration over the
    tetrahedron are constructed. The formulas are fully symmetric with respect
    to the tetrahedron, and in some cases are the minimum point rules with this
    symmetry.

    https://people.sc.fsu.edu/~jburkardt/datasets/quadrature_rules_tet/quadrature_rules_tet.html
    '''
    def __init__(self, index):
        if index == 0:
            # Does no appear in Keast's article.
            self.weights = numpy.array([
                1.0
                ])
            bary = _s4()
            self.degree = 1
        elif index == 1:
            # Does no appear in Keast's article.
            self.weights = 0.25 * numpy.ones(4)
            bary = _s31(0.1381966011250105)
            self.degree = 2
        elif index == 2:
            # Does no appear in Keast's article.
            self.weights = numpy.concatenate([
                -0.8 * numpy.ones(1),
                0.45 * numpy.ones(4),
                ])
            bary = numpy.concatenate([
                _s4(),
                _s31(1.0/6.0),
                ])
            self.degree = 3
        elif index == 3:
            # Does no appear in Keast's article.
            self.weights = numpy.concatenate([
                0.2177650698804054 * numpy.ones(4),
                0.0214899534130631 * numpy.ones(6),
                ])
            bary = numpy.concatenate([
                _s31(0.1438564719343852),
                _s22(0.5),
                ])
            self.degree = 3
        elif index == 4:
            self.weights = numpy.concatenate([
                -148.0 / 1875.0 * numpy.ones(1),
                343.0 / 7500.0 * numpy.ones(4),
                56.0 / 375.0 * numpy.ones(6),
                ])
            bary = numpy.concatenate([
                _s4(),
                _s31(1.0/14.0),
                _s22(0.3994035761667992),
                ])
            self.degree = 4
        elif index == 5:
            self.weights = numpy.concatenate([
                2.0/105.0 * numpy.ones(6),
                0.0885898247429807 * numpy.ones(4),
                0.1328387466855907 * numpy.ones(4),
                ])
            bary = numpy.concatenate([
                _s22(0.5),
                _s31(0.1005267652252045),
                _s31(0.3143728734931922),
                ])
            self.degree = 4
        elif index == 6:
            self.weights = numpy.concatenate([
                6544.0 / 36015.0 * numpy.ones(1),
                81.0 / 2240.0 * numpy.ones(4),
                161051.0 / 2304960.0 * numpy.ones(4),
                338.0 / 5145.0 * numpy.ones(6),
                ])
            bary = numpy.concatenate([
                _s4(),
                _s31(1.0/3.0),
                _s31(1.0/11.0),
                _s22(0.0665501535736643),
                ])
            self.degree = 5
        elif index == 7:
            self.weights = numpy.concatenate([
                0.0399227502581679 * numpy.ones(4),
                0.0100772110553207 * numpy.ones(4),
                0.0553571815436544 * numpy.ones(4),
                27.0/560.0 * numpy.ones(12),
                ])
            bary = numpy.concatenate([
                _s31(0.2146028712591517),
                _s31(0.0406739585346113),
                _s31(0.3223378901422757),
                _s211(0.0636610018750175, 0.2696723314583159)
                ])
            self.degree = 6
        elif index == 8:
            self.weights = numpy.concatenate([
                0.1095853407966528 * numpy.ones(1),
                0.0635996491464850 * numpy.ones(4),
                -0.3751064406859797 * numpy.ones(4),
                0.0293485515784412 * numpy.ones(4),
                0.0058201058201058 * numpy.ones(6),
                0.1653439153439105 * numpy.ones(12),
                ])
            bary = numpy.concatenate([
                _s4(),
                _s31(0.0782131923303186),
                _s31(0.1218432166639044),
                _s31(0.3325391644464206),
                _s22(0.5),
                _s211(0.1, 0.2),
                ])
            self.degree = 7
        elif index == 9:
            self.weights = numpy.concatenate([
                -0.2359620398477557 * numpy.ones(1),
                0.0244878963560562 * numpy.ones(4),
                0.0039485206398261 * numpy.ones(4),
                0.0263055529507371 * numpy.ones(6),
                0.0829803830550589 * numpy.ones(6),
                0.0254426245481023 * numpy.ones(12),
                0.0134324384376852 * numpy.ones(12),
                ])
            bary = numpy.concatenate([
                _s4(),
                _s31(0.1274709365666390),
                _s31(0.0320788303926323),
                _s22(0.0497770956432810),
                _s22(0.1837304473985499),
                _s211(0.2319010893971509, 0.5132800333608811),
                _s211(0.0379700484718286, 0.1937464752488044),
                ])
            self.degree = 8
        elif index == 10:
            self.weights = 6 * numpy.concatenate([
                # Note: In Keast's article, the first weight is incorrectly
                # given with a positive sign.
                -0.393270066412926145e-01 * numpy.ones(1),
                +0.408131605934270525e-02 * numpy.ones(4),
                +0.658086773304341943e-03 * numpy.ones(4),
                +0.438425882512284693e-02 * numpy.ones(6),
                +0.138300638425098166e-01 * numpy.ones(6),
                +0.424043742468372453e-02 * numpy.ones(12),
                +0.223873973961420164e-02 * numpy.ones(12),
                ])
            bary = numpy.concatenate([
                _s4(),
                _s31(0.127470936566639015e-00),
                _s31(0.320788303926322960e-01),
                _s22(0.497770956432810185e-01),
                _s22(0.183730447398549945e-00),
                _s211(0.231901089397150906e-00, 0.229177878448171174e-01),
                _s211(0.379700484718286102e-01, 0.730313427807538396e-00),
                ])
            self.degree = 8
        else:
            raise ValueError('Illegal Keast index')

        self.points = bary[:, 1:]
        return


class LiuVinokur(object):
    '''
    Y. Liu and M. Vinokur,
    Exact Integrations of Polynomials and Symmetric Quadrature Formulas over
    Arbitrary Polyhedral Grids,
    Journal of Computational Physics, 140, 122–147 (1998).
    DOI: 10.1006/jcph.1998.5884,
    <http://dx.doi.org/10.1006/jcph.1998.5884>.
    '''
    def __init__(self, index):
        if index == 1:
            self.weights = numpy.concatenate([
                1.0 * numpy.ones(1),
                ])
            bary = numpy.concatenate([
                _s4(),
                ])
            self.degree = 1
        elif index == 2:
            self.weights = numpy.concatenate([
                0.25 * numpy.ones(4),
                ])
            bary = numpy.concatenate([
                self._r_alpha(1.0),
                ])
            self.degree = 1
        elif index == 3:
            self.weights = numpy.concatenate([
                0.25 * numpy.ones(4),
                ])
            bary = numpy.concatenate([
                self._r_alpha(1.0 / numpy.sqrt(5.0)),
                ])
            self.degree = 2
        elif index == 4:
            self.weights = numpy.concatenate([
                0.8 * numpy.ones(1),
                0.05 * numpy.ones(4),
                ])
            bary = numpy.concatenate([
                _s4(),
                self._r_alpha(1.0),
                ])
            self.degree = 2
        elif index == 5:
            self.weights = numpy.concatenate([
                -0.8 * numpy.ones(1),
                0.45 * numpy.ones(4),
                ])
            bary = numpy.concatenate([
                _s4(),
                self._r_alpha(1.0/3.0),
                ])
            self.degree = 3
        elif index == 6:
            self.weights = numpy.concatenate([
                1.0/40.0 * numpy.ones(4),
                9.0/40.0 * numpy.ones(4),
                ])
            bary = numpy.concatenate([
                self._r_alpha(1.0),
                self._r_alpha(-1.0/3.0),
                ])
            self.degree = 3
        elif index == 7:
            self.weights = numpy.concatenate([
                -148.0/1875.0 * numpy.ones(1),
                343.0/7500.0 * numpy.ones(4),
                56.0/375.0 * numpy.ones(6),
                ])
            bary = numpy.concatenate([
                _s4(),
                self._r_alpha(5.0/7.0),
                self._r_beta(numpy.sqrt(70.0)/28.0),
                ])
            self.degree = 4
        elif index == 8:
            alpha1 = (
                + numpy.sqrt(65944.0 - 19446*numpy.sqrt(11))
                + 51*numpy.sqrt(11) - 154.0
                ) / 89.0
            alpha2 = (
                - numpy.sqrt(65944.0 - 19446*numpy.sqrt(11))
                + 51*numpy.sqrt(11) - 154.0
                ) / 89.0
            self.weights = numpy.concatenate([
                (17*alpha2 - 7.0)/(420.0*alpha1**2 * (alpha2 - alpha1))
                * numpy.ones(4),
                (17*alpha1 - 7.0)/(420.0*alpha2**2 * (alpha1 - alpha2))
                * numpy.ones(4),
                2.0/105.0 * numpy.ones(6),
                ])
            bary = numpy.concatenate([
                self._r_alpha(alpha1),
                self._r_alpha(alpha2),
                self._r_beta(0.5),
                ])
            self.degree = 4
        elif index == 9:
            self.weights = numpy.concatenate([
                -32.0/15.0 * numpy.ones(1),
                3.0/280.0 * numpy.ones(4),
                125.0/168.0 * numpy.ones(4),
                2.0/105.0 * numpy.ones(6),
                ])
            bary = numpy.concatenate([
                _s4(),
                self._r_alpha(1),
                self._r_alpha(0.2),
                self._r_beta(0.5),
                ])
            self.degree = 4
        elif index == 10:
            self.weights = numpy.concatenate([
                32.0/105.0 * numpy.ones(1),
                -31.0/840.0 * numpy.ones(4),
                27.0/280.0 * numpy.ones(4),
                4.0/105.0 * numpy.ones(12),
                ])
            bary = numpy.concatenate([
                _s4(),
                self._r_alpha(1),
                self._r_alpha(-1.0/3.0),
                self._r_gamma_delta(
                    (2 + numpy.sqrt(2.0)) / 4.0,
                    (2 - numpy.sqrt(2.0)) / 4.0,
                    ),
                ])
            self.degree = 4
        elif index == 11:
            self.weights = numpy.concatenate([
                (11.0 - 4*numpy.sqrt(2.0)) / 840.0 * numpy.ones(4),
                (243.0 - 108*numpy.sqrt(2.0)) / 1960.0 * numpy.ones(4),
                (62.0 + 44*numpy.sqrt(2.0)) / 735.0 * numpy.ones(4),
                2.0/105.0 * numpy.ones(6),
                ])
            bary = numpy.concatenate([
                self._r_alpha(1),
                self._r_alpha(-1.0/3.0),
                self._r_alpha(numpy.sqrt(2.0) - 1.0),
                self._r_beta(0.5),
                ])
            self.degree = 4
        elif index == 12:
            lmbda = 4.0/27.0 * (4.0 * numpy.sqrt(79.0)*numpy.cos(
                (numpy.arccos(67*numpy.sqrt(79.0)/24964.0) + 2*numpy.pi) / 3.0
                ) + 71.0
                )
            alpha1 = (
                + numpy.sqrt(9*lmbda**2 - 248*lmbda + 1680) + 28.0 - 3*lmbda
                ) / (112.0 - 10*lmbda)
            alpha2 = (
                - numpy.sqrt(9*lmbda**2 - 248*lmbda + 1680) + 28.0 - 3*lmbda
                ) / (112.0 - 10*lmbda)
            w1 = ((21.0 - lmbda)*alpha2 - 7.0) \
                / (420.0*alpha1**2 * (alpha2 - alpha1))
            w2 = ((21.0 - lmbda)*alpha1 - 7.0) \
                / (420.0*alpha2**2 * (alpha1 - alpha2))
            self.weights = numpy.concatenate([
                w1 * numpy.ones(4),
                w2 * numpy.ones(4),
                lmbda**2/840.0 * numpy.ones(6),
                ])
            bary = numpy.concatenate([
                self._r_alpha(alpha1),
                self._r_alpha(alpha2),
                self._r_beta(1.0 / numpy.sqrt(lmbda)),
                ])
            self.degree = 5
        elif index == 13:
            self.weights = numpy.concatenate([
                -16.0/21.0 * numpy.ones(1),
                (2249.0 - 391.0*numpy.sqrt(13.0)) / 10920.0 * numpy.ones(4),
                (2249.0 + 391.0*numpy.sqrt(13.0)) / 10920.0 * numpy.ones(4),
                2.0 / 105.0 * numpy.ones(6),
                ])
            bary = numpy.concatenate([
                _s4(),
                self._r_alpha((2.0 + numpy.sqrt(13.0)) / 9.0),
                self._r_alpha((2.0 - numpy.sqrt(13.0)) / 9.0),
                self._r_beta(0.5),
                ])
            self.degree = 5
        elif index == 14:
            self.weights = numpy.concatenate([
                16.0/105.0 * numpy.ones(1),
                1.0/280.0 * numpy.ones(4),
                81.0/1400.0 * numpy.ones(4),
                64.0/525.0 * numpy.ones(4),
                2.0/105.0 * numpy.ones(6),
                ])
            bary = numpy.concatenate([
                _s4(),
                self._r_alpha(1.0),
                self._r_alpha(-1.0/3.0),
                self._r_alpha(0.5),
                self._r_beta(0.5),
                ])
            self.degree = 5
        else:
            raise ValueError('Illegal Liu-Vinokur index')

        self.points = bary[:, 1:]
        return

    def _r_alpha(self, alpha):
        '''From the article:

        mu_i = (1 + (n-1) alpha) / n,
        mu_j = (1 - alpha) / n    for j!=i,

        where n is the number of vertices
        '''
        a = (1.0 + 3*alpha) / 4.0
        b = (1.0 - alpha) / 4.0
        return numpy.array([
            [a, b, b, b],
            [b, a, b, b],
            [b, b, a, b],
            [b, b, b, a],
            ])

    def _r_beta(self, beta):
        '''From the article:

        mu_i = (1+(n-2)*beta) / n,
        mu_j = mu_i,
        mu_k = (1 - 2*beta) / n    for k!=i, k!=j,

        where n is the number of vertices.
        '''
        a = (1.0 + 2*beta) / 4.0
        b = (1.0 - 2*beta) / 4.0
        return numpy.array([
            [a, a, b, b],
            [a, b, a, b],
            [b, a, a, b],
            [a, b, b, a],
            [b, a, b, a],
            [b, b, a, a],
            ])

    def _r_gamma_delta(self, gamma, delta):
        '''From the article:

        mu_i = (1 + (n-1) gamma - delta) / n,
        mu_j = (1 + (n-1) delta - gamma) / n,
        mu_k = (1 - gamma - delta) / n    for k!=i, k!=j,

        where n is the number of vertices
        '''
        b = (1.0 + 3*gamma - delta) / 4.0
        c = (1.0 + 3*delta - gamma) / 4.0
        a = (1.0 - gamma - delta) / 4.0
        return numpy.array([
            [a, a, b, c],
            [a, b, a, c],
            [b, a, a, c],
            [a, b, c, a],
            [b, a, c, a],
            [b, c, a, a],
            [a, a, c, b],
            [a, c, a, b],
            [c, a, a, b],
            [a, c, b, a],
            [c, a, b, a],
            [c, b, a, a],
            ])


class Zienkiewicz(object):
    '''
    Olgierd Zienkiewicz,
    The Finite Element Method,
    Sixth Edition,
    Butterworth-Heinemann, 2005,
    ISBN: 0750663200,
    <http://www.sciencedirect.com/science/book/9780750664318>,
    <https://people.sc.fsu.edu/~jburkardt/datasets/quadrature_rules_tet/quadrature_rules_tet.html>.
    '''
    def __init__(self, index):
        if index == 4:
            self.weights = 0.25 * numpy.ones(4)
            bary = _s31(0.1381966011250105)
            self.degree = 2
        elif index == 5:
            self.weights = numpy.concatenate([
                -0.8 * numpy.ones(1),
                0.45 * numpy.ones(4),
                ])
            bary = numpy.concatenate([
                _s4(),
                _s31(1.0/6.0),
                ])
            self.degree = 3
        else:
            raise ValueError('Illegal closed Newton-Cotes index')

        self.points = bary[:, [1, 2, 3]]
        return


class ZhangCuiLiu(object):
    '''
    Linbo Zhang, Tao Cui and Hui Liu,
    A set of symmetric quadrature rules on triangles and tetrahedra,
    Journal of Computational Mathematics
    Vol. 27, No. 1 (January 2009), pp. 89-96,
    <http://www.jstor.org/stable/43693493>.

    Abstract:
    We present a program for computing symmetric quadrature rules on triangles
    and tetrahedra. A set of rules are obtained by using this program.
    Quadrature rules up to order 21 on triangles and up to order 14 on
    tetrahedra have been obtained which are useful for use in finite element
    computations. All rules presented here have positive weights with points
    lying within the integration domain.
    '''
    def __init__(self, index):
        if index == 1:
            self.weights = numpy.concatenate([
                0.0063971477799023213214514203351730 * numpy.ones(4),
                0.0401904480209661724881611584798178 * numpy.ones(4),
                0.0243079755047703211748691087719226 * numpy.ones(4),
                0.0548588924136974404669241239903914 * numpy.ones(4),
                0.0357196122340991824649509689966176 * numpy.ones(6),
                0.0071831906978525394094511052198038 * numpy.ones(12),
                0.0163721819453191175409381397561191 * numpy.ones(12),
                ])
            bary = numpy.concatenate([
                _s31(.0396754230703899012650713295393895),
                _s31(.3144878006980963137841605626971483),
                _s31(.1019866930627033000000000000000000),
                _s31(.1842036969491915122759464173489092),
                _s22(.0634362877545398924051412387018983),
                _s211(
                    .0216901620677280048026624826249302,
                    .7199319220394659358894349533527348
                    ),
                _s211(
                    .2044800806367957142413355748727453,
                    .5805771901288092241753981713906204
                    ),
                ])
            self.degree = 8
        elif index == 2:
            self.weights = numpy.concatenate([
                .0040651136652707670436208836835636 * numpy.ones(4),
                .0022145385334455781437599569500071 * numpy.ones(4),
                .0058134382678884505495373338821455 * numpy.ones(4),
                .0196255433858357215975623333961715 * numpy.ones(4),
                .0003875737905908214364538721248394 * numpy.ones(4),
                .0116429719721770369855213401005552 * numpy.ones(12),
                .0052890429882817131317736883052856 * numpy.ones(12),
                .0018310854163600559376697823488069 * numpy.ones(12),
                .0082496473772146452067449669173660 * numpy.ones(12),
                .0030099245347082451376888748208987 * numpy.ones(24),
                .0008047165617367534636261808760312 * numpy.ones(24),
                .0029850412588493071187655692883922 * numpy.ones(24),
                .0056896002418760766963361477811973 * numpy.ones(24),
                .0041590865878545715670013980182613 * numpy.ones(24),
                .0007282389204572724356136429745654 * numpy.ones(24),
                .0054326500769958248216242340651926 * numpy.ones(24),
                ])
            bary = numpy.concatenate([
                _s31(.3272533625238485639093096692685289),
                _s31(.0447613044666850808837942096478842),
                _s31(.0861403311024363536537208740298857),
                _s31(.2087626425004322968265357083976176),
                _s31(.0141049738029209600635879152102928),
                _s211(
                    .1021653241807768123476692526982584,
                    .5739463675943338202814002893460107
                    ),
                _s211(
                    .4075700516600107157213295651301783,
                    .0922278701390201300000000000000000
                    ),
                _s211(
                    .0156640007402803585557586709578084,
                    .7012810959589440327139967673208426
                    ),
                _s211(
                    .2254963562525029053780724154201103,
                    .4769063974420887115860583354107011
                    ),
                _s1111(
                    .3905984281281458000000000000000000,
                    .2013590544123922168123077327235092,
                    .0161122880710300298578026931548371
                    ),
                _s1111(
                    .1061350679989021455556139029848079,
                    .0327358186817269284944004077912660,
                    .0035979076537271666907971523385925
                    ),
                _s1111(
                    .5636383731697743896896816630648502,
                    .2302920722300657454502526874135652,
                    .1907199341743551862712487790637898
                    ),
                _s1111(
                    .3676255095325860844092206775991167,
                    .2078851380230044950717102125250735,
                    .3312104885193449000000000000000000
                    ),
                _s1111(
                    .7192323689817295295023401840796991,
                    .1763279118019329762157993033636973,
                    .0207602362571310090754973440611644
                    ),
                _s1111(
                    .5278249952152987298409240075817276,
                    .4372890892203418165526238760841918,
                    .0092201651856641949463177554949220
                    ),
                _s1111(
                    .5483674544948190728994910505607746,
                    .3447815506171641228703671870920331,
                    .0867217283322215394629438740085828
                    ),
                ])
            self.degree = 15
        else:
            raise ValueError('Illegal Zhang index')

        self.points = bary[:, [1, 2, 3]]
        return


class XiaoGimbutas(object):
    '''
    Hong Xiao, Zydrunas Gimbutas,
    A numerical algorithm for the construction of efficient quadrature rules in
    two and higher dimensions,
    Computers & Mathematics with Applications,
    Volume 59, Issue 2, January 2010, Pages 663–676,
    <http://dx.doi.org/10.1016/j.camwa.2009.10.027>.

    Abstract:
    We present a numerical algorithm for the construction of efficient,
    high-order quadratures in two and higher dimensions. Quadrature rules
    constructed via this algorithm possess positive weights and interior nodes,
    resembling the Gaussian quadratures in one dimension. In addition, rules
    can be generated with varying degrees of symmetry, adaptable to individual
    domains. We illustrate the performance of our method with numerical
    examples, and report quadrature rules for polynomials on triangles,
    squares, and cubes, up to degree 50. These formulae are near optimal in the
    number of nodes used, and many of them appear to be new.

    Data adapted from
    <https://people.sc.fsu.edu/~jburkardt/f_src/triangle_symq_rule/triangle_symq_rule.f90>.
    '''
    def __init__(self, index):
        # True most of the time, but overridden for some indices.
        self.degree = index

        if index == 1:
            bary = numpy.array([
                [
                    0.25, 0.25,
                    0.25, 0.25,
                ],
                ])
            self.weights = numpy.array([
                1.0,
                ])
        elif index == 2:
            bary = numpy.array([
                [
                    0.365314518814635, 0.180029693510365,
                    0.00692323557362747, 0.447732552101373,
                ],
                [
                    0.457461587085596, 0.155933120499186,
                    0.381765356069347, 0.0048399363458718,
                ],
                [
                    0.000375515028729282, 0.216076429184848,
                    0.430701707077836, 0.352846348708587,
                ],
                [
                    0.123666800328458, 0.82157254096762,
                    0.0399330486414984, 0.0148276100624234,
                ],
                ])
            self.weights = numpy.array([
                0.300520939336976,
                0.278777576686568,
                0.319093935501475,
                0.101607548474981,
                ])
        elif index == 3:
            bary = numpy.array([
                [
                    0.439858947649275, 0.190117002439284,
                    0.0114033294445572, 0.358620720466884,
                ],
                [
                    0.124804862165247, 0.158685163227441,
                    0.585662805655216, 0.130847168952096,
                ],
                [
                    0.345444155719731, 0.0109052122111892,
                    0.281523802123546, 0.362126829945534,
                ],
                [
                    0.141482751969504, 0.571226052149115,
                    0.14691839008717, 0.140372805794211,
                ],
                [
                    0.037871631782357, 0.170816925164989,
                    0.152818143090927, 0.638493299961727,
                ],
                [
                    0.641429791495696, 0.162001491698524,
                    0.183850350492098, 0.0127183663136814,
                ],
                ])
            self.weights = numpy.array([
                0.132568027144445,
                0.224415166917557,
                0.128066412710747,
                0.252003980809502,
                0.140624409660403,
                0.122322002757345,
                ])
        elif index == 4:
            bary = numpy.array([
                [
                    0.106604172561994, 0.0972046445875833,
                    0.68439041545304, 0.111800767397383,
                ],
                [
                    0.329232959742647, 0.0295694952064796,
                    0.317903560213395, 0.323293984837479,
                ],
                [
                    0.103844116410993, 0.432710239047769,
                    0.353823239209297, 0.109622405331941,
                ],
                [
                    0.304448402434497, 0.240276664928073,
                    0.126801725915392, 0.328473206722038,
                ],
                [
                    0.538007203916186, 0.12941137378891,
                    0.330190414837464, 0.00239100745743937,
                ],
                [
                    0.00899126009333578, 0.121541991333928,
                    0.30649398842969, 0.562972760143046,
                ],
                [
                    0.432953490481356, 0.450765876091277,
                    0.0594566162994338, 0.0568240171279337,
                ],
                [
                    0.0533412395357452, 0.419266313879513,
                    0.0477814355590867, 0.479611011025655,
                ],
                [
                    0.741228882093623, 0.0672232948933834,
                    0.0351839297735987, 0.156363893239395,
                ],
                [
                    0.0814049184028593, 0.752508507009655,
                    0.0680993709382067, 0.0979872036492791,
                ],
                [
                    0.174694058697231, 0.0404905067275904,
                    0.0135607018798029, 0.771254732695376,
                ],
                ])
            self.weights = numpy.array([
                0.10646803415549,
                0.110234232428498,
                0.154976116016246,
                0.193410812049634,
                0.0761627152455584,
                0.0794266800680253,
                0.0694699659376354,
                0.0599331851465595,
                0.0553937988715764,
                0.0552733691559369,
                0.03925109092484,
                ])
        elif index == 5:
            bary = numpy.array([
                [
                    0.0927352503108913, 0.0927352503108913,
                    0.721794249067326, 0.0927352503108911,
                ],
                [
                    0.0455037041256497, 0.45449629587435,
                    0.45449629587435, 0.0455037041256496,
                ],
                [
                    0.45449629587435, 0.0455037041256497,
                    0.45449629587435, 0.0455037041256497,
                ],
                [
                    0.0455037041256497, 0.0455037041256497,
                    0.45449629587435, 0.45449629587435,
                ],
                [
                    0.310885919263301, 0.310885919263301,
                    0.0673422422100981, 0.310885919263301,
                ],
                [
                    0.310885919263301, 0.0673422422100983,
                    0.310885919263301, 0.3108859192633,
                ],
                [
                    0.0673422422100983, 0.310885919263301,
                    0.310885919263301, 0.310885919263301,
                ],
                [
                    0.310885919263301, 0.310885919263301,
                    0.310885919263301, 0.067342242210098,
                ],
                [
                    0.0927352503108913, 0.721794249067326,
                    0.0927352503108912, 0.0927352503108913,
                ],
                [
                    0.0927352503108913, 0.0927352503108911,
                    0.0927352503108913, 0.721794249067326,
                ],
                [
                    0.721794249067326, 0.0927352503108912,
                    0.0927352503108913, 0.0927352503108913,
                ],
                [
                    0.45449629587435, 0.45449629587435,
                    0.0455037041256496, 0.0455037041256497,
                ],
                [
                    0.0455037041256497, 0.45449629587435,
                    0.0455037041256497, 0.45449629587435,
                ],
                [
                    0.45449629587435, 0.0455037041256497,
                    0.0455037041256496, 0.45449629587435,
                ],
                ])
            self.weights = numpy.array([
                0.073493043116362,
                0.0425460207770815,
                0.0425460207770815,
                0.0425460207770815,
                0.112687925718016,
                0.112687925718016,
                0.112687925718016,
                0.112687925718016,
                0.0734930431163619,
                0.0734930431163619,
                0.0734930431163619,
                0.0425460207770814,
                0.0425460207770815,
                0.0425460207770815,
                ])
        elif index == 6:
            bary = numpy.array([
                [
                    0.0243189742481429, 0.0388360843448845,
                    0.902928799013611, 0.0339161423933614,
                ],
                [
                    0.267844198183576, 0.0647694369300529,
                    0.636767508558514, 0.0306188563278576,
                ],
                [
                    0.0234677955730546, 0.0647751604471051,
                    0.390862050671012, 0.520894993308829,
                ],
                [
                    0.0637328952949977, 0.277903669330078,
                    0.594909689021796, 0.0634537463531287,
                ],
                [
                    0.0836788140600551, 0.0660986624146805,
                    0.63005455511099, 0.220167968414275,
                ],
                [
                    0.329379718549198, 0.325119658577025,
                    0.326833504619046, 0.0186671182547306,
                ],
                [
                    0.304169265349782, 0.319194280348931,
                    0.0443833443572082, 0.332253109944079,
                ],
                [
                    0.038288670738245, 0.328388171231222,
                    0.320287433697693, 0.313035724332841,
                ],
                [
                    0.351939197334705, 0.0550990224907257,
                    0.38108430890631, 0.21187747126826,
                ],
                [
                    0.152103811309931, 0.124649963637486,
                    0.201234567364421, 0.522011657688162,
                ],
                [
                    0.624321363553429, 0.0659249231600099,
                    0.2535936747432, 0.0561600385433603,
                ],
                [
                    0.211297658581586, 0.00735452383806937,
                    0.25118449527753, 0.530163322302815,
                ],
                [
                    0.0631999809425695, 0.617455720147269,
                    0.258449148983926, 0.0608951499262361,
                ],
                [
                    0.255820784264986, 0.279420052945988,
                    0.269569929633272, 0.195189233155754,
                ],
                [
                    0.577345781389727, 0.287725094826464,
                    0.0646206380733685, 0.0703084857104406,
                ],
                [
                    0.0651779927633704, 0.594717301875796,
                    0.0666032980076031, 0.273501407353231,
                ],
                [
                    0.530063275481017, 0.0667895997817381,
                    0.0769927171009672, 0.326154407636278,
                ],
                [
                    0.248449540118895, 0.626540201708882,
                    0.0621155331835988, 0.0628947249886239,
                ],
                [
                    0.213041183236186, 0.0600105830202691,
                    0.0258426862607033, 0.701105547482842,
                ],
                [
                    0.0539961408359145, 0.275786300469851,
                    0.0600161491661687, 0.610201409528066,
                ],
                [
                    0.841138951662318, 0.0513252061652029,
                    0.0372647521383555, 0.0702710900341231,
                ],
                [
                    0.0087819577775189, 0.0405760510668179,
                    0.0886003504689102, 0.862041640686753,
                ],
                [
                    0.0228658238140231, 0.903770001332182,
                    0.0293357210831787, 0.0440284537706163,
                ],
                ])
            self.weights = numpy.array([
                0.00709579485165953,
                0.0315094098827064,
                0.0242312868774444,
                0.0488900759024422,
                0.0530333239081694,
                0.0432392966954734,
                0.067135816212557,
                0.0598213476614292,
                0.0626144752813113,
                0.0643340219730875,
                0.0435903980606292,
                0.0225656672781428,
                0.0466131341265807,
                0.112599404494068,
                0.053935010628312,
                0.0497686300915143,
                0.0630663618855205,
                0.0471480304722612,
                0.0255043242670424,
                0.0397140976490823,
                0.0159254791850038,
                0.0104233357236959,
                0.00724127689186697,
                ])
        elif index == 7:
            bary = numpy.array([
                [
                    0.00199682581829981, 0.0192079934885854,
                    0.651334895848238, 0.327460284844877,
                ],
                [
                    0.0609221845854508, 0.323456841789598,
                    0.61517098831187, 0.000449985313081031,
                ],
                [
                    0.063969430325799, 0.0624740225231503,
                    0.812872555571, 0.0606839915800507,
                ],
                [
                    0.23078490023767, 0.0140330844733053,
                    0.566163074530697, 0.189018940758327,
                ],
                [
                    0.323948070989182, 0.0624444127129091,
                    0.586321285830122, 0.0272862304677867,
                ],
                [
                    0.350115304507171, 0.261508769176583,
                    0.0119758768891576, 0.376400049427089,
                ],
                [
                    0.022532983493832, 0.260420587998262,
                    0.564650102467691, 0.152396326040215,
                ],
                [
                    0.500378669849815, 0.258280547367444,
                    0.0826690956073921, 0.158671687175349,
                ],
                [
                    0.289861281908691, 0.397174402994917,
                    0.171048877818779, 0.141915437277613,
                ],
                [
                    0.157241855986003, 0.55045594162486,
                    0.0437434701607319, 0.248558732228405,
                ],
                [
                    0.631548473918005, 0.0258331677317304,
                    0.280405238101906, 0.062213120248359,
                ],
                [
                    0.111251133426943, 0.107462430783153,
                    0.475849161739315, 0.305437274050589,
                ],
                [
                    0.217554444216353, 0.252130530629395,
                    0.448739255383575, 0.0815757697706759,
                ],
                [
                    0.0446302679066366, 0.601823577631812,
                    0.289994034365513, 0.0635521200960386,
                ],
                [
                    0.0762414702839689, 0.0331656998310357,
                    0.274801534897994, 0.615791294987002,
                ],
                [
                    0.437248089764549, 0.109895976327021,
                    0.276571682738858, 0.176284251169573,
                ],
                [
                    0.0740087021391158, 0.41035809599494,
                    0.244761650919342, 0.270871550946603,
                ],
                [
                    0.218812622547504, 0.176438223014948,
                    0.175766110266451, 0.428983044171096,
                ],
                [
                    0.00161353261999009, 0.199110572052883,
                    0.263747375338565, 0.535528519988562,
                ],
                [
                    0.234396497335962, 0.528711306413653,
                    0.216998299345866, 0.0198938969045188,
                ],
                [
                    0.350528406837283, 0.00392965148708786,
                    0.241844613058583, 0.403697328617046,
                ],
                [
                    0.550888978142213, 0.223470202530143,
                    0.225528537697264, 0.000112281630380141,
                ],
                [
                    0.0680111048992614, 0.297785234383524,
                    0.0476494431008923, 0.586554217616322,
                ],
                [
                    0.627983229358597, 0.293770036523707,
                    0.0274823781928344, 0.0507643559248611,
                ],
                [
                    0.599019239879897, 0.0528776293788545,
                    0.0549795828955141, 0.293123547845734,
                ],
                [
                    0.275309810687132, 0.0530001383345468,
                    0.0449776631268801, 0.626712387851441,
                ],
                [
                    0.319658376097012, 0.599100943620026,
                    0.0352137952974546, 0.0460268849855079,
                ],
                [
                    0.062815072845237, 0.820745300741595,
                    0.0589104128256091, 0.057529213587559,
                ],
                [
                    0.824544066695395, 0.0598941950699869,
                    0.0567758666899469, 0.0587858715446707,
                ],
                [
                    0.0521366890580109, 0.0620110919366441,
                    0.0571821545167788, 0.828670064488566,
                ],
                [
                    0.000500433444271841, 0.635521510583761,
                    0.0598944722319085, 0.304083583740058,
                ],
                ])
            self.weights = numpy.array([
                0.00770818116200049,
                0.0120037921882199,
                0.0232168093278622,
                0.0224113653953913,
                0.0232909869573198,
                0.0273299143176464,
                0.0287962835952346,
                0.0429911619639807,
                0.0527816656535537,
                0.0418385316076004,
                0.0207120821637628,
                0.0603015155912097,
                0.0667112071657317,
                0.0314111274554996,
                0.0283127876119325,
                0.0667394894208807,
                0.0641888389354599,
                0.0823381687805698,
                0.0208727051617902,
                0.0245624298859732,
                0.0223486714825842,
                0.0221803191752118,
                0.0369358091114385,
                0.0167020010636449,
                0.033795865302751,
                0.0280611783139331,
                0.0210927658418785,
                0.0205903486322805,
                0.0192028117961788,
                0.0180570774841578,
                0.0125141074543206,
                ])
        elif index == 8:
            bary = numpy.array([
                [
                    0.0176071561268785, 0.00885559427870577,
                    0.948563929799005, 0.024973319795411,
                ],
                [
                    0.189074468870033, 0.0362046719285183,
                    0.731367360036089, 0.043353499165359,
                ],
                [
                    0.230743496794649, 0.611336533691884,
                    0.00557577303043824, 0.152344196483028,
                ],
                [
                    0.0258068488725323, 0.0277767579935654,
                    0.466540585890919, 0.479875807242983,
                ],
                [
                    0.0464861294110928, 0.156486685040066,
                    0.751496536151838, 0.0455306493970033,
                ],
                [
                    0.249637083057875, 0.195546081922602,
                    0.541793182461809, 0.013023652557713,
                ],
                [
                    0.0490853443274963, 0.0414941590182784,
                    0.71717735709395, 0.192243139560275,
                ],
                [
                    0.257916673154309, 0.220977464998818,
                    0.0123959233601955, 0.508709938486678,
                ],
                [
                    0.0431223833778798, 0.415076584269989,
                    0.494799169319991, 0.0470018630321401,
                ],
                [
                    0.199906729032922, 0.479406653352866,
                    0.320095606750398, 0.000591010863814574,
                ],
                [
                    0.123978489327818, 0.0622443994610205,
                    0.403654775010059, 0.410122336201102,
                ],
                [
                    0.0338367380972239, 0.212519226117529,
                    0.50564195098037, 0.248002084804877,
                ],
                [
                    0.382880501165727, 0.397275457461443,
                    0.0817336282047911, 0.138110413168039,
                ],
                [
                    0.472133219549673, 0.0454473742628588,
                    0.435666994545663, 0.0467524116418051,
                ],
                [
                    0.49359008083402, 0.216139692630079,
                    0.0391905731975356, 0.251079653338365,
                ],
                [
                    0.250227446293038, 0.0452907498885836,
                    0.493144767959065, 0.211337035859313,
                ],
                [
                    0.182246049223361, 0.428407770736019,
                    0.0619469615468447, 0.327399218493776,
                ],
                [
                    0.228080184055079, 0.142514629908895,
                    0.128143739766618, 0.501261446269409,
                ],
                [
                    0.0308224720999311, 0.181262191170945,
                    0.25934638915961, 0.528568947569513,
                ],
                [
                    0.164695505900328, 0.249520766079952,
                    0.249905550725755, 0.335878177293964,
                ],
                [
                    0.0424303011456228, 0.48622524586616,
                    0.275236027299907, 0.196108425688311,
                ],
                [
                    0.200330706877803, 0.227462049986755,
                    0.448954528663698, 0.123252714471744,
                ],
                [
                    0.411896203648412, 0.15825909334589,
                    0.207391735140623, 0.222452967865074,
                ],
                [
                    0.511106071913577, 0.0288272589009354,
                    0.229540713072656, 0.230525956112832,
                ],
                [
                    0.48351828029101, 0.229540615063575,
                    0.24201755731748, 0.0449235473279347,
                ],
                [
                    0.209642302870646, 0.485313557638069,
                    0.198619977669231, 0.106424161822054,
                ],
                [
                    0.250471921917321, 0.0226109096366605,
                    0.222434642492779, 0.50448252595324,
                ],
                [
                    0.0367806497347482, 0.720511165717872,
                    0.204368923907325, 0.0383392606400548,
                ],
                [
                    0.461811725168263, 0.465315160413036,
                    0.00542218330717809, 0.0674509311115227,
                ],
                [
                    0.0504550069317247, 0.0393802186845056,
                    0.173195608683351, 0.736969165700418,
                ],
                [
                    0.748574560745763, 0.0454345303521096,
                    0.163299343299354, 0.0426915656027734,
                ],
                [
                    0.0309505292161329, 0.424650054079589,
                    0.136206241225198, 0.40819317547908,
                ],
                [
                    0.0543830156062334, 0.216264148890651,
                    0.0512537651338738, 0.678099070369241,
                ],
                [
                    0.70165677606439, 0.204491813747223,
                    0.0468686532808731, 0.0469827569075136,
                ],
                [
                    0.0447802154960318, 0.719573330071695,
                    0.055990644682102, 0.179655809750171,
                ],
                [
                    0.723709495041749, 0.0462005821486641,
                    0.0434988144519503, 0.186591108357637,
                ],
                [
                    0.0357625708787201, 0.500329672032976,
                    0.00811205075570606, 0.455795706332598,
                ],
                [
                    0.448778007752483, 0.0410502981454823,
                    0.0456853657461182, 0.464486328355917,
                ],
                [
                    0.164386930984808, 0.039856677923423,
                    0.0344820754789425, 0.761274315612826,
                ],
                [
                    0.150637711781425, 0.762367884954453,
                    0.0524383899287033, 0.0345560133354185,
                ],
                [
                    0.41392128343882, 0.498254961782204,
                    0.0797578709669057, 0.00806588381206996,
                ],
                [
                    0.0045711843745157, 0.048689004639022,
                    0.0221620710966624, 0.9245777398898,
                ],
                [
                    0.940808202831602, 0.0300522477759322,
                    0.00671967882215319, 0.0224198705703125,
                ],
                [
                    0.00097187836901502, 0.957381626058303,
                    0.0160079842312982, 0.0256385113413841,
                ],
                ])
            self.weights = numpy.array([
                0.00174518353530565,
                0.0150637694851031,
                0.00987651679488672,
                0.0101289212507486,
                0.0176125361851335,
                0.0156163892037806,
                0.0179888898978599,
                0.0165293668005523,
                0.0225045659680212,
                0.0127993833726196,
                0.0272549359344731,
                0.0322930006408464,
                0.0281856859000071,
                0.0241583439278137,
                0.0322412533439274,
                0.0365500907076331,
                0.0415674904154734,
                0.0390627099489507,
                0.0251390860705886,
                0.0528629287060251,
                0.0327272747535415,
                0.0557924877977275,
                0.0533538024478554,
                0.0271175384854857,
                0.0400988051413301,
                0.0517796239390085,
                0.0227437206345037,
                0.0147199071754273,
                0.00689742831637566,
                0.0169752292580147,
                0.0173892025625115,
                0.0225592387535023,
                0.0234989235386931,
                0.0201467108467895,
                0.0205450363445627,
                0.0178988038072929,
                0.00752115035186082,
                0.0219244986065216,
                0.0137357725582855,
                0.0153884454124109,
                0.0118654206970732,
                0.00254690051934298,
                0.00207908456701888,
                0.00151394539511506,
                ])
        elif index == 9:
            bary = numpy.array([
                [
                    0.0403857712760577, 0.223347667813601,
                    0.723724094807067, 0.0125424661032744,
                ],
                [
                    0.0419547320076876, 0.0420664854098785,
                    0.875196026528405, 0.0407827560540285,
                ],
                [
                    0.213353780462222, 0.0149238239784768,
                    0.72761122983064, 0.0441111657286617,
                ],
                [
                    0.0116791877673534, 0.0396771205159151,
                    0.47317164143189, 0.475472050284842,
                ],
                [
                    0.0401113782404464, 0.0331316669554182,
                    0.713691124061697, 0.213065830742438,
                ],
                [
                    0.0254593439902073, 0.18095213245167,
                    0.682058612968494, 0.111529910589629,
                ],
                [
                    0.612340802182086, 0.143214340397823,
                    0.000666217908743757, 0.243778639511346,
                ],
                [
                    0.380737034941527, 0.194621680265471,
                    0.420505174202867, 0.00413611059013532,
                ],
                [
                    0.00580738125855198, 0.435066176799439,
                    0.447184150342226, 0.111942291599784,
                ],
                [
                    0.226837319964301, 0.416782083325252,
                    0.00779839281859621, 0.348582203891851,
                ],
                [
                    0.192371795270148, 0.124285648730518,
                    0.656138223504377, 0.0272043324949568,
                ],
                [
                    0.0610766003173578, 0.444345247810464,
                    0.474856882867235, 0.0197212690049435,
                ],
                [
                    0.356752136898719, 0.132883433039591,
                    0.0205145714017887, 0.489849858659902,
                ],
                [
                    0.361950881374389, 0.0155201159921829,
                    0.39243368052707, 0.230095322106358,
                ],
                [
                    0.458244669513536, 0.0366754648901354,
                    0.463585726400412, 0.041494139195917,
                ],
                [
                    0.103011513806394, 0.231314248871532,
                    0.00286457798839654, 0.662809659333677,
                ],
                [
                    0.183985390917369, 0.0528125899288537,
                    0.579144072483221, 0.184057946670556,
                ],
                [
                    0.124235622988202, 0.0274327152138568,
                    0.412543124292686, 0.435788537505256,
                ],
                [
                    0.0391203352168918, 0.17990450159705,
                    0.476509401004044, 0.304465762182014,
                ],
                [
                    0.141716159874522, 0.227159869315033,
                    0.517598979528501, 0.113524991281944,
                ],
                [
                    0.222247573716264, 0.374496979076987,
                    0.363925352762609, 0.0393300944441401,
                ],
                [
                    0.45874567579555, 0.360156713211527,
                    0.0368998311021246, 0.144197779890798,
                ],
                [
                    0.336434527121508, 0.228984009070693,
                    0.0827335053473291, 0.35184795846047,
                ],
                [
                    0.270966213108107, 0.333619190568023,
                    0.199823030101454, 0.195591566222416,
                ],
                [
                    0.166874972870679, 0.572956368580224,
                    0.0777442683512465, 0.182424390197851,
                ],
                [
                    0.152468317173523, 0.147687068101471,
                    0.09407076219108, 0.605773852533925,
                ],
                [
                    0.0834237885206363, 0.422228601671921,
                    0.303141864574498, 0.191205745232944,
                ],
                [
                    0.363356680112364, 0.414761922299037,
                    0.162526363750601, 0.0593550338379973,
                ],
                [
                    0.10961245832859, 0.353700358434538,
                    0.117934406191924, 0.418752777044948,
                ],
                [
                    0.181977223477481, 0.165062840907306,
                    0.309246440579088, 0.343713495036125,
                ],
                [
                    0.378744394121169, 0.143482922419707,
                    0.34694080625476, 0.130831877204364,
                ],
                [
                    0.0458087378144924, 0.130665687575531,
                    0.235477104647691, 0.588048469962286,
                ],
                [
                    0.557160321974948, 0.132504385419056,
                    0.12240359518817, 0.187931697417827,
                ],
                [
                    0.0153895998106676, 0.339432294095281,
                    0.241869511998084, 0.403308594095967,
                ],
                [
                    0.351609177188374, 0.0550373938296805,
                    0.196941061937647, 0.396412367044298,
                ],
                [
                    0.103157146828274, 0.645449463437002,
                    0.202551715395404, 0.0488416743393194,
                ],
                [
                    0.00689136683929516, 0.72038072033592,
                    0.244078663540675, 0.0286492492841097,
                ],
                [
                    0.709802719558639, 0.0448310591511101,
                    0.211317992359171, 0.03404822893108,
                ],
                [
                    0.565516352082529, 0.215845533526719,
                    0.186190938826938, 0.0324471755638134,
                ],
                [
                    0.604426299960602, 0.0175868132550817,
                    0.20371686346026, 0.174270023324056,
                ],
                [
                    0.0313878366926266, 0.0230247668978293,
                    0.201015109996088, 0.744572286413456,
                ],
                [
                    0.276077439823471, 0.633534755777452,
                    0.0202948586616078, 0.070092945737469,
                ],
                [
                    0.183854997817626, 0.020944276301084,
                    0.170438917807265, 0.624761808074025,
                ],
                [
                    0.0196505604208404, 0.644358309838968,
                    0.134094535449186, 0.201896594291005,
                ],
                [
                    0.0513736820386085, 0.737898449375068,
                    0.0105248700657296, 0.200202998520594,
                ],
                [
                    0.273754969152287, 0.586619406367851,
                    0.133173713253393, 0.00645191122646915,
                ],
                [
                    0.730498994262046, 0.187147292114549,
                    0.037069865897692, 0.0452838477257126,
                ],
                [
                    0.0333272032037566, 0.483732396697471,
                    0.0372285314523825, 0.44571186864639,
                ],
                [
                    0.23077311207171, 0.0317115615353829,
                    0.0291491310298444, 0.708366195363063,
                ],
                [
                    0.751889344488304, 0.0302097149701842,
                    0.039313282697247, 0.178587657844265,
                ],
                [
                    0.155578908302726, 0.783023838067657,
                    0.0372273140607443, 0.024169939568873,
                ],
                [
                    0.500770113322833, 0.0244822382813636,
                    0.0493321397035171, 0.425415508692286,
                ],
                [
                    0.515285061557277, 0.440521404847323,
                    0.0330743569254283, 0.0111191766699716,
                ],
                [
                    0.00837326895113094, 0.218303550548395,
                    0.0638376081133778, 0.709485572387096,
                ],
                [
                    0.0458590194760227, 0.0458983297924952,
                    0.039300651257047, 0.868941999474435,
                ],
                [
                    0.034740224418429, 0.873984284469283,
                    0.0480297338872506, 0.0432457572250377,
                ],
                [
                    0.884773595262314, 0.0374671558210411,
                    0.0431398494500383, 0.0346193994666062,
                ],
                ])
            self.weights = numpy.array([
                0.00585015968298785,
                0.00709368813491062,
                0.00710578009623748,
                0.00719978622104616,
                0.0117625365392465,
                0.0125729071224739,
                0.00788014097822491,
                0.0098253611048022,
                0.00977940257414991,
                0.0142664460853428,
                0.0148955483507123,
                0.0116249531334101,
                0.0132862503909676,
                0.0151187789916045,
                0.0157173772734417,
                0.00819830028372906,
                0.0262804926837485,
                0.0198888106065709,
                0.0263755884179657,
                0.0326397088280212,
                0.0252926268168459,
                0.0253925114063473,
                0.0352203626334114,
                0.0418753477132892,
                0.0318453046101087,
                0.0281272186457365,
                0.0382210859139534,
                0.0256518819817813,
                0.0352793647430814,
                0.0491021245617486,
                0.0452113830792155,
                0.0230094892217704,
                0.0357165326982349,
                0.0164753907780877,
                0.033121074422278,
                0.0223807110172663,
                0.00429720962642725,
                0.0129875311378096,
                0.0213542997099183,
                0.0129752582233438,
                0.00704677269435751,
                0.0103114858636024,
                0.013677235408553,
                0.0153837327949132,
                0.00714003971619962,
                0.00703165129466608,
                0.0130858695430802,
                0.0132739160467493,
                0.00916519439529406,
                0.00914657068489851,
                0.00544666268677799,
                0.0132311029056477,
                0.00660114055543908,
                0.00829623576285018,
                0.008021210535256,
                0.00674140042162541,
                0.00550105224984015,
                ])
        elif index == 10:
            bary = numpy.array([
                [
                    0.112124386464979, 0.532588923650052,
                    0.236241958845761, 0.119044731039208,
                ],
                [
                    0.532588923649936, 0.119044731039276,
                    0.236241958845661, 0.112124386465127,
                ],
                [
                    0.119044731039282, 0.112124386465023,
                    0.236241958845699, 0.532588923649996,
                ],
                [
                    0.114537986315841, 0.490895346760997,
                    0.024954022067238, 0.369612644855923,
                ],
                [
                    0.490895346760553, 0.369612644856217,
                    0.0249540220672398, 0.11453798631599,
                ],
                [
                    0.369612644856148, 0.114537986316025,
                    0.0249540220671651, 0.490895346760662,
                ],
                [
                    0.126639490878871, 0.0307019608706964,
                    0.811477229498194, 0.0311813187522381,
                ],
                [
                    0.0307019608707451, 0.0311813187522109,
                    0.811477229497971, 0.126639490879073,
                ],
                [
                    0.0311813187522021, 0.126639490878582,
                    0.81147722949849, 0.0307019608707261,
                ],
                [
                    0.620258301289887, 0.329984187563428,
                    0.0324034637009129, 0.017354047445772,
                ],
                [
                    0.329984187563711, 0.0173540474457835,
                    0.0324034637009263, 0.620258301289579,
                ],
                [
                    0.0173540474456847, 0.620258301290051,
                    0.0324034637009163, 0.329984187563348,
                ],
                [
                    0.45348592435879, 0.298635089789364,
                    0.128556392359953, 0.119322593491894,
                ],
                [
                    0.298635089789335, 0.119322593491917,
                    0.128556392359763, 0.453485924358984,
                ],
                [
                    0.119322593491742, 0.453485924358994,
                    0.128556392359958, 0.298635089789306,
                ],
                [
                    0.404377014488368, 0.41747625187081,
                    0.161337142171161, 0.0168095914696608,
                ],
                [
                    0.417476251870908, 0.0168095914696486,
                    0.161337142171081, 0.404377014488362,
                ],
                [
                    0.016809591469599, 0.404377014488366,
                    0.161337142171075, 0.41747625187096,
                ],
                [
                    0.780572245824388, 0.0351895822687681,
                    0.0330735998255433, 0.1511645720813,
                ],
                [
                    0.0351895822687085, 0.15116457208164,
                    0.033073599825577, 0.780572245824075,
                ],
                [
                    0.151164572081518, 0.780572245824151,
                    0.0330735998255729, 0.0351895822687586,
                ],
                [
                    0.633928034390357, 0.0230972587755699,
                    0.17336085927366, 0.169613847560413,
                ],
                [
                    0.0230972587755565, 0.169613847560395,
                    0.173360859273732, 0.633928034390317,
                ],
                [
                    0.169613847560402, 0.633928034390302,
                    0.173360859273759, 0.0230972587755374,
                ],
                [
                    0.633587565314398, 0.177018351018918,
                    0.165053055346399, 0.0243410283202849,
                ],
                [
                    0.177018351018947, 0.0243410283202735,
                    0.165053055346375, 0.633587565314405,
                ],
                [
                    0.0243410283202645, 0.633587565314261,
                    0.165053055346508, 0.177018351018967,
                ],
                [
                    0.0302939377577043, 0.351030926661914,
                    0.0326605800532647, 0.586014555527117,
                ],
                [
                    0.351030926661772, 0.586014555527252,
                    0.0326605800532898, 0.0302939377576865,
                ],
                [
                    0.586014555527477, 0.0302939377577213,
                    0.032660580053272, 0.351030926661529,
                ],
                [
                    0.302001907326645, 0.328345521473841,
                    0.303026128942095, 0.0666264422574188,
                ],
                [
                    0.328345521473828, 0.0666264422574022,
                    0.303026128941855, 0.302001907326915,
                ],
                [
                    0.0666264422573126, 0.302001907326744,
                    0.303026128942078, 0.328345521473865,
                ],
                [
                    0.413701128449536, 0.0126764316485514,
                    0.409075224011871, 0.164547215890041,
                ],
                [
                    0.0126764316485456, 0.164547215889915,
                    0.409075224011948, 0.413701128449591,
                ],
                [
                    0.164547215890011, 0.413701128449435,
                    0.409075224012006, 0.0126764316485479,
                ],
                [
                    0.120713111635809, 0.339513062621138,
                    0.411092657494867, 0.128681168248186,
                ],
                [
                    0.339513062620902, 0.12868116824813,
                    0.411092657494958, 0.120713111636009,
                ],
                [
                    0.128681168248194, 0.120713111635856,
                    0.411092657495011, 0.33951306262094,
                ],
                [
                    0.150268790251704, 0.0830249468821678,
                    0.0384967818689647, 0.728209480997164,
                ],
                [
                    0.0830249468819636, 0.728209480997427,
                    0.0384967818689939, 0.150268790251615,
                ],
                [
                    0.728209480997069, 0.150268790251755,
                    0.0384967818689953, 0.0830249468821806,
                ],
                [
                    0.515916816614274, 0.132467010744771,
                    0.107446461585059, 0.244169711055896,
                ],
                [
                    0.132467010744642, 0.244169711055904,
                    0.107446461585154, 0.5159168166143,
                ],
                [
                    0.244169711055665, 0.515916816614441,
                    0.107446461585192, 0.132467010744702,
                ],
                [
                    0.0122804285624344, 0.41260083617917,
                    0.397904362185717, 0.177214373072678,
                ],
                [
                    0.412600836179202, 0.177214373072706,
                    0.397904362185566, 0.0122804285625255,
                ],
                [
                    0.177214373072742, 0.012280428562444,
                    0.397904362185594, 0.41260083617922,
                ],
                [
                    0.0322052864177144, 0.814902282940503,
                    0.119376795136335, 0.0335156355054478,
                ],
                [
                    0.814902282940798, 0.03351563550542,
                    0.11937679513607, 0.0322052864177124,
                ],
                [
                    0.0335156355054175, 0.0322052864177284,
                    0.119376795135861, 0.814902282940993,
                ],
                [
                    0.175799607249302, 0.0293551168604181,
                    0.620841510435641, 0.174003765454638,
                ],
                [
                    0.0293551168603722, 0.174003765454579,
                    0.620841510435722, 0.175799607249327,
                ],
                [
                    0.174003765454628, 0.175799607249215,
                    0.620841510435776, 0.0293551168603806,
                ],
                [
                    0.0311446124900868, 0.599273801139227,
                    0.336597526383028, 0.0329840599876588,
                ],
                [
                    0.599273801139516, 0.0329840599876767,
                    0.336597526382707, 0.0311446124901005,
                ],
                [
                    0.0329840599876792, 0.0311446124900787,
                    0.336597526382512, 0.59927380113973,
                ],
                [
                    0.337948919826428, 0.0357390844115414,
                    0.592532870170898, 0.0337791255911334,
                ],
                [
                    0.0357390844115456, 0.0337791255911184,
                    0.592532870170714, 0.337948919826622,
                ],
                [
                    0.0337791255911396, 0.337948919826095,
                    0.592532870171222, 0.0357390844115429,
                ],
                [
                    0.55966008885546, 0.180760249570227,
                    0.00743879573116732, 0.252140865843146,
                ],
                [
                    0.180760249570056, 0.252140865843321,
                    0.00743879573119961, 0.559660088855423,
                ],
                [
                    0.252140865843033, 0.559660088855703,
                    0.00743879573121437, 0.18076024957005,
                ],
                [
                    0.946719848292354, 0.00666708044835105,
                    0.00806750556190488, 0.0385455656973901,
                ],
                [
                    0.00666708044865899, 0.0385455656973744,
                    0.00806750556177988, 0.946719848292187,
                ],
                [
                    0.0385455656974801, 0.946719848291852,
                    0.00806750556217394, 0.00666708044849378,
                ],
                [
                    0.874025132764932, 0.103593660247555,
                    0.0185543150543456, 0.00382689193316734,
                ],
                [
                    0.103593660248003, 0.00382689193304392,
                    0.0185543150543368, 0.874025132764616,
                ],
                [
                    0.00382689193302969, 0.874025132765168,
                    0.0185543150543571, 0.103593660247446,
                ],
                [
                    0.257071980762428, 0.257071980762551,
                    0.228784057712463, 0.257071980762559,
                ],
                [
                    0.00484488952776817, 0.0048448895275733,
                    0.985465331416737, 0.00484488952792108,
                ],
                [
                    0.166959769317206, 0.16695976931758,
                    0.499120692048112, 0.166959769317101,
                ],
                [
                    0.318206200820324, 0.318206200820592,
                    0.0453813975386287, 0.318206200820455,
                ],
                [
                    0.133659949532392, 0.133659949532611,
                    0.599020151402527, 0.133659949532469,
                ],
                ])
            self.weights = numpy.array([
                0.0206705933360102,
                0.0206705933360524,
                0.0206705933360491,
                0.0123879646659701,
                0.0123879646659734,
                0.0123879646659471,
                0.00662034590248817,
                0.00662034590249252,
                0.00662034590248503,
                0.00613915423984513,
                0.00613915423984776,
                0.00613915423982548,
                0.0254070758511639,
                0.025407075851157,
                0.0254070758511519,
                0.0125681159062517,
                0.0125681159062387,
                0.0125681159062194,
                0.00698496100499754,
                0.00698496100500238,
                0.00698496100500363,
                0.0131485181666441,
                0.0131485181666366,
                0.0131485181666345,
                0.0137067046817388,
                0.0137067046817351,
                0.0137067046817304,
                0.00913797993619988,
                0.00913797993620436,
                0.00913797993620943,
                0.0268269448377026,
                0.0268269448377089,
                0.0268269448377121,
                0.0112421913509066,
                0.0112421913508941,
                0.0112421913509016,
                0.0280925624549168,
                0.0280925624549413,
                0.0280925624549464,
                0.0125034790003,
                0.012503479000285,
                0.0125034790002917,
                0.0273232991949671,
                0.0273232991949706,
                0.0273232991949802,
                0.0118169631889114,
                0.011816963188952,
                0.0118169631889198,
                0.00714877145464674,
                0.00714877145463965,
                0.00714877145464187,
                0.016664429455077,
                0.0166644294550532,
                0.0166644294550571,
                0.0101749860913436,
                0.0101749860913507,
                0.0101749860913456,
                0.0113922185850228,
                0.0113922185850181,
                0.0113922185850242,
                0.00821204732481041,
                0.00821204732482145,
                0.00821204732482332,
                0.000790099114745726,
                0.000790099114751852,
                0.000790099114756652,
                0.00169256583915585,
                0.00169256583914716,
                0.00169256583914468,
                0.0465785219844192,
                0.00038191631629908,
                0.0117551058920687,
                0.0279115676882241,
                0.0114169733674978,
                ])
        elif index == 11:
            bary = numpy.array([
                [
                    0.728873249484653, 0.116023081854425,
                    0.135592364575494, 0.0195113040854278,
                ],
                [
                    0.116023081854311, 0.019511304085456,
                    0.135592364575472, 0.72887324948476,
                ],
                [
                    0.0195113040853993, 0.728873249484144,
                    0.135592364576106, 0.11602308185435,
                ],
                [
                    0.473392726282396, 0.00762104076479343,
                    0.506837355763621, 0.01214887718919,
                ],
                [
                    0.00762104076469388, 0.012148877189292,
                    0.506837355764064, 0.473392726281951,
                ],
                [
                    0.0121488771892421, 0.473392726283015,
                    0.506837355763665, 0.00762104076407806,
                ],
                [
                    0.0168886401897685, 0.363347525696901,
                    0.280802863730816, 0.338960970382515,
                ],
                [
                    0.363347525697624, 0.338960970382143,
                    0.280802863730395, 0.0168886401898389,
                ],
                [
                    0.338960970382072, 0.0168886401897474,
                    0.280802863730256, 0.363347525697924,
                ],
                [
                    0.680860745134595, 0.0173048958376222,
                    0.157779396731644, 0.144054962296138,
                ],
                [
                    0.0173048958374878, 0.14405496229638,
                    0.15777939673188, 0.680860745134253,
                ],
                [
                    0.144054962296286, 0.680860745134503,
                    0.157779396731746, 0.0173048958374647,
                ],
                [
                    0.474182128645854, 0.142994640166548,
                    0.144348866503299, 0.238474364684298,
                ],
                [
                    0.142994640166434, 0.238474364684594,
                    0.144348866502935, 0.474182128646037,
                ],
                [
                    0.238474364684246, 0.474182128645578,
                    0.144348866503849, 0.142994640166326,
                ],
                [
                    0.811198981443021, 0.0177983897923629,
                    0.145295910885661, 0.0257067178789547,
                ],
                [
                    0.0177983897923111, 0.025706717879011,
                    0.145295910885563, 0.811198981443115,
                ],
                [
                    0.0257067178790229, 0.811198981442227,
                    0.145295910886405, 0.0177983897923449,
                ],
                [
                    0.494502062127405, 0.0295177425032737,
                    0.296998009659033, 0.178982185710289,
                ],
                [
                    0.0295177425035284, 0.178982185709863,
                    0.296998009659455, 0.494502062127154,
                ],
                [
                    0.178982185709254, 0.494502062126533,
                    0.296998009660745, 0.0295177425034678,
                ],
                [
                    0.556351869431587, 0.268993301708489,
                    0.0221892132299926, 0.152465615629931,
                ],
                [
                    0.268993301708777, 0.152465615629865,
                    0.0221892132300191, 0.556351869431339,
                ],
                [
                    0.152465615629878, 0.556351869431363,
                    0.0221892132301095, 0.268993301708649,
                ],
                [
                    0.121338199233653, 0.0272384438972301,
                    0.822137157904796, 0.0292861989643212,
                ],
                [
                    0.0272384438973111, 0.0292861989641832,
                    0.822137157904945, 0.121338199233561,
                ],
                [
                    0.0292861989645277, 0.121338199237199,
                    0.822137157900739, 0.0272384438975338,
                ],
                [
                    0.0296027258670734, 0.544675004555141,
                    0.227882722511225, 0.19783954706656,
                ],
                [
                    0.544675004555975, 0.197839547066041,
                    0.227882722510874, 0.0296027258671096,
                ],
                [
                    0.197839547066301, 0.0296027258670368,
                    0.227882722510613, 0.544675004556049,
                ],
                [
                    0.828341131139443, 0.0118674337483947,
                    0.0334920286219499, 0.126299406490213,
                ],
                [
                    0.0118674337485698, 0.126299406490286,
                    0.033492028621908, 0.828341131139236,
                ],
                [
                    0.126299406490289, 0.828341131139333,
                    0.0334920286218663, 0.0118674337485122,
                ],
                [
                    0.498482050332391, 0.0322988133183324,
                    0.132050066271644, 0.337169070077632,
                ],
                [
                    0.0322988133182837, 0.337169070077692,
                    0.132050066271586, 0.498482050332438,
                ],
                [
                    0.337169070077169, 0.49848205033292,
                    0.132050066271644, 0.0322988133182673,
                ],
                [
                    0.0194238351514799, 0.556669403476659,
                    0.0774013887211524, 0.346505372650708,
                ],
                [
                    0.556669403476599, 0.346505372650919,
                    0.0774013887210278, 0.0194238351514536,
                ],
                [
                    0.346505372651121, 0.0194238351515506,
                    0.0774013887207089, 0.556669403476619,
                ],
                [
                    0.737515826090928, 0.0932838602527992,
                    0.0118757474130086, 0.157324566243265,
                ],
                [
                    0.0932838602532346, 0.157324566243232,
                    0.0118757474130362, 0.737515826090497,
                ],
                [
                    0.157324566242965, 0.737515826090206,
                    0.0118757474136774, 0.0932838602531518,
                ],
                [
                    0.280166444545332, 0.0338895066707502,
                    0.657524551760272, 0.0284194970236465,
                ],
                [
                    0.0338895066708348, 0.0284194970236365,
                    0.657524551760484, 0.280166444545045,
                ],
                [
                    0.0284194970232859, 0.280166444548593,
                    0.657524551757306, 0.0338895066708156,
                ],
                [
                    0.127545627361564, 0.310774423669185,
                    0.260990145113876, 0.300689803855375,
                ],
                [
                    0.310774423669647, 0.300689803854399,
                    0.260990145114484, 0.12754562736147,
                ],
                [
                    0.30068980385497, 0.127545627361447,
                    0.260990145113821, 0.310774423669763,
                ],
                [
                    0.491088052617866, 0.286494911377532,
                    0.11082033247165, 0.111596703532952,
                ],
                [
                    0.286494911377242, 0.111596703533136,
                    0.110820332471535, 0.491088052618087,
                ],
                [
                    0.111596703533014, 0.491088052617963,
                    0.110820332471767, 0.286494911377257,
                ],
                [
                    0.460111304675021, 0.12553611316684,
                    0.299470385376176, 0.114882196781963,
                ],
                [
                    0.125536113167282, 0.114882196781783,
                    0.299470385375898, 0.460111304675036,
                ],
                [
                    0.114882196781495, 0.460111304673332,
                    0.299470385377665, 0.125536113167508,
                ],
                [
                    0.0406042421911239, 0.250053241237449,
                    0.458580906651289, 0.250761609920138,
                ],
                [
                    0.250053241237633, 0.250761609920117,
                    0.458580906651254, 0.0406042421909956,
                ],
                [
                    0.250761609920906, 0.0406042421910061,
                    0.458580906650393, 0.250053241237695,
                ],
                [
                    0.635319477206719, 0.0234461159320501,
                    0.0326609860400843, 0.308573420821147,
                ],
                [
                    0.0234461159321118, 0.308573420821199,
                    0.0326609860399893, 0.6353194772067,
                ],
                [
                    0.308573420821234, 0.635319477206775,
                    0.0326609860399005, 0.0234461159320906,
                ],
                [
                    0.309093680236532, 0.0902935356263497,
                    0.507996039113848, 0.0926167450232704,
                ],
                [
                    0.0902935356265847, 0.0926167450230192,
                    0.507996039113706, 0.30909368023669,
                ],
                [
                    0.0926167450231032, 0.30909368023533,
                    0.507996039115837, 0.0902935356257293,
                ],
                [
                    0.67783513645382, 0.100235474598686,
                    0.101178135308516, 0.120751253638979,
                ],
                [
                    0.100235474598534, 0.12075125363903,
                    0.101178135308674, 0.677835136453761,
                ],
                [
                    0.120751253638675, 0.677835136452938,
                    0.101178135309797, 0.10023547459859,
                ],
                [
                    0.0121600892353425, 0.154928587401345,
                    0.67495628076497, 0.157955042598343,
                ],
                [
                    0.154928587401735, 0.157955042597938,
                    0.674956280765045, 0.0121600892352808,
                ],
                [
                    0.157955042598642, 0.0121600892351608,
                    0.674956280764345, 0.154928587401852,
                ],
                [
                    0.493695627079059, 0.138106941917312,
                    0.0327366341722219, 0.335460796831406,
                ],
                [
                    0.138106941917413, 0.335460796831543,
                    0.0327366341721367, 0.493695627078907,
                ],
                [
                    0.335460796831434, 0.493695627078928,
                    0.0327366341722014, 0.138106941917437,
                ],
                [
                    0.422621045899046, 0.116898196693367,
                    0.450468335150446, 0.0100124222571409,
                ],
                [
                    0.116898196693389, 0.0100124222571166,
                    0.450468335150403, 0.422621045899092,
                ],
                [
                    0.0100124222569327, 0.422621045898728,
                    0.450468335150789, 0.11689819669355,
                ],
                [
                    0.00607257838916173, 0.105521930421362,
                    0.482547152473874, 0.405858338715603,
                ],
                [
                    0.105521930421263, 0.405858338714324,
                    0.482547152475786, 0.00607257838862685,
                ],
                [
                    0.40585833871604, 0.00607257838914559,
                    0.482547152473637, 0.105521930421177,
                ],
                [
                    0.906620021088922, 0.0388428646249606,
                    0.0279126021220965, 0.0266245121640208,
                ],
                [
                    0.0388428646249556, 0.0266245121640002,
                    0.0279126021220656, 0.906620021088979,
                ],
                [
                    0.0266245121640047, 0.906620021088839,
                    0.0279126021222462, 0.0388428646249105,
                ],
                [
                    0.757055676475516, 0.185161386691705,
                    0.0260784340060858, 0.0317045028266932,
                ],
                [
                    0.185161386691674, 0.0317045028266919,
                    0.0260784340060996, 0.757055676475535,
                ],
                [
                    0.0317045028266906, 0.757055676475585,
                    0.0260784340061994, 0.185161386691525,
                ],
                [
                    0.613355585987273, 0.0370774799197033,
                    0.314724910389794, 0.0348420237032293,
                ],
                [
                    0.037077479919721, 0.0348420237031944,
                    0.314724910389817, 0.613355585987268,
                ],
                [
                    0.0348420237032176, 0.613355585985641,
                    0.314724910391352, 0.0370774799197898,
                ],
                [
                    0.0341321238405652, 0.528053533786363,
                    0.0041249745082722, 0.4336893678648,
                ],
                [
                    0.528053533786073, 0.433689367865033,
                    0.0041249745082621, 0.0341321238406326,
                ],
                [
                    0.433689367865469, 0.0341321238406368,
                    0.00412497450795262, 0.528053533785941,
                ],
                [
                    0.0217435616197467, 0.0217435616212349,
                    0.934769315139362, 0.021743561619656,
                ],
                [
                    0.113969534812368, 0.113969534811609,
                    0.658091395563691, 0.113969534812332,
                ],
                [
                    0.327771112724207, 0.327771112724047,
                    0.0166866618275801, 0.327771112724166,
                ],
                [
                    0.296008469913471, 0.296008469913485,
                    0.111974590259687, 0.296008469913357,
                ],
                [
                    0.196826864504454, 0.19682686450449,
                    0.409519406486427, 0.19682686450463,
                ],
                ])
            self.weights = numpy.array([
                0.00637292530335371,
                0.00637292530335911,
                0.00637292530337129,
                0.00146352947038229,
                0.00146352947038678,
                0.00146352947032248,
                0.00976499154298919,
                0.00976499154303561,
                0.00976499154296398,
                0.00701855882624452,
                0.00701855882623061,
                0.0070185588262267,
                0.0196918030926611,
                0.0196918030926224,
                0.0196918030927788,
                0.00316795225578531,
                0.00316795225578524,
                0.00316795225580605,
                0.0116977958341326,
                0.0116977958341842,
                0.0116977958342907,
                0.011242243277915,
                0.01124224327791,
                0.0112422432779479,
                0.00433961113962316,
                0.00433961113961477,
                0.00433961113972021,
                0.0124290247483488,
                0.012429024748352,
                0.0124290247483379,
                0.0026559268793122,
                0.00265592687933327,
                0.00265592687932271,
                0.0128988396346887,
                0.0128988396346839,
                0.0128988396347081,
                0.00830489168415584,
                0.0083048916841537,
                0.0083048916841826,
                0.00514249768733537,
                0.00514249768734461,
                0.00514249768746952,
                0.00633397798193504,
                0.00633397798193941,
                0.00633397798179939,
                0.0275842823005871,
                0.0275842823005925,
                0.0275842823006,
                0.0200503514292947,
                0.0200503514292504,
                0.020050351429261,
                0.0216491227212618,
                0.0216491227212519,
                0.0216491227212978,
                0.0173573262921592,
                0.0173573262920914,
                0.0173573262921232,
                0.00607720876951255,
                0.00607720876951442,
                0.00607720876949382,
                0.0174108339520662,
                0.0174108339520814,
                0.0174108339520445,
                0.0152045953549939,
                0.0152045953550004,
                0.0152045953549907,
                0.00720176444101583,
                0.00720176444098691,
                0.00720176444098596,
                0.0155827228273156,
                0.0155827228272887,
                0.0155827228273276,
                0.00722554275754135,
                0.00722554275753895,
                0.00722554275747397,
                0.00511355126018984,
                0.00511355126003714,
                0.0051135512601792,
                0.00279376493792108,
                0.00279376493791642,
                0.00279376493793115,
                0.00607705350355771,
                0.00607705350355829,
                0.00607705350357844,
                0.00903093460916613,
                0.00903093460917312,
                0.00903093460920998,
                0.00327032615678453,
                0.00327032615678126,
                0.00327032615674194,
                0.00111123046588825,
                0.0179962275149355,
                0.0116375079842378,
                0.0297645933126211,
                0.0270285887056,
                ])
        elif index == 12:
            bary = numpy.array([
                [
                    0.522471551355402, 0.431274828111507,
                    0.0108332023128508, 0.0354204182202404,
                ],
                [
                    0.43127482811151, 0.0354204182202372,
                    0.0108332023128508, 0.522471551355402,
                ],
                [
                    0.0354204182202329, 0.522471551355408,
                    0.0108332023128462, 0.431274828111513,
                ],
                [
                    0.102169569094289, 0.0288780033877441,
                    0.247431243635563, 0.621521183882403,
                ],
                [
                    0.0288780033877445, 0.621521183882406,
                    0.247431243635559, 0.102169569094291,
                ],
                [
                    0.621521183882401, 0.102169569094283,
                    0.247431243635572, 0.0288780033877442,
                ],
                [
                    0.410693314090151, 0.0895525091070139,
                    0.364760249193369, 0.134993927609465,
                ],
                [
                    0.0895525091070089, 0.13499392760946,
                    0.364760249193378, 0.410693314090153,
                ],
                [
                    0.134993927609458, 0.410693314090152,
                    0.364760249193383, 0.0895525091070077,
                ],
                [
                    0.0765677842092839, 0.260055987362752,
                    0.0619341779789965, 0.601442050448968,
                ],
                [
                    0.260055987362767, 0.601442050448967,
                    0.0619341779789937, 0.0765677842092726,
                ],
                [
                    0.601442050448956, 0.0765677842092811,
                    0.0619341779789934, 0.260055987362769,
                ],
                [
                    0.114767516763106, 0.259903154085836,
                    0.233453931951302, 0.391875397199756,
                ],
                [
                    0.259903154085834, 0.391875397199764,
                    0.233453931951304, 0.114767516763098,
                ],
                [
                    0.391875397199756, 0.114767516763099,
                    0.23345393195131, 0.259903154085834,
                ],
                [
                    0.655079631029842, 0.30506096657721,
                    0.0264703515098401, 0.0133890508831078,
                ],
                [
                    0.305060966577206, 0.0133890508831075,
                    0.0264703515098399, 0.655079631029847,
                ],
                [
                    0.0133890508831104, 0.655079631029834,
                    0.0264703515098407, 0.305060966577215,
                ],
                [
                    0.602148546636171, 0.0799434865871736,
                    0.197260085334115, 0.12064788144254,
                ],
                [
                    0.0799434865871708, 0.120647881442537,
                    0.197260085334122, 0.60214854663617,
                ],
                [
                    0.120647881442539, 0.602148546636172,
                    0.197260085334123, 0.0799434865871666,
                ],
                [
                    0.545950460998922, 0.0201343353228147,
                    0.315572302857257, 0.118342900821007,
                ],
                [
                    0.0201343353228129, 0.11834290082101,
                    0.31557230285726, 0.545950460998917,
                ],
                [
                    0.118342900821009, 0.545950460998917,
                    0.315572302857261, 0.0201343353228126,
                ],
                [
                    0.481042632269802, 0.233792173057883,
                    0.269781924982593, 0.0153832696897217,
                ],
                [
                    0.233792173057882, 0.015383269689725,
                    0.26978192498259, 0.481042632269804,
                ],
                [
                    0.0153832696897247, 0.481042632269803,
                    0.269781924982592, 0.23379217305788,
                ],
                [
                    0.100249754372136, 0.220841759313371,
                    0.451459949509977, 0.227448536804516,
                ],
                [
                    0.220841759313376, 0.227448536804515,
                    0.451459949509971, 0.100249754372138,
                ],
                [
                    0.227448536804512, 0.100249754372136,
                    0.451459949509978, 0.220841759313374,
                ],
                [
                    0.426127974255652, 0.130127094762025,
                    0.127383168726021, 0.316361762256302,
                ],
                [
                    0.130127094762023, 0.316361762256309,
                    0.127383168726014, 0.426127974255654,
                ],
                [
                    0.316361762256301, 0.426127974255657,
                    0.127383168726015, 0.130127094762026,
                ],
                [
                    0.0746260513272087, 0.128036327678861,
                    0.0802610178929508, 0.717076603100979,
                ],
                [
                    0.128036327678866, 0.717076603100972,
                    0.0802610178929499, 0.0746260513272125,
                ],
                [
                    0.717076603100971, 0.0746260513272115,
                    0.08026101789295, 0.128036327678868,
                ],
                [
                    0.851985048949244, 0.0591969943784215,
                    0.0176569601908347, 0.0711609964814997,
                ],
                [
                    0.0591969943784213, 0.0711609964814978,
                    0.0176569601908337, 0.851985048949247,
                ],
                [
                    0.0711609964814969, 0.851985048949248,
                    0.0176569601908337, 0.0591969943784215,
                ],
                [
                    0.464161060804975, 0.0856815735302437,
                    0.426828186751401, 0.0233291789133808,
                ],
                [
                    0.0856815735302422, 0.0233291789133806,
                    0.426828186751394, 0.464161060804983,
                ],
                [
                    0.0233291789133806, 0.464161060804987,
                    0.426828186751394, 0.0856815735302377,
                ],
                [
                    0.0612354874441953, 0.232417998956387,
                    0.697518900952387, 0.00882761264703054,
                ],
                [
                    0.232417998956387, 0.00882761264703515,
                    0.69751890095239, 0.0612354874441881,
                ],
                [
                    0.00882761264703292, 0.0612354874441866,
                    0.697518900952386, 0.232417998956394,
                ],
                [
                    0.292248264310623, 0.185900408683766,
                    0.502598623355028, 0.0192527036505837,
                ],
                [
                    0.185900408683767, 0.0192527036505833,
                    0.502598623355022, 0.292248264310628,
                ],
                [
                    0.0192527036505841, 0.292248264310633,
                    0.502598623355022, 0.18590040868376,
                ],
                [
                    0.024615216819616, 0.0243599100699364,
                    0.852514471650135, 0.0985104014603124,
                ],
                [
                    0.0243599100699361, 0.0985104014603152,
                    0.852514471650132, 0.0246152168196165,
                ],
                [
                    0.0985104014603048, 0.0246152168196152,
                    0.852514471650145, 0.0243599100699349,
                ],
                [
                    0.0947626190290201, 0.404502368563266,
                    0.291823515567251, 0.208911496840463,
                ],
                [
                    0.404502368563276, 0.208911496840468,
                    0.291823515567244, 0.0947626190290126,
                ],
                [
                    0.208911496840467, 0.0947626190290192,
                    0.29182351556725, 0.404502368563264,
                ],
                [
                    0.296222795087948, 0.0620182193026911,
                    0.561713963720754, 0.0800450218886065,
                ],
                [
                    0.0620182193026887, 0.0800450218886009,
                    0.561713963720765, 0.296222795087946,
                ],
                [
                    0.0800450218886068, 0.296222795087942,
                    0.561713963720764, 0.0620182193026874,
                ],
                [
                    0.342531997950151, 0.00917208007007445,
                    0.485862460739408, 0.162433461240367,
                ],
                [
                    0.0091720800700746, 0.162433461240372,
                    0.48586246073941, 0.342531997950144,
                ],
                [
                    0.162433461240369, 0.342531997950151,
                    0.485862460739406, 0.00917208007007333,
                ],
                [
                    0.694139972529529, 0.023627641314443,
                    0.264381081506819, 0.0178513046492095,
                ],
                [
                    0.0236276413144455, 0.01785130464921,
                    0.264381081506813, 0.694139972529531,
                ],
                [
                    0.0178513046492101, 0.694139972529533,
                    0.264381081506813, 0.0236276413144447,
                ],
                [
                    0.0249315640402738, 0.29729015531711,
                    0.297442217416373, 0.380336063226243,
                ],
                [
                    0.297290155317107, 0.380336063226243,
                    0.297442217416377, 0.0249315640402734,
                ],
                [
                    0.380336063226246, 0.0249315640402727,
                    0.297442217416372, 0.297290155317109,
                ],
                [
                    0.270890203928969, 0.560665883770015,
                    0.150162560127795, 0.0182813521732212,
                ],
                [
                    0.56066588377002, 0.0182813521732223,
                    0.150162560127791, 0.270890203928966,
                ],
                [
                    0.018281352173223, 0.270890203928966,
                    0.150162560127793, 0.560665883770019,
                ],
                [
                    0.377106399417617, 0.574872758913607,
                    0.0304912794861778, 0.0175295621825974,
                ],
                [
                    0.574872758913612, 0.0175295621825988,
                    0.0304912794861782, 0.377106399417611,
                ],
                [
                    0.0175295621826013, 0.377106399417613,
                    0.0304912794861796, 0.574872758913606,
                ],
                [
                    0.0299575541295916, 0.483342697532054,
                    0.476493674683287, 0.0102060736550675,
                ],
                [
                    0.483342697532047, 0.0102060736550701,
                    0.476493674683292, 0.0299575541295909,
                ],
                [
                    0.0102060736550687, 0.0299575541295917,
                    0.476493674683286, 0.483342697532054,
                ],
                [
                    0.236378033338292, 0.526759566994199,
                    0.0254247651160521, 0.211437634551457,
                ],
                [
                    0.526759566994189, 0.211437634551462,
                    0.0254247651160507, 0.236378033338298,
                ],
                [
                    0.211437634551457, 0.236378033338298,
                    0.0254247651160502, 0.526759566994194,
                ],
                [
                    0.954618484866729, 0.00457955574287844,
                    0.0179058660074248, 0.0228960933829676,
                ],
                [
                    0.00457955574287584, 0.0228960933829682,
                    0.0179058660074233, 0.954618484866733,
                ],
                [
                    0.0228960933829668, 0.954618484866734,
                    0.0179058660074227, 0.00457955574287667,
                ],
                [
                    0.16333095462719, 0.0256118593510928,
                    0.115447871299236, 0.695609314722481,
                ],
                [
                    0.0256118593510928, 0.695609314722482,
                    0.115447871299235, 0.16333095462719,
                ],
                [
                    0.695609314722476, 0.163330954627191,
                    0.115447871299239, 0.0256118593510939,
                ],
                [
                    0.446315518264942, 0.402881624628451,
                    0.0261995607562525, 0.124603296350354,
                ],
                [
                    0.402881624628445, 0.124603296350356,
                    0.0261995607562525, 0.446315518264947,
                ],
                [
                    0.124603296350348, 0.446315518264951,
                    0.0261995607562522, 0.402881624628448,
                ],
                [
                    0.507548605120255, 0.231647695217254,
                    0.126623713234392, 0.1341799864281,
                ],
                [
                    0.231647695217251, 0.134179986428097,
                    0.126623713234393, 0.507548605120259,
                ],
                [
                    0.134179986428096, 0.507548605120259,
                    0.126623713234395, 0.23164769521725,
                ],
                [
                    0.843032546078339, 0.0343858276593477,
                    0.0990866132622776, 0.0234950130000354,
                ],
                [
                    0.0343858276593471, 0.023495013000035,
                    0.0990866132622732, 0.843032546078345,
                ],
                [
                    0.0234950130000359, 0.843032546078344,
                    0.0990866132622728, 0.034385827659347,
                ],
                [
                    0.118317157542655, 0.0274200248677327,
                    0.701648904118846, 0.152613913470766,
                ],
                [
                    0.0274200248677319, 0.152613913470765,
                    0.701648904118846, 0.118317157542658,
                ],
                [
                    0.152613913470766, 0.118317157542651,
                    0.70164890411885, 0.0274200248677339,
                ],
                [
                    0.0831251561121388, 0.689839510369901,
                    0.0240810955367417, 0.202954237981219,
                ],
                [
                    0.689839510369895, 0.202954237981222,
                    0.0240810955367422, 0.0831251561121415,
                ],
                [
                    0.20295423798122, 0.08312515611214,
                    0.0240810955367423, 0.689839510369898,
                ],
                [
                    0.4891098147268, 0.367009893737499,
                    0.11512444438173, 0.0287558471539715,
                ],
                [
                    0.367009893737501, 0.0287558471539708,
                    0.115124444381728, 0.489109814726801,
                ],
                [
                    0.0287558471539704, 0.489109814726801,
                    0.115124444381729, 0.3670098937375,
                ],
                [
                    0.744238507663164, 0.00430783216071411,
                    0.152343720516269, 0.099109939659853,
                ],
                [
                    0.00430783216071248, 0.0991099396598518,
                    0.152343720516272, 0.744238507663164,
                ],
                [
                    0.0991099396598548, 0.744238507663162,
                    0.152343720516271, 0.00430783216071211,
                ],
                [
                    0.858904439184522, 0.117645344816038,
                    0.0198161779595624, 0.00363403803987792,
                ],
                [
                    0.117645344816035, 0.00363403803987569,
                    0.0198161779595609, 0.858904439184528,
                ],
                [
                    0.00363403803987428, 0.858904439184525,
                    0.019816177959561, 0.11764534481604,
                ],
                [
                    0.793988849912225, 0.00355709537726892,
                    0.0330547791775564, 0.169399275532949,
                ],
                [
                    0.00355709537726869, 0.16939927553295,
                    0.0330547791775573, 0.793988849912224,
                ],
                [
                    0.169399275532948, 0.793988849912226,
                    0.0330547791775572, 0.00355709537726875,
                ],
                [
                    0.00219091239834531, 0.290641762236923,
                    0.672266868777166, 0.0349004565875657,
                ],
                [
                    0.290641762236919, 0.0349004565875678,
                    0.672266868777173, 0.0021909123983405,
                ],
                [
                    0.0349004565875677, 0.00219091239833891,
                    0.672266868777167, 0.290641762236926,
                ],
                [
                    0.692501417588047, 0.0728291271168857,
                    0.000524571221017455, 0.23414488407405,
                ],
                [
                    0.0728291271168834, 0.234144884074049,
                    0.000524571221016469, 0.692501417588051,
                ],
                [
                    0.23414488407405, 0.692501417588051,
                    0.000524571221014633, 0.072829127116884,
                ],
                [
                    0.117684339714556, 0.117684339714559,
                    0.646946980856328, 0.117684339714557,
                ],
                [
                    0.00533607701964334, 0.00533607701965128,
                    0.983991768941056, 0.00533607701964902,
                ],
                [
                    0.332496959976636, 0.332496959976649,
                    0.00250912007007478, 0.33249695997664,
                ],
                [
                    0.305329584336056, 0.305329584336061,
                    0.0840112469918198, 0.305329584336063,
                ],
                [
                    0.248212371556229, 0.248212371556224,
                    0.255362885331328, 0.248212371556219,
                ],
                ])
            self.weights = numpy.array([
                0.00208630129324048,
                0.00208630129324056,
                0.00208630129323957,
                0.00629907711427731,
                0.00629907711427754,
                0.00629907711427777,
                0.0131394519285629,
                0.0131394519285624,
                0.0131394519285621,
                0.00858375505374076,
                0.00858375505374059,
                0.00858375505374044,
                0.0155266787406683,
                0.0155266787406669,
                0.0155266787406653,
                0.00281635848673284,
                0.00281635848673272,
                0.0028163584867331,
                0.011887985191612,
                0.0118879851916125,
                0.0118879851916123,
                0.00737803689793369,
                0.00737803689793309,
                0.00737803689793278,
                0.00780703596787129,
                0.00780703596787227,
                0.00780703596787218,
                0.0195085608307975,
                0.0195085608307976,
                0.0195085608307968,
                0.0169084708873414,
                0.0169084708873396,
                0.0169084708873404,
                0.00868875735071152,
                0.00868875735071224,
                0.00868875735071202,
                0.00312673072542453,
                0.00312673072542443,
                0.00312673072542446,
                0.00771631583170163,
                0.00771631583170171,
                0.00771631583170164,
                0.00315397360253617,
                0.00315397360253695,
                0.00315397360253645,
                0.00912078610871593,
                0.00912078610871582,
                0.00912078610871601,
                0.00316318718311667,
                0.0031631871831167,
                0.00316318718311642,
                0.0187833784369295,
                0.018783378436929,
                0.0187833784369294,
                0.011551780344482,
                0.0115517803444818,
                0.0115517803444821,
                0.00533229215437933,
                0.00533229215437945,
                0.0053322921543788,
                0.00333962716769685,
                0.00333962716769722,
                0.00333962716769718,
                0.0117038335604756,
                0.0117038335604752,
                0.0117038335604753,
                0.00841852280506379,
                0.00841852280506408,
                0.00841852280506428,
                0.00420521442389025,
                0.00420521442389042,
                0.0042052144238911,
                0.00322158043528684,
                0.00322158043528719,
                0.00322158043528708,
                0.0111398807725981,
                0.0111398807725977,
                0.0111398807725975,
                0.000505742879640303,
                0.000505742879640224,
                0.00050574287964021,
                0.0083158083535094,
                0.00831580835350929,
                0.00831580835350986,
                0.0114596002941691,
                0.0114596002941693,
                0.0114596002941694,
                0.0219522411284444,
                0.0219522411284448,
                0.0219522411284446,
                0.00367774167811291,
                0.00367774167811276,
                0.0036777416781129,
                0.00800059602405499,
                0.00800059602405485,
                0.00800059602405496,
                0.00784650855436964,
                0.00784650855437009,
                0.00784650855437006,
                0.0121567376184139,
                0.0121567376184137,
                0.0121567376184136,
                0.00283599891293076,
                0.00283599891293056,
                0.00283599891293057,
                0.00128945607217019,
                0.00128945607217001,
                0.00128945607216997,
                0.0020963338165057,
                0.00209633381650571,
                0.00209633381650572,
                0.00221706436878065,
                0.00221706436878014,
                0.00221706436877999,
                0.00261484345760874,
                0.0026148434576086,
                0.00261484345760843,
                0.0111059850732994,
                0.000200199942236043,
                0.00494295544168239,
                0.0255171528012982,
                0.0295049673779978,
                ])
        elif index == 13:
            self.degree = 14
            bary = numpy.array([
                [
                    0.818026162194412, 0.013371428943564,
                    0.107457129743794, 0.0611452791182301,
                ],
                [
                    0.0133714289435258, 0.0611452791183259,
                    0.10745712974381, 0.818026162194339,
                ],
                [
                    0.0611452791182966, 0.818026162194297,
                    0.107457129743849, 0.0133714289435574,
                ],
                [
                    0.400097929629891, 0.0829145204330444,
                    0.4641321089537, 0.0528554409833644,
                ],
                [
                    0.0829145204330399, 0.0528554409833555,
                    0.464132108953597, 0.400097929630008,
                ],
                [
                    0.0528554409833098, 0.400097929630126,
                    0.464132108953625, 0.0829145204329388,
                ],
                [
                    0.486917892917434, 0.0306708675760842,
                    0.416442127799289, 0.0659691117071927,
                ],
                [
                    0.0306708675760624, 0.0659691117071544,
                    0.41644212779934, 0.486917892917443,
                ],
                [
                    0.0659691117071845, 0.486917892917536,
                    0.416442127799194, 0.0306708675760856,
                ],
                [
                    0.168227625703714, 0.0518298141536549,
                    0.0127590379000881, 0.767183522242543,
                ],
                [
                    0.051829814153633, 0.767183522242568,
                    0.0127590379000584, 0.16822762570374,
                ],
                [
                    0.767183522242537, 0.168227625703764,
                    0.0127590379000647, 0.0518298141536341,
                ],
                [
                    0.0158306343508983, 0.484774657158783,
                    0.0183305707875621, 0.481064137702757,
                ],
                [
                    0.484774657158741, 0.481064137702812,
                    0.0183305707875624, 0.0158306343508839,
                ],
                [
                    0.481064137702792, 0.0158306343509015,
                    0.0183305707875518, 0.484774657158754,
                ],
                [
                    0.212441759266561, 0.370442555958176,
                    0.0106815230635501, 0.406434161711712,
                ],
                [
                    0.370442555958057, 0.406434161711827,
                    0.0106815230635702, 0.212441759266546,
                ],
                [
                    0.406434161711731, 0.212441759266616,
                    0.0106815230635699, 0.370442555958083,
                ],
                [
                    0.0178260609007786, 0.287470635892888,
                    0.385617293714959, 0.309086009491375,
                ],
                [
                    0.287470635892881, 0.309086009491372,
                    0.38561729371497, 0.0178260609007777,
                ],
                [
                    0.30908600949137, 0.0178260609007819,
                    0.385617293714966, 0.287470635892882,
                ],
                [
                    0.272077441542799, 0.00960895234835501,
                    0.217347346263903, 0.500966259844943,
                ],
                [
                    0.00960895234833769, 0.500966259845028,
                    0.217347346263923, 0.272077441542712,
                ],
                [
                    0.500966259844967, 0.272077441542766,
                    0.21734734626392, 0.00960895234834742,
                ],
                [
                    0.533327730920418, 0.0788509969514415,
                    0.16634216529448, 0.221479106833661,
                ],
                [
                    0.078850996951403, 0.221479106833696,
                    0.16634216529448, 0.533327730920422,
                ],
                [
                    0.221479106833624, 0.533327730920471,
                    0.166342165294459, 0.0788509969514449,
                ],
                [
                    0.16038086409574, 0.780025722472745,
                    0.0414431673398121, 0.0181502460917031,
                ],
                [
                    0.780025722472703, 0.0181502460917103,
                    0.0414431673398047, 0.160380864095782,
                ],
                [
                    0.0181502460917112, 0.160380864095821,
                    0.0414431673397762, 0.780025722472692,
                ],
                [
                    0.102430878922965, 0.276668775818295,
                    0.402000548240723, 0.218899797018017,
                ],
                [
                    0.276668775818374, 0.218899797017987,
                    0.402000548240724, 0.102430878922915,
                ],
                [
                    0.218899797017973, 0.102430878922911,
                    0.402000548240698, 0.276668775818417,
                ],
                [
                    0.48197145243094, 0.0175623092363264,
                    0.341432014866781, 0.159034223465953,
                ],
                [
                    0.0175623092363335, 0.159034223465929,
                    0.341432014866806, 0.481971452430931,
                ],
                [
                    0.159034223465936, 0.481971452430907,
                    0.34143201486682, 0.0175623092363365,
                ],
                [
                    0.661983417474541, 0.0122725481672795,
                    0.173645669158287, 0.152098365199893,
                ],
                [
                    0.0122725481672642, 0.152098365199948,
                    0.173645669158308, 0.661983417474479,
                ],
                [
                    0.152098365199895, 0.661983417474465,
                    0.173645669158358, 0.0122725481672826,
                ],
                [
                    0.0773186488433034, 0.5438135338904,
                    0.196086175513052, 0.182781641753245,
                ],
                [
                    0.543813533890327, 0.182781641753255,
                    0.196086175513082, 0.0773186488433358,
                ],
                [
                    0.182781641753172, 0.0773186488433082,
                    0.196086175513172, 0.543813533890347,
                ],
                [
                    0.779622092897011, 0.0863975719064645,
                    0.072172897942185, 0.0618074372543398,
                ],
                [
                    0.0863975719063824, 0.0618074372543111,
                    0.0721728979422066, 0.7796220928971,
                ],
                [
                    0.0618074372542844, 0.779622092897153,
                    0.0721728979421318, 0.0863975719064307,
                ],
                [
                    0.941281149352309, 0.0089130123624666,
                    0.030236874511, 0.0195689637742239,
                ],
                [
                    0.00891301236248357, 0.0195689637742393,
                    0.0302368745110069, 0.94128114935227,
                ],
                [
                    0.0195689637742709, 0.941281149352236,
                    0.0302368745110066, 0.00891301236248671,
                ],
                [
                    0.173580235845092, 0.0289043635248354,
                    0.357082484218001, 0.440432916412071,
                ],
                [
                    0.0289043635248878, 0.440432916412,
                    0.357082484218023, 0.173580235845089,
                ],
                [
                    0.440432916412081, 0.173580235845064,
                    0.357082484217993, 0.028904363524862,
                ],
                [
                    0.0903518334035954, 0.0227008501117902,
                    0.865817656785222, 0.0211296596993925,
                ],
                [
                    0.0227008501117934, 0.0211296596993924,
                    0.865817656785192, 0.0903518334036225,
                ],
                [
                    0.0211296596993804, 0.0903518334034983,
                    0.86581765678534, 0.0227008501117813,
                ],
                [
                    0.445169479233205, 0.0214883127020709,
                    0.212734909199721, 0.320607298865004,
                ],
                [
                    0.0214883127020669, 0.320607298865048,
                    0.212734909199735, 0.445169479233149,
                ],
                [
                    0.320607298865012, 0.445169479233177,
                    0.212734909199736, 0.0214883127020745,
                ],
                [
                    0.0802385011622648, 0.617486648324989,
                    0.0719578452270715, 0.230317005285675,
                ],
                [
                    0.617486648324915, 0.230317005285725,
                    0.0719578452270639, 0.080238501162296,
                ],
                [
                    0.230317005285633, 0.0802385011623273,
                    0.0719578452271305, 0.61748664832491,
                ],
                [
                    0.659637499955212, 0.0945288121975531,
                    0.0706560126462567, 0.175177675200978,
                ],
                [
                    0.0945288121975159, 0.175177675200956,
                    0.0706560126462949, 0.659637499955233,
                ],
                [
                    0.175177675200921, 0.659637499955317,
                    0.0706560126462181, 0.0945288121975437,
                ],
                [
                    0.282093867541703, 0.691284914660533,
                    0.00589668853655629, 0.0207245292612076,
                ],
                [
                    0.691284914660524, 0.0207245292612111,
                    0.00589668853655086, 0.282093867541714,
                ],
                [
                    0.020724529261209, 0.282093867541785,
                    0.00589668853653658, 0.691284914660469,
                ],
                [
                    0.584552241935574, 0.017577541940982,
                    0.0808011880664406, 0.317069028057003,
                ],
                [
                    0.0175775419409742, 0.317069028057004,
                    0.0808011880664319, 0.584552241935589,
                ],
                [
                    0.317069028056945, 0.584552241935619,
                    0.080801188066464, 0.0175775419409727,
                ],
                [
                    0.0966346181353643, 0.358943001077193,
                    0.230580859444538, 0.313841521342904,
                ],
                [
                    0.358943001077144, 0.313841521342926,
                    0.230580859444564, 0.0966346181353659,
                ],
                [
                    0.313841521342904, 0.0966346181353586,
                    0.230580859444533, 0.358943001077204,
                ],
                [
                    0.547115266351136, 0.0890256669907118,
                    0.0252548503950358, 0.338604216263117,
                ],
                [
                    0.0890256669906873, 0.3386042162631,
                    0.0252548503950389, 0.547115266351174,
                ],
                [
                    0.338604216263121, 0.547115266351173,
                    0.0252548503950499, 0.0890256669906569,
                ],
                [
                    0.561185464162414, 0.349775871867066,
                    0.0100132749524236, 0.0790253890180963,
                ],
                [
                    0.349775871866966, 0.0790253890181477,
                    0.0100132749524376, 0.561185464162449,
                ],
                [
                    0.0790253890181082, 0.561185464162455,
                    0.0100132749524286, 0.349775871867008,
                ],
                [
                    0.878818746835957, 0.0336131453302366,
                    0.00841215865842347, 0.0791559491753833,
                ],
                [
                    0.0336131453302448, 0.0791559491753919,
                    0.00841215865841498, 0.878818746835948,
                ],
                [
                    0.0791559491754355, 0.87881874683591,
                    0.00841215865838887, 0.0336131453302656,
                ],
                [
                    0.810872665144813, 0.0314518100476794,
                    0.14652045906117, 0.0111550657463385,
                ],
                [
                    0.0314518100476593, 0.01115506574635,
                    0.146520459061148, 0.810872665144843,
                ],
                [
                    0.0111550657463448, 0.810872665144839,
                    0.146520459061165, 0.0314518100476507,
                ],
                [
                    0.703560141816559, 0.156191534162668,
                    0.128232413502758, 0.0120159105180149,
                ],
                [
                    0.156191534162667, 0.0120159105180117,
                    0.128232413502749, 0.703560141816573,
                ],
                [
                    0.0120159105180016, 0.703560141816627,
                    0.128232413502744, 0.156191534162627,
                ],
                [
                    0.532135976831517, 0.236242305861953,
                    0.0306611166321087, 0.200960600674421,
                ],
                [
                    0.236242305861898, 0.200960600674485,
                    0.0306611166321184, 0.532135976831499,
                ],
                [
                    0.200960600674406, 0.53213597683155,
                    0.0306611166321389, 0.236242305861905,
                ],
                [
                    0.122749062866958, 0.390929607439404,
                    0.0875638865524715, 0.398757443141166,
                ],
                [
                    0.390929607439354, 0.398757443141171,
                    0.0875638865525015, 0.122749062866974,
                ],
                [
                    0.398757443141132, 0.122749062866969,
                    0.0875638865525005, 0.390929607439399,
                ],
                [
                    0.606895467300538, 0.0776379207679784,
                    0.305895247233166, 0.00957136469831744,
                ],
                [
                    0.0776379207679863, 0.00957136469831809,
                    0.305895247233132, 0.606895467300564,
                ],
                [
                    0.00957136469829877, 0.606895467300527,
                    0.305895247233178, 0.077637920767996,
                ],
                [
                    0.0354595140750026, 0.164569131215242,
                    0.538551546842193, 0.261419807867562,
                ],
                [
                    0.164569131215226, 0.261419807867527,
                    0.538551546842231, 0.0354595140750151,
                ],
                [
                    0.261419807867579, 0.0354595140750057,
                    0.538551546842199, 0.164569131215216,
                ],
                [
                    0.63847471898315, 0.0654176689080234,
                    0.220672862895764, 0.0754347492130629,
                ],
                [
                    0.0654176689079865, 0.0754347492130809,
                    0.220672862895759, 0.638474718983173,
                ],
                [
                    0.0754347492130388, 0.638474718983192,
                    0.22067286289572, 0.0654176689080496,
                ],
                [
                    0.243413562240788, 0.100319853633252,
                    0.590605933231053, 0.0656606508949075,
                ],
                [
                    0.100319853633265, 0.0656606508949501,
                    0.590605933231018, 0.243413562240767,
                ],
                [
                    0.0656606508949013, 0.243413562240951,
                    0.590605933230827, 0.10031985363332,
                ],
                [
                    0.884492068224789, 0.0814557826085823,
                    0.0254490039036399, 0.00860314526298921,
                ],
                [
                    0.0814557826086041, 0.00860314526297599,
                    0.0254490039036264, 0.884492068224794,
                ],
                [
                    0.00860314526296295, 0.884492068224839,
                    0.0254490039036199, 0.0814557826085779,
                ],
                [
                    0.0265723408459754, 0.505432376991335,
                    0.0969018715631563, 0.371093410599533,
                ],
                [
                    0.505432376991312, 0.371093410599567,
                    0.0969018715631426, 0.026572340845978,
                ],
                [
                    0.371093410599533, 0.0265723408459748,
                    0.0969018715631302, 0.505432376991362,
                ],
                [
                    0.0151571582474894, 0.117142028395503,
                    0.737075571829331, 0.130625241527677,
                ],
                [
                    0.117142028395487, 0.130625241527677,
                    0.737075571829356, 0.0151571582474804,
                ],
                [
                    0.130625241527669, 0.0151571582475133,
                    0.737075571829336, 0.117142028395481,
                ],
                [
                    0.4002127949623, 0.110849502299599,
                    0.326319710535484, 0.162617992202616,
                ],
                [
                    0.110849502299585, 0.162617992202607,
                    0.326319710535487, 0.400212794962321,
                ],
                [
                    0.16261799220257, 0.400212794962304,
                    0.326319710535522, 0.110849502299603,
                ],
                [
                    0.446414699962637, 0.0247742969059819,
                    0.521328780953973, 0.00748222217740826,
                ],
                [
                    0.0247742969059782, 0.00748222217739249,
                    0.521328780953992, 0.446414699962637,
                ],
                [
                    0.00748222217740122, 0.446414699962571,
                    0.521328780954065, 0.0247742969059626,
                ],
                [
                    0.441805588880389, 0.206922362630268,
                    0.140434894083911, 0.210837154405432,
                ],
                [
                    0.206922362630213, 0.210837154405425,
                    0.140434894083957, 0.441805588880404,
                ],
                [
                    0.210837154405392, 0.441805588880392,
                    0.14043489408396, 0.206922362630256,
                ],
                [
                    0.268842851768175, 0.00741446097725757,
                    0.0282138124054504, 0.695528874849117,
                ],
                [
                    0.00741446097723596, 0.695528874849135,
                    0.0282138124054633, 0.268842851768166,
                ],
                [
                    0.695528874849122, 0.268842851768176,
                    0.0282138124054619, 0.00741446097724042,
                ],
                [
                    0.235908125275048, 0.0271249110341808,
                    0.714803025662879, 0.0221639380278925,
                ],
                [
                    0.0271249110341816, 0.0221639380278992,
                    0.714803025662853, 0.235908125275066,
                ],
                [
                    0.0221639380279053, 0.235908125274959,
                    0.714803025662953, 0.027124911034183,
                ],
                [
                    0.341793074232021, 0.00259416526518736,
                    0.579768534585111, 0.07584422591768,
                ],
                [
                    0.00259416526521004, 0.0758442259176827,
                    0.579768534585075, 0.341793074232032,
                ],
                [
                    0.0758442259176955, 0.341793074232085,
                    0.579768534585002, 0.00259416526521801,
                ],
                [
                    0.70864310892357, 0.120828704769109,
                    0.00291446664138564, 0.167613719665935,
                ],
                [
                    0.120828704769109, 0.167613719665954,
                    0.00291446664141049, 0.708643108923526,
                ],
                [
                    0.167613719666, 0.708643108923496,
                    0.00291446664135644, 0.120828704769147,
                ],
                [
                    0.660612504418027, 0.00423850950551797,
                    0.3059064193537, 0.029242566722755,
                ],
                [
                    0.00423850950552509, 0.0292425667227533,
                    0.305906419353717, 0.660612504418005,
                ],
                [
                    0.0292425667227547, 0.660612504417956,
                    0.305906419353755, 0.00423850950553484,
                ],
                [
                    0.300649769447687, 0.137450394796745,
                    0.560869397778206, 0.00103043797736148,
                ],
                [
                    0.137450394796727, 0.00103043797737725,
                    0.560869397778249, 0.300649769447646,
                ],
                [
                    0.00103043797733855, 0.300649769447711,
                    0.560869397778215, 0.137450394796735,
                ],
                [
                    0.0951170007288927, 0.0951170007290063,
                    0.714648997813215, 0.0951170007288864,
                ],
                [
                    0.0103451072565879, 0.0103451072565237,
                    0.968964678230288, 0.0103451072566002,
                ],
                [
                    0.309555018343051, 0.309555018343096,
                    0.0713349449707516, 0.309555018343101,
                ],
                [
                    0.166863287041671, 0.16686328704156,
                    0.499410138875189, 0.166863287041581,
                ],
                [
                    0.250558886939582, 0.250558886939549,
                    0.248323339181307, 0.250558886939562,
                ],
                ])
            self.weights = numpy.array([
                0.00213073554438118,
                0.00213073554437863,
                0.00213073554438061,
                0.00706724632965415,
                0.00706724632966034,
                0.00706724632964317,
                0.00488685515082972,
                0.00488685515082227,
                0.00488685515082136,
                0.00271814270323768,
                0.00271814270323416,
                0.00271814270323462,
                0.00249261137815028,
                0.00249261137814903,
                0.00249261137815022,
                0.00559023864720133,
                0.00559023864720696,
                0.00559023864720624,
                0.00758331046311318,
                0.007583310463114,
                0.00758331046311446,
                0.00476072882671893,
                0.00476072882671578,
                0.00476072882671803,
                0.011462750188317,
                0.0114627501883131,
                0.0114627501883208,
                0.00311014414497174,
                0.00311014414497243,
                0.00311014414497197,
                0.0154268175124682,
                0.0154268175124637,
                0.0154268175124669,
                0.00676662254176413,
                0.00676662254176676,
                0.00676662254176657,
                0.00463862968174892,
                0.00463862968174465,
                0.00463862968174884,
                0.012764679941297,
                0.0127646799413048,
                0.0127646799412994,
                0.00552767467446384,
                0.00552767467446142,
                0.00552767467445978,
                0.000650491962223052,
                0.000650491962224175,
                0.000650491962225108,
                0.00914135063407055,
                0.0091413506340875,
                0.00914135063407942,
                0.00222704248813541,
                0.00222704248813577,
                0.00222704248813359,
                0.00829497134333861,
                0.00829497134333823,
                0.00829497134333961,
                0.00932032853674417,
                0.0093203285367464,
                0.00932032853675295,
                0.00947137172071942,
                0.00947137172071802,
                0.00947137172071935,
                0.00143120814943112,
                0.00143120814943081,
                0.00143120814942936,
                0.00563280540239885,
                0.00563280540239663,
                0.005632805402397,
                0.0177701313327262,
                0.0177701313327248,
                0.0177701313327235,
                0.00693514714390151,
                0.00693514714389973,
                0.00693514714390042,
                0.00414277317641505,
                0.00414277317641925,
                0.0041427731764158,
                0.00134085154787107,
                0.00134085154787044,
                0.00134085154786929,
                0.00208839061214727,
                0.00208839061214855,
                0.00208839061214737,
                0.00451042464299934,
                0.00451042464299912,
                0.00451042464299527,
                0.0100812968357896,
                0.0100812968357908,
                0.0100812968357923,
                0.0153606971274897,
                0.0153606971274921,
                0.015360697127492,
                0.00393054515240602,
                0.00393054515240648,
                0.00393054515240341,
                0.0108524316767907,
                0.0108524316767932,
                0.010852431676792,
                0.00965867320973849,
                0.00965867320973635,
                0.00965867320973853,
                0.0106587174774231,
                0.0106587174774302,
                0.0106587174774369,
                0.00129097495695665,
                0.00129097495695525,
                0.00129097495695388,
                0.00785916073165542,
                0.00785916073165636,
                0.00785916073165506,
                0.00480157227821793,
                0.00480157227821545,
                0.00480157227822234,
                0.019820199409255,
                0.0198201994092487,
                0.0198201994092569,
                0.00221486739500074,
                0.00221486739499855,
                0.0022148673949988,
                0.0187005659706802,
                0.0187005659706834,
                0.0187005659706804,
                0.00213650370482382,
                0.00213650370482205,
                0.00213650370482248,
                0.00397154117891947,
                0.0039715411789203,
                0.00397154117892264,
                0.00241278737214882,
                0.00241278737215133,
                0.00241278737215364,
                0.00256019158755153,
                0.00256019158755455,
                0.00256019158754794,
                0.00201678998548853,
                0.00201678998548882,
                0.00201678998549014,
                0.00320503623716379,
                0.00320503623716661,
                0.00320503623716001,
                0.00863139047907635,
                0.00024805946751688,
                0.0170056826234713,
                0.0140401366837056,
                0.0258236446193837,
                ])
        elif index == 14:
            self.degree = 16
            bary = numpy.array([
                [
                    0.215369322514279, 0.0716238048007973,
                    0.0661407842999457, 0.646866088384978,
                ],
                [
                    0.0716238048001562, 0.646866088384849,
                    0.0661407842993252, 0.215369322515669,
                ],
                [
                    0.646866088384544, 0.215369322515079,
                    0.0661407842992802, 0.0716238048010972,
                ],
                [
                    0.0840031187301689, 0.240326325974372,
                    0.10503653090557, 0.570634024389889,
                ],
                [
                    0.240326325971861, 0.570634024389719,
                    0.105036530908253, 0.084003118730167,
                ],
                [
                    0.570634024389941, 0.0840031187298655,
                    0.105036530907377, 0.240326325972817,
                ],
                [
                    0.722007497840839, 0.0145553762630801,
                    0.243111580834535, 0.0203255450615459,
                ],
                [
                    0.0145553762634442, 0.0203255450614079,
                    0.243111580835629, 0.722007497839518,
                ],
                [
                    0.0203255450614588, 0.722007497840107,
                    0.243111580835371, 0.0145553762630636,
                ],
                [
                    0.54975956322041, 0.0125290598080411,
                    0.121940646122287, 0.315770730849263,
                ],
                [
                    0.0125290598081035, 0.315770730850069,
                    0.121940646121559, 0.549759563220269,
                ],
                [
                    0.315770730851296, 0.549759563218567,
                    0.121940646122027, 0.0125290598081097,
                ],
                [
                    0.517513525717232, 0.384562096865036,
                    0.0129463331518483, 0.0849780442658844,
                ],
                [
                    0.384562096864772, 0.0849780442656661,
                    0.0129463331518913, 0.51751352571767,
                ],
                [
                    0.0849780442659308, 0.517513525717932,
                    0.0129463331516057, 0.384562096864532,
                ],
                [
                    0.167752470281799, 0.358544527163581,
                    0.346556326285294, 0.127146676269326,
                ],
                [
                    0.358544527164529, 0.127146676269758,
                    0.346556326284038, 0.167752470281675,
                ],
                [
                    0.127146676269092, 0.167752470283245,
                    0.3465563262838, 0.358544527163863,
                ],
                [
                    0.653388018866312, 0.224732675518662,
                    0.0169926270656682, 0.104886678549358,
                ],
                [
                    0.224732675518587, 0.104886678548849,
                    0.0169926270659983, 0.653388018866566,
                ],
                [
                    0.10488667854954, 0.653388018866976,
                    0.0169926270658288, 0.224732675517655,
                ],
                [
                    0.306404774778961, 0.0892356846875987,
                    0.0928171540005135, 0.511542386532927,
                ],
                [
                    0.0892356846886177, 0.511542386532909,
                    0.0928171539998072, 0.306404774778666,
                ],
                [
                    0.511542386532586, 0.306404774778727,
                    0.0928171540004167, 0.0892356846882702,
                ],
                [
                    0.540479768065727, 0.00729435538130419,
                    0.245376315222932, 0.206849561330037,
                ],
                [
                    0.00729435538155172, 0.206849561330101,
                    0.245376315221688, 0.540479768066659,
                ],
                [
                    0.20684956133125, 0.540479768065415,
                    0.24537631522196, 0.0072943553813742,
                ],
                [
                    0.308984692817387, 0.0973720336353292,
                    0.492908872135997, 0.100734401411287,
                ],
                [
                    0.0973720336363442, 0.100734401412185,
                    0.492908872132838, 0.308984692818633,
                ],
                [
                    0.100734401410623, 0.308984692817731,
                    0.492908872136955, 0.0973720336346908,
                ],
                [
                    0.00924736361783223, 0.399013906227181,
                    0.582903743612111, 0.00883498654287528,
                ],
                [
                    0.399013906225403, 0.00883498654301956,
                    0.58290374361367, 0.00924736361790737,
                ],
                [
                    0.00883498654308674, 0.00924736361820384,
                    0.582903743616868, 0.399013906221841,
                ],
                [
                    0.583278015992226, 0.021520825534561,
                    0.379120808460464, 0.0160803500127489,
                ],
                [
                    0.021520825534508, 0.0160803500126914,
                    0.379120808464382, 0.583278015988419,
                ],
                [
                    0.0160803500131374, 0.583278015993719,
                    0.379120808458791, 0.0215208255343529,
                ],
                [
                    0.898965060538575, 0.0688331739588598,
                    0.0144676216404639, 0.0177341438621016,
                ],
                [
                    0.0688331739583355, 0.0177341438621541,
                    0.0144676216406489, 0.898965060538862,
                ],
                [
                    0.0177341438623076, 0.898965060538664,
                    0.014467621640217, 0.0688331739588118,
                ],
                [
                    0.384645703607397, 0.0027476239716159,
                    0.276455708804184, 0.336150963616804,
                ],
                [
                    0.00274762397135499, 0.336150963616514,
                    0.276455708803799, 0.384645703608332,
                ],
                [
                    0.336150963618088, 0.384645703604847,
                    0.27645570880599, 0.00274762397107473,
                ],
                [
                    0.227356386877528, 0.530397783966067,
                    0.00856896690510582, 0.233676862251299,
                ],
                [
                    0.530397783966474, 0.233676862250729,
                    0.00856896690513553, 0.227356386877662,
                ],
                [
                    0.233676862250474, 0.227356386876841,
                    0.008568966905196, 0.530397783967488,
                ],
                [
                    0.376181813691294, 0.473082394578608,
                    0.0723615512045186, 0.0783742405255793,
                ],
                [
                    0.473082394578429, 0.0783742405257319,
                    0.0723615512046556, 0.376181813691184,
                ],
                [
                    0.0783742405253044, 0.376181813693192,
                    0.0723615512048998, 0.473082394576603,
                ],
                [
                    0.350859996445968, 0.552218210434529,
                    0.00493132522606704, 0.0919904678934361,
                ],
                [
                    0.552218210434274, 0.0919904678936557,
                    0.0049313252264271, 0.350859996445644,
                ],
                [
                    0.0919904678930437, 0.350859996445081,
                    0.0049313252269524, 0.552218210434922,
                ],
                [
                    0.0134111646469713, 0.661298203678223,
                    0.0960128293407929, 0.229277802334013,
                ],
                [
                    0.661298203678323, 0.229277802333868,
                    0.0960128293406573, 0.0134111646471517,
                ],
                [
                    0.229277802334997, 0.0134111646470756,
                    0.0960128293404185, 0.661298203677508,
                ],
                [
                    0.834383890577588, 0.0222896364443385,
                    0.124280339121779, 0.019046133856295,
                ],
                [
                    0.022289636444388, 0.0190461338562963,
                    0.124280339120884, 0.834383890578432,
                ],
                [
                    0.0190461338563061, 0.83438389057594,
                    0.124280339123369, 0.0222896364443848,
                ],
                [
                    0.261259669495948, 0.00766750793953502,
                    0.430441339819084, 0.300631482745432,
                ],
                [
                    0.00766750793968263, 0.300631482744547,
                    0.430441339819725, 0.261259669496046,
                ],
                [
                    0.300631482744768, 0.261259669495217,
                    0.430441339820285, 0.00766750793972928,
                ],
                [
                    0.0623040467790808, 0.216006544345622,
                    0.214511628108885, 0.507177780766412,
                ],
                [
                    0.216006544346219, 0.507177780764676,
                    0.214511628110329, 0.0623040467787759,
                ],
                [
                    0.507177780765179, 0.0623040467788091,
                    0.214511628109916, 0.216006544346097,
                ],
                [
                    0.473925854915257, 0.394299156898155,
                    0.114533594128679, 0.0172413940579091,
                ],
                [
                    0.394299156900111, 0.0172413940579183,
                    0.114533594128509, 0.473925854913462,
                ],
                [
                    0.0172413940579389, 0.473925854914619,
                    0.114533594128916, 0.394299156898526,
                ],
                [
                    0.079687330561579, 0.0188309925640223,
                    0.881916327466506, 0.0195653494078926,
                ],
                [
                    0.0188309925636995, 0.0195653494076864,
                    0.881916327468804, 0.0796873305598099,
                ],
                [
                    0.0195653494079884, 0.0796873305625418,
                    0.881916327465428, 0.0188309925640421,
                ],
                [
                    0.0985770407995853, 0.0197499513461522,
                    0.0758618120329568, 0.805811195821306,
                ],
                [
                    0.0197499513461391, 0.805811195822627,
                    0.075861812032311, 0.0985770407989226,
                ],
                [
                    0.805811195821979, 0.0985770407990899,
                    0.0758618120327287, 0.0197499513462029,
                ],
                [
                    0.770990022926281, 0.019522912627666,
                    0.0101562087925883, 0.199330855653465,
                ],
                [
                    0.0195229126276986, 0.199330855653668,
                    0.0101562087926593, 0.770990022925974,
                ],
                [
                    0.199330855653424, 0.77099002292622,
                    0.0101562087927045, 0.0195229126276519,
                ],
                [
                    0.452648871995361, 0.178343490613546,
                    0.21415536427039, 0.154852273120703,
                ],
                [
                    0.178343490613104, 0.15485227311972,
                    0.21415536427179, 0.452648871995386,
                ],
                [
                    0.154852273120587, 0.452648871994808,
                    0.214155364270965, 0.178343490613641,
                ],
                [
                    0.040759326740824, 0.0460496575093691,
                    0.516322768208848, 0.396868247540959,
                ],
                [
                    0.0460496575090221, 0.396868247541765,
                    0.516322768209083, 0.0407593267401296,
                ],
                [
                    0.396868247541129, 0.0407593267406208,
                    0.516322768209267, 0.0460496575089825,
                ],
                [
                    0.2056632530542, 0.0541112613089665,
                    0.206114517270472, 0.534110968366362,
                ],
                [
                    0.0541112613092881, 0.534110968365748,
                    0.206114517269766, 0.205663253055198,
                ],
                [
                    0.534110968366231, 0.205663253054063,
                    0.206114517270704, 0.0541112613090022,
                ],
                [
                    0.223533146236679, 0.650210097913948,
                    0.026421594174992, 0.0998351616743815,
                ],
                [
                    0.650210097915271, 0.0998351616742987,
                    0.0264215941749068, 0.223533146235523,
                ],
                [
                    0.0998351616745546, 0.223533146235423,
                    0.0264215941747995, 0.650210097915223,
                ],
                [
                    0.071365091252099, 0.0771453147297703,
                    0.658252879686536, 0.193236714331595,
                ],
                [
                    0.0771453147294132, 0.193236714328254,
                    0.658252879690726, 0.0713650912516075,
                ],
                [
                    0.193236714329183, 0.0713650912511828,
                    0.658252879689991, 0.0771453147296435,
                ],
                [
                    0.7061532545902, 0.0194067506859661,
                    0.0754366247922549, 0.199003369931579,
                ],
                [
                    0.019406750685987, 0.199003369931178,
                    0.0754366247922418, 0.706153254590594,
                ],
                [
                    0.199003369931599, 0.706153254589724,
                    0.0754366247926759, 0.0194067506860014,
                ],
                [
                    0.787767898624377, 0.094095000643041,
                    0.0193107884933718, 0.0988263122392104,
                ],
                [
                    0.0940950006428947, 0.0988263122394028,
                    0.0193107884933751, 0.787767898624327,
                ],
                [
                    0.0988263122397104, 0.787767898624153,
                    0.019310788493374, 0.0940950006427622,
                ],
                [
                    0.761555055760951, 0.203923191200666,
                    0.0144005374203604, 0.0201212156180224,
                ],
                [
                    0.203923191200236, 0.0201212156180306,
                    0.0144005374203023, 0.761555055761431,
                ],
                [
                    0.020121215618045, 0.76155505576108,
                    0.0144005374202976, 0.203923191200578,
                ],
                [
                    0.350261451517994, 0.0463757776170109,
                    0.241238715357575, 0.36212405550742,
                ],
                [
                    0.0463757776170434, 0.362124055506635,
                    0.241238715357848, 0.350261451518473,
                ],
                [
                    0.362124055507801, 0.35026145151815,
                    0.241238715357409, 0.0463757776166394,
                ],
                [
                    0.161004565613499, 0.0383054671100454,
                    0.38636881567317, 0.414321151603285,
                ],
                [
                    0.0383054671097917, 0.414321151603789,
                    0.38636881567304, 0.161004565613379,
                ],
                [
                    0.414321151602714, 0.161004565613873,
                    0.386368815673321, 0.0383054671100919,
                ],
                [
                    0.0970412542591999, 0.285151067515758,
                    0.363985089583656, 0.253822588641386,
                ],
                [
                    0.285151067515384, 0.25382258864259,
                    0.363985089582452, 0.0970412542595749,
                ],
                [
                    0.253822588642379, 0.0970412542593522,
                    0.363985089583363, 0.285151067514906,
                ],
                [
                    0.0187741987473799, 0.101440509622378,
                    0.184304953149282, 0.69548033848096,
                ],
                [
                    0.101440509622356, 0.695480338480568,
                    0.184304953149556, 0.0187741987475209,
                ],
                [
                    0.695480338480578, 0.0187741987475054,
                    0.184304953149368, 0.101440509622549,
                ],
                [
                    0.0182320377168822, 0.675694927668797,
                    0.210284481894713, 0.0957885527196078,
                ],
                [
                    0.675694927669442, 0.0957885527190889,
                    0.21028448189463, 0.0182320377168399,
                ],
                [
                    0.0957885527196007, 0.018232037716781,
                    0.21028448189458, 0.675694927669038,
                ],
                [
                    0.00820980056996963, 0.293548850577753,
                    0.600621351466888, 0.0976199973853897,
                ],
                [
                    0.293548850577034, 0.0976199973853832,
                    0.600621351467699, 0.00820980056988381,
                ],
                [
                    0.0976199973850212, 0.00820980056996794,
                    0.600621351466928, 0.293548850578083,
                ],
                [
                    0.207677080283025, 0.503544547262571,
                    0.079081518682363, 0.209696853772041,
                ],
                [
                    0.503544547262585, 0.209696853771787,
                    0.079081518682243, 0.207677080283385,
                ],
                [
                    0.209696853771923, 0.207677080282593,
                    0.0790815186829545, 0.50354454726253,
                ],
                [
                    0.578344735427168, 0.382300946491868,
                    0.0225554241212266, 0.0167988939597373,
                ],
                [
                    0.382300946491731, 0.0167988939596847,
                    0.0225554241211662, 0.578344735427419,
                ],
                [
                    0.0167988939597068, 0.578344735427275,
                    0.0225554241212664, 0.382300946491752,
                ],
                [
                    0.847905447599425, 0.0193223727481762,
                    0.0563838544470134, 0.0763883252053857,
                ],
                [
                    0.0193223727481835, 0.0763883252052791,
                    0.0563838544473551, 0.847905447599182,
                ],
                [
                    0.0763883252049609, 0.847905447600313,
                    0.0563838544466199, 0.0193223727481066,
                ],
                [
                    0.11548607976973, 0.111455158338512,
                    0.762756409274305, 0.0103023526174528,
                ],
                [
                    0.111455158338697, 0.0103023526168254,
                    0.762756409274348, 0.115486079770129,
                ],
                [
                    0.0103023526170701, 0.115486079770071,
                    0.76275640927402, 0.111455158338839,
                ],
                [
                    0.0294603567291924, 0.17754788331361,
                    0.403024150799614, 0.389967609157584,
                ],
                [
                    0.177547883314335, 0.389967609156404,
                    0.403024150800095, 0.029460356729166,
                ],
                [
                    0.389967609156757, 0.0294603567291843,
                    0.403024150800324, 0.177547883313735,
                ],
                [
                    0.195522193757886, 0.0382221895288287,
                    0.562855207221547, 0.203400409491739,
                ],
                [
                    0.0382221895291049, 0.203400409491504,
                    0.562855207221458, 0.195522193757934,
                ],
                [
                    0.2034004094916, 0.195522193757697,
                    0.562855207221453, 0.0382221895292494,
                ],
                [
                    0.580195762401336, 0.017482878960968,
                    0.0230457271156524, 0.379275631522044,
                ],
                [
                    0.0174828789608984, 0.379275631522244,
                    0.0230457271156301, 0.580195762401227,
                ],
                [
                    0.379275631522015, 0.58019576240141,
                    0.0230457271156328, 0.0174828789609419,
                ],
                [
                    0.0912071842858754, 0.00411013141124884,
                    0.398990492863493, 0.505692191439382,
                ],
                [
                    0.00411013141151714, 0.505692191439168,
                    0.398990492865036, 0.0912071842842784,
                ],
                [
                    0.505692191438336, 0.0912071842855746,
                    0.398990492864471, 0.0041101314116178,
                ],
                [
                    0.00478884476429851, 0.952659191058426,
                    0.0332996103306336, 0.00925235384664224,
                ],
                [
                    0.952659191059029, 0.00925235384642567,
                    0.033299610330241, 0.004788844764304,
                ],
                [
                    0.00925235384606473, 0.00478884476393093,
                    0.0332996103300427, 0.952659191059962,
                ],
                [
                    0.385980189187548, 0.391993350183891,
                    0.0306082825276454, 0.191418178100916,
                ],
                [
                    0.391993350183357, 0.191418178100784,
                    0.0306082825277231, 0.385980189188136,
                ],
                [
                    0.191418178100992, 0.385980189186922,
                    0.0306082825276405, 0.391993350184446,
                ],
                [
                    0.547935626185202, 0.0679470990326355,
                    0.303613592364941, 0.0805036824172211,
                ],
                [
                    0.0679470990322547, 0.0805036824168604,
                    0.303613592365006, 0.547935626185879,
                ],
                [
                    0.0805036824174764, 0.547935626184953,
                    0.303613592364535, 0.0679470990330357,
                ],
                [
                    0.153806036080323, 0.332296083385487,
                    0.164432709777014, 0.349465170757176,
                ],
                [
                    0.332296083385749, 0.349465170756816,
                    0.164432709777204, 0.15380603608023,
                ],
                [
                    0.34946517075658, 0.153806036080343,
                    0.164432709777114, 0.332296083385963,
                ],
                [
                    0.680146917763508, 0.101517159170244,
                    0.116272488104425, 0.102063434961823,
                ],
                [
                    0.101517159169978, 0.102063434961844,
                    0.11627248810455, 0.680146917763628,
                ],
                [
                    0.102063434961655, 0.680146917763664,
                    0.11627248810427, 0.101517159170411,
                ],
                [
                    0.00560141769488334, 0.104034774509157,
                    0.602941331965744, 0.287422475830216,
                ],
                [
                    0.104034774509461, 0.287422475829685,
                    0.602941331966148, 0.00560141769470586,
                ],
                [
                    0.287422475830375, 0.00560141769466357,
                    0.602941331965925, 0.104034774509036,
                ],
                [
                    0.0220692941586695, 0.212942537145956,
                    0.743707421056965, 0.0212807476384094,
                ],
                [
                    0.212942537144676, 0.0212807476383709,
                    0.743707421058246, 0.0220692941587074,
                ],
                [
                    0.0212807476385626, 0.0220692941588891,
                    0.743707421060142, 0.212942537142406,
                ],
                [
                    0.923299965157474, 0.0132755319408302,
                    0.00201005864911595, 0.0614144442525802,
                ],
                [
                    0.0132755319407074, 0.0614144442527853,
                    0.00201005864981013, 0.923299965156697,
                ],
                [
                    0.0614144442524975, 0.923299965158544,
                    0.00201005864838767, 0.0132755319405705,
                ],
                [
                    0.00323980932956962, 0.0840088766143168,
                    0.386296150270937, 0.526455163785177,
                ],
                [
                    0.0840088766149807, 0.526455163784271,
                    0.38629615027056, 0.00323980933018845,
                ],
                [
                    0.526455163784847, 0.00323980932993712,
                    0.386296150271221, 0.0840088766139957,
                ],
                [
                    0.51564396354686, 0.234940612488403,
                    0.247491278386732, 0.00192414557800577,
                ],
                [
                    0.234940612489976, 0.00192414557825694,
                    0.24749127838584, 0.515643963545927,
                ],
                [
                    0.00192414557823006, 0.515643963545392,
                    0.247491278387476, 0.234940612488902,
                ],
                [
                    0.302918119329301, 0.302918119329376,
                    0.0912456420123424, 0.30291811932898,
                ],
                [
                    0.00685770368095973, 0.00685770368146038,
                    0.979426888957842, 0.00685770367973804,
                ],
                [
                    0.165887520255092, 0.165887520255045,
                    0.502337439235168, 0.165887520254695,
                ],
                [
                    0.077815923168826, 0.0778159231681738,
                    0.766552230491878, 0.0778159231711218,
                ],
                [
                    0.331723952615001, 0.33172395261399,
                    0.00482814215598728, 0.331723952615022,
                ],
                [
                    0.243221031941515, 0.24322103194167,
                    0.270336904174709, 0.243221031942106,
                ],
                ])
            self.weights = numpy.array([
                0.00432018667747893,
                0.00432018667749443,
                0.00432018667752395,
                0.00669965151714122,
                0.00669965151713374,
                0.00669965151710723,
                0.00155703712356756,
                0.00155703712363116,
                0.00155703712353203,
                0.00368357802029608,
                0.00368357802031626,
                0.00368357802032442,
                0.00347447295226473,
                0.0034744729522679,
                0.00347447295224767,
                0.0110896231152734,
                0.011089623115292,
                0.0110896231151896,
                0.00387126937692817,
                0.00387126937697221,
                0.00387126937694966,
                0.00855055128865891,
                0.00855055128860428,
                0.00855055128867795,
                0.00303071772036869,
                0.00303071772040013,
                0.00303071772040199,
                0.00910786761176,
                0.0091078676117102,
                0.00910786761176689,
                0.00100506631502414,
                0.00100506631503538,
                0.0010050663150537,
                0.00206471289047336,
                0.00206471289046593,
                0.00206471289047783,
                0.000998550935823318,
                0.000998550935835688,
                0.000998550935817332,
                0.00201331727128512,
                0.00201331727127266,
                0.00201331727123011,
                0.00380217207928969,
                0.00380217207928735,
                0.00380217207930181,
                0.00820899791949511,
                0.00820899791944332,
                0.0082089979193634,
                0.00203833519073128,
                0.0020383351907901,
                0.00203833519084034,
                0.00380927411944604,
                0.00380927411947343,
                0.00380927411946211,
                0.00173774080446882,
                0.00173774080447274,
                0.00173774080448579,
                0.00394986517858152,
                0.00394986517861816,
                0.00394986517858676,
                0.0104662994341898,
                0.0104662994341199,
                0.0104662994341631,
                0.00542440929865961,
                0.00542440929867369,
                0.005424409298691,
                0.00157410514067064,
                0.00157410514063102,
                0.00157410514068373,
                0.00307156369548683,
                0.00307156369548445,
                0.00307156369548269,
                0.00151038329450212,
                0.0015103832945096,
                0.00151038329451145,
                0.0150471942142723,
                0.0150471942142768,
                0.0150471942143217,
                0.00572726178378774,
                0.00572726178372018,
                0.00572726178376134,
                0.0100434014204694,
                0.0100434014205505,
                0.0100434014205477,
                0.00546098929129092,
                0.00546098929124484,
                0.00546098929118188,
                0.00734950144224688,
                0.0073495014422093,
                0.00734950144220906,
                0.00408127554061428,
                0.00408127554061233,
                0.00408127554065572,
                0.00362402054426982,
                0.00362402054427563,
                0.00362402054427505,
                0.00196759613460662,
                0.00196759613460262,
                0.00196759613460275,
                0.0114767413960457,
                0.0114767413960974,
                0.0114767413960522,
                0.00961815872955747,
                0.00961815872951902,
                0.00961815872953188,
                0.0147017854453943,
                0.014701785445436,
                0.0147017854454777,
                0.00484593281959669,
                0.00484593281965996,
                0.00484593281964591,
                0.00493101081460294,
                0.00493101081456387,
                0.00493101081456059,
                0.0034643594447675,
                0.00346435944475051,
                0.0034643594447608,
                0.0132295742411856,
                0.0132295742411817,
                0.013229574241251,
                0.00283508246465819,
                0.00283508246464522,
                0.00283508246465808,
                0.00262094309420437,
                0.00262094309418154,
                0.00262094309421372,
                0.00314384255747847,
                0.00314384255738525,
                0.00314384255742799,
                0.00913061913294172,
                0.00913061913291068,
                0.00913061913293557,
                0.00929995524575934,
                0.00929995524575646,
                0.00929995524576649,
                0.00308056444559775,
                0.00308056444558062,
                0.0030805644455898,
                0.00227724226836112,
                0.00227724226838451,
                0.00227724226841222,
                0.000306242271812582,
                0.000306242271805222,
                0.000306242271791608,
                0.00944673970204934,
                0.00944673970204913,
                0.00944673970206581,
                0.010075594148571,
                0.0100755941485464,
                0.0100755941485896,
                0.0179006739481068,
                0.0179006739481154,
                0.0179006739481161,
                0.0100585702279102,
                0.0100585702279099,
                0.0100585702279198,
                0.00309502298940197,
                0.00309502298938067,
                0.00309502298936173,
                0.0028684551031174,
                0.00286845510311146,
                0.002868455103146,
                0.000386552336917729,
                0.000386552336931858,
                0.000386552336897364,
                0.00225666323399646,
                0.00225666323407603,
                0.00225666323404025,
                0.00260666255577667,
                0.00260666255582001,
                0.00260666255582962,
                0.0148895307014724,
                0.000132630471555432,
                0.0162192703850506,
                0.00475972339540625,
                0.00287595285363191,
                0.0190689583089531,
                ])
        elif index == 15:
            self.degree = 18
            bary = numpy.array([
                [
                    0.402153395912455, 0.267805847317026,
                    0.320387028932337, 0.00965372783818291,
                ],
                [
                    0.267805847317044, 0.00965372783817742,
                    0.320387028932318, 0.40215339591246,
                ],
                [
                    0.00965372783817779, 0.402153395912491,
                    0.320387028932303, 0.267805847317029,
                ],
                [
                    0.477411856648227, 0.267326785868425,
                    0.162728234374927, 0.0925331231084208,
                ],
                [
                    0.267326785868413, 0.0925331231083885,
                    0.162728234374953, 0.477411856648245,
                ],
                [
                    0.0925331231084195, 0.477411856648248,
                    0.162728234374932, 0.2673267858684,
                ],
                [
                    0.208457799408109, 0.255795941906351,
                    0.0113344782305252, 0.524411780455015,
                ],
                [
                    0.255795941906343, 0.52441178045503,
                    0.0113344782305276, 0.208457799408099,
                ],
                [
                    0.524411780455004, 0.208457799408117,
                    0.011334478230524, 0.255795941906355,
                ],
                [
                    0.154374253798279, 0.0731393403677088,
                    0.704703873882069, 0.0677825319519432,
                ],
                [
                    0.0731393403677068, 0.0677825319519276,
                    0.704703873882079, 0.154374253798287,
                ],
                [
                    0.067782531951944, 0.15437425379826,
                    0.704703873882076, 0.0731393403677198,
                ],
                [
                    0.0151184354245824, 0.0476594460606897,
                    0.0750995589695265, 0.862122559545201,
                ],
                [
                    0.0476594460606902, 0.862122559545204,
                    0.0750995589695242, 0.0151184354245819,
                ],
                [
                    0.862122559545201, 0.0151184354245831,
                    0.0750995589695319, 0.0476594460606845,
                ],
                [
                    0.74269158348725, 0.235285750794224,
                    0.0116727591178493, 0.0103499066006764,
                ],
                [
                    0.235285750794233, 0.0103499066006743,
                    0.0116727591178434, 0.74269158348725,
                ],
                [
                    0.0103499066006717, 0.742691583487255,
                    0.0116727591178462, 0.235285750794227,
                ],
                [
                    0.0718595893919928, 0.00882912276839053,
                    0.363125126637097, 0.55618616120252,
                ],
                [
                    0.00882912276839673, 0.556186161202529,
                    0.363125126637092, 0.0718595893919827,
                ],
                [
                    0.556186161202537, 0.0718595893919791,
                    0.363125126637095, 0.00882912276838916,
                ],
                [
                    0.273898899050255, 0.0484857732603446,
                    0.605341640005943, 0.0722736876834575,
                ],
                [
                    0.0484857732603445, 0.0722736876834419,
                    0.605341640005955, 0.273898899050259,
                ],
                [
                    0.0722736876834459, 0.273898899050245,
                    0.60534164000596, 0.0484857732603499,
                ],
                [
                    0.0136722640125436, 0.451058467949059,
                    0.0102920818969314, 0.524977186141466,
                ],
                [
                    0.451058467949049, 0.524977186141473,
                    0.0102920818969337, 0.0136722640125444,
                ],
                [
                    0.52497718614148, 0.0136722640125399,
                    0.0102920818969296, 0.451058467949051,
                ],
                [
                    0.185669571420531, 0.00940743474102812,
                    0.498715106027506, 0.306207887810935,
                ],
                [
                    0.00940743474103265, 0.306207887810909,
                    0.49871510602753, 0.185669571420529,
                ],
                [
                    0.306207887810928, 0.185669571420529,
                    0.498715106027514, 0.00940743474102935,
                ],
                [
                    0.371858381761708, 0.00909794171229087,
                    0.605704636558363, 0.0133390399676383,
                ],
                [
                    0.00909794171229431, 0.0133390399676398,
                    0.605704636558364, 0.371858381761702,
                ],
                [
                    0.0133390399676393, 0.3718583817617,
                    0.605704636558373, 0.0090979417122871,
                ],
                [
                    0.00884804648943756, 0.0290441392868168,
                    0.937266061300961, 0.0248417529227848,
                ],
                [
                    0.0290441392868121, 0.0248417529227802,
                    0.937266061300955, 0.00884804648945242,
                ],
                [
                    0.0248417529227838, 0.0088480464894326,
                    0.937266061300963, 0.0290441392868204,
                ],
                [
                    0.770601840442029, 0.0148809324152256,
                    0.145750781988841, 0.0687664451539042,
                ],
                [
                    0.0148809324152255, 0.0687664451539022,
                    0.145750781988846, 0.770601840442026,
                ],
                [
                    0.0687664451539047, 0.770601840442021,
                    0.14575078198885, 0.014880932415225,
                ],
                [
                    0.666734932699802, 0.0688293887795721,
                    0.232066567804036, 0.0323691107165891,
                ],
                [
                    0.0688293887795737, 0.0323691107165826,
                    0.232066567804036, 0.666734932699807,
                ],
                [
                    0.0323691107165853, 0.666734932699818,
                    0.23206656780404, 0.0688293887795564,
                ],
                [
                    0.0910900179584052, 0.343030573977829,
                    0.235433868754166, 0.3304455393096,
                ],
                [
                    0.343030573977809, 0.330445539309593,
                    0.235433868754169, 0.0910900179584291,
                ],
                [
                    0.330445539309608, 0.0910900179584178,
                    0.235433868754155, 0.343030573977819,
                ],
                [
                    0.225555068788837, 0.382826132321645,
                    0.0126442918856655, 0.378974507003852,
                ],
                [
                    0.382826132321636, 0.378974507003854,
                    0.0126442918856658, 0.225555068788844,
                ],
                [
                    0.378974507003849, 0.225555068788825,
                    0.0126442918856677, 0.382826132321658,
                ],
                [
                    0.175288263255126, 0.333784772736308,
                    0.15365688986232, 0.337270074146246,
                ],
                [
                    0.333784772736311, 0.337270074146264,
                    0.153656889862301, 0.175288263255125,
                ],
                [
                    0.337270074146239, 0.175288263255117,
                    0.1536568898623, 0.333784772736344,
                ],
                [
                    0.0160230796339641, 0.423660805665255,
                    0.189701660181996, 0.370614454518784,
                ],
                [
                    0.42366080566525, 0.370614454518775,
                    0.18970166018201, 0.0160230796339652,
                ],
                [
                    0.370614454518771, 0.0160230796339625,
                    0.189701660182, 0.423660805665266,
                ],
                [
                    0.302386926524839, 0.128608112153654,
                    0.506936134632715, 0.0620688266887915,
                ],
                [
                    0.12860811215365, 0.06206882668878,
                    0.506936134632725, 0.302386926524845,
                ],
                [
                    0.0620688266887944, 0.302386926524843,
                    0.506936134632727, 0.128608112153636,
                ],
                [
                    0.451820102412816, 0.013710451058618,
                    0.354024102363695, 0.180445344164871,
                ],
                [
                    0.0137104510586196, 0.180445344164866,
                    0.35402410236368, 0.451820102412834,
                ],
                [
                    0.180445344164869, 0.451820102412822,
                    0.354024102363693, 0.0137104510586164,
                ],
                [
                    0.012771480361006, 0.109575547548148,
                    0.863012752765895, 0.014640219324951,
                ],
                [
                    0.109575547548147, 0.0146402193249524,
                    0.863012752765897, 0.0127714803610037,
                ],
                [
                    0.0146402193249535, 0.0127714803610061,
                    0.863012752765901, 0.109575547548139,
                ],
                [
                    0.0241862526630113, 0.298238620313726,
                    0.328276689484856, 0.349298437538406,
                ],
                [
                    0.298238620313713, 0.349298437538428,
                    0.328276689484843, 0.0241862526630148,
                ],
                [
                    0.349298437538417, 0.0241862526630172,
                    0.328276689484833, 0.298238620313733,
                ],
                [
                    0.343066772448071, 0.172551366066797,
                    0.291028042550599, 0.193353818934532,
                ],
                [
                    0.172551366066847, 0.19335381893454,
                    0.291028042550647, 0.343066772447966,
                ],
                [
                    0.193353818934486, 0.343066772448103,
                    0.291028042550592, 0.172551366066819,
                ],
                [
                    0.0219855041555483, 0.452269887306733,
                    0.365652845101929, 0.160091763435789,
                ],
                [
                    0.452269887306771, 0.160091763435774,
                    0.365652845101904, 0.0219855041555522,
                ],
                [
                    0.160091763435806, 0.0219855041555533,
                    0.365652845101891, 0.45226988730675,
                ],
                [
                    0.0161066476285061, 0.195597672240866,
                    0.504888949609758, 0.28340673052087,
                ],
                [
                    0.19559767224087, 0.283406730520856,
                    0.504888949609768, 0.0161066476285053,
                ],
                [
                    0.283406730520853, 0.0161066476285065,
                    0.504888949609763, 0.195597672240878,
                ],
                [
                    0.473859783075317, 0.172112737761709,
                    0.162468866833267, 0.191558612329707,
                ],
                [
                    0.172112737761722, 0.191558612329691,
                    0.162468866833286, 0.473859783075302,
                ],
                [
                    0.191558612329699, 0.473859783075331,
                    0.162468866833269, 0.172112737761701,
                ],
                [
                    0.608123092139794, 0.0113254032838463,
                    0.296091788088397, 0.0844597164879624,
                ],
                [
                    0.0113254032838496, 0.0844597164879612,
                    0.296091788088401, 0.608123092139789,
                ],
                [
                    0.0844597164879628, 0.608123092139788,
                    0.2960917880884, 0.0113254032838495,
                ],
                [
                    0.172764400522925, 0.0836452861047611,
                    0.28369432202267, 0.459895991349645,
                ],
                [
                    0.083645286104733, 0.459895991349659,
                    0.283694322022679, 0.172764400522929,
                ],
                [
                    0.45989599134965, 0.17276440052292,
                    0.28369432202267, 0.0836452861047597,
                ],
                [
                    0.649951635549552, 0.146884718449437,
                    0.018299964833187, 0.184863681167824,
                ],
                [
                    0.146884718449427, 0.184863681167814,
                    0.0182999648331872, 0.649951635549572,
                ],
                [
                    0.184863681167804, 0.649951635549572,
                    0.0182999648331871, 0.146884718449437,
                ],
                [
                    0.741516029707964, 0.0165109343118972,
                    0.228212657161731, 0.0137603788184073,
                ],
                [
                    0.0165109343118981, 0.0137603788184072,
                    0.22821265716174, 0.741516029707954,
                ],
                [
                    0.0137603788184045, 0.741516029707968,
                    0.228212657161732, 0.0165109343118952,
                ],
                [
                    0.149498332264701, 0.642534016257413,
                    0.177734249077034, 0.0302334024008524,
                ],
                [
                    0.642534016257424, 0.0302334024008539,
                    0.17773424907704, 0.149498332264683,
                ],
                [
                    0.0302334024008516, 0.149498332264693,
                    0.17773424907704, 0.642534016257415,
                ],
                [
                    0.486998239792346, 0.0493519007432767,
                    0.149725236712158, 0.313924622752219,
                ],
                [
                    0.0493519007432852, 0.31392462275222,
                    0.149725236712157, 0.486998239792338,
                ],
                [
                    0.313924622752226, 0.486998239792331,
                    0.149725236712162, 0.0493519007432809,
                ],
                [
                    0.328874443626287, 0.0862424016770105,
                    0.432331128508379, 0.152552026188323,
                ],
                [
                    0.0862424016770119, 0.152552026188312,
                    0.432331128508386, 0.328874443626291,
                ],
                [
                    0.152552026188339, 0.328874443626274,
                    0.432331128508377, 0.0862424016770104,
                ],
                [
                    0.559647144007178, 0.0135684748258195,
                    0.409015522247993, 0.0177688589190101,
                ],
                [
                    0.0135684748258199, 0.0177688589190096,
                    0.409015522247997, 0.559647144007173,
                ],
                [
                    0.0177688589190103, 0.559647144007177,
                    0.409015522247994, 0.0135684748258183,
                ],
                [
                    0.0851402862219274, 0.289852700316415,
                    0.38910094543047, 0.235906068031188,
                ],
                [
                    0.289852700316443, 0.235906068031188,
                    0.389100945430451, 0.0851402862219178,
                ],
                [
                    0.23590606803119, 0.0851402862219275,
                    0.38910094543046, 0.289852700316422,
                ],
                [
                    0.632408604110488, 0.194821777558372,
                    0.079764983472711, 0.0930046348584288,
                ],
                [
                    0.194821777558362, 0.0930046348584223,
                    0.0797649834727282, 0.632408604110488,
                ],
                [
                    0.0930046348584268, 0.632408604110494,
                    0.0797649834727117, 0.194821777558367,
                ],
                [
                    0.716898888020733, 0.195894463180211,
                    0.0158635157491919, 0.0713431330498636,
                ],
                [
                    0.195894463180209, 0.0713431330498587,
                    0.0158635157491958, 0.716898888020736,
                ],
                [
                    0.0713431330498541, 0.716898888020737,
                    0.0158635157491914, 0.195894463180217,
                ],
                [
                    0.85813195995647, 0.0122514981411778,
                    0.0188057482031822, 0.11081079369917,
                ],
                [
                    0.0122514981411758, 0.11081079369917,
                    0.0188057482031809, 0.858131959956473,
                ],
                [
                    0.110810793699169, 0.858131959956473,
                    0.0188057482031802, 0.0122514981411784,
                ],
                [
                    0.72086448940575, 0.0134395201221559,
                    0.0767176683216295, 0.188978322150464,
                ],
                [
                    0.0134395201221537, 0.188978322150464,
                    0.0767176683216285, 0.720864489405754,
                ],
                [
                    0.18897832215046, 0.720864489405759,
                    0.0767176683216252, 0.0134395201221557,
                ],
                [
                    0.0187195076655647, 0.0787740768184682,
                    0.817464709540279, 0.0850417059756883,
                ],
                [
                    0.078774076818469, 0.085041705975691,
                    0.817464709540276, 0.0187195076655642,
                ],
                [
                    0.085041705975693, 0.0187195076655653,
                    0.817464709540278, 0.0787740768184642,
                ],
                [
                    0.100724525378687, 0.00783983320806742,
                    0.681257697378422, 0.210177944034823,
                ],
                [
                    0.00783983320807373, 0.21017794403482,
                    0.68125769737842, 0.100724525378686,
                ],
                [
                    0.210177944034818, 0.100724525378693,
                    0.681257697378414, 0.00783983320807488,
                ],
                [
                    0.40317650797845, 0.0149909317108765,
                    0.502106631164005, 0.0797259291466689,
                ],
                [
                    0.0149909317108771, 0.0797259291466705,
                    0.502106631164002, 0.40317650797845,
                ],
                [
                    0.0797259291466689, 0.403176507978446,
                    0.502106631164005, 0.01499093171088,
                ],
                [
                    0.479624556176077, 0.0698898746008778,
                    0.257293140079446, 0.193192429143599,
                ],
                [
                    0.0698898746008937, 0.193192429143604,
                    0.257293140079458, 0.479624556176045,
                ],
                [
                    0.193192429143603, 0.479624556176067,
                    0.257293140079451, 0.0698898746008791,
                ],
                [
                    0.561348432347315, 0.22389067731113,
                    0.189835104483064, 0.024925785858491,
                ],
                [
                    0.223890677311116, 0.0249257858584865,
                    0.189835104483061, 0.561348432347337,
                ],
                [
                    0.0249257858584887, 0.561348432347325,
                    0.189835104483052, 0.223890677311134,
                ],
                [
                    0.629185887095386, 0.108352902538992,
                    0.175898224128579, 0.0865629862370421,
                ],
                [
                    0.108352902538975, 0.0865629862370412,
                    0.175898224128594, 0.62918588709539,
                ],
                [
                    0.086562986237039, 0.629185887095383,
                    0.175898224128595, 0.108352902538983,
                ],
                [
                    0.449849274559981, 0.140296415952602,
                    0.0681055875518738, 0.341748721935543,
                ],
                [
                    0.140296415952605, 0.341748721935546,
                    0.068105587551874, 0.449849274559974,
                ],
                [
                    0.341748721935556, 0.449849274559965,
                    0.0681055875518764, 0.140296415952602,
                ],
                [
                    0.0509087234595358, 0.16525047454901,
                    0.606894649086132, 0.176946152905322,
                ],
                [
                    0.165250474549021, 0.176946152905315,
                    0.60689464908612, 0.0509087234595436,
                ],
                [
                    0.176946152905304, 0.0509087234595319,
                    0.60689464908614, 0.165250474549024,
                ],
                [
                    0.481985201364133, 0.26055902569048,
                    0.0651935573644129, 0.192262215580974,
                ],
                [
                    0.260559025690468, 0.192262215580966,
                    0.0651935573644146, 0.481985201364151,
                ],
                [
                    0.19226221558098, 0.481985201364128,
                    0.0651935573644163, 0.260559025690476,
                ],
                [
                    0.331408497762104, 0.112643597753789,
                    0.0134868064234796, 0.542461098060628,
                ],
                [
                    0.112643597753794, 0.542461098060611,
                    0.0134868064234806, 0.331408497762115,
                ],
                [
                    0.542461098060611, 0.331408497762118,
                    0.01348680642348, 0.112643597753791,
                ],
                [
                    0.22896225807556, 0.7059180690514,
                    0.0170323187293366, 0.0480873541437034,
                ],
                [
                    0.705918069051398, 0.0480873541437022,
                    0.0170323187293369, 0.228962258075563,
                ],
                [
                    0.0480873541436896, 0.228962258075567,
                    0.017032318729337, 0.705918069051406,
                ],
                [
                    0.0651912939675188, 0.0158826143750247,
                    0.532580403618771, 0.386345688038686,
                ],
                [
                    0.0158826143750231, 0.386345688038688,
                    0.532580403618781, 0.0651912939675076,
                ],
                [
                    0.386345688038682, 0.0651912939675148,
                    0.532580403618777, 0.0158826143750266,
                ],
                [
                    0.610756489884835, 0.0915568727490535,
                    0.0868292128362024, 0.210857424529909,
                ],
                [
                    0.0915568727490545, 0.210857424529909,
                    0.0868292128362066, 0.610756489884829,
                ],
                [
                    0.210857424529913, 0.610756489884832,
                    0.0868292128362, 0.0915568727490549,
                ],
                [
                    0.0810520623738859, 0.37665321562474,
                    0.0151894508664422, 0.527105271134932,
                ],
                [
                    0.376653215624739, 0.527105271134929,
                    0.0151894508664427, 0.0810520623738891,
                ],
                [
                    0.527105271134922, 0.0810520623738846,
                    0.0151894508664418, 0.376653215624751,
                ],
                [
                    0.688797160634863, 0.215420862140538,
                    0.0779441205594219, 0.017837856665177,
                ],
                [
                    0.21542086214055, 0.0178378566651735,
                    0.0779441205594128, 0.688797160634864,
                ],
                [
                    0.0178378566651758, 0.688797160634867,
                    0.077944120559417, 0.21542086214054,
                ],
                [
                    0.495650718185935, 0.0670060501118294,
                    0.362874044201664, 0.0744691875005714,
                ],
                [
                    0.0670060501118351, 0.0744691875005657,
                    0.362874044201665, 0.495650718185934,
                ],
                [
                    0.0744691875005779, 0.49565071818592,
                    0.362874044201664, 0.0670060501118385,
                ],
                [
                    0.222146433641716, 0.021535566444681,
                    0.736831906669808, 0.019486093243795,
                ],
                [
                    0.0215355664446781, 0.0194860932437937,
                    0.73683190666982, 0.222146433641708,
                ],
                [
                    0.0194860932437952, 0.222146433641712,
                    0.736831906669812, 0.0215355664446808,
                ],
                [
                    0.783190190804705, 0.0894662874536291,
                    0.109398094390016, 0.0179454273516499,
                ],
                [
                    0.0894662874536356, 0.0179454273516508,
                    0.109398094390016, 0.783190190804698,
                ],
                [
                    0.0179454273516488, 0.783190190804698,
                    0.109398094390021, 0.0894662874536319,
                ],
                [
                    0.0241059655532886, 0.586686678533797,
                    0.0192045879174376, 0.370002767995476,
                ],
                [
                    0.586686678533799, 0.370002767995477,
                    0.0192045879174364, 0.0241059655532868,
                ],
                [
                    0.370002767995487, 0.0241059655532882,
                    0.0192045879174383, 0.586686678533786,
                ],
                [
                    0.0586261448900714, 0.494791505465875,
                    0.0797762381765805, 0.366806111467473,
                ],
                [
                    0.494791505465885, 0.366806111467477,
                    0.0797762381765776, 0.0586261448900609,
                ],
                [
                    0.366806111467468, 0.0586261448900774,
                    0.0797762381765807, 0.494791505465873,
                ],
                [
                    0.775446737784912, 0.0739439684097598,
                    0.0608872016505133, 0.0897220921548154,
                ],
                [
                    0.0739439684097541, 0.0897220921548168,
                    0.0608872016505138, 0.775446737784915,
                ],
                [
                    0.0897220921548125, 0.77544673778491,
                    0.0608872016505195, 0.0739439684097584,
                ],
                [
                    0.943379208507337, 0.0199121066091266,
                    0.0160859786513147, 0.0206227062322215,
                ],
                [
                    0.0199121066091266, 0.0206227062322205,
                    0.0160859786513156, 0.943379208507337,
                ],
                [
                    0.0206227062322206, 0.943379208507339,
                    0.0160859786513136, 0.0199121066091266,
                ],
                [
                    0.827877848865186, 0.0745911424654966,
                    0.00411031172598635, 0.0934206969433314,
                ],
                [
                    0.0745911424654928, 0.0934206969433272,
                    0.0041103117259856, 0.827877848865194,
                ],
                [
                    0.0934206969433283, 0.827877848865184,
                    0.0041103117259892, 0.0745911424654982,
                ],
                [
                    0.560793513977681, 0.019097732714869,
                    0.0634892906576511, 0.356619462649799,
                ],
                [
                    0.0190977327148682, 0.356619462649797,
                    0.0634892906576537, 0.560793513977681,
                ],
                [
                    0.35661946264979, 0.560793513977684,
                    0.0634892906576574, 0.0190977327148689,
                ],
                [
                    0.00192202346444369, 0.635837625185532,
                    0.226082229966677, 0.136158121383348,
                ],
                [
                    0.635837625185554, 0.13615812138335,
                    0.226082229966662, 0.00192202346443342,
                ],
                [
                    0.136158121383348, 0.00192202346443377,
                    0.226082229966665, 0.635837625185554,
                ],
                [
                    0.0172018730067493, 0.86030781907455,
                    0.0218233687948384, 0.100666939123862,
                ],
                [
                    0.86030781907455, 0.100666939123863,
                    0.0218233687948374, 0.0172018730067494,
                ],
                [
                    0.100666939123864, 0.0172018730067486,
                    0.0218233687948379, 0.86030781907455,
                ],
                [
                    0.0194168552544057, 0.00316346535220149,
                    0.092253471337479, 0.885166208055914,
                ],
                [
                    0.00316346535220335, 0.885166208055921,
                    0.0922534713374701, 0.0194168552544052,
                ],
                [
                    0.885166208055926, 0.0194168552544045,
                    0.0922534713374724, 0.00316346535219705,
                ],
                [
                    0.279251760813055, 0.709847918239123,
                    0.00782663616837473, 0.00307368477944758,
                ],
                [
                    0.709847918239126, 0.00307368477944705,
                    0.00782663616837429, 0.279251760813053,
                ],
                [
                    0.00307368477943649, 0.279251760813076,
                    0.00782663616836957, 0.709847918239118,
                ],
                [
                    0.213749749548486, 0.003009152671001,
                    0.688367350645104, 0.0948737471354093,
                ],
                [
                    0.00300915267100175, 0.0948737471354112,
                    0.688367350645104, 0.213749749548483,
                ],
                [
                    0.0948737471354105, 0.213749749548485,
                    0.688367350645095, 0.00300915267100897,
                ],
                [
                    0.263214069283374, 0.541644794758494,
                    0.19400964245214, 0.00113149350599312,
                ],
                [
                    0.541644794758496, 0.00113149350599239,
                    0.19400964245214, 0.263214069283371,
                ],
                [
                    0.00113149350599936, 0.263214069283379,
                    0.19400964245214, 0.541644794758481,
                ],
                [
                    1.42801265828626e-6, 0.528723493573472,
                    0.0883575261899214, 0.382917552223948,
                ],
                [
                    0.528723493573471, 0.38291755222395,
                    0.0883575261899276, 1.42801265199966e-6,
                ],
                [
                    0.382917552223954, 1.42801266289304e-6,
                    0.0883575261899238, 0.528723493573459,
                ],
                [
                    0.311317746110995, 0.311317746110987,
                    0.0660467616670131, 0.311317746111005,
                ],
                [
                    0.162728432016174, 0.162728432016166,
                    0.511814703951478, 0.162728432016183,
                ],
                [
                    0.220307180915872, 0.220307180915861,
                    0.339078457252562, 0.220307180915704,
                ],
                [
                    0.27189840912706, 0.271898409127019,
                    0.184304772618955, 0.271898409126966,
                ],
                ])
            self.weights = numpy.array([
                0.00264204266351612,
                0.00264204266351436,
                0.0026420426635147,
                0.00692471665149891,
                0.00692471665149564,
                0.006924716651498,
                0.00317777017609773,
                0.00317777017609816,
                0.00317777017609754,
                0.00457987450781227,
                0.00457987450781163,
                0.00457987450781255,
                0.00122052064353493,
                0.00122052064353494,
                0.00122052064353511,
                0.000861411684166711,
                0.000861411684166416,
                0.000861411684166366,
                0.00192329971875275,
                0.00192329971875317,
                0.00192329971875218,
                0.00439205750253336,
                0.0043920575025326,
                0.00439205750253247,
                0.00106773278306368,
                0.00106773278306392,
                0.00106773278306337,
                0.0029835906830448,
                0.00298359068304603,
                0.00298359068304528,
                0.00102285715387307,
                0.00102285715387335,
                0.00102285715387291,
                0.000305696996767753,
                0.000305696996768183,
                0.000305696996767539,
                0.00214506712571504,
                0.00214506712571527,
                0.00214506712571538,
                0.00363791963695073,
                0.00363791963694982,
                0.00363791963694919,
                0.0101472888016191,
                0.0101472888016213,
                0.0101472888016193,
                0.00459907075211436,
                0.00459907075211469,
                0.00459907075211475,
                0.0109625660914245,
                0.0109625660914176,
                0.0109625660914211,
                0.00449251766034198,
                0.00449251766034242,
                0.00449251766034175,
                0.0072235890487306,
                0.00722358904872958,
                0.00722358904873072,
                0.00421124324697362,
                0.0042112432469736,
                0.004211243246973,
                0.000858067778537887,
                0.000858067778537844,
                0.000858067778537943,
                0.00586264963777523,
                0.00586264963777447,
                0.00586264963777552,
                0.0122967514211141,
                0.0122967514211237,
                0.0122967514211141,
                0.005041142997484,
                0.0050411429974846,
                0.00504114299748524,
                0.00469610955916966,
                0.00469610955916985,
                0.0046961095591703,
                0.0114576702539844,
                0.0114576702539863,
                0.0114576702539828,
                0.00303216399755384,
                0.0030321639975543,
                0.0030321639975545,
                0.00922097640767167,
                0.00922097640766967,
                0.00922097640767155,
                0.00407080334659724,
                0.00407080334659738,
                0.00407080334659664,
                0.00148214944256619,
                0.00148214944256621,
                0.0014821494425658,
                0.0051898147386761,
                0.00518981473867607,
                0.00518981473867613,
                0.00784520802719463,
                0.00784520802719414,
                0.00784520802719452,
                0.010856114652411,
                0.0108561146524108,
                0.0108561146524114,
                0.00179366292405914,
                0.00179366292405919,
                0.0017936629240591,
                0.0113353143929493,
                0.0113353143929463,
                0.0113353143929487,
                0.00713332186898381,
                0.00713332186898471,
                0.00713332186898412,
                0.00302772576899891,
                0.00302772576899942,
                0.00302772576899869,
                0.00113119526107161,
                0.00113119526107142,
                0.00113119526107153,
                0.00295301010838164,
                0.00295301010838128,
                0.00295301010838141,
                0.00270610565396758,
                0.00270610565396759,
                0.00270610565396768,
                0.00252414485616197,
                0.00252414485616274,
                0.00252414485616309,
                0.00389426240307846,
                0.00389426240307858,
                0.00389426240307924,
                0.0100080591891181,
                0.0100080591891207,
                0.0100080591891181,
                0.0060193568426668,
                0.00601935684266574,
                0.00601935684266567,
                0.00803165987668141,
                0.00803165987668101,
                0.00803165987668238,
                0.00982302304621952,
                0.00982302304622013,
                0.00982302304621996,
                0.0066642412692711,
                0.0066642412692708,
                0.00666424126927031,
                0.010080849110559,
                0.010080849110559,
                0.0100808491105595,
                0.0042739265137534,
                0.00427392651375389,
                0.00427392651375379,
                0.00288555216389123,
                0.00288555216389123,
                0.00288555216389136,
                0.00357683467377106,
                0.00357683467377095,
                0.00357683467377161,
                0.00839014917153562,
                0.00839014917153661,
                0.00839014917153609,
                0.00422699916760202,
                0.00422699916760212,
                0.00422699916760205,
                0.00378306413257887,
                0.00378306413257825,
                0.00378306413257855,
                0.00760652886054426,
                0.0076065288605441,
                0.00760652886054491,
                0.00201119303800152,
                0.00201119303800112,
                0.0020111930380014,
                0.0030449304604489,
                0.00304493046044918,
                0.00304493046044891,
                0.00250233602742444,
                0.00250233602742419,
                0.00250233602742453,
                0.00807281385853882,
                0.0080728138585382,
                0.00807281385853888,
                0.00492987765936846,
                0.00492987765936844,
                0.00492987765936852,
                0.000665807306131382,
                0.000665807306131388,
                0.000665807306131311,
                0.0011274750604805,
                0.00112747506048044,
                0.00112747506048069,
                0.00430850430308928,
                0.00430850430308939,
                0.00430850430308945,
                0.00142987215228879,
                0.00142987215228772,
                0.00142987215228735,
                0.00159349938559486,
                0.00159349938559481,
                0.00159349938559481,
                0.000540231508089309,
                0.000540231508089322,
                0.000540231508089061,
                0.000485494681520505,
                0.000485494681520465,
                0.000485494681520031,
                0.0017861249815082,
                0.00178612498150836,
                0.0017861249815091,
                0.00225995618483301,
                0.00225995618483306,
                0.00225995618483389,
                0.00155092314083127,
                0.00155092314083083,
                0.00155092314083171,
                0.0112483006511975,
                0.0144449373186453,
                0.00941098059566846,
                0.00907033305470961,
                ])
        else:
            raise ValueError('Illegal Xiao-Gimbutas index')

        self.points = bary[:, [1, 2, 3]]
        return


class ShunnHam(object):
    '''
    Lee Shunn, Frank Ham,
    Symmetric quadrature rules for tetrahedra based on a cubic
    close-packed lattice arrangement,
    Journal of Computational and Applied Mathematics,
    2012,
    <http://dx.doi.org/10.1016/j.cam.2012.03.032>.

    Abstract:
    A family of quadrature rules for integration over tetrahedral volumes is
    developed. The underlying structure of the rules is based on the cubic
    close-packed (CCP) lattice arrangement using 1, 4, 10, 20, 35, and 56
    quadrature points. The rules are characterized by rapid convergence,
    positive weights, and symmetry. Each rule is an optimal approximation in
    the sense that lower-order terms have zero contribution to the truncation
    error and the leading-order error term is minimized. Quadrature formulas up
    to order 9 are presented with relevant numerical examples.
    '''
    def __init__(self, index):
        if index == 1:
            self.weights = numpy.array([
                1.0
                ])
            bary = _s4()
            self.degree = 1
        elif index == 2:
            self.weights = 0.25 * numpy.ones(4)
            bary = _s31(0.1381966011250110)
            self.degree = 2
        elif index == 3:
            self.weights = numpy.concatenate([
                0.0476331348432089 * numpy.ones(4),
                0.1349112434378610 * numpy.ones(6),
                ])
            bary = numpy.concatenate([
                _s31(0.0738349017262234),
                _s22(0.0937556561159491),
                ])
            self.degree = 3
        elif index == 4:
            self.weights = numpy.concatenate([
                0.0070670747944695 * numpy.ones(4),
                0.0469986689718877 * numpy.ones(12),
                0.1019369182898680 * numpy.ones(4),
                ])
            bary = numpy.concatenate([
                _s31(0.0323525947272439),
                _s211(0.0603604415251421, 0.2626825838877790),
                _s31(0.3097693042728620),
                ])
            self.degree = 5
        elif index == 5:
            self.weights = numpy.concatenate([
                0.0021900463965388 * numpy.ones(4),
                0.0143395670177665 * numpy.ones(12),
                0.0250305395686746 * numpy.ones(6),
                0.0479839333057554 * numpy.ones(12),
                0.0931745731195340 * numpy.ones(1)
                ])
            bary = numpy.concatenate([
                _s31(0.0267367755543735),
                _s211(0.0391022406356488, 0.7477598884818090),
                _s22(0.0452454000155172),
                _s211(0.2232010379623150, 0.0504792790607720),
                numpy.array([[0.25, 0.25, 0.25, 0.25]]),
                ])
            self.degree = 6
        elif index == 6:
            self.weights = numpy.concatenate([
                0.0010373112336140 * numpy.ones(4),
                0.0096016645399480 * numpy.ones(12),
                0.0164493976798232 * numpy.ones(12),
                0.0153747766513310 * numpy.ones(12),
                0.0293520118375230 * numpy.ones(12),
                0.0366291366405108 * numpy.ones(4),
                ])
            bary = numpy.concatenate([
                _s31(0.0149520651530592),
                _s211(0.0340960211962615, 0.1518319491659370),
                _s211(0.0462051504150017, 0.5526556431060170),
                _s211(0.2281904610687610, 0.0055147549744775),
                _s211(0.3523052600879940, 0.0992057202494530),
                _s31(0.1344783347929940)
                ])
            self.degree = 8
        else:
            raise ValueError('Illegal Shunn-Ham index')

        self.points = bary[:, 1:]
        return
