import numpy
import pytest
from numpy import cos, pi, sin

import quadpy


def test_x():
    val, _ = quadpy.c1.integrate_adaptive(lambda x: x, [-1, 1])
    exact = 0.0
    assert abs(exact - val) < 1.0e-10


def test_372():
    # https://github.com/nschloe/quadpy/issues/372
    val, _ = quadpy.c1.integrate_adaptive(lambda x: [0 * x, 2 * x], [0, 1])
    exact = [0.0, 1.0]
    assert numpy.all(numpy.abs(exact - val) < 1.0e-10)


def test_sin():
    val, _ = quadpy.c1.integrate_adaptive(sin, [0.0, pi], 1.0e-10)
    exact = 2.0
    assert abs(exact - val) < 1.0e-10

    val, _ = quadpy.c1.integrate_adaptive(lambda x: x * sin(x), [0.0, pi], 1.0e-10)
    exact = pi
    assert abs(exact - val) < 1.0e-10


@pytest.mark.parametrize("k", range(1, 6))
def test_vector_valued(k):
    # We need to set eps_rel=None here since the second integral can be 0. This leads to
    # an unreachable stopping criterion.
    val, err = quadpy.c1.integrate_adaptive(
        lambda x: [x * sin(k * x), x * cos(k * x)], [0.0, pi], 1.0e-10, eps_rel=None
    )
    exact = [
        (sin(pi * k) - pi * k * cos(pi * k)) / k ** 2,
        (cos(pi * k) + pi * k * sin(pi * k) - 1.0) / k ** 2,
    ]
    assert numpy.all(err < 1.0e-10)
    assert numpy.all(numpy.abs(exact - val) < 1.0e-9)


def test_multidim():
    # simple scalar integration
    val, err = quadpy.c1.integrate_adaptive(sin, [0.0, 1.0])
    assert err < 1.0e-10
    assert val.shape == ()
    exact = 1.0 - cos(1.0)
    assert abs(val - exact) < 1.0e-10

    # # scalar integration on 3 subdomains
    # val, err = quadpy.c1.integrate_adaptive(
    #     sin, [[0.0, 1.0, 2.0], [1.0, 2.0, 3.0]]
    # )
    # assert err.shape == (3,)
    # assert all(e < 1.0e-10 for e in err)
    # assert val.shape == (3,)
    # exact = [cos(0.0) - cos(1.0), cos(1.0) - cos(2.0), cos(2.0) - cos(3.0)]
    # assert all(abs(v - ex) < 1.0e-10 for v, ex in zip(val, exact))

    # scalar integration in 3D
    alpha = 10.31
    val, err = quadpy.c1.integrate_adaptive(
        lambda x: sin(alpha * x[0]),
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
    )
    assert err < 1.0e-10
    assert val.shape == ()
    exact = -1 / alpha * (cos(alpha * 1.0) - cos(alpha * 0.0))
    assert abs(val - exact) < 1.0e-10

    # vector-valued integration on 1 subdomain
    val, err = quadpy.c1.integrate_adaptive(lambda x: [sin(x), cos(x)], [0.0, 1.0])
    assert err.shape == (2,)
    assert all(e < 1.0e-10 for e in err)
    exact = [cos(0.0) - cos(1.0), sin(1.0) - sin(0.0)]
    assert val.shape == (2,)
    assert all(abs(v - ex) < 1.0e-10 for v, ex in zip(val, exact))

    # # vector-valued integration on 3 subdomains
    # val, err = quadpy.c1.integrate_adaptive(
    #     lambda x: [sin(x), cos(x)], [[0.0, 1.0, 2.0], [1.0, 2.0, 3.0]]
    # )
    # assert err.shape == (2, 3)
    # assert numpy.all(err < 1.0e-10)
    # assert val.shape == (2, 3)
    # exact = [
    #     [cos(0.0) - cos(1.0), cos(1.0) - cos(2.0), cos(2.0) - cos(3.0)],
    #     [sin(1.0) - sin(0.0), sin(2.0) - sin(1.0), sin(3.0) - sin(2.0)],
    # ]
    # assert numpy.all(numpy.abs(val - exact) < 1.0e-10)

    # vector-valued integration in 3D
    val, err = quadpy.c1.integrate_adaptive(
        lambda x: [x[0] + sin(x[1]), cos(x[0]) * x[2]],
        [[0.0, 1.0, 2.0], [1.0, 2.0, 3.0]],
    )
    assert err.shape == (2,)
    assert numpy.all(err < 1.0e-10)
    assert val.shape == (2,)

    # another vector-valued integration in 3D
    # This is one case where the integration routine may not properly recognize the
    # dimensionality of the domain. Use the `dim` parameter.
    val, err = quadpy.c1.integrate_adaptive(
        lambda x: [x[0] + sin(x[1]), cos(x[0]) * x[2], sin(x[0]) + x[1] + x[2]],
        [[0.0, 1.0, 2.0], [1.0, 2.0, 3.0]],
        domain_shape=(3,),
        range_shape=(3,),
    )
    assert val.shape == (3,)
    assert err.shape == (3,)


@pytest.mark.parametrize("k", range(4, 12))
def test_sink(k):
    val, _ = quadpy.c1.integrate_adaptive(
        lambda x: sin(k * x), [0.0, pi], 1.0e-10, eps_rel=None
    )
    exact = (1.0 - cos(k * pi)) / k
    assert abs(exact - val) < 1.0e-9


def test_236():
    # https://github.com/nschloe/quadpy/issues/236
    def f(x):
        return numpy.exp(-1.0 / (1 - x ** 2))

    val, err = quadpy.quad(f, -1, 1)
    assert err < 1.0e-9


def test_infinite_limits():
    tol = 1.0e-7
    val, err = quadpy.quad(lambda x: numpy.exp(-(x ** 2)), -numpy.inf, numpy.inf)
    assert abs(val - numpy.sqrt(numpy.pi)) < tol
    assert err < tol

    val, err = quadpy.quad(lambda x: numpy.exp(-x), 0.0, numpy.inf)
    assert abs(val - 1.0) < tol
    assert err < tol

    val, err = quadpy.quad(lambda x: numpy.exp(+x), -numpy.inf, 0)
    assert abs(val - 1.0) < tol
    assert err < tol


def test_245():
    # https://github.com/nschloe/quadpy/issues/245
    def f(x):
        return x + x * 1j

    val, err = quadpy.quad(f, 0, 1)
    assert err < 1.0e-9


if __name__ == "__main__":
    test_372()
    # test_vector_valued(1)
    # test_simple()
