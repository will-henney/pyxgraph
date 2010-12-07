"""Plot a two-dimensional error as bitmap and a colorbar."""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
import pyx
from numerix import arange, sqrt, cos, NewAxis, ravel

def array_example2(epsoutfile):
    x = (arange(50.0)-25)/2.0
    y = (arange(50.0)-25)/2.0
    r = sqrt(x[:,NewAxis]**2+y**2)
    z = 5.0*cos(r)  

    colmap = ColMapper.ColorMapper("yellow-red", exponent=0.55, brightness=0.5)
    lut = colmap.generate_lut()

    c = pyx.canvas.canvas()
    g = pyxgraph(xlimits=(min(x), max(x)), ylimits=(min(y), max(y)),
                 width=6, height=6)
    g.pyxplot("y(x)=sin(x)", style="p")  # FIXME: can't do empty plots!
    g.pyxplotarray(z, colmap=lut)
    c.insert(g)

    cb = pyxcolorbar(lut=lut, frame=g, pos=(1.1,0.0),
                     minvalue=min(ravel(z)), maxvalue=max(ravel(z)))
    c.insert(cb)
    
    pyxsave(c, epsoutfile)


if __name__=="__main__":
    array_example2("array2.eps")
