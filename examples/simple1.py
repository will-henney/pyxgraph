"""A simple example for the usage of pyxgraph and pyxplot"""

import sys;   sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
from numerix import arange, cos


def simple1(epsoutfile):
    x = arange(0.0, 10.0, 0.1)

    g=pyxgraph(title="A first plot ;-)",  # one graph (essentially a
               xlabel=r"$x$",             #    pyx.grapxy instance)
               ylabel=r"$f(x)$",
               key="bl")     
    g.pyxplot("y(x)=sin(x)", style="p", title=None)
    
    g.pyxplot((x, cos(x)))
    g.pyxplot("test_data.dat", style="l", lt=0,
                              lw=3, title="Optional title")
    g.pyxplot(("test_data.dat",1,4), title=False)
    g.pyxplot(("test_data.dat",1, "$4+$5*$1/4"), style="lp", pt=6,
              lw=0.1, ps=0.8, title="blurb2",
              color='cyan', linecolor='purple')
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    simple1("simple1.eps")
