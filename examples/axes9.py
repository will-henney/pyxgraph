"""
Put axes labels slightly below the line of the x-tick labels.
and similarly for the y-axis.

Some prefer this style of labeling.
"""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def axes9(epsoutfile):
    """Different axis label positions"""
    c = pyx.canvas.canvas()
    
    g1 = pyxgraph(xlimits=(0.0, 10.0), key="bl")
    g1.pyxplot("y(x)=sin(x)")
    g1.pyx_xlabel("x")
    g1.pyx_ylabel("y")
    c.insert(g1)
    
    g2=pyxgraph(ypos=g1.ypos-1.2*g1.height, xlimits=(0.0, 0.1), key=False)
    g2.pyxplot("y(x)=sin(x)")
    g2.pyx_xlabel("x", xpos=0.7, yshift=-0.5)
    g2.pyx_ylabel("y", ypos=0.8, xshift=-2.0)
    g2.pyxlabel((0.4, 0.8), "Shifting labels in x and y, respectively")
    c.insert(g2)

    pyxsave(c, epsoutfile)


if __name__=="__main__":
    axes9("axes9.eps")


