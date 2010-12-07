"""
Plot without ticks and labels.
"""

import sys;    sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def axes_example11(epsoutfile):
    g=pyxgraph(xlimits=(-1.0, 7.0), ylimits=(-2.0,4.0), key=False,
               xticks=False, yticks=False)

    # if everything is ok, the sin extends over the full y axis
    g.pyxplot("y(x)=1.0+3*sin(x)")
    g.pyxsave(epsoutfile)

    
if __name__=="__main__":
    axes_example11("axes11.eps")
