"""Example for a contour plot."""

import sys;    sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
from numerix import arange, sin, cos, NewAxis

def array_example1(epsoutfile):
    x = (arange(100.0)-50)/25.0
    y = (arange(100.0)-50)/25.0
    # Important: z[y, x] -- y first!
    z = 5.0*sin(2*x[NewAxis, :]) + 3.0*cos(3*y[:, NewAxis])

    g=pyxgraph(xlimits=(min(x), max(x)), ylimits=(min(y), max(y)),
               width=6, height=6, key=False)
    g.pyxplotcontour(z, x, y, levels=15, colors='map',
                     colmap=ColMapper.ColorMapper("pm3d",
                                                exponent=1.0, brightness=0.2))
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    array_example1("array4.eps")
