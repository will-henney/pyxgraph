"""Combine matplotlib and pyxgraph

   Matplotlib does a fantastic job for bitmapped graphics,
   including anti-aliasing and transparency.
   Because transparency is not supported in Postscript
   it can be useful to create a bitmapped figure using matplotlib
   and embed it in PyX to do the labeling.

   """

import sys;  sys.path.append("../")           # so that pyxgraph is found

import os

import pylab

from pyxgraph import *


def matplotlib_plot(fname):
    Xs, Ys = 6, 6
    fig = pylab.figure(figsize=(Xs, Ys), frameon=False)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
    ax.set_xticks([])
    ax.set_yticks([])    
    N = 1000
    x, y = pylab.randn(N), pylab.randn(N)
    color = pylab.randn(N)
    size = abs(400*pylab.randn(N))
    p = pylab.scatter(x, y, c=color, s=size, alpha=0.75)
    pylab.xlim(-2.0, 2.0)
    pylab.ylim(-2.0, 2.0)
    pylab.savefig(fname, dpi=200)
    return Xs, Ys

    
    
def matplotlib_pyx(epsoutfile):
    mpl_file = os.path.split(epsoutfile)[0]+"_tmp.png"
    Xs, Ys = matplotlib_plot(mpl_file)
    #Xs, Ys = 6, 6
    g = pyxgraph(width=2*Xs, height=2*Ys,
                 xlimits=(-2.0, 2.0), ylimits=(-2.0, 2.0)) 
    g.pyxplot("y(x)=sin(x)", style="p")


    # It seems the following comment is not correct! (Fortunately):
    #
    # We also need the `Image`, the Python Image Library (PIL),
    # to ensure that no `Flate` encoded images will end up
    # in the resulting postscript because this is a Postscript
    # Level 3 printer feature (and not all available printers eat that level).

    # However, for a different reason:
    # We also need the `Image`, the Python Image Library (PIL),
    # because newer versions of matplotlib cannot write jpg files,
    # but pyx (via g.pyxbitmap) either needs a jpg or a PIL image.
    # So we open using the PIL and use that in g.pyxbitmap.
    import Image
    im = Image.open(mpl_file)
    g.pyxbitmap(im)
    # This would be shorter, but does not work:
    #g.pyxbitmap(mpl_file)
    g.pyxsave(epsoutfile)


if __name__=="__main__":
    matplotlib_pyx("matplotlib_pyx.eps")
    #matplotlib_plot("testing.jpg")
