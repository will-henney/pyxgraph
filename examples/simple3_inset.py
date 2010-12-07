"""Plot with inset

# FIXME: Getting the fonts smaller is a bit hackish at the moment ...
"""


import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
import pyx

from IPython.Shell import IPythonShellEmbed 
ipshell = IPythonShellEmbed() 

def simple3(epsoutfile):
    c = pyx.canvas.canvas()          # canvas for the whole drawing

    # first plot
    g1=pyxgraph(xlimits=(0.0, 10.0))
    g1.pyxplot("y(x)=(x-5.0)**2", style="p")
    c.insert(g1)

    # second plot as inset
    g2=pyxgraph(width=g1.width/2.5, height=g1.height/2.5,
                xpos=g1.xpos+0.4*g1.width, ypos=g1.ypos+0.5*g1.height,
                xlimits=(0.0,5.0),
                axesdist=0.15*0.8*pyx.unit.v_cm)
    g2.pyxplot("y(x)=10**6*cos(x)", style="l", color=(0.0, 0.2, 1.0))

    # Modify the distance of the axes to the labels.
    # Note that in this example only the first has
    # to be modified as all the other seem to be the
    # same instance. Thus successively applying the factor is not good.
    # Just accessing the first element in the list of axes does the job
    for ax_key in g2.axes.keys()[0]:
        ax = g2.axes[ax_key]
        print ax.axis.painter.labeldist
        ax.axis.painter.labeldist = 0.5*ax.axis.painter.labeldist
        
    save_xscale = pyx.unit.scale["x"]
    save_vscale = pyx.unit.scale["v"]
    #save_wscale = pyx.unit.scale["w"]
    print pyx.unit.scale
    pyx.unit.set(xscale=0.5*save_xscale)
    pyx.unit.set(vscale=0.5*save_vscale)
    #pyx.unit.set(wscale=0.15*save_wscale)  # effect????
    g2.doaxes()
    g2.dokey()
    c.insert(g2)
    pyx.unit.set(xscale=save_xscale)            
    pyx.unit.set(vscale=save_vscale)            
    #pyx.unit.set(wscale=save_wscale)            

    pyxsave(c, epsoutfile)
    

if __name__=="__main__":
    simple3("simple3_inset.eps")
