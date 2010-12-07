"""Plot a two-dimensional error as bitmap."""

import sys;    sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
import pyx
from numerix import arange, sqrt, sin, NewAxis

def array_example1(epsoutfile):
    x = (arange(50.0)-25)/2.0
    y = (arange(50.0)-25)/2.0
    r = sqrt(x[:,NewAxis]**2+y**2)
    z = 5.0*sin(r)  

    g=pyxgraph(xlimits=(min(x), max(x)), ylimits=(min(y), max(y)),
               width=6, height=6, key=False)
    # WARNING: if key is not specified to be False, one gets a weird
    # error ....
    #g.pyxplot("y(x)=sin(x)", style="p")  # FIXME: can't do empty plots!
    g.pyxplotarray(z, colmap=ColMapper.ColorMapper("yellow-red",
                                                exponent=0.55, brightness=0.5))
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    array_example1("array1.eps")
