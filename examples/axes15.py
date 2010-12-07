"""axis example with fractional numbers and background color"""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
from math import pi


def axes_example15(epsoutfile):
    g=pyxgraph(xlimits=(0.0, 2.0), key="bl", xaxistype="frac", ylabel="$y$",
               xticks=(0,2,0.25),
               backgroundattrs=[pyx.deco.filled(
                                      [pyx.color.rgb(0.9, 0.9, 1.0)])])
    g.pyxplot("y(x)=sin(x*2*pi)", title=r"$\sin(2\pi x)$", style="l")
    g.pyxplot("y(x)=cos(x*2*pi)", title=r"$\cos(2\pi x)$", style="l", lw=2, dl=3)
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    axes_example15("axes15.eps")
