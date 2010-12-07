"""Different colorbars."""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
import pyx
from numerix import arange, sqrt, cos, NewAxis, ravel


def colorbars(epsoutfile):
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

    minz = minvalue=min(ravel(z))
    maxz = maxvalue=max(ravel(z))

    # --- vertical bars
    dist = 1.2
    for orientation, position in [("vertical", "right"),
                                  ("vertical", "middle"),
                                  ("vertical2", "middle")]:
        cb = pyxcolorbar(lut=lut, frame=g,
                         pos=(dist, 0),
                         orientation = orientation,
                         position = position,
                         minvalue = minz, maxvalue=maxz)
        # add a short note on the style:
        txt = orientation[0]
        if "2" in orientation:
            txt += "2"
        txt += ", "+position[0]            
        cb.pyxlabel( (0.0, 1.3), txt, style=[pyx.text.halign.left])

        c.insert(cb)
        dist = dist + 0.5

    # horizontal ones:
    dist = -0.3
    for orientation, position in [("horizontal", "middle"),
                                  ("horizontal2", "middle")]:
        cb = pyxcolorbar(lut=lut, frame=g, pos=(0.0, dist),
                         orientation = orientation,
                         position = position,
                         minvalue = minz, maxvalue=maxz)
        # add a short note on the style:
        txt = orientation[0]
        if "2" in orientation:
            txt += "2"
        txt += ", "+position[0]            
        cb.pyxlabel( (1.3, 0.5), txt, style=[pyx.text.halign.left])

        c.insert(cb)
        dist = dist - 0.3
    
    pyxsave(c, epsoutfile)


if __name__=="__main__":
    colorbars("colorbars.eps")
