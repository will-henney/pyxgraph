"""Labels with arrows"""

import sys;   sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *



def make_plot(epsoutfile):
    
    g=pyxgraph(ylimits=(-1.4, 1.4), xlimits=(-0.7, 0.7),
               width=6.0, height=3.0, xlabel=None, ylabel=None,
               xpaint=False, ypaint=False, x2axistype=False, y2axistype=False, 
               key=False)

    g.pyxplot(([-0.5,0.5,0.5,-0.5,-0.5],[-1.0,-1.0,1.0,1.0,-1.0]), 
              style="l", lt=0, lw=3, color=0)
              
    g.pyxdimlabel((-0.55, -1.0), (-0.55, 1.0), (-0.6,-0.05), r"$y$", 0.05, 
                  barlw=0.5, difffact=0.02, inout="in", arrowlength=0.5,
                  arrowstyle=[pyx.style.linewidth.thin, 
                  pyx.deco.earrow.normal, pyx.color.rgb(0.0,0.0,0.0)]) 
                  
    g.pyxdimlabel((-0.5, -1.2), (0.5, -1.2), (0.0,-1.3), r"$x$", 0.2, 
                  barlw=0.5, difffact=0.01, inout="out", arrowlength=0.1,
                  arrowstyle=[pyx.style.linewidth.thin, 
                  pyx.deco.earrow.normal, pyx.color.rgb(0.0,0.0,0.0)]) 

    g.pyxsave(epsoutfile)


make_plot("make_labels_with_arrows.eps")
