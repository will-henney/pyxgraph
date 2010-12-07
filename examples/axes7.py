"""piaxis example and background color"""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
from math import pi


def axes_example7(epsoutfile):
    g=pyxgraph(xlimits=(0.0, 2.0*pi), key="bl", xaxistype="pi", ylabel="$y$",
               backgroundattrs=[pyx.deco.filled(
                                      [pyx.color.rgb(0.9, 0.9, 1.0)])])
    g.pyxplot("y(x)=sin(x)", title=r"$\sin(x)$", style="l")
    g.pyxplot("y(x)=cos(x)", title=r"$\cos(x)$", style="l", lw=2, dl=3)
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    axes_example7("axes7.eps")
