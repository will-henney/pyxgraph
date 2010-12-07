"""Different ways of specifying colors"""

import sys;   sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *

class DemoColorClass:
    cyan=10
    magenta=255
    y=200
    black=50

def  colors1(epsoutfile):        
    g = pyxgraph(xlimits=(0, 1), ylimits=(-1, 10),
                  xticks=(0, 1, 1), yticks=(0, 9, 1),
                  ylabel='some colors', key=None, width=9)
    
    col=[pyx.color.cmyk.Black,
         'green',
         'YEL',
         # you should get a message saying it doesn't know lime
         'lime',           
         4,                # returns the 4th default color
         0.25,             # 25% grey
         (0.0,0.5,255),    # RGB - note the use of float and int :)
         # here you should get a warning about multiple values for brightness
         {'h': 0.3, 's': 1.0, 'b':128, 'brightness':0.2},
         DemoColorClass(), # see above: the right attributes will be picked out
         sys               # if you give complete crap, you get black
        ]
         
    for i in xrange(10):
        g.pyxplot(([0.0, 1.0], [i, i]), style="l", lt=0, lw=5, color=col[i])

    g.pyxsave(epsoutfile)


if __name__=="__main__":
    colors1("colors1.eps")
