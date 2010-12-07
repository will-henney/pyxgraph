"""Plot with tick specification and smaller legend"""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *

def axes_example3(epsoutfile):
    key = pyx.graph.key.key(pos="tl", textattrs=[pyx.text.size(-3)])
    g=pyxgraph(xlimits=(0.0, 8.0), xticks=(0.0, 8.0, 4.0), xticksformat="%5.4f",
               ylimits=(0.0, 100.0), yticks=(0.0, 100.0, 25.0), key=key)
    g.pyxplot(("test_data2.dat", 1, 2), title=r"$x^2$")
    g.pyxplot(("test_data2.dat", 1, 3), title=r"$x^4$")
    g.pyxplot(("test_data2.dat", 1, 4), title=r"$\exp(x)$")
    g.pyxplot(("test_data2.dat", 1, "75*$5"), title=r"$75\exp(-x)$")
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    axes_example3("axes3.eps")
