"""Plot with x2axes and y2axes."""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def axes_example4(epsoutfile):
    g=pyxgraph(xticks=False, yticks=False,
               # the xlimits and ylimits are needed so that it is
               # known on which axes the function will be plotted.
               xlimits=(0.0,8.0), ylimits=(0.0,100.0),
               x2axistype="linear", y2axistype="linear",
               x2limits=(0.0,8.0), x2ticks=(0.0,8.0,4.0), 
               y2limits=(0.0,100.0), y2ticks=(0.0,100.0,25.0),
               x2texter=None, y2texter=None,
               )
    g.pyxplot("y(x)=x**2", title=r"$x^2$", style="l", linetype=4)
    g.pyxsave(epsoutfile)

# FIXME: how to get ticks, but no labels at x and y ? --> linked stuff...

if __name__=="__main__":
    axes_example4("axes4.eps")
