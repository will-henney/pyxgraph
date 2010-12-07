"""
Demonstrate the usage sans-serif fonts with cmbright.

Remarks:
- Debian etch package needed for this:
    aptitude install texlive-fonts-extra
    aptitude install cm-super
  (not sure whether the last one is really needed, but why not ;-)
- Good references on Mathematics fonts in LaTeX
  http://cg.scs.carleton.ca/~luc/math.html
  ftp://ctan.cms.math.ca/tex-archive/documentation/Free_Math_Font_Survey/en/survey.html

"""

import sys;    sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


# choose sans-serif for text and math
pyx.text.preamble(r"""\renewcommand{\familydefault}{\sfdefault}""")
pyx.text.preamble(r"""\usepackage{amsmath}""")
pyx.text.preamble(r"""\usepackage{cmbright}""")

pyx.unit.set(xscale=1.5)                           # scale (everything?)


def sans_serif_fonts2(epsoutfile):
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
    g.pyxlabel((0.025, 0.6), r"\small $abcdefghijklmnopqrstuvwxyz$",
               [pyx.text.halign.left])

    g.pyxlabel((0.025, 0.4), r"\small $\alpha\beta\gamma\delta\epsilon\rho\phi\varphi\mu\nu$",
               [pyx.text.halign.left])
    g.pyxsave(epsoutfile)

    
if __name__=="__main__":
    sans_serif_fonts2("sans_serif_fonts2.eps")
