"""Plot with no ticks on opposite sides."""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def axes_example6(epsoutfile):
    g=pyxgraph(xlimits=(0.0, 8.0), xticks=(0.0, 8.0, 4.0), 
               ylimits=(0.0, 100.0),
               x2ticks=False, y2ticks=False
               )
    g.pyxplot(("test_data2.dat",1,2), title=r"$x^2$", style="l", color=2, lw=3)
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    axes_example6("axes6.eps")
