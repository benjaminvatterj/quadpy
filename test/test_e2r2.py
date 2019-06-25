# -*- coding: utf-8 -*-
#
import numpy
import pytest

import quadpy
from helpers import check_degree, integrate_monomial_over_enr2

schemes = [
    quadpy.e2r2.haegemans_piessens_a(),
    quadpy.e2r2.haegemans_piessens_b(),
    quadpy.e2r2.rabinowitz_richter_1(),
    quadpy.e2r2.rabinowitz_richter_2(),
    quadpy.e2r2.rabinowitz_richter_3(),
    quadpy.e2r2.rabinowitz_richter_4(),
    quadpy.e2r2.rabinowitz_richter_5(),
    quadpy.e2r2.stroud_4_1(),
    quadpy.e2r2.stroud_5_1(),
    quadpy.e2r2.stroud_5_2(),
    quadpy.e2r2.stroud_7_1(),
    quadpy.e2r2.stroud_7_2(),
    quadpy.e2r2.stroud_9_1(),
    quadpy.e2r2.stroud_11_1(),
    quadpy.e2r2.stroud_11_2(),
    quadpy.e2r2.stroud_13_1(),
    quadpy.e2r2.stroud_15_1(),
    quadpy.e2r2.stroud_secrest_v(),
    quadpy.e2r2.stroud_secrest_vi(),
]


@pytest.mark.parametrize("scheme", schemes)
def test_scheme(scheme, tol=1.0e-14):
    assert scheme.points.dtype == numpy.float64, scheme.name
    assert scheme.weights.dtype == numpy.float64, scheme.name

    degree = check_degree(
        lambda poly: scheme.integrate(poly),
        integrate_monomial_over_enr2,
        2,
        scheme.degree + 1,
        tol=tol,
    )
    assert degree == scheme.degree, "{}    Observed: {}   expected: {}".format(
        scheme.name, degree, scheme.degree
    )
    return


@pytest.mark.parametrize("scheme", [quadpy.e2r2.rabinowitz_richter_1()])
def test_show(scheme):
    scheme.show()
    return


if __name__ == "__main__":
    # scheme_ = quadpy.e2r2.Stroud["7-2"]()
    # test_scheme(scheme_, 1.0e-14)
    # test_show(scheme_)
    from helpers import find_equal

    find_equal(schemes)
