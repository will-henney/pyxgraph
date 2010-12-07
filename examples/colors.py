"""Color sequence example"""

import sys;   sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def colors(epsoutfile):        
    c = pyx.canvas.canvas()          # canvas for the whole drawing
    x = [0.0, 1.0]
    
    # first plot, with colors 'color11'
    g1 = pyxgraph(xlimits=(0 ,1), ylimits=(-1, 11),
                  xticks=(0, 1, 1),yticks=(0, 10, 1),
                  ylabel='color11', key=None, colors="color11", width=8)
    for i in xrange(11):
        g1.pyxplot((x, [i, i]), style="l", lt=0, lw=5, color=i)           
    c.insert(g1)

    # second plot below, with colors 'grey10'
    # The important difference is, that ypos is adjusted by the height of
	# the first plot.
    g2 = pyxgraph(width=8, ypos=g1.ypos-1.2*g1.height,
                  xlimits=(0, 1), xticks=(0, 1, 1),
                  ylimits=(-1, 5), yticks=(0, 4, 1),
                  ylabel='grey5', key=None, colors="grey5")
    for i in xrange(5):
        g2.pyxplot((x, [i, i]), style="l", lt=0, lw=5, color=i)        
    c.insert(g2)
    
    # third plot below, with colors 'rainbow'
    g3=pyxgraph(width=8, ypos=g2.ypos-1.2*g2.height,
                xlimits=(0, 1), xticks=(0, 1, 1),
                ylimits=(-1, 11), yticks=(0, 10, 1),
                ylabel='rainbow', key=None, colors="rainbow")
    for i in xrange(11):
        g3.pyxplot((x, [i, i]), style="l", lt=0, lw=5, color=i)        
    c.insert(g3)
    
    pyxsave(c, epsoutfile)


if __name__=="__main__":
    colors("colors.eps")
