"""Plot a two-dimensional error as bitmap and a colorbar, using segmented color mapper"""

import sys; sys.path.append("../")           # so that pyxgraph is found

from pyxgraph import *
import pyx
from numerix import arange, sqrt, cos, NewAxis, ravel

def array_example3(epsoutfile):
    x = (arange(200.0)-100)/10.0
    y = (arange(200.0)-100)/10.0
    r = sqrt(x[:,NewAxis]**2+y**2)
    z = 5.0*cos(r)  
    
    colmap1 = ColMapper.ColorMapper("red")
    colmap1.exponent = 0.9
    colmap1.invert = True
    
    colmap2 = ColMapper.ColorMapper("green")
    colmap2.exponent = 0.9
    
    colmap3 = ColMapper.ColorMapper("green")
    colmap3.invert = True
    colmap3.exponent = 0.9
    
    colmap4 = ColMapper.ColorMapper("blue")
    colmap4.exponent = 0.9
    
    
    colmap = ColMapper.SegmentedColorMapping([ (-5.0, -2.5, colmap1), (-2.5, 0.0, colmap2),
                                               (0.0, 2.5, colmap3), (2.5, 5.0, colmap4),], -5.0, 5.0)

#     colmap = ColMapper.example_SegmentedColorMapping(min(ravel(z)),max(ravel(z)))
    lut = colmap.generate_lut()

    pilbitmap = ColMapper.Array2PIL(z, lut=lut)        
                            
    c = pyx.canvas.canvas()
    g = pyxgraph(xlimits=(min(x), max(x)), ylimits=(min(y), max(y)),
                 width=6, height=6, key=False)
    g.pyxplot("y(x)=sin(x)+20", style="p")  # FIXME: can't do empty plots!
    
    g.pyxbitmap(pilbitmap)    
    
    c.insert(g)

    cb = pyxcolorbar(lut=lut, frame=g, pos=(1.1,0.0),
                     minvalue=min(ravel(z)), maxvalue=max(ravel(z)))
    c.insert(cb)
    
    pyxsave(c, epsoutfile)


if __name__=="__main__":
    array_example3("array3.eps")
