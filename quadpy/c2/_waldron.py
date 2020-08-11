import numpy

from ..helpers import techreport
from ._helpers import C2Scheme

source = techreport(
    authors=["Shayne Waldron"],
    title="Symmetries of linear functionals",
    institution="University of Wisconsin-Madison, Center for Mathematical Sciences",
    note="CMS Technical Summary Report",
    month="oct",
    year="1994",
    url="http://ftp.cs.wisc.edu/Approx/symmetries.pdf",
)


def waldron(r, alpha):
    assert r ** 2 >= 1 / 3

    R = r / numpy.sqrt(3 * r ** 2 - 1)

    beta = alpha + numpy.pi / 2

    sin_alpha = numpy.sin(alpha)
    cos_alpha = numpy.cos(alpha)
    sin_beta = numpy.sin(beta)
    cos_beta = numpy.cos(beta)

    points = numpy.array(
        [
            [+r * cos_alpha, +r * sin_alpha],
            [-r * cos_alpha, -r * sin_alpha],
            [+R * cos_beta, +R * sin_beta],
            [-R * cos_beta, -R * sin_beta],
        ]
    )

    weights = numpy.array(
        [2 / 3 / r ** 2, 2 / 3 / r ** 2, 2 / 3 / R ** 2, 2 / 3 / R ** 2]
    )
    weights /= 4
    return C2Scheme("Waldron", weights, points, 3, source)
