"""Stroking and filling of regions"""

import sys;   sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
from numerix import arange, sin, cos, pi


def convert_to_path(g, x, y, close_path=True):
    """Convert the coordinates from the arrays x and y to a (closed) path."""
    p = pyx.path.path()
    p.append(pyx.path.moveto(*g.pos(x[0], y[0])))
    for i in xrange(1, len(x)):
        p.append(pyx.path.lineto(*g.pos(x[i], y[i])))
    if close_path:
        p.append(pyx.path.closepath())
        
    return p


def filled_regions(epsoutfile):
    x = arange(0.0, 10.0, 0.1)
    phi = arange(0.0, 2.0*pi, 0.1)
    x_circ = cos(phi)-1.5
    y_circ = sin(phi)-1.0

    x_ell = 1.5*cos(phi)+1.0
    y_ell = 0.5*sin(phi)+0.5

    g=pyxgraph(xlabel=r"$x$", ylabel=r"$y$", xlimits=(-3.0, 3.0),
               ylimits=(-4.0, 4.0), key=False)      
    g.pyxplot((x, -sin(x)-1.0), style="p", title=None)  # we need at least one plot!!
                                                   # even if invisible
    p1 = convert_to_path(g, x_circ, y_circ)
    g.stroke(p1, [pyx.deco.filled([pyx.color.rgb(0.8, 0.8, 0.8)])])

    p2 = convert_to_path(g, x_ell, y_ell)
    g.stroke(p2, [pyx.deco.stroked([pyx.color.rgb(0.8, 0.2, 0.0)]),
                 pyx.style.linewidth(0.35),
                 pyx.deco.filled([pyx.color.rgb(0.8, 0.8, 0.8)]),
                 ])

    # a more funny shape
    p3 = convert_to_path(g, phi/2.0/pi*x_ell-2.4, 3*y_ell+0.5)
    g.fill(p3, [pyx.deco.filled([pyx.color.rgb(0.2, 0.8, 0.2)]),
                 ])

    g.pyxsave(epsoutfile)


if __name__=="__main__":
    filled_regions("filled_regions.eps")
