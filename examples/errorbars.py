"""
Plot with errorbars
"""

import sys;    sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def errorbars(epsoutfile):
    g = pyxgraph(xlimits=(0,1), ylimits=(0,1), key="br")
    
    x = [0.1, 0.3, 0.5, 0.7, 0.9]
    mean = [0.05, 0.1, 0.2, 0.4, 0.8]
    error = [0.05, 0.07, 0.17, 0.15, 0.15]
    
    g.pyxerrorbar(x, mean, error, pt=17, ps=1.0, lt=0, lw=1, title="data")
    
    g.pyxsave(epsoutfile)

    
if __name__=="__main__":
    errorbars("errorbars.eps")
