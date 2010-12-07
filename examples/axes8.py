"""
Key outside of the graph.

Contributed by Nikolai Hlubek.
"""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
from scipy import special


def axes8(epsoutfile):
    """Plot of Chebychev polynomials"""    
    g = pyxgraph(key=pyx.graph.key.key(pos="mr",hinside=0),
                 ylimits=(-1.1, 1.1), xlabel="$x$", ylabel="$T_j(x)$")
    x = arange(-1.0,1.01,0.01)
    for i in xrange(5):
        g.pyxplot((x, special.chebyt(i)(x)),
                  title="$T_%d(x)$" % i, style="l", dl=2, color=0)
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    axes8("axes8.eps")
