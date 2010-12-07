"""3d example 1"""

from pyxgraph import *
from numpy import *

def plot3d_example(fileout):
    
    x = linspace(-1.0, 1.0, 100)[:,newaxis]*ones(100)
    y = transpose(x)
    z = 2-x**2-y**2
    z = exp(-6*(x**2+y**2))

    if int(pyx.__version__.replace("0.",""))<10:
        print "3D is only supported for pyx>=0.10"
        g=pyxgraph(title=r"3D is only supported for pyx$\geq$0.10",
                   xlimits=(0,2*pi),ylimits=(-1,1))
        g.pyxplot("y(x)=sin(x)", style="p", title=None)
        g.pyxsave(fileout)
        return
    
    g = pyxgraph3d(xlabel=r"$x$", ylabel=r"$y$", zlabel=r"$z$", 
                   size=4, 
                   xlimits=(-1, 1), ylimits=(-1, 1), zlimits=(0, 1))
                
    g.pyxplotsurface((x,y,z), style="surface")
    
    g.pyxsave(fileout)
    
    
if __name__=="__main__":
    plot3d_example("plot_3d_1.eps")
