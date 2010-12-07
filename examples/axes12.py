"""
ticks and subticks
"""

import sys;    sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def axes_example12(epsoutfile):
    #from pyx.graph.axis import tick

    g=pyxgraph(xlimits=(0.01, 10.0), ylimits=(-2.0,2.0), key=False,
               xaxistype="log",
               xticks=(0.01, 10.0, 10, 10),
               yticks=(-2.0, 2.0, 1.0, 5))

    # if everything is ok, the sin extends over the full y axis
    g.pyxplot("y(x)=2*sin(x)", style="l", color="blue")
    g.pyxsave(epsoutfile)

    
if __name__=="__main__":
    axes_example12("axes12.eps")
