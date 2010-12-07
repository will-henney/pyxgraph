"""
Outside ticks and other painter tricks.

FIXME: x2ticks and y2ticks don't work.

"""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def axes10(epsoutfile):
    """Different painter"""
    # longer red outside xticks:
    paint0 = pyx.graph.axis.painter.regular(innerticklength=None,
        outerticklength=pyx.graph.axis.painter.ticklength.long,
        tickattrs=[pyx.color.rgb.red, pyx.style.linewidth.thick])
    # longer blue inside xticks:
    paint1 = pyx.graph.axis.painter.linked(
        innerticklength=pyx.graph.axis.painter.ticklength.long,
        tickattrs=[pyx.color.rgb.blue, pyx.style.linewidth.thick])
    # longer dark green insside xticks:
    paint2 = pyx.graph.axis.painter.linked(
        innerticklength=pyx.graph.axis.painter.ticklength.LOng,
        tickattrs=[pyx.color.rgb(0.0, 0.0, 0.8), pyx.style.linewidth.thick])
    # longer dark green outside xticks:
    paint3 = pyx.graph.axis.painter.linked(innerticklength=None,
        outerticklength=pyx.graph.axis.painter.ticklength.long,
        tickattrs=[pyx.color.rgb(0.0, 0.0, 0.6), pyx.style.linewidth.thick])

    c = pyx.canvas.canvas()
    
    g1l = pyxgraph(width=5, xlimits=(0.0, 10.0), ylimits=(None, 2), key=False)
    g1l.pyxplot("y(x)=sin(x)", style="l")
    c.insert(g1l)

    g1r=pyxgraph(width=5, xpos=g1l.xpos+1.3*g1l.width,
                 xlimits=(0.0, 10.0), ylimits=(None, 2), key=False,
                 xpaint=paint0, x2paint=paint1)
    g1r.pyxplot("y(x)=sin(x)", style="l")
    g1r.pyxlabel((0.5, 0.8), "x: outside; x2: inside")
    c.insert(g1r)

    g2l=pyxgraph(width=5, ypos=g1l.ypos-1.4*g1l.height,
                 xlimits=(0.0, 10.0), ylimits=(None, 2), key=False,
                 ypaint=paint0, x2paint=paint1)
    g2l.pyxplot("y(x)=sin(x)", style="l")
    g2l.pyxlabel((0.5, 0.8), "y: outside; x2: inside")
    c.insert(g2l)

    g2r=pyxgraph(width=5,
                 xpos=g1l.xpos+1.3*g1l.width, ypos=g1l.ypos-1.4*g1l.height,
                 xlimits=(0.0, 10.0), ylimits=(None, 2), key=False,
                 xpaint=paint0, ypaint=paint0, x2paint=paint3, y2paint=paint2)
    g2r.pyxplot("y(x)=sin(x)", style="l")
    g2r.pyxlabel((0.5, 0.8), "x, y: out; x2: out, y2: in")
    c.insert(g2r)

    pyxsave(c, epsoutfile)


if __name__=="__main__":
    axes10("axes10.eps")


