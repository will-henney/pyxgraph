"""Showing off all symbols"""

import sys;   sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
from numerix import zeros, arange


def symbols(epsoutfile):
    y = arange(5)/5.0+0.1
    
    g = pyxgraph(xlimits=(-1, 25), ylimits=(0, 1),           
                 xticks=(0, 24, 2), yticks=(0, 1, 1), key=None) 
    
    for i in xrange(25):
        x = zeros(5)+i   
        g.pyxplot((x, y), style="p", pt=i)   # ``pt=i`` can be omitted
                                             # (then the next symbol is choosen
                                             #  automatically)
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    symbols("symbols.eps")
