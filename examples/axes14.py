"""
linear plot, ticks in exponential notation
"""

import sys;    sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
from pyx.graph import axis


def axes_example1(epsoutfile):
    g=pyxgraph(yaxistype=axis.axis.linear(min=0, max=10e-4),
               xlimits=(0, 100), key="br")
               
    x = arange(100)
    y = x**2/10e6
               
    g.pyxplot((x, y), title=r"$x^2/10^{-6}$")
    g.dodata()               # draw data first and then the border on top
    g.pyxsave(epsoutfile)

    
if __name__=="__main__":
    axes_example1("axes14.eps")
