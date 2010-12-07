"""Additional attributes for lines.

Background:

Postscript has a command "setlinejoin" which selects either
mitred, rounded, or beveled corners.
http://www.capcode.de/help/setlinejoin


"""

import sys;   sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
from numerix import arange


def styles_example2(epsoutfile):
    x = arange(2.0, 10.0, 0.1)
    y = 0.0*x
    y[::2] = 1.0
    
    g = pyxgraph(xlimits=(0, 10), ylimits=(-1, 6), key=None, width=8)

    # lines for comparison:
    x2 = arange(0.0, 5.0, 0.1)
    for i in xrange(6):
        g.pyxplot((x2, 0*x2+i), color=(0.6, 0.6, 0.6), style="l",
                  lt=0, lw=0.25)

    g.pyxplot((x, y), style="l", lt=0)  # pyx.style.linejoin.meter is default
    g.pyxplot((x, y+2), style="l", lt=0,
              lineattrs=[pyx.style.linejoin.bevel])
    g.pyxplot((x, y+4), style="l", lt=0,
              lineattrs=[pyx.style.linejoin.round])

    txtstyle = [pyx.text.halign.left, pyx.text.valign.middle]
    g.pyxlabel((0.5, 0.5), "miter", txtstyle, graphcoords=True)
    g.pyxlabel((0.5, 2.5), "bevel", txtstyle, graphcoords=True)
    g.pyxlabel((0.5, 4.5), "round", txtstyle, graphcoords=True)
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    styles_example2("styles_example2.eps")
