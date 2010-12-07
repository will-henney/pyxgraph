"""Arrows and labels."""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def simple4(epsoutfile):
    g=pyxgraph(xlimits=(0.0,10.0),
               xlabel=r"$\rho$", ylabel=r"$f(\rho)$", key="bl")

    g.pyxplot("y(x)=sin(x)", style="p")

    g.pyxarrow((0.1, 0.2),(0.4, 0.5))
    g.pyxarrow((0.1, 0.2),(0.3, 0.25), length=0.45)
    g.pyxlabel((0.4, 0.5),"A nice label",
             style=[pyx.text.halign.left, pyx.text.valign.bottom])
    g.pyxarrow((0.5, 0.8),(0.8, 0.45), length=0.25,
             arrowstyle=[pyx.style.linewidth.THIck, pyx.deco.earrow.Large,
                         pyx.color.rgb(0.8,0.0,0.0)])
    g.pyxlabel((0.98, 0.25),
      'By default there are no linebreaks -- but you can use a \\tt{parbox}.',
      style=[pyx.text.halign.boxright, pyx.text.valign.top,
             pyx.text.parbox(4)])
    g.pyxlabel((0.5,1.1),r"\Large Another text -- $\sqrt{\sin(x)}$")

    g.pyxarrow((1, 0.75), (2, 0.0), graphcoords=True)
    
    g.pyxsave(epsoutfile)

if __name__=="__main__":
    simple4("simple4_arrows_labels.eps")
