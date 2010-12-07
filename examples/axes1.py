"""
semi-log plot
"""

import sys;    sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def axes_example1(epsoutfile):
    g=pyxgraph(yaxistype="log", xlimits=(0, 10), ylimits=(10**-5, 10**5),
               key="br")
    g.pyxplot(("test_data2.dat", 1, 2), title=r"$x^2$")
    g.pyxplot(("test_data2.dat", 1, 3), title=r"$x^4$")
    g.pyxplot(("test_data2.dat", 1, 4), title=r"$\exp(x)$")
    g.pyxplot("x(y)=y*y", title=r"$\sqrt{x}$")
    g.dodata()               # draw data first and then the border on top
    g.pyxsave(epsoutfile)

    
if __name__=="__main__":
    axes_example1("axes1.eps")
