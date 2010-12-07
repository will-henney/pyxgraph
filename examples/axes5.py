"""Plot with x2axis, y2axis removed."""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def axes_example5(epsoutfile):
    g=pyxgraph(xlimits=(0.0, 8.0), xticks=(0.0, 8.0, 4.0), 
               ylimits=(0.0, 100.0), yticks=(0.0, 100.0, 25.0),
               x2axistype=False, y2axistype=False)
    g.pyxplot(("test_data2.dat", 1, 2), title=r"$x^2$", style="l", color=3)
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    axes_example5("axes5.eps")
