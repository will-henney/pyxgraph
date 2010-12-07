"""example for axis with ticks and without numbers"""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
from math import pi


def axes_example16(epsoutfile):
    c = pyx.canvas.canvas()

    g1 = pyxgraph(xlimits=(0.0, 2.0*pi), key="bl", xaxistype="linear", ylabel="$y$",
               xticks=(0, 2*pi, 1))
               
    g1.pyxplot("y(x)=sin(x)", title=r"$\sin(x)$", style="l")
    g1.pyxplot("y(x)=cos(x)", title=r"$\cos(x)$", style="l", lw=2, dl=3)
    
    c.insert(g1)
    
    g2 = pyxgraph(xlimits=(0.0, 2.0), key="bl", xaxistype=pyx.graph.axis.linkedaxis(g1.axes["x"]), 
               ylabel="$y$",
               xticks=False, ypos=+6.5)
                                      
    g2.pyxplot("y(x)=sin(x)", title=r"$\sin(x)$", style="l")
    g2.pyxplot("y(x)=cos(x)", title=r"$\cos(x)$", style="l", lw=2, dl=3)
    
    c.insert(g2)
    
    pyxsave(c, epsoutfile)


if __name__=="__main__":
    axes_example16("axes16.eps")
