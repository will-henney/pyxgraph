"""Some arrow tricks..."""

import sys;   sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *

# ----------------------------------------------------------
# for debugging/development:
from IPython.Shell import IPythonShellEmbed 
ipshell = IPythonShellEmbed() 

# on error go to IPYTHON
import sys, IPython.ultraTB  
sys.excepthook = IPython.ultraTB.FormattedTB(#mode='Verbose',
                                             color_scheme='Linux',
                                             call_pdb=1)
# ----------------------------------------------------------



def make_arrows(epsoutfile):
    g=pyxgraph(xlimits=(0.0, 10.0), key="bl")      
    g.pyxplot("y(x)=sin(x)", style="p", title=None)

    DarkGreen = pyx.color.rgb(0.0,0.4,0.0)
    DarkBlue = pyx.color.rgb(0.0,0.0,0.4)
    ArrowColor = pyx.color.rgb( 0.45882353,  0.85882353,  0.49411765)
    xm,ym=g.pos(4.0, 0.25)
    g.stroke(pyx.path.path(pyx.path.arc(xm,ym,2.2,0,180)),
                     [pyx.style.linewidth(0.35), pyx.deco.barrow.LARGe,
                      DarkGreen])

    xm,ym=g.pos(6.0, -0.25)
    arc2 = pyx.path.path(pyx.path.arc(xm,ym,2.2,0,170))
    # use a transformation to scale a path in y direction:
    trans = pyx.trafo.trafo()
    g.stroke(arc2.transformed(trans.scaled(1.0, 0.5)),
             [pyx.style.linewidth(0.35), pyx.deco.barrow.LARGe, DarkBlue])


    xl, yl =  g.pos(2.0, 0.1)
    xm1, ym1 =  g.pos(3.0, 0.5)
    xm2, ym2 =  g.pos(5.0, 0.5)
    xr, yr =  g.pos(6.0, 0.1)
    
    g.stroke(pyx.path.curve(xl, yl, xm1, ym1,xm2, ym2, xr, yr),
                     [pyx.style.linewidth(0.35), pyx.deco.barrow.LARGe,
                      ArrowColor, #pyx.style.linewidth.THin,
                      #pyx.deco.stroked([pyx.color.palette.Rainbow])
                      pyx.deco.stroked([pyx.color.rgb.green])
                      ])

    g.pyxsave(epsoutfile)


make_arrows("make_arrows.eps")
