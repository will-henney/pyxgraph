"""Contour on top of bitmap plot, with labeling."""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
import pyx
from numerix import arange, sin, cos, NewAxis, ravel

def array_example2(epsoutfile):
    x = (arange(100.0)-50)/25.0
    y = (arange(100.0)-50)/25.0
    # Important: z[y, x] -- y first!
    z = 5.0*sin(2*x[NewAxis, :]) + 3.0*cos(3*y[:, NewAxis])

    colmap = ColMapper.ColorMapper("yellow-red", invert=1, exponent=0.55,
                                   brightness=0.5)
    #lut = colmap.generate_lut()

#    c = pyx.canvas.canvas()
    g = pyxgraph(xlimits=(min(x), max(x)), ylimits=(min(y), max(y)),
                 width=6, height=6, key=False)
    g.pyxplotarray(z[::-1,:], colmap=colmap)
    g.pyxplotcontour(z, x, y, colors='color', color='black', labels=True)
   
    pyxsave(g, epsoutfile)


if __name__=="__main__":
    array_example2("array5.eps")
