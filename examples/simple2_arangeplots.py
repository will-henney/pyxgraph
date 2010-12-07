"""Arange two plots."""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
import pyx

def simple2(epsoutfile):
    c = pyx.canvas.canvas()          # canvas for the whole drawing

    # first plot
    g1 = pyxgraph(xlimits=(0.0, 10.0), key="bl")
    g1.pyxplot("y(x)=sin(x)", style="p")    
    c.insert(g1)

    # second plot below
	# Caution: Adjust ypos by the height of the first plot. 
    g2=pyxgraph(ypos=g1.ypos-1.2*g1.height, xlimits=(0.0, 5.0), key="bl")
    g2.pyxplot("y(x)=10**6*cos(x)", style="l", lw=3, color=(1.0, 0.5, 0.0))
    c.insert(g2)

    g1.pyxlabel((8,-0.5), "label1 in graphcoords", graphcoords=True)
    g2.pyxlabel((2,200000),"label2 in graphcoords",  [pyx.text.halign.left],
                graphcoords=True)

    pyxsave(c, epsoutfile)


if __name__=="__main__":
    simple2("simple2_arangeplots.eps")
