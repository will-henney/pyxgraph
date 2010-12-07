"""
Demonstrate the usage of amsmath specific features and overall scaling.
"""

import sys;    sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *

pyx.text.preamble(r"""\usepackage{amsmath}""")     # for \text, 
pyx.text.preamble(r"""\usepackage{amsfonts}""")    # for \mathbb, \mathfrak
pyx.text.preamble(r"""\usepackage[mathscr]{eucal}""")  # for \mathscr
pyx.unit.set(xscale=1.5)                           # scale (everything?)


def amsmath_and_xscale(epsoutfile):
    g=pyxgraph(width=12,
               xlimits=(0, 10), key=False,
               xlabel=r"$h_{\text{heff}}^{-1}$")
    g.pyxplot(("test_data2.dat", 1, 3), title=r"$x^4$")
    g.pyxplot(("test_data2.dat", 1, 4), title=r"$\exp(x)$")

    g.pyxlabel((0.025, 0.9), r"\small$\mathcal{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$",
               [pyx.text.halign.left])
    g.pyxlabel((0.025, 0.8), r"\small$\mathscr{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$",
               [pyx.text.halign.left])
    g.pyxlabel((0.025, 0.7), r"\small$\mathbb{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$",
               [pyx.text.halign.left])
    g.pyxlabel((0.025, 0.6), r"\small$\mathfrak{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$",
               [pyx.text.halign.left])
    g.pyxlabel((0.025, 0.5), r"\small$\mathfrak{abcdefghijklmnopqrstuvwxyz}$",
               [pyx.text.halign.left])
    g.pyxlabel((0.025, 0.4), r"\small$\mathbf{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$",
               [pyx.text.halign.left])
    g.pyxlabel((0.025, 0.3), r"\small$\mathbf{abcdefghijklmnopqrstuvwxyz}$",
               [pyx.text.halign.left])
    g.pyxsave(epsoutfile)

    
if __name__=="__main__":
    amsmath_and_xscale("amsmath_and_xscale.eps")
