"""A simple example for the inclusion of a bitmap.

   Keep the aspect ratio of the original bitmap."""

import sys;  sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def bitmap_example4(epsoutfile):
    g=pyxgraph(width=10, height=3, xlimits=(0.0, 10.0)) 
    g.pyxplot("y(x)=sin(x)", style="p")    
    g.pyxbitmap("tst.jpg", xpos=0.05, ypos=0.1, scale=0.2)  
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    bitmap_example4("bitmap4.eps")
