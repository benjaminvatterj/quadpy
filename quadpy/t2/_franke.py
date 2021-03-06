import numpy

from ..helpers import article
from ._helpers import T2Scheme, register

source = article(
    authors=["Richard Franke"],
    title="Obtaining cubatures for rectangles and other planar regions by using orthogonal polynomials",
    journal="Math. Comp.",
    volume="25",
    year="1971",
    pages="803-817",
    url="https://doi.org/10.1090/S0025-5718-1971-0300440-5",
)


def franke_09():
    a1 = 0.646341098016171e-1
    a2 = 0.250478764260821
    a3 = 0.405288113134598
    a4 = 0.483428507060240
    b1 = 0.490241549057468e-1
    c1 = 0.312418129002285
    b2 = 0.272654917225016e-1
    c2 = 0.649829918830148
    b3 = 0.748092005042521e-2
    c3 = 0.922929224698637
    b4 = 0.166718687651425
    c4 = 0.775796880494268
    b5 = 0.151969575382297
    c5 = 0.569101341800312

    points = numpy.array(
        [
            [a1, a2, a3, a4, b1, c1, b2, c2, b3, c3, b4, c4, b5, c5],
            [a1, a2, a3, a4, c1, b1, c2, b2, c3, b3, c4, b4, c5, b5],
        ]
    )
    weights = 2 * numpy.array(
        [
            0.263321501360460e-1,
            0.666750609902085e-1,
            0.598398472297514e-1,
            0.302244308027287e-1,
            0.387139102462897e-1,
            0.387139102462897e-1,
            0.223103130816147e-1,
            0.223103130816147e-1,
            0.930956404694027e-2,
            0.930956404694027e-2,
            0.365382927009296e-1,
            0.365382927009296e-1,
            0.515921753448585e-1,
            0.515921753448585e-1,
        ]
    )
    points = numpy.array([points[0], points[1], 1 - points[0] - points[1]])

    return T2Scheme("Franke 9", {"plain": numpy.vstack([weights, points])}, 7, source)


def franke_10():
    a1 = 0.643211570115959e-1
    a2 = 0.252998331385515
    a3 = 0.409747314294030
    a4 = 0.485462287928209
    b1 = 0.504085933570127e-1
    c1 = 0.310554843559296
    b2 = 0.279122578437840e-1
    c2 = 0.647673797923676
    b3 = 0.364079378827516e-1
    c3 = 0.895785844039319
    b4 = 0.202348915694331
    c4 = 0.743375252660890
    b5 = 0.160040255710345
    c5 = 0.564851216876248

    points = numpy.array(
        [
            [a1, a2, a3, a4, b1, c1, b2, c2, b3, c3, b4, c4, b5, c5],
            [a1, a2, a3, a4, c1, b1, c2, b2, c3, b3, c4, b4, c5, b5],
        ]
    )
    weights = 2 * numpy.array(
        [
            0.260816160868233e-1,
            0.663602357926664e-1,
            0.561731171392644e-1,
            0.239526221275731e-1,
            0.394576126986614e-1,
            0.394576126986614e-1,
            0.235501218540342e-1,
            0.235501218540342e-1,
            0.162658476936259e-1,
            0.162658476936259e-1,
            0.318232366904684e-1,
            0.318232366904684e-1,
            0.526193854900464e-1,
            0.526193854900464e-1,
        ]
    )
    points = numpy.array([points[0], points[1], 1 - points[0] - points[1]])

    return T2Scheme("Franke 10", {"plain": numpy.vstack([weights, points])}, 7, source)


register([franke_09, franke_10])
