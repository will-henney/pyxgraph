"""Linestyle definition with strings"""

import sys;   sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
from numerix import ones, arange


def styles_example(epsoutfile):
    mystyles = ['.', '-', '-"', '_ ', '6_1 ', '- . ']
    count = len(mystyles)
    x1 = 0.8*arange(2)

    g = pyxgraph(xlimits=(-0.1, 1.1), xticks=(0, 1, 1),
                 ylimits=(-1, count), yticks=(0, count-1, 1),
                 ylabel='linestyles', key=None, width=8)

    for i in xrange(count):
        y = ones(2)+i-1 
        g.pyxplot((x1, y), style="l", lw=1, color=0, lt=mystyles[i])
        g.pyxlabel((0.85, i),
                   '\\tt{'+repr(mystyles[i]).replace('_','\\_')+'}',
                   style=[pyx.text.halign.left], graphcoords=True)
        
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    styles_example("styles_example3.eps")
