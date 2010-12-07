"""A simple example for the inclusion of a bitmap.

Here the bitmpa is in front of the lines.
This is achieved using `go.dodata()`.
However,  because the graph is essentially finished,
it is not possible to plot any further lines
after this which would be in front of the bitmap."""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def bitmap_example2(epsoutfile):
    g=pyxgraph(xlimits=(0.0, 10.0)) 
    g.pyxplot("y(x)=sin(x)", style="p")    
    g.dodata()
    g.pyxbitmap("tst.jpg", xpos=0.2, ypos=0.4, width=0.5, height=0.4)  
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    bitmap_example2("bitmap2.eps")
