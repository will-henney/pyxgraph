"""Different linestyles"""

import sys;   sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
from numerix import ones, arange


def styles_example(epsoutfile):
    x1 = 0.25*arange(2)
    x2 = x1+0.5-0.125
    x3 = x1+1.0-0.25
    
    g = pyxgraph(xlimits=(-0.1, 1.1), xticks=(0, 1, 1),
                 ylimits=(-1, 12), yticks=(0, 11, 1),
                 ylabel='linestyles', key=None, width=8)
    for i in xrange(12):
        y = ones(2)+i-1 
        g.pyxplot((x1, y), style="l", lw=1, color=0, lt=i)
        g.pyxplot((x2, y), style="l", lw=3, color=0, lt=i)
        g.pyxplot((x3, y), style="l", lw=1, color=0, lt=i, dl=4)
    g.pyxlabel( (0.125,1.05), "lw=1", [pyx.text.halign.center])
    g.pyxlabel( (0.5,1.05), "lw=3", [pyx.text.halign.center])
    g.pyxlabel( (0.875,1.05), "lw=1, dl=4", [pyx.text.halign.center])

    g.pyxsave(epsoutfile)


if __name__=="__main__":
    styles_example("styles_example.eps")
