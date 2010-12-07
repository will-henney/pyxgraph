"""A simple example for the inclusion of a bitmap."""


import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *

def bitmap_example1(epsoutfile):
    g=pyxgraph(xlimits=(0.0, 10.0)) 
    g.pyxplot("y(x)=sin(x)", style="p")    
    g.pyxbitmap("tst.jpg")                   # insert a bitmap from file 
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    bitmap_example1("bitmap1.eps")
