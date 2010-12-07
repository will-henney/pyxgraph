"""Double log plot and skipping of data"""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *


def axes_example2(epsoutfile):
    g=pyxgraph(yaxistype="log", ylimits=(10**-5, 10**5),
               xaxistype="log", xlimits=(10**-2, 10),
               dashlength=4)
    g.pyxplot(("test_data2.dat", 1, 2), title=r"$x^2$", style="l", lw=3)
    g.pyxplot(("test_data2.dat", 1, 3), title=r"$x^4$", style="l", lw=3)
    g.pyxplot(("test_data2.dat", 1, 4), title=r"$\exp(x)$", style="l", lw=3)
    g.pyxplot(("test_data2.dat", 1, 5, dict(skiphead=5, skiptail=20)),
              title=r"$\exp(-x)$ (with skip)", style="l", lw=3, dl=0.5)
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    axes_example2("axes2.eps")
	
