"""A simple example for the inclusion of a bitmap.

   Keep the aspect ratio of the original bitmap."""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def bitmap_example3(epsoutfile):
    g=pyxgraph(xlimits=(0.0, 10.0)) 
    g.pyxplot("y(x)=sin(x)", style="p")    
    g.pyxbitmap("tst.jpg", xpos=0.2, ypos=0.4, scale=0.5)  
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    bitmap_example3("bitmap3.eps")
