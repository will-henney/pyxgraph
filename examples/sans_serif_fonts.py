"""
Demonstrate the usage sans-serif fonts.

To use this you will have to get the file sfmath.sty
and put it somewhere, where latex can find it
(eg the same directory or into some directory which
is in the TEXINPUTS path)

Getting the file::

  wget http://dtrx.de/od/tex/archive/sfmath.sty.v0.7
  mv sfmath.sty.v0.7 sfmath.sty

See: http://dtrx.de/od/tex/sfmath.html by Olaf Dietrich <olaf@dtrx.de>
"""

import sys;    sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


# choose sans-serif for text and math
pyx.text.preamble(r"""\renewcommand{\familydefault}{\sfdefault}""")
pyx.text.preamble(r"""\usepackage{sfmath}""")    
pyx.text.preamble(r"""\usepackage{amsmath}""")     # for \text, 
pyx.unit.set(xscale=1.5)                           # scale (everything?)


def sans_serif_fonts(epsoutfile):
    g=pyxgraph(width=12,
               xlimits=(0, 10), key=False,
               xlabel=r"$h_{\text{heff}}^{-1}$")
    g.pyxplot(("test_data2.dat", 1, 3), title=r"$x^4$")
    g.pyxplot(("test_data2.dat", 1, 4), title=r"$\exp(x)$")

    g.pyxlabel((0.025, 0.9), r"\small ABCDEFGHIJKLMNOPQRSTUVWXYZ",
               [pyx.text.halign.left])
    g.pyxlabel((0.025, 0.8), r"\small$ABCDEFGHIJKLMNOPQRSTUVWXYZ$",
               [pyx.text.halign.left])
    g.pyxlabel((0.025, 0.7), r"\small abcdefghijklmnopqrstuvwxyz",
               [pyx.text.halign.left])
    g.pyxlabel((0.025, 0.6), r"\small$abcdefghijklmnopqrstuvwxyz$",
               [pyx.text.halign.left])

    g.pyxlabel((0.025, 0.4), r"\small$\alpha\beta\gamma\delta\epsilon\rho\phi\varphi\mu\nu$",
               [pyx.text.halign.left])
    g.pyxsave(epsoutfile)

    
if __name__=="__main__":
    sans_serif_fonts("sans_serif_fonts.eps")
