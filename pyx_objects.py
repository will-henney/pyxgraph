"""
Collection of routines which can  be useful for a normal PyX
graphxy/canvas etc.
So we don't put them in the pyxgraph class.
"""

import os
import pyx
import types

from numerix import sqrt, transpose, arange, ones, where, argmin, arctan, pi, array, log, exp
from numerix import histogram, reshape

from numerix import ColMapper

from contour import contour_gencoords, contour_rectgrid, contour_nogrid

def pyxbitmap(graphics, bitmap,
              xpos=0.0, ypos=0.0,
              width=1.0, height=1.0,
              scale=None,
              #compressmode="DCT", #Flate",  # None, or DCT
              compressmode="Flate",
              flatecompresslevel=6,
              dctquality=100, dctoptimize=0, dctprogression=0,
              graphcoords=False,
              PSbinexpand=2
              ):
    """
     xpos,ypos from [0.0, 1.0]
     width,height from [0.0, 1.0]
     If scale != None, width/height is ignored and
        the `width` is set to `scale` and the height
        adpated such that the aspect ratio of the original image
        is preserved.


    Warning:
        FlateEncode (LanguageLevel 3)
        FlateDecode (LanguageLevel 3)

    See e.g.: http://www.capcode.de/help/filter

    """

    # FIXME: TODO: allow more general images (from PIL would be fine)
    if type(bitmap) is types.StringType:   # should be a file
        image = pyx.bitmap.jpegimage(bitmap) #, PSbinexpand=PSbinexpand)
        compressmode = None  # compression of a compressed image not supported 
    else:
        image = bitmap
    
    if scale is not None:  # preserve aspect ratio of the original image
        width = scale
        height = (scale*image.size[1]/image.size[0]
                  *graphics.width/graphics.height)

    if graphcoords == True:
        x1, y1 = graphics.pos(xpos, ypos)
        x2, y2 = graphics.pos(xpos+width, ypos+height)
    else:
        x1 = graphics.xpos+xpos*graphics.width
        y1 = graphics.ypos+ypos*graphics.height
        x2 = graphics.xpos+(xpos+width)*graphics.width
        y2 = graphics.ypos+(ypos+height)*graphics.height

    bitmap = pyx.bitmap.bitmap(x1, y1, image, height=y2-y1, width=x2-x1,
                               compressmode=compressmode,
                               flatecompresslevel=flatecompresslevel,
                               dctquality=dctquality,
                               dctoptimize=dctoptimize,
                               dctprogression=dctprogression,
                              # PSbinexpand=PSbinexpand
                               )

    graphics.insert(bitmap)


def pyxplothist(graph, x_sample, Nbins=80, bin_range=None, norm=False, bars=0,
                lw=0, lt=0, color=(0,0,0), xlogscale=False, ylogscale=False,
                y_given=None, title=False):
    """ Plots a histogram of 'x_sample'.
    
        Arguments:
        'x_sampe'    - data
        'Nbins'      - number of bins
        'bin_range'  - intervall to be divided into 'Nbins' equidistant parts
        'norm'       - normalization of histogram 
                       (comparison with density function)
        'bars'       - style parameter: bars (bars=1) or steps (bars=0)   
        'lw', 'lt'   - linewidth, linetype
        'title'      - title
        'color'      - color of histogram (r,g,b)
        'xlogscale'  - takes bins with logarithmically constant width,
                       makes only sense, when 'xaxistype' of 'graph' 
                       is set to 'log' 
        'ylogscale'  - activates necessary changes, if y-axis is logarithmic, 
                       makes only sense, when 'yaxistype' of 'graph' 
                       is set to 'log'
        'ygiven'     - if you already know the y-values
    """
    steps = 1-bars
    
    # determine max. x-value for the bins
    x_max = max(x_sample)
    if bin_range != None:
        x_max = bin_range[1]
    
    # changes due to logarithmic x-axis:
    #  take log of the data, check if data or range is <= zero
    if xlogscale:
        if min(x_sample) > 0:
            x_sample = log(x_sample)
            if bin_range != None:
                if bin_range[0] > 0 and bin_range[1] > 0:
                    bin_range = (log(bin_range[0]),log(bin_range[1]))
                else:
                    print "Given range includes values <= 0!"
                    print "Ignoring given range..."
                    bin_range = None
        else:
            print "Data is smaller than zero, no logarithmic x-axis possible!"
            print "Continuing linearly..."
            xlogscale = False
    
    if y_given != None:
        x_l = x_sample
        x_hist = y_given
        Nbins = len(x_l)
    else:
        ## histogram of 'x_sample': gives number 'x_hist' of sample points within 
        ##   'Nbins' different of bins within 'bin_range', where the bins are 
        ##   specified by their left edge coordinate 'x_l'
        x_hist, x_l = histogram(x_sample, bins=Nbins, range=bin_range, normed=norm)
        
    # if logarithmic x-axis: exponentiate bin positions and data
    if xlogscale:
        x_l = exp(x_l)
        x_sample = exp(x_sample)
        
    y_min = 0
    # offset for logarithmic y-axis
    if ylogscale:
        x_hist = x_hist+1e-16
        y_min = 1e-16

    # plot histogram manually
    for i in xrange(Nbins):
        # horzontal lines
        if i < Nbins-1:       
            graph.pyxplot(([x_l[i],x_l[i+1]],[x_hist[i],x_hist[i]]), 
                          style="l", color=color, lt=lt, lw=lw, title=False)
        else:
            graph.pyxplot(([x_l[i],x_max],[x_hist[i],x_hist[i]]), 
                          style="l", color=color, lt=lt, lw=lw, title=False)
                      
        # vertical lines
        if i != Nbins-1:
            graph.pyxplot(([x_l[i+1],x_l[i+1]],[x_hist[i],x_hist[i+1]]), 
                          style="l", color=color, lt=lt, lw=lw, title=False)
        if i == 0:
            graph.pyxplot(([x_l[i],x_l[i]],[x_hist[i],y_min]), 
                          style="l", color=color, lt=lt, lw=lw, title=title)
        if i == Nbins-1:
            graph.pyxplot(([x_max,x_max],[x_hist[i],y_min]), 
                          style="l", color=color, lt=lt, lw=lw, title=False)
    
    ## This gives an error if plottet on a logarithmic y-axis, WHY?
    #hist = transpose( reshape( zip((x_l, x_hist)), (2,Nbins) ) )
    #d = pyx.graph.data.list(hist, x=1, y=2)
    #print hist
    
    #graph.plot(d, styles=[pyx.graph.style.histogram(steps=steps,
                          #autohistogrampointpos=0.0, 
                          #lineattrs=[pyx.deco.stroked, pyx.style.linewidth(lw), 
                                  #pyx.color.rgb(color[0],color[1],color[2])])])



def pyxplotarray(canvas, arr,
                 minvalue=None, maxvalue=None,
                 xpos=0.0, ypos=0.0,
                 width=1.0, height=1.0,
                 scale=None,
                 compressmode="DCT", #"Flate",  # None, or DCT
                 flatecompresslevel=6,
                 dctquality=100, dctoptimize=0, dctprogression=0,
                 colmap=None,
                 graphcoords=False,
                 PSbinexpand=2):
    if colmap==None:
        colmap=ColMapper.ColorMapper("gauss")

    if isinstance(colmap, ColMapper.ColorMapper):
        lut = colmap.generate_lut()
    else:
        lut = colmap
    pilbitmap=ColMapper.Array2PIL(arr, lut=lut,
                                  minvalue=minvalue, maxvalue=maxvalue)
    # hmm: these following ones are passed - so what is the problem??
    #print "WARNING: xpos, ypos, width, height are ignored in pyxplotarray!!!!"

    
    canvas.pyxbitmap(pilbitmap, xpos=xpos, ypos=ypos,
                     width=width, height=height, scale=scale,
                     compressmode=compressmode,
                     flatecompresslevel=flatecompresslevel,
                     dctquality=dctquality, dctoptimize=dctoptimize,
                     dctprogression=dctprogression,
                     graphcoords=graphcoords,
                     PSbinexpand=PSbinexpand)

def pyxplotcontour(canvas, data, x=None, y=None, levels=8,
                   colors='map', colmap=None, color=None,
                   labels=False, labelsize=0.4,
                   **kwargs):
    """do contour plot.
    
    data[y, x]: 2d real array containing z values
    x, y: None - equidistant point spacing
          1d array: rectangular non-equidistant grid
          2d array: arbitrary coordinates
    levels: int (level count) or list of z values
            default: 8 equispaced levels
    colors: "map": use colmap (ColorMapper)
            "map_invert": use colmap but invert color
                          (max visibility on top of bitmap plot)
            "color_array": color and levels must be arrays of the same
                           length, level i get's the color i
            "color": use color (as in pyxgraph.pyxplot)
    labels: draw text labels designating the level value of each contour
    labelsize: label text size (relative to normal text size)
    kwargs: are passed to pyxplot
    """
    
    zmin, zmax = data.min(), data.max()
    # define a function zcolor(z) that returns the color to use
    if 'map' in colors:
        if colmap==None:
            colmap=ColMapper.ColorMapper("gauss")
        if 'inv' in colors:
            def zcolor(z):
                r, g, b = colmap.colfct((z-zmin)/(zmax-zmin))
                return 1-r, 1-g, 1-b
        else:
            def zcolor(z):
                return colmap.colfct((z-zmin)/(zmax-zmin))

    elif colors == "color_array":
        levels = array(levels)
        assert hasattr(color, "__iter__")    # for this color and levels
        assert hasattr(levels, "__iter__")   # have to be lists of the
        assert len(color)==len(levels)       # same length
        def zcolor(z):
            return color[argmin(abs(levels - z))]
                                             # return most suitable color
    
    else:  #use color
        def zcolor(z):
            return color
            
    # calculate level list
    if isinstance(levels, int):
        levels = (arange(levels)+0.5)*(zmax-zmin)/levels + zmin

    # calculate the levels
    if x is None or y is None:
        clines = contour_nogrid(data, levels)
    elif len(x.shape) == 1 and len(y.shape) == 1:
        clines = contour_rectgrid(x, y, data, levels)
    elif x.shape == y.shape == data.shape:
        clines = contour_gencoord(x, y, data, levels)
    else:
        raise ValueError, 'pyxplotcontour: x and/or y misshaped'
    # clines is clines[levidx][lineidx][0 or 1 for x/y]
    # set default args
    if 'linetype' not in kwargs and 'lt' not in kwargs:
        kwargs['linetype']=pyx.style.linestyle.solid
    if 'style' not in kwargs:
        kwargs['style'] = 'lines'
    # plot
    for levidx, level in enumerate(levels):
        llabel = '%0.4g'%level
        levelcolor = zcolor(level)
        for line in clines[levidx]:
            canvas.pyxplot((line[0], line[1]),
                           color=levelcolor, title=False, **kwargs)
            if labels:
                # find label position
                x, y = line
                xy  = map(canvas.pos, x, y)
                canvas_x = array([i[0] for i in xy])
                canvas_y = array([i[1] for i in xy])
                dcx = canvas_x[1:] - canvas_x[:-1]
                dcy = canvas_y[1:] - canvas_y[:-1]
                dcx = where(dcx==0, min(dcx)/10, dcx)  # avoid singularity problems
                ind = argmin(abs(dcy/dcx))
                # try to avoid placing labels on plot borders
                # FIXME: find better method for that?
                relx = canvas_x[ind] - canvas.xpos
                if not (labelsize < relx < canvas.width-labelsize): # label at left or right border
                    #if ind < 3 or ind > len(x)-4:     # probably a line ending at border
                    ind = len(x) / 2
                # label position (graphcoords)
                lx, ly = x[ind], y[ind]
                angle = arctan(dcy[ind]/dcx[ind])*180/pi
                if abs(angle) < 5:
                    angle = 0
                # FIXME: do something against labels exceeding plot area

                canvas.pyxlabel((lx, ly), llabel, graphcoords=True,
                                style=[pyx.trafo.translate(0, 0.05),
                                       pyx.trafo.rotate(angle),
                                       pyx.trafo.scale(labelsize),
                                       pyx.text.halign.center,
                                       pyx.text.valign.bottom])
                # debug: mark text anchor position
                # canvas.pyxplot(([lx], [ly]), color='black', style='p', pt=1)
    
    #print "WARNING: xpos, ypos, width, height are ignored in pyxplotarray!!!!"

   

def pyxlabel(canvas, xypos, textstring, style=None, graphcoords=False):
    """Display `textstring` at the the position `xypos=(xpos, ypos)`.
    
       `xypos=(xpos, ypos)` are coordinates from [0.0, 1.0]
       relative to the canvas area.
       Values smaller than 0 and larger than 1 are also allowed.
    """
##    print "canvas.xpos", canvas.xpos
##    print "canvas.ypos", canvas.ypos
##    print "canvas.width", canvas.width
##    print "canvas.height", canvas.height
    if style ==  None:
        style = [pyx.text.halign.center]
    if graphcoords == True:
        #print "so what ???"
##        if not canvas.did(canvas.dolayout):
##            #canvas.dolayout()
##            print "forced dolayout here (YEP)"
        x0, y0 = canvas.pos(xypos[0], xypos[1])
    else:
        x0 = canvas.xpos+xypos[0]*canvas.width
        y0 = canvas.ypos+xypos[1]*canvas.height
##    x0=canvas.xpos
##    y0=canvas.ypos
##    print canvas
##    print x0, y0
##    print textstring
##    print style
    canvas.text(x0, y0, textstring, style)


def pyxline(canvas, xystart, xyend, length=None, linestyle=None,
            graphcoords=False):
    """Draw a line in the `canvas`.
       Either from `xystart` to `xyend`.
       If `length` is defined then the line is
       from the point `xystart` in the directoin of `xyend` and has length
       `length`.
       `xystart` and `xyend` are a each a tuple with entries from [0.0, 1.0]
       Setting `graphcoords` to `True` uses the actual coordinates of
       the graph."""
    if linestyle == None:
        linestyle = [pyx.style.linewidth.THIck]
    pyxarrow(canvas, xystart, xyend, length=length,
             arrowstyle=linestyle, graphcoords=graphcoords)
             

def pyxarrow(canvas, xystart, xyend, length=None, arrowstyle=None,
             graphcoords=False):
    """
       xystart=(,)
       xyend=(,)
       are coordinates from [0.0, 1.0]
       relative to the canvas (or graph) area
       (values outside of this range are also allowed).
       If length is not None
       the direction is specified by xystart,xyend
    """
    if arrowstyle == None:
        arrowstyle = [pyx.style.linewidth.THIck, pyx.deco.earrow.Large]

#    print "canvas.xpos",canvas.xpos
#    print "canvas.ypos",canvas.ypos
#    print "canvas.width",canvas.width
#    print "canvas.height",canvas.height
    
    if graphcoords == True:
        # canvas.pos only works after dolayout!
        xmin = canvas.axes["x"].axis.min
        xmax = canvas.axes["x"].axis.max
        ymin = canvas.axes["y"].axis.min
        ymax = canvas.axes["y"].axis.max

        if xmin == None or ymin == None or xmax == None or ymax == None:
            #if not canvas.did(canvas.dolayout):
            #    canvas.dolayout()
            #    print "forced dolayout here"
            x0, y0 = canvas.pos(xystart[0], xystart[1])
            x1, y1 = canvas.pos(xyend[0], xyend[1])
        else:
           
            def convertxy(position):
                """Convert from [0.0, 1.0] coordinates to canvas coordinates """
                return ( (position[0]-xmin)/(xmax-xmin),
                         (position[1]-ymin)/(ymax-ymin)  )
                         
            def convertxy_logx(position):
                """Convert from [0.0, 1.0] coordinates to canvas coordinates 
                   on a logarithmic scale in x-direction"""
                return ( (log(position[0])-log(xmin))/(log(xmax)-log(xmin)),
                         (position[1]-ymin)/(ymax-ymin)  )
                         
            def convertxy_logy(position):
                """Convert from [0.0, 1.0] coordinates to canvas coordinates 
                   on a logarithmic scale in y-direction"""
                return ( (position[0]-xmin)/(xmax-xmin),
                         (log(position[1])-log(ymin))/(log(ymax)-log(ymin))  )
                         
            def convertxy_loglog(position):
                """Convert from [0.0, 1.0] coordinates to canvas coordinates 
                   on a logarithmic scale in x- and y-direction"""
                return ( (log(position[0])-log(xmin))/(log(xmax)-log(xmin)),
                         (log(position[1])-log(ymin))/(log(ymax)-log(ymin))  )

            if canvas.xaxistype == "linear" and canvas.yaxistype == "linear":
                xystart_normalized = convertxy(xystart)
                xyend_normalized = convertxy(xyend)
            elif canvas.xaxistype == "log" and canvas.yaxistype == "linear":
                xystart_normalized = convertxy_logx(xystart)
                xyend_normalized = convertxy_logx(xyend)
            elif canvas.xaxistype == "linear" and canvas.yaxistype == "log":
                xystart_normalized = convertxy_logy(xystart)
                xyend_normalized = convertxy_logy(xyend)
            elif canvas.xaxistype == "log" and canvas.yaxistype == "log":
                xystart_normalized = convertxy_loglog(xystart)
                xyend_normalized = convertxy_loglog(xyend)
            else:
                xystart_normalized = convertxy(xystart)
                xyend_normalized = convertxy(xyend)

            x0 = canvas.xpos+xystart_normalized[0]*canvas.width
            x1 = canvas.xpos+xyend_normalized[0]*canvas.width
            y0 = canvas.ypos+xystart_normalized[1]*canvas.height
            y1 = canvas.ypos+xyend_normalized[1]*canvas.height
    else:
        x0 = canvas.xpos+xystart[0]*canvas.width
        x1 = canvas.xpos+xyend[0]*canvas.width
        y0 = canvas.ypos+xystart[1]*canvas.height
        y1 = canvas.ypos+xyend[1]*canvas.height
        
        
    if length != None:
        dx = xyend[0]-xystart[0]
        dy = xyend[1]-xystart[1]
        norm = sqrt(dx**2+dy**2)
        dx, dy = length*dx/norm, length*dy/norm

        x1 = canvas.xpos+xyend[0]*canvas.width+dx*canvas.width
        y1 = canvas.xpos+xyend[1]*canvas.height+dy*canvas.height

    path = pyx.path.path(pyx.path.moveto(x0, y0), pyx.path.lineto(x1, y1))
    canvas.stroke(path, arrowstyle)

def pyxdimlabel(graph, xystart, xyend, labelpos, labeltext, barlength, 
                inout="in", arrowlength=0.5, barlw=1.0, difffact=0.05, 
                arrowstyle=None):
    """
    Makes dimension-lables for objects (arrows with label).
    This does only work in graphcoords, yet.
    xystart:       tupel (x,y) of starting point
    xyend:         tupel (x,y) of end point
    labelpos:      tupel (x,y) of label position
    labeltext:     text of label
    barlength:     length of the bars
    inout:         arrows inside the bar or outside ("in", "out")
    arrowlength:   length of the arrows
    barlw:         linewidth of the bars
    difffact:      factor for space between arrows and bars
    arrowstyle:    the style of the arrows
    """
                
    if xystart[0] == xyend[0]:
        style = "vertical"
    elif xystart[1] == xyend[1]:
        style = "horizontal"
    else:
        print "WARNING: Your pyxdimlabel is neither vertical nor horizontal."
        print "This will not end well..."
         
    dx, dy = abs(xyend[0]-xystart[0]), abs(xyend[1]-xystart[1])     

    if arrowstyle == None:
        arrowstyle = [pyx.style.linewidth.thin, pyx.deco.earrow.small]

    # minimal and maxmal x, y
    x0 = min(xystart[0], xyend[0])
    x1 = max(xystart[0], xyend[0])
    y0 = min(xystart[1], xyend[1])
    y1 = max(xystart[1], xyend[1])
    
    # plot the arrows, inside the bars or outside
    if inout == "in":
        graph.pyxarrow((x0+dx*difffact,y0+dy*difffact), 
                    (x1-dx*difffact,y1-dy*difffact), 
                    arrowstyle=arrowstyle, graphcoords=True)
        graph.pyxarrow((x1-dx*difffact,y1-dy*difffact), 
                    (x0+dx*difffact,y0+dy*difffact), 
                    arrowstyle=arrowstyle, graphcoords=True)
    elif inout == "out":
        if style == "horizontal":
            graph.pyxarrow((x0-arrowlength,y0), 
                        (x0-dx*difffact,y0), 
                        arrowstyle=arrowstyle, graphcoords=True)
            graph.pyxarrow((x1+arrowlength,y0), 
                        (x1+dx*difffact,y0), 
                        arrowstyle=arrowstyle, graphcoords=True)        
        elif style == "vertical":
            graph.pyxarrow((x0,y0-arrowlength), 
                        (x0,y0-dy*difffact), 
                        arrowstyle=arrowstyle, graphcoords=True)
            graph.pyxarrow((x0,y1+arrowlength), 
                        (x0,y1+dy*difffact), 
                        arrowstyle=arrowstyle, graphcoords=True)  
                   
    # plot the bars
    if style == "vertical":
        graph.pyxplot(([x0-barlength/2,x0+barlength/2],[y0,y0]), style="l", 
                      lw=barlw, lt=0, color=pyx.color.rgb(0,0,0))
        graph.pyxplot(([x0-barlength/2,x0+barlength/2],[y1,y1]), style="l", 
                      lw=barlw, lt=0, color=pyx.color.rgb(0,0,0))
    elif style == "horizontal":
        graph.pyxplot(([x0,x0],[y0-barlength/2,y0+barlength/2]), style="l", 
                      lw=barlw, lt=0, color=pyx.color.rgb(0,0,0))
        graph.pyxplot(([x1,x1],[y0-barlength/2,y0+barlength/2]), style="l", 
                      lw=barlw, lt=0, color=pyx.color.rgb(0,0,0)) 
                                           
    # plot the label
    graph.pyxlabel(labelpos, labeltext, graphcoords=True)
                                         
def pyxerrorbar(graph, xval=[], mean=[], error=[], 
                pt=17, ps=1.0, color=0, lt=1, lw=1, title=False):
    """
    Plots data and errorbars as lines.
    xval, mean, error:     data to plot
    pt, ps, color:         pointtype, poinstize, color of data points
    lt, lw:                linewidth, linestyle of error lines  
    title:                 title of error-plot    
    """  
                           
    graph.pyxplot((xval, mean), style="p", pt=pt, ps=ps, color=color, 
                  title=title)                     
    for i in xrange(len(xval)):
        graph.pyxplot(([xval[i],xval[i]], [mean[i]+error[i],mean[i]-error[i]]), 
                      style="l", lt=lt, lw=lw, color=color, title=False)
                         
def pyxsave(graphics, epsoutfile, prefix="", show_gv_command=True,
            use_paper_format=None):
    """Save the canvas `graphics` as eps file.

       By using A4 as paperformat the resulting plot is centered on A4.
       Consequenes:
         - one can print the resulting file
         - one can ensure that no negative bounding box coordinates arise
       If the plot is larger than A4 a warning will be issued
       (this is only true with PyX SVN> 09.03.2006). 
    """
    # workaround empty keys (does not work)
    #print "graphics.key:", graphics.key
    #print "graphics.key:", graphics.key.columns
    #if graphics.key.columns==0:
    #    graphics.key = False
    
    psout = os.path.join(prefix, epsoutfile)

    if use_paper_format is None:
        graphics.writeEPSfile(psout, paperformat=pyx.document.paperformat.A4)
    elif not use_paper_format:
        graphics.writeEPSfile(psout)
    else:
        graphics.writeEPSfile(psout, paperformat=use_paper_format)
    if show_gv_command:
        print "Out: ! gv ", psout

  
