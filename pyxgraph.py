# pylint: disable-msg=W0511  
# pylint: disable-msg=R0912
# pylint: disable-msg=R0913
# pylint: disable-msg=R0914
# pylint: disable-msg=R0915
# pylint: disable-msg=W0142
# pylint: disable-msg=C0103 


# Explanation:
#
# W0511   FIXME
# R0912   Too many branches 
# R0913   Too many arguments 
# R0914   Too many local variables
# R0915   Too many statements
# C0103   "pyxgraph" (should match [A-Z_][a-zA-Z0-9]+$)
###############################################################################

"""
Routines to make plotting with PyX simpler.

`PyX <http://pyx.sourceforge.net/>`_
allows to generate publication quality postscript and pdf.
Convince yourself by looking at the 
`examples <http://pyx.sourceforge.net/examples/index.html>`_

PyX is extremely flexible and well designed,
see the `documentation <http://pyx.sourceforge.net/documentation.html>`_
(pdf and FAQ).

However, for slightly more complicated graphs
the code can become very extensive.
PyXgraph tries to address this by setting up
some routines to make plotting simpler.


Arnd Baecker (2005, 2006, 2007).

Contributions/Testing/Suggestions:
  Nikolai Hlubek, Steffen Loeck, Johannes Loehnert, Lars Schilling.

"""

    
__version__ = "0.2.5"

# can we use this at some point?
#__all__ = [pyxgraph, pyxsave, pyxbitmap, pyxlabel, pyxarrow, pyxline,
#           pyxplotarray, pyx, pyxcolorbar, ColMapper]

import os
import types
import copy

from numerix import arange, ones, transpose, ColMapper, reshape

import pyx
pyx.text.set(mode="latex")

# --- local imports:
import styles
from styles import _scaled_symbol
from color_provider import _to_pyxcolor
from pyx_objects import pyxsave, pyxbitmap, pyxlabel, pyxarrow, pyxline
from pyx_objects import pyxplotarray, pyxplotcontour
from pyx_objects import pyxplothist, pyxdimlabel, pyxerrorbar
import pyx_objects

from axes import _setup_axis

### ----------------------------------------------------------
### for debugging/development:
##from IPython.Shell import IPythonShellEmbed 
##ipshell = IPythonShellEmbed() 

### on error go to IPYTHON
##import sys, IPython.ultraTB  
##sys.excepthook = IPython.ultraTB.FormattedTB(#mode='Verbose',
##                                             color_scheme='Linux',
##                                             call_pdb=1)
### ----------------------------------------------------------






# NOTE: we don't use PyxGraph (which our coding style suggests), because
#       all other classes of PyX are in small caps.
class pyxgraph(pyx.graph.graphxy):
    """Class to provide simplified usage of pyx.graphxy.

       FIXME: TODO: more details here  (easy)
    """
    # --- symbols from pyx_objects.py:
    # FIXME: pylint complains about these. Further attention needed. :) (JL)
    # (but that's the only place where they work properly - FFpylint)
    pyxsave = pyxsave
    pyxbitmap = pyxbitmap
    pyxlabel = pyxlabel
    pyxarrow = pyxarrow
    pyxline = pyxline
    pyxplotarray = pyxplotarray
    pyxplotcontour = pyxplotcontour
    pyxplothist = pyxplothist
    pyxdimlabel = pyxdimlabel
    pyxerrorbar = pyxerrorbar
    
    def __init__(self,
                 xpos=0, ypos=0,
                 width=None, height=None, ratio=1.6180339887498949,
                 backgroundattrs=None,
                 xaxisat=None, yaxisat=None,
                 axesdist=0.8*pyx.unit.v_cm, 
                 title=None,
                 
                 # --- primary axes:
                 xaxis=None, yaxis=None,          # deprecated              
                 xaxistype="linear", yaxistype="linear",                 
                 xlimits=(None, None), ylimits=(None, None),
                 xticks=None, yticks=None,
                 xlabel=None, ylabel=None,
                 xticksformat=None, yticksformat=None,                 
                 xtexter=None, ytexter=None,

                 # --- secondary axes (oposite sides):
                 x2axis=None, y2axis=None,         # deprecated
#                 x2axistype="linked", y2axistype="linked",
                 x2axistype=None, y2axistype=None,
                 x2limits=(None, None), y2limits=(None, None),
                 x2ticks=None, y2ticks=None,   
                 x2label=None, y2label=None,
                 x2ticksformat=None, y2ticksformat=None,
                 x2texter=False, y2texter=False,

                 # --- show a key
                 key=True,                 

                 # --- axis painters:
                 xpaint=None, ypaint=None, x2paint=None, y2paint=None,

                 # --- dictionary for parters (advanced users only ;-)
                 xparter_dict=None, yparter_dict=None,
                 x2parter_dict=None, y2parter_dict=None,
                 
                 # --- color sequences, line patterns and symbol patterns
                 colors="default",
                 linepatterns="default",
                 symbols="default",
                 dashlength=1,

                 # ---
                 embed_labels=False,
                 ):
        """
         xpos,ypos: position relative to canvas corner in cm
                    This has effect only when doing more than 1 plot.
         width,height: width and height of the plot in cm
                    - length unit can be changed via
                    pyx.unit.set(defaultunit='mm')

         ratio: desired aspect ratio. This is ignored if both width
                and height are specified.
         key: True/False: display a legend
              If key is a string, it is used as position information:
              Eg. key="tr" (for top-right) or  key="bl" (bottom-left)
              
              It can also be a pyx.graph.key.key instance, e.g.:
              key=pyx.graph.key.key(pos="br",vdist=0.1*pyx.unit.cm)


         backgroundattrs: list of attributes for drawing the background.
         # FIXME: add descriptions (easy)
         axesdist: distance between axes drawn at the same side of the graph
         xaxisat, yaxisat

         xaxistype, yaxistype:
            - "linear"        # default
            - "log", "log10"   
            - "ln"            # FIXME: NOT YET IMPLEMENTED (easy, if needed)
            - "pi"            - ...    
            - "frac"          fractional number             
            - "linked"        for x2axistype and y2axistype:
                              linked with xaxis and yaxis
         xlimits, ylimits:  tuple with (rangemin, rangemax). Examples:
            -  (0, 10)
            -  (0, None)
            -  (None, 10)

         xticks, yticks: 
            - (0, 2)           # FIXME: NOT YET IMPLEMENTED (see gnuplot
                               # FIXME:   `help xticks` (easy, if needed))
            - (0.0, 5.0, 1.0)  # xmin,xmax,tickstep
                               # For log: tickstep is factor
            - 
          xticksformat, yticksformat:  format string a la "%5.4f"
          
          xpaint, ypaint:
            - if set to False, axes will not be plotted
        """

        # FIXME: TODO (->AB)
        # FIXME: try clipping ... (only works with modified pyx ...)
        ##    pp=pyx.path
        ##    rect=pp.path(pp.moveto(0, 0),
        ##                 pp.lineto(6, 0),
        ##                 pp.lineto(6, 10),
        ##                 pp.lineto(0, 10),
        ##                 pp.closepath())
        ##    clp=pyx.canvas.clip(rect)

      
        # --- temporary conversion (until the end of deprecation ;-)
        # {x,y}[2]axis -> {x,y}[2]axistype
        if xaxis is not None:
            print "DeprecationWarning: xaxis deprecated. Use xaxistype instead"
            xaxistype = xaxis
        if yaxis is not None:
            print "DeprecationWarning: yaxis deprecated. Use yaxistype instead"
            yaxistype = yaxis
        if x2axis is not None:
            print "DeprecationWarning: x2axis deprecated. Use x2axistype."
            x2axistype = x2axis
        if y2axis is not None:
            print "DeprecationWarning: y2axis deprecated. Use y2axistype."
            y2axistype = y2axis

        # --- axes painter
        # FIXME: not sure about this one here:
        # FIXME: we could add xpaint_attrs, ypaint_attrs and so on
        # FIXME: and then have routines:
        # FIXME:   xpaint = _setup_default_painter(xpaint, xpaint_attrs)
        # FIXME: But, the user could also just supply
        # FIXME: his own painter,
        # FIXME:   xpaint = pyx.graph.axis.painter.regular(<user_attrs>)
        # FIXME: so there is no real need to implement the first variant?!
        # FIXME: Maybe all this condition is obsolete with the linked stuf...
        default_painter = pyx.graph.axis.painter.regular()

        if xpaint is None:
            xpaint = default_painter
        if ypaint is None:
            ypaint = default_painter
         
        # if xpaint is set to False, the axis will not be painted
        # so one can make a plot without axes   
        if xpaint is False:
            xpaint = None
        if ypaint is False:
            ypaint = None

        # --- axes
        # FIXME: an axis can 
        # FIXME: - have ticks and labels
        # FIXME: - have ticks
        # FIXME: - have no ticks
        # FIMXE: - be not drawn at all
        # FIXME:
        # FIXME: The default should be that x2 and y2 axis are coupled to x/y
        # FIXME: but have no labels.
        # FIXME: In addition they should inherit the painter from x/y
        # FIXME: supplying a different 
        axes_dict = dict()
        xlinkpainter = None
        ylinkpainter = None
        if (x2axis is None) and (x2paint is not None):
            xlinkpainter = x2paint
        if (y2axis is None) and (y2paint is not None):
            ylinkpainter = y2paint

        if x2paint is None:
            x2paint = xpaint
        if y2paint is None:
            y2paint = ypaint
            

##        if embed_labels:
##            self.embed_xlabel = xlabel
##            xlabel = None
##            self.embed_ylabel = ylabel
##            ylabel = None
####            self.embed_x2label = x2label
####            x2label = None
####            self.embed_y2label = y2label
####            y2label = None

        #print "linkpainter:", xlinkpainter, ylinkpainter
        
        if type(xaxistype) != str:
            axes_dict["x"] = xaxistype
        else:
            axes_dict["x"] = _setup_axis("x", xaxistype, xlimits, xticks,
                                     xpaint, xticksformat, xtexter, xlabel,
                                     xlinkpainter)
        if type(yaxistype) != str:
            axes_dict["y"] = yaxistype
        else:
            axes_dict["y"] = _setup_axis("y", yaxistype, ylimits, yticks,
                                     ypaint, yticksformat, ytexter, ylabel,
                                     ylinkpainter)

        axes_dict["x2"] = _setup_axis("x2", x2axistype, x2limits, x2ticks,
                                      x2paint, x2ticksformat, x2texter, x2label)
        axes_dict["y2"] = _setup_axis("y2", y2axistype, y2limits, y2ticks,
                                      y2paint, y2ticksformat, y2texter, y2label)
 
        self.xaxistype = xaxistype
        self.yaxistype = yaxistype
        #print "axes_dict", axes_dict
        
        # if not enough specification is given, remove it.
        # FIXME: this also removes the painter - HMM!!!
        if axes_dict["x2"] == False:
            axes_dict.pop("x2")
        if axes_dict["y2"] == False:
            axes_dict.pop("y2")

        # remove axes, if they are requested not to be drawn:
        if x2axistype == False:
            axes_dict["x2"] = None
        if y2axistype == False:
            axes_dict["y2"] = None

        #print "axes_dict", axes_dict

        # --- key
        if key == True:
            curr_key = pyx.graph.key.key(pos="tl")
        elif key == False:
            curr_key = None
        elif type(key) is types.StringType:  # specify position of the key
            curr_key = pyx.graph.key.key(pos=key)
        else:  # FIXME: check if this is a key instance.
            curr_key = key

        # --- default width of the graph
        if (width is None) and (height is None):
            width = 10*pyx.unit.cm
            #type(width) is types.NoneType and type(height) is types.NoneType:
        ## Q: why did this one not work ???    
        ##    if width == None and height == None:
        ##        width = 10*pyx.unit.cm

        # --- styles
        color_d, linepattern_d, symbol_d = styles.provide_styles(dashlength)
  
        # --- color sequence
        # FIXME: I (=AB) don't understand the reason of JL constructs below
        if type(colors) is types.StringType:
            self.color_seq = color_d.get(colors, [][:])
        else:
            if hasattr(colors, '__getitem__') and hasattr(colors, '__len__'):
                self.color_seq = colors
            else:
                self.color_seq = [][:]

        # --- line pattern sequence
        if type(linepatterns) is types.StringType:
            self.linepattern_seq = linepattern_d[linepatterns]
        else:
            self.linepattern_seq = linepatterns
            
        # --- symbols sequence
        if type(symbols) is types.StringType:
            self.symbol_seq = symbol_d[symbols]
        else:
            self.symbol_seq = symbols

        pyx.graph.graphxy.__init__(self, xpos=xpos, ypos=ypos,
                     width=width,
                     height=height,ratio=ratio,
                     key=curr_key,
                     backgroundattrs=backgroundattrs,   
                     axesdist=axesdist,                 
                     xaxisat=xaxisat, yaxisat=yaxisat,  # FIXME: what for ???
                     # Now the axis specifications:
                     **axes_dict
                     #attribs=[clp]                     # FIXME: what for?
                     )

##        # FIXME: none of this is working anymore ???
##        #
##        # FIXME: default ordering could be made optional:
##        # changed default ordering by which things are displayed.
##        # pylint: disable-msg=E0201(+2)  # does not work!
##        self.domethods = [ self.dolayout,  self.dobackground, self.dodata,
##                           self.doaxes, self.dokey, self.mist]

        self.title = False
        if title:
            #print "FIXME: title not working anymore!!!"
            self.title = title
            #self.domethods.append(self.pyx_do_title)

    def finish(self):
        #print "GOING INTO finish"
        self.dobackground()
        self.doaxes()
        self.dodata()
        self.dokey()
        self.pyx_do_title()
##        try:
##            self.did_embedded_labels
##        except:
##            self.pyx_do_embedded_labels()
##            self.did_embedded_labels = True
        

    def pyx_do_embedded_labels(self):
        """Embed any labels into the axes - experimental feature.
        """
        print "DOING embedded labels"
        if self.embed_xlabel:
            label = self.embed_xlabel
            if isinstance(label, tuple):
                self.pyx_xlabel(label[0], label[1])
                #, xpos=None, xshift=0, yshift=0):
            else:
                self.pyx_xlabel(label)
            self.embed_xlabel = None  # we did the job

        if self.embed_ylabel:
            label = self.embed_ylabel
            if isinstance(label, tuple):
                self.pyx_ylabel(label[0], label[1])
                #, xpos=None, xshift=0, yshift=0):
            else:
                self.pyx_ylabel()
            self.embed_ylabel = None  # we did the job
        


            

    def mist(self):
        print "never gettinghere..."


    def pyx_do_title(self):
        """If requested, do a title at the very end."""
        #print "DOING TITLE"
        #if not self.removedomethod(self.pyx_do_title):
        #    return

        # this only works after `dolayout`
        # FIXME: make title more flexible. Namely, allow:
        # FIXME:   title="title"
        # FIXME:   title=("title", xpos, ypos)
        # FIXME: the default vertical distance is not always optimal IMHO
        if self.title:
            self.pyxlabel((0.5, 1.05), self.title)
        self.title = None  # we did the job.

        
    def pyxplot(self, data,
                style="linespoints",
                linetype=None, lt=None,
                pointtype=None, pt=None,
                pointsize=None, ps=None,
                linewidth=None, lw=None,
                dashlength=None, dl=None,
                color=None, linecolor=None, 
                title=None,
                lineattrs=list()
                ): 
        """
        FIXME: Note: not everything is implemented!!!

        data:
           - "y(x)=sin(x)"
           - (x,y)   arrays/lists for x,y
           - "filename.dat"
           - ("filename.dat", x_column, y_column)
           - PyX data instance: `pyx.data` (most flexible)
        style: 
           - "l" , "lines"
           - "lp", "linespoints"
           - "p",  "points"
        linetype, lt:
           - None: automatic association
           - 0,...,len(linepattern_seq)-1
                (larger values are taken via mod)
           - PyX line style instance
           - string like '- -._ ', possible chars: . ' " - _ <space>        " 
        pointtype, pt:
           - None: automatic association
           - 0,...,len(symbol_seq)-1
                (larger values are taken via mod)
           - PyX symbol instance
        color:
           - None: automatic association
           - 0,...,len(color_seq)-1
                (larger values are taken via mod)
           - PyX color instance: `pyx.color.color`
        linecolor:
            - Overrides color values for the lines.
              Only meaningful for linespoints graph type.
        pointsize, ps:
           - multiplication factor for symbol sizes
        linewidth, lw:
           - multiplication factor for lines
           - PyX linewidth instance
        dashlength, dl:
           - multiplication for for the dash length
        title: name of the data row for legend, default: consecutive number
            If you want no title for a particular plot, set title=False.
        """

        try:
            self.pltctr = self.pltctr+1
        except AttributeError:
            self.pltctr = 0

        # When a key is specified, but no title for
        # any of the lines one gets an error from PyX.
        # To avoid this we give each line a title when a key is requested:
        if (self.key is not None) and (title is None):
            title = str(self.pltctr+1)
            # REMARK: this is more a bug of PyX than ...
        if title == False:
            title = None

        if not style in ["l" , "lines", "lp", "linespoints", "p",  "points"]:
            raise ValueError("Invalid style '%s'. " % (style))

        # --- check attributes for linetype, linewidth, pointtype, pointsize
        #     and dashlength and use default values if appropriate
        def _check_attr(attr1, attr2, str1, str2, default=None):
            """Test if both `attr1` and `attr2` are defined.
               In this case select the first and issue a warning.
               If only one is defined, then this is returned.
            """
            attr = default
            if attr1 is not None:
                attr = attr1
            if attr2 is not None:
                if attr1 is None:
                    attr = attr2
                else:
                    raise Warning("Do not specify both `%s` and `%s`"
                                  "- using %s." % (str1, str2, str1 ))
            return attr
                    
        linetype = _check_attr(linetype, lt, "linetype", "lt")
        linewidth = _check_attr(linewidth, lw, "linewidth", "lw", 1.0)
        pointtype = _check_attr(pointtype, pt, "pointtype", "pt")
        pointsize = _check_attr(pointsize, ps, "pointsize", "ps", 1.0)
        dashlength = _check_attr(dashlength, dl, "dashlength", "dl", 1.0)

        # --- associate color
        if color is None:
            try:
                self.colctr = self.colctr+1
            except AttributeError:
                self.colctr = 0
            color = self.color_seq[self.colctr % len(self.color_seq)]
        else:
            color = _to_pyxcolor(color, self.color_seq)
        
        if linecolor is None:
            linecolor = color
        else:
            linecolor = _to_pyxcolor(linecolor, self.color_seq)

        # --- point style
        if pointtype is None:
            pointtype = self.symbol_seq[self.pltctr % len(self.symbol_seq)]

        if type(pointtype) is types.IntType:
            pointtype = self.symbol_seq[pointtype % len(self.symbol_seq)]

        # --- line style
        if linetype is None:
            linetype = self.linepattern_seq[self.pltctr %
                                             len(self.linepattern_seq)]
        if type(linetype) is types.IntType:
            linetype = self.linepattern_seq[linetype %
                                           len(self.linepattern_seq)]
        if type(linetype) in types.StringTypes:
            linetype = styles.linepattern_from_string(linetype)

        if (dashlength != 1.0) and isinstance(linetype, pyx.style.dash):
            # stretch the dash-pattern by dashlength
            pattern = []
            for dash in linetype.pattern:
                pattern.append(dashlength*dash)
            linetype = copy.copy(linetype)
            linetype.pattern  = pattern

        # certain linetypes (see styles.py) are instances
        # of pyx.style.linestyle together with a dash pattern
        # in linetype.d.pattern:
        if (dashlength != 1.0) and isinstance(linetype, pyx.style.linestyle):
            # stretch the dash-pattern by dashlength
            if linetype.d:
                pattern = []
                for dash in linetype.d.pattern:
                    pattern.append(dashlength*dash)
                linetype = copy.copy(linetype)
                linetype.d.pattern  = pattern

        # --- linewidth
        if (type(linewidth) is types.FloatType
            or type(linewidth) is types.IntType):
            #linewidth = 5.0*linewidth*pyx.style.linewidth.normal

            # 0.72 ...
            #linewidth = pyx.style.linewidth(linewidth
            #                                  *pyx.style.linewidth.normal)
            # PyX>= 0.81
            linewidth = pyx.style.linewidth(0.02*linewidth)
            #*pyx.style.linewidth.normal)

        # --- combine the plot style
        if style == "points" or style == "p":
            plot_style = [_scaled_symbol(pointtype[0], [color]+pointtype[1],
                                         factor=pointsize)]
        if style == "lines" or style == "l":
            plot_style = [pyx.graph.style.line(lineattrs=[linetype, linewidth,
                                                          linecolor]+lineattrs)]
        if style == "linespoints" or style == "lp":
            plot_style = [pyx.graph.style.line(lineattrs=[linetype, linewidth,
                                                          linecolor]+lineattrs),
                          _scaled_symbol(pointtype[0], [color]+pointtype[1],
                                         factor=pointsize)]

        # --- set up plot_dat
        # get the data:   FIXME: put this into some subroutine (pretty easy)
        plot_dat = None
        if type(data) is types.StringType:
            if "=" in data:    # explicit function specification,  uses "="
                plot_dat = pyx.graph.data.function(data, title=title)
                       #, **kwargs)
            else:  # presumably a file
                if not os.path.exists(data):
                    raise Exception, "file not found:"+data
                plot_dat = pyx.graph.data.file(data, x=1, y=2, title=title)

        if type(data) is types.TupleType:
            if len(data) == 2:  # just (x,y) data specified
                if type(data[0]) in [types.StringType,
                                     types.UnicodeType]:
                    # (fname, additional_key_dict)
                    # FIXME: test that data[1] is a dictionary
                    plot_dat = pyx.graph.data.file(data[0], title=title,
                                                   **data[1])
                else:
                    # x,y
                    # FIXME: check that data[0] and data[1]
                    # FIXME: are 1D lists or 1D arrays
                    plot_dat = pyx.graph.data.list(zip(data[0], data[1]),
                                                   x=1, y=2, title=title)
            elif (len(data) == 3) or (len(data) ==4):
                # (filename, x_column, y_column)
                # (filename, x_column, y_column, additionalkeys)
                if not type(data[0]) is types.StringType:
                    raise TypeError, "first element of data should be string"
                if (     (not type(data[1]) is types.IntType)
                     and (not type(data[1]) is types.StringType) ):
                    raise TypeError, (
                      "2nd element of data should be Int or String")
                if (     (not type(data[2]) is types.IntType)
                     and (not type(data[2]) is types.StringType) ):
                    raise TypeError, (
                      "3nd element of data should be Int or String")
                additional_keys = dict()
                if len(data) == 4:
                    additional_keys = data[3]
                plot_dat = pyx.graph.data.file(data[0], x=data[1], y=data[2],
                                        title=title, **additional_keys)
            
            else:
                raise TypeError, "tuple of length 2 expected for 2nd argument"

        if isinstance(data, pyx.graph.data._data):
            plot_dat = data

        if plot_dat == None:
            raise Exception, "No valid 2nd argument for data!"

        self.plot(plot_dat, plot_style)


    def pyx_xlabel(self, label, xpos=None, xshift=0, yshift=0):
        """Label embedded in the x-axis labels.

           The xposition is determined to be half way between the last
           two tickslabels and the vertical position is such that
           the middle is at the height of the baseline of tick labels.
           
           xpos: value from [0.0,1.0]
                 (this overrides the `half way` positioning)
           xshift: optional shift in x direction
           yshift: optional shift in y direction
                    (units for both: labeldist, i.e. the distance
                     between the horizontal line and the upper edge
                     of the ticks labels)
        """
        #print "Before pyx_xlabel dolayout"
        self.dolayout()                # all the following only works after this
        #print "after pyx_xlabel dolayout"

        # determine position of the last two labels:
        x_ax=self.axes["x"]
        prelast_t = None
        last_t = None
        for t in x_ax.data.ticks:   # loop over all ticks
            if t.label:             # only labeled ticks have a box
                prelast_t = last_t
                last_t = t
                
        if prelast_t == None:
            print "Uups, just one label for the whole axis? (problem!)"

        if xpos == None:
            xpos1, dummy = self.pos(1.0*prelast_t.num/prelast_t.denom, 47.11)
            xpos2, dummy = self.pos(1.0*last_t.num/last_t.denom, 47.11)
            xpos = pyx.unit.tocm((xpos1+xpos2)/2.0)
        else:  # xpos is from [0.0, 1.0], convert to right coords
            bb = self.bbox()
            lx = bb.left()
            rx = bb.right()
            xpos = lx+xpos*(rx-lx)

        #print "here we are .."
        
        # get baseline of xlabels, shift (if requested) and draw.
        #print dir(self)
        #bb = self.canvas.bbox() #
        bb = self.bbox()  # this calls finish again ===> recursion!
        #print "here we are ..1"
        baseline = bb.bottom()
        #print "here we are ..2"
        labeldist = x_ax.axis.painter.labeldist
        #print "here we are ..3"
        yshift = yshift*labeldist
        xshift = xshift*labeldist
        #print "here we are ..4"
        self.text(xpos + xshift, baseline + yshift, label,
                  [pyx.text.valign.middle, pyx.text.halign.center])
        #print "end of pyx_xlabel"

        
    def pyx_ylabel(self, label, ypos=None, yshift=0, xshift=0):
        """Label embedded in the y-axis labels.

           The yposition is determined to be half way between the last
           two tickslabels and the horizontal position is such that
           the middle is at the left edge of the bounding box for
           the graph
           
           ypos: value from [0.0,1.0]
                 (this overrides the `half way` positioning)
           xshift: optional shift in x direction
           yshift: optional shift in y direction
                    (units for both: labeldist, i.e. the distance
                     between the grph line and the right edge
                     of the ticks labels)
        """
        self.dolayout()                # all the following only works after this
        # determine position of the last two labels:
        y_ax=self.axes["y"]
        prelast_t = None
        last_t = None
        for t in y_ax.data.ticks:   # loop over all ticks
            if t.label:             # only labeled ticks have a box
                prelast_t = last_t
                last_t = t
                #print "Label:", t.num, t.label
                
        if prelast_t == None:
            print "Uups, just one label for the whole y axis?"

        if ypos == None:
            dummy, ypos1  = self.pos(47.11, 1.0*prelast_t.num/prelast_t.denom)
            dummy, ypos2  = self.pos(47.11, 1.0*last_t.num/last_t.denom)
            ypos = pyx.unit.tocm((ypos1+ypos2)/2.0)
        else:  # ypos is from [0.0, 1.0], convert to right coords
            bb = self.bbox()
            ly = bb.bottom()
            uy = bb.top()
            ypos = ly+ypos*(uy-ly)

        # get baseline of xlabels, shift (if requested) and draw.
        bb=self.bbox()
        leftline = bb.left()
        labeldist = y_ax.axis.painter.labeldist
        yshift = yshift*labeldist
        xshift = xshift*labeldist
        self.text(leftline + xshift, ypos + yshift, label,
                  [pyx.text.valign.middle, pyx.text.halign.center])



# NOTE: we don't use PyxGraph (which our coding style suggests), because
#       all other classes of PyX are in small caps.
if "graphxyz" in pyx.graph.__dict__:
    class pyxgraph3d(pyx.graph.graphxyz):
        """Class to provide simplified usage of pyx.graphxyz.
           YOU NEED PYX 0.1 or better!!!
           ALL METHODS SHOULD BE TESTED AND MODIFIED
    
           FIXME: TODO: more details here  (easy)
        """
        # --- symbols from pyx_objects.py:
        # FIXME: pylint complains about these. Further attention needed. :) (JL)
        # (but that's the only place where they work properly - FFpylint)
        pyxsave = pyxsave
        pyxbitmap = pyxbitmap
        pyxlabel = pyxlabel
        pyxarrow = pyxarrow
        pyxline = pyxline
        pyxplotarray = pyxplotarray
        pyxplotcontour = pyxplotcontour
        pyxplothist = pyxplothist
        pyxdimlabel = pyxdimlabel
        pyxerrorbar = pyxerrorbar
        
        def __init__(self,
                     xpos=0, ypos=0,
                     size=5, xscale=1, yscale=1, zscale=0.61803398874989479,
                     title=None, projector=pyx.graph.graphxyz.parallel(135, 35),
                     
                     # --- primary axes:
                     xaxis=None, yaxis=None, zaxis=None,         # deprecated              
                     xaxistype="linear", yaxistype="linear", zaxistype="linear",                 
                     xlimits=(None, None), ylimits=(None, None), zlimits=(None, None),
                     xticks=None, yticks=None, zticks=None,
                     xlabel=None, ylabel=None, zlabel=None,
                     xticksformat=None, yticksformat=None, zticksformat=None,                
                     xtexter=None, ytexter=None, ztexter=None,
    
                     # --- secondary axes (oposite sides):
                     x2axis=None, y2axis=None, z2axis=None,        # deprecated
    #                 x2axistype="linked", y2axistype="linked",
                     x2axistype=None, y2axistype=None, z2axistype=None,
                     x2limits=(None, None), y2limits=(None, None), z2limits=(None, None),
                     x2ticks=None, y2ticks=None, z2ticks=None,   
                     x2label=None, y2label=None, z2label=None,
                     x2ticksformat=None, y2ticksformat=None, z2ticksformat=None,
                     x2texter=False, y2texter=False, z2texter=False,
    
                     # --- show a key
                     key=True,                 
    
                     # --- axis painters:
                     xpaint=None, ypaint=None, zpaint=None, 
                     x2paint=None, y2paint=None, z2paint=None,
    
                     # --- dictionary for parters (advanced users only ;-)
                     xparter_dict=None, yparter_dict=None, zparter_dict=None,
                     x2parter_dict=None, y2parter_dict=None, z2parter_dict=None,
                     
                     # --- color sequences, line patterns and symbol patterns
                     colors="default",
                     linepatterns="default",
                     symbols="default",
                     dashlength=1,
    
                     # ---
                     embed_labels=False,
                     ):
            """
             xpos,ypos: position relative to canvas corner in cm
                        This has effect only when doing more than 1 plot.
             size: size of the plot in cm
                        - length unit can be changed via
                        pyx.unit.set(defaultunit='mm')
    
             key: True/False: display a legend
                  If key is a string, it is used as position information:
                  Eg. key="tr" (for top-right) or  key="bl" (bottom-left)
                  
                  It can also be a pyx.graph.key.key instance, e.g.:
                  key=pyx.graph.key.key(pos="br",vdist=0.1*pyx.unit.cm)
    
    
             xaxistype, yaxistype, zaxistype:
                - "linear"        # default
                - "log", "log10"   
                - "ln"            # FIXME: NOT YET IMPLEMENTED (easy, if needed)
                - "pi"            - ...    
                - "frac"          fractional number             
                - "linked"        for x2axistype and y2axistype:
                                  linked with xaxis and yaxis
             xlimits, ylimits, zlimits:  tuple with (rangemin, rangemax). Examples:
                -  (0, 10)
                -  (0, None)
                -  (None, 10)
    
             xticks, yticks, zticks: 
                - (0, 2)           # FIXME: NOT YET IMPLEMENTED (see gnuplot
                                   # FIXME:   `help xticks` (easy, if needed))
                - (0.0, 5.0, 1.0)  # xmin,xmax,tickstep
                                   # For log: tickstep is factor
                - 
              xticksformat, yticksformat, zticksformat:  format string a la "%5.4f"
              
              xpaint, ypaint, zpaint:
                - if set to False, axes will not be plotted
            """
    
            # FIXME: TODO (->AB)
            # FIXME: try clipping ... (only works with modified pyx ...)
            ##    pp=pyx.path
            ##    rect=pp.path(pp.moveto(0, 0),
            ##                 pp.lineto(6, 0),
            ##                 pp.lineto(6, 10),
            ##                 pp.lineto(0, 10),
            ##                 pp.closepath())
            ##    clp=pyx.canvas.clip(rect)
    
          
            # --- temporary conversion (until the end of deprecation ;-)
            # {x,y}[2]axis -> {x,y}[2]axistype
            if xaxis is not None:
                print "DeprecationWarning: xaxis deprecated. Use xaxistype instead"
                xaxistype = xaxis
            if yaxis is not None:
                print "DeprecationWarning: yaxis deprecated. Use yaxistype instead"
                yaxistype = yaxis
            if zaxis is not None:
                print "DeprecationWarning: yaxis deprecated. Use yaxistype instead"
                zaxistype = zaxis
            if x2axis is not None:
                print "DeprecationWarning: x2axis deprecated. Use x2axistype."
                x2axistype = x2axis
            if y2axis is not None:
                print "DeprecationWarning: y2axis deprecated. Use y2axistype."
                y2axistype = y2axis
            if z2axis is not None:
                print "DeprecationWarning: y2axis deprecated. Use y2axistype."
                z2axistype = z2axis
    
            # --- axes painter
            # FIXME: not sure about this one here:
            # FIXME: we could add xpaint_attrs, ypaint_attrs and so on
            # FIXME: and then have routines:
            # FIXME:   xpaint = _setup_default_painter(xpaint, xpaint_attrs)
            # FIXME: But, the user could also just supply
            # FIXME: his own painter,
            # FIXME:   xpaint = pyx.graph.axis.painter.regular(<user_attrs>)
            # FIXME: so there is no real need to implement the first variant?!
            # FIXME: Maybe all this condition is obsolete with the linked stuf...
            default_painter = pyx.graph.axis.painter.regular()
    
            if xpaint is None:
                xpaint = default_painter
            if ypaint is None:
                ypaint = default_painter
            if zpaint is None:
                zpaint = default_painter
             
            # if xpaint is set to False, the axis will not be painted
            # so one can make a plot without axes   
            if xpaint is False:
                xpaint = None
            if ypaint is False:
                ypaint = None
            if zpaint is False:
                zpaint = None
    
            # --- axes
            # FIXME: an axis can 
            # FIXME: - have ticks and labels
            # FIXME: - have ticks
            # FIXME: - have no ticks
            # FIMXE: - be not drawn at all
            # FIXME:
            # FIXME: The default should be that x2 and y2 axis are coupled to x/y
            # FIXME: but have no labels.
            # FIXME: In addition they should inherit the painter from x/y
            # FIXME: supplying a different 
            axes_dict = dict()
            xlinkpainter = None
            ylinkpainter = None
            zlinkpainter = None
            if (x2axis is None) and (x2paint is not None):
                xlinkpainter = x2paint
            if (y2axis is None) and (y2paint is not None):
                ylinkpainter = y2paint
            if (z2axis is None) and (z2paint is not None):
                zlinkpainter = z2paint
    
            if x2paint is None:
                x2paint = xpaint
            if y2paint is None:
                y2paint = ypaint
            if z2paint is None:
                z2paint = zpaint            
    
    ##        if embed_labels:
    ##            self.embed_xlabel = xlabel
    ##            xlabel = None
    ##            self.embed_ylabel = ylabel
    ##            ylabel = None
    ####            self.embed_x2label = x2label
    ####            x2label = None
    ####            self.embed_y2label = y2label
    ####            y2label = None
    
            #print "linkpainter:", xlinkpainter, ylinkpainter
            
            if type(xaxistype) != str:
                axes_dict["x"] = xaxistype
            else:
                axes_dict["x"] = _setup_axis("x", xaxistype, xlimits, xticks,
                                         xpaint, xticksformat, xtexter, xlabel,
                                         xlinkpainter)
            if type(yaxistype) != str:
                axes_dict["y"] = yaxistype
            else:
                axes_dict["y"] = _setup_axis("y", yaxistype, ylimits, yticks,
                                         ypaint, yticksformat, ytexter, ylabel,
                                         ylinkpainter)
            if type(yaxistype) != str:
                axes_dict["z"] = zaxistype
            else:
                axes_dict["z"] = _setup_axis("z", zaxistype, zlimits, zticks,
                                         zpaint, zticksformat, ztexter, zlabel,
                                         zlinkpainter)
    
            axes_dict["x2"] = _setup_axis("x2", x2axistype, x2limits, x2ticks,
                                          x2paint, x2ticksformat, x2texter, x2label)
            axes_dict["y2"] = _setup_axis("y2", y2axistype, y2limits, y2ticks,
                                          y2paint, y2ticksformat, y2texter, y2label)
            axes_dict["z2"] = _setup_axis("z2", z2axistype, z2limits, z2ticks,
                                          z2paint, z2ticksformat, z2texter, z2label)
     
            self.xaxistype = xaxistype
            self.yaxistype = yaxistype
            self.zaxistype = zaxistype
            #print "axes_dict", axes_dict
            
            # if not enough specification is given, remove it.
            # FIXME: this also removes the painter - HMM!!!
            if axes_dict["x2"] == False:
                axes_dict.pop("x2")
            if axes_dict["y2"] == False:
                axes_dict.pop("y2")
            if axes_dict["z2"] == False:
                axes_dict.pop("z2")
    
            # remove axes, if they are requested not to be drawn:
            if x2axistype == False:
                axes_dict["x2"] = None
            if y2axistype == False:
                axes_dict["y2"] = None
            if z2axistype == False:
                axes_dict["z2"] = None
    
            #print "axes_dict", axes_dict
    
            # --- key
            if key == True:
                curr_key = pyx.graph.key.key(pos="tl")
            elif key == False:
                curr_key = None
            elif type(key) is types.StringType:  # specify position of the key
                curr_key = pyx.graph.key.key(pos=key)
            else:  # FIXME: check if this is a key instance.
                curr_key = key
    
            # --- styles
            color_d, linepattern_d, symbol_d = styles.provide_styles(dashlength)
      
            # --- color sequence
            # FIXME: I (=AB) don't understand the reason of JL constructs below
            if type(colors) is types.StringType:
                self.color_seq = color_d.get(colors, [][:])
            else:
                if hasattr(colors, '__getitem__') and hasattr(colors, '__len__'):
                    self.color_seq = colors
                else:
                    self.color_seq = [][:]
    
            # --- line pattern sequence
            if type(linepatterns) is types.StringType:
                self.linepattern_seq = linepattern_d[linepatterns]
            else:
                self.linepattern_seq = linepatterns
                
            # --- symbols sequence
            if type(symbols) is types.StringType:
                self.symbol_seq = symbol_d[symbols]
            else:
                self.symbol_seq = symbols
    
            pyx.graph.graphxyz.__init__(self, xpos=xpos, ypos=ypos,
                         size=size, xscale=xscale, yscale=yscale, zscale=zscale,
                         key=curr_key, projector=projector,              
                         # Now the axis specifications:
                         **axes_dict
                         #attribs=[clp]                     # FIXME: what for?
                         )
    
    ##        # FIXME: none of this is working anymore ???
    ##        #
    ##        # FIXME: default ordering could be made optional:
    ##        # changed default ordering by which things are displayed.
    ##        # pylint: disable-msg=E0201(+2)  # does not work!
    ##        self.domethods = [ self.dolayout,  self.dobackground, self.dodata,
    ##                           self.doaxes, self.dokey, self.mist]
    
            self.title = False
            if title:
                #print "FIXME: title not working anymore!!!"
                self.title = title
                #self.domethods.append(self.pyx_do_title)
    
        def finish(self):
            #print "GOING INTO finish"
            self.dobackground()
            self.doaxes()
            self.dodata()
            self.dokey()
            self.pyx_do_title()
    ##        try:
    ##            self.did_embedded_labels
    ##        except:
    ##            self.pyx_do_embedded_labels()
    ##            self.did_embedded_labels = True
            
    
        def pyx_do_embedded_labels(self):
            """Embed any labels into the axes - experimental feature.
            """
            print "DOING embedded labels"
            if self.embed_xlabel:
                label = self.embed_xlabel
                if isinstance(label, tuple):
                    self.pyx_xlabel(label[0], label[1])
                    #, xpos=None, xshift=0, yshift=0):
                else:
                    self.pyx_xlabel(label)
                self.embed_xlabel = None  # we did the job
    
            if self.embed_ylabel:
                label = self.embed_ylabel
                if isinstance(label, tuple):
                    self.pyx_ylabel(label[0], label[1])
                    #, xpos=None, xshift=0, yshift=0):
                else:
                    self.pyx_ylabel()
                self.embed_ylabel = None  # we did the job
            
            if self.embed_zlabel:
                label = self.embed_zlabel
                if isinstance(label, tuple):
                    self.pyx_ylabel(label[0], label[1])
                    #, xpos=None, xshift=0, yshift=0):
                else:
                    self.pyx_zlabel()
                self.embed_zlabel = None  # we did the job
    
                
    
        def mist(self):
            print "never gettinghere..."
    
    
        def pyx_do_title(self):
            """If requested, do a title at the very end."""
            #print "DOING TITLE"
            #if not self.removedomethod(self.pyx_do_title):
            #    return
    
            # this only works after `dolayout`
            # FIXME: make title more flexible. Namely, allow:
            # FIXME:   title="title"
            # FIXME:   title=("title", xpos, ypos)
            # FIXME: the default vertical distance is not always optimal IMHO
            if self.title:
                self.pyxlabel((0.5, 1.05), self.title)
            self.title = None  # we did the job.
    
            
        def pyxplot(self, data,
                    style="linespoints",
                    linetype=None, lt=None,
                    pointtype=None, pt=None,
                    pointsize=None, ps=None,
                    linewidth=None, lw=None,
                    dashlength=None, dl=None,
                    color=None, linecolor=None, 
                    title=None,
                    lineattrs=list()
                    ): 
            """
            FIXME: Note: not everything is implemented!!!
    
            data:
               - "z(x,y)=sin(x*y)" not tested
               - (x,y,z)   arrays/lists for x,y,z
               - "filename.dat" not tested
               - ("filename.dat", x_column, y_column, z_column) not tested
               - PyX data instance: `pyx.data` (most flexible)
            style: 
               - "l" , "lines"
               - "lp", "linespoints"
               - "p",  "points"
            linetype, lt:
               - None: automatic association
               - 0,...,len(linepattern_seq)-1
                    (larger values are taken via mod)
               - PyX line style instance
               - string like '- -._ ', possible chars: . ' " - _ <space>
            pointtype, pt:
               - None: automatic association
               - 0,...,len(symbol_seq)-1
                    (larger values are taken via mod)
               - PyX symbol instance
            color:
               - None: automatic association
               - 0,...,len(color_seq)-1
                    (larger values are taken via mod)
               - PyX color instance: `pyx.color.color`
            linecolor:
                - Overrides color's value for the lines.
                  Only senseful for linespoints graph type.
            pointsize, ps:
               - multiplication factor for symbol sizes
            linewidth, lw:
               - multiplication factor for lines
               - PyX linewidth instance
            dashlength, dl:
               - multiplication for for the dash length
            title: name of the data row for legend, default: consecutive number
                If you want no title for a particular plot, set title=False.
            """
    
            try:
                self.pltctr = self.pltctr+1
            except AttributeError:
                self.pltctr = 0
    
            # When a key is specified, but no title for
            # any of the lines one gets an error from PyX.
            # To avoid this we give each line a title when a key is requested:
            if (self.key is not None) and (title is None):
                title = str(self.pltctr+1)
                # REMARK: this is more a bug of PyX than ...
            if title == False:
                title = None
    
            if not style in ["l" , "lines", "lp", "linespoints", "p",  "points"]:
                raise ValueError("Invalid style '%s'. " % (style))
    
            # --- check attributes for linetype, linewidth, pointtype, pointsize
            #     and dashlength and use default values if appropriate
            def _check_attr(attr1, attr2, str1, str2, default=None):
                """Test if both `attr1` and `attr2` are defined.
                   In this case select the first and issue a warning.
                   If only one is defined, then this is returned.
                """
                attr = default
                if attr1 is not None:
                    attr = attr1
                if attr2 is not None:
                    if attr1 is None:
                        attr = attr2
                    else:
                        raise Warning("Don't specify both `%s` and `%s`"
                                      "- using %s." % (str1, str2, str1 ))
                return attr
                        
            linetype = _check_attr(linetype, lt, "linetype", "lt")
            linewidth = _check_attr(linewidth, lw, "linewidth", "lw", 1.0)
            pointtype = _check_attr(pointtype, pt, "pointtype", "pt")
            pointsize = _check_attr(pointsize, ps, "pointsize", "ps", 1.0)
            dashlength = _check_attr(dashlength, dl, "dashlength", "dl", 1.0)
    
            # --- associate color
            if color is None:
                try:
                    self.colctr = self.colctr+1
                except AttributeError:
                    self.colctr = 0
                color = self.color_seq[self.colctr % len(self.color_seq)]
            else:
                color = _to_pyxcolor(color, self.color_seq)
            
            if linecolor is None:
                linecolor = color
            else:
                linecolor = _to_pyxcolor(linecolor, self.color_seq)
    
            # --- point style
            if pointtype is None:
                pointtype = self.symbol_seq[self.pltctr % len(self.symbol_seq)]
    
            if type(pointtype) is types.IntType:
                pointtype = self.symbol_seq[pointtype % len(self.symbol_seq)]
    
            # --- line style
            if linetype is None:
                linetype = self.linepattern_seq[self.pltctr %
                                                 len(self.linepattern_seq)]
            if type(linetype) is types.IntType:
                linetype = self.linepattern_seq[linetype %
                                               len(self.linepattern_seq)]
            if type(linetype) in types.StringTypes:
                linetype = styles.linepattern_from_string(linetype)
    
            if (dashlength != 1.0) and isinstance(linetype, pyx.style.dash):
                # stretch the dash-pattern by dashlength
                pattern = []
                for dash in linetype.pattern:
                    pattern.append(dashlength*dash)
                linetype = copy.copy(linetype)
                linetype.pattern  = pattern
    
            # certain linetypes (see styles.py) are instances
            # of pyx.style.linestyle together with a dash pattern
            # in linetype.d.pattern:
            if (dashlength != 1.0) and isinstance(linetype, pyx.style.linestyle):
                # stretch the dash-pattern by dashlength
                if linetype.d:
                    pattern = []
                    for dash in linetype.d.pattern:
                        pattern.append(dashlength*dash)
                    linetype = copy.copy(linetype)
                    linetype.d.pattern  = pattern
    
            # --- linewidth
            if (type(linewidth) is types.FloatType
                or type(linewidth) is types.IntType):
                #linewidth = 5.0*linewidth*pyx.style.linewidth.normal
    
                # 0.72 ...
                #linewidth = pyx.style.linewidth(linewidth
                #                                  *pyx.style.linewidth.normal)
                # PyX>= 0.81
                linewidth = pyx.style.linewidth(0.02*linewidth)
                #*pyx.style.linewidth.normal)
    
            # --- combine the plot style
            if style == "points" or style == "p":
                plot_style = [_scaled_symbol(pointtype[0], [color]+pointtype[1],
                                             factor=pointsize)]
            if style == "lines" or style == "l":
                plot_style = [pyx.graph.style.line(lineattrs=[linetype, linewidth,
                                                              linecolor]+lineattrs)]
            if style == "linespoints" or style == "lp":
                plot_style = [pyx.graph.style.line(lineattrs=[linetype, linewidth,
                                                              linecolor]+lineattrs),
                              _scaled_symbol(pointtype[0], [color]+pointtype[1],
                                             factor=pointsize)]
    
            # --- set up plot_dat
            # get the data:   FIXME: put this into some subroutine (pretty easy)
            plot_dat = None
            if type(data) is types.StringType:
                if "=" in data:    # explicit function specification,  uses "="
                    plot_dat = pyx.graph.data.function(data, title=title)
                           #, **kwargs)
                else:  # presumably a file
                    if not os.path.exists(data):
                        raise Exception, "file not found:"+data
                    plot_dat = pyx.graph.data.file(data, x=1, y=2, title=title)
    
            if type(data) is types.TupleType:
                if len(data) == 3:  # just (x,y,z) data specified
                    if type(data[0]) in [types.StringType,
                                         types.UnicodeType]:
                        # (fname, additional_key_dict)
                        # FIXME: test that data[1] is a dictionary
                        plot_dat = pyx.graph.data.file(data[0], title=title,
                                                       **data[1])
                    else:
                        # x,y
                        # FIXME: check that data[0] and data[1]
                        # FIXME: are 1D lists or 1D arrays
                        plot_dat = pyx.graph.data.list(zip(data[0], data[1], data[2]),
                                                       x=1, y=2, z=3, title=title)
                elif (len(data) == 4) or (len(data) == 5):
                    # (filename, x_column, y_column)
                    # (filename, x_column, y_column, additionalkeys)
                    if not type(data[0]) is types.StringType:
                        raise TypeError, "first element of data should be string"
                    if (     (not type(data[1]) is types.IntType)
                         and (not type(data[1]) is types.StringType) ):
                        raise TypeError, (
                          "2nd element of data should be Int or String")
                    if (     (not type(data[2]) is types.IntType)
                         and (not type(data[2]) is types.StringType) ):
                        raise TypeError, (
                          "3nd element of data should be Int or String")
                    additional_keys = dict()
                    if len(data) == 5:
                        additional_keys = data[4]
                    plot_dat = pyx.graph.data.file(data[0], x=data[1], y=data[2], z=data[3],
                                            title=title, **additional_keys)
                
                else:
                    raise TypeError, "tuple of length 3 expected for 2nd argument"
    
            if isinstance(data, pyx.graph.data._data):
                plot_dat = data
    
            if plot_dat == None:
                raise Exception, "No valid 2nd argument for data!"
    
            self.plot(plot_dat, plot_style)
            
        def pyxplotsurface(self, data, style=None, title=None, 
                           gradient=pyx.color.lineargradient.Grey, gridcolor=None,
                           backcolor=None):
            """ plot a 2d surface in a 3d plot:
                data:  (x, y, z) 1d or 2d arrays of the same shape
                style: "grid" or "surface"
                gradient: color gradient for surface plot
                gridcolor: plot grid in gridcolor
                backcolor: color for background
            """
            
            if style == None:
                style = "surface"
                
            if title == False:
                title = None
            
            if len(data) != 3:
                raise TypeError, "tuple of length 3 expected for 1nd argument (data)"
            else:
                if data[0].ndim == 2:
                    datax = reshape(data[0], len(data[0][:,0])*len(data[0][0,:]))
                else:
                    datax = data[0]
                if data[1].ndim == 2:
                    datay = reshape(data[1], len(data[1][:,1])*len(data[1][1,:]))
                else:
                    datay = data[1]
                if data[2].ndim == 2:
                    dataz = reshape(data[2], len(data[2][:,2])*len(data[2][2,:]))
                else:
                    dataz = data[2]
                    
            plot_dat = pyx.graph.data.list(zip(datax, datay, dataz),
                                           x=1, y=2, z=3, title=title) 
                
            if style == "grid":
                plot_style = pyx.graph.style.grid()
            elif style == "surface":
                plot_style = pyx.graph.style.surface(gradient=gradient, 
                                     gridcolor=gridcolor, backcolor=backcolor)
            
            self.plot(plot_dat, [plot_style])
                    
    
        ## TODO: below here
        ## NOTHING TESTED
    
        def pyx_xlabel(self, label, xpos=None, xshift=0, yshift=0):
            """Label embedded in the x-axis labels.
    
               The xposition is determined to be half way between the last
               two tickslabels and the vertical position is such that
               the middle is at the height of the baseline of tick labels.
               
               xpos: value from [0.0,1.0]
                     (this overrides the `half way` positioning)
               xshift: optional shift in x direction
               yshift: optional shift in y direction
                        (units for both: labeldist, i.e. the distance
                         between the horizontal line and the upper edge
                         of the ticks labels)
            """
            #print "Before pyx_xlabel dolayout"
            self.dolayout()                # all the following only works after this
            #print "after pyx_xlabel dolayout"
    
            # determine position of the last two labels:
            x_ax=self.axes["x"]
            prelast_t = None
            last_t = None
            for t in x_ax.data.ticks:   # loop over all ticks
                if t.label:             # only labeled ticks have a box
                    prelast_t = last_t
                    last_t = t
                    
            if prelast_t == None:
                print "Uups, just one label for the whole axis? (problem!)"
    
            if xpos == None:
                xpos1, dummy = self.pos(1.0*prelast_t.num/prelast_t.denom, 47.11)
                xpos2, dummy = self.pos(1.0*last_t.num/last_t.denom, 47.11)
                xpos = pyx.unit.tocm((xpos1+xpos2)/2.0)
            else:  # xpos is from [0.0, 1.0], convert to right coords
                bb = self.bbox()
                lx = bb.left()
                rx = bb.right()
                xpos = lx+xpos*(rx-lx)
    
            #print "here we are .."
            
            # get baseline of xlabels, shift (if requested) and draw.
            #print dir(self)
            #bb = self.canvas.bbox() #
            bb = self.bbox()  # this calls finish again ===> recursion!
            #print "here we are ..1"
            baseline = bb.bottom()
            #print "here we are ..2"
            labeldist = x_ax.axis.painter.labeldist
            #print "here we are ..3"
            yshift = yshift*labeldist
            xshift = xshift*labeldist
            #print "here we are ..4"
            self.text(xpos + xshift, baseline + yshift, label,
                      [pyx.text.valign.middle, pyx.text.halign.center])
            #print "end of pyx_xlabel"
    
            
        def pyx_ylabel(self, label, ypos=None, yshift=0, xshift=0):
            """Label embedded in the y-axis labels.
    
               The yposition is determined to be half way between the last
               two tickslabels and the horizontal position is such that
               the middle is at the left edge of the bounding box for
               the graph
               
               ypos: value from [0.0,1.0]
                     (this overrides the `half way` positioning)
               xshift: optional shift in x direction
               yshift: optional shift in y direction
                        (units for both: labeldist, i.e. the distance
                         between the grph line and the right edge
                         of the ticks labels)
            """
            self.dolayout()                # all the following only works after this
            # determine position of the last two labels:
            y_ax=self.axes["y"]
            prelast_t = None
            last_t = None
            for t in y_ax.data.ticks:   # loop over all ticks
                if t.label:             # only labeled ticks have a box
                    prelast_t = last_t
                    last_t = t
                    #print "Label:", t.num, t.label
                    
            if prelast_t == None:
                print "Uups, just one label for the whole y axis?"
    
            if ypos == None:
                dummy, ypos1  = self.pos(47.11, 1.0*prelast_t.num/prelast_t.denom)
                dummy, ypos2  = self.pos(47.11, 1.0*last_t.num/last_t.denom)
                ypos = pyx.unit.tocm((ypos1+ypos2)/2.0)
            else:  # ypos is from [0.0, 1.0], convert to right coords
                bb = self.bbox()
                ly = bb.bottom()
                uy = bb.top()
                ypos = ly+ypos*(uy-ly)
    
            # get baseline of xlabels, shift (if requested) and draw.
            bb=self.bbox()
            leftline = bb.left()
            labeldist = y_ax.axis.painter.labeldist
            yshift = yshift*labeldist
            xshift = xshift*labeldist
            self.text(leftline + xshift, ypos + yshift, label,
                      [pyx.text.valign.middle, pyx.text.halign.center])

                  

##############
# FIXME: this uses pyxgraph, so definining this in pyx_objects.py
# means that these have to import pyxgraph.py.
# But pyxgraph.py imports pyx_objects.py
# Hmm, this smells like a bad design decision.
def pyxcolorbar(width=None, height=None, frame=None, pos=(0, 0),
                lut=None, minvalue=0.0, maxvalue=1.0,
                minlabel=None, maxlabel=None, border_style=None,
                orientation="vertical", position="right",
                label_dist_factor=1.0, textattrs=[]
                ):
    """ Vertical or horizontal color bar with labels at minimum and maximum.
                
      # FIXME: not all implemented here!
      orientation: "horizontal", "vertical"
                   "horizontal2", "vertical2"
           (position: "middle", "top", "bottom" (NOT IMPLEMENTED!)

      position: "left", "right", "middle": 

      
      minvalue/maxvalue: "%g" % value

      
      frame: if not None, pos=(posx, posy) are relative coordinates
      pos=(posx, posy): absolute or relative (i.e from [0.0,1.0]
      coordinates for the place of the lower left corner (CHECK!)
      of the color bar.

      vertical
      --------

      Here we have::
      
        ypos+height ........
                      max      >
                               >  delta_o 
                    +------+
                    |      |
                    .      .
                    .      .
                    .      .
                    |      |
                    +------+
                               >
                       0       >  delta_u
        ypos        ........

      vertical2
      ---------

      Here::
      
                      max      >
                               >  delta_o 
        ypos+height +------+
                    |      |
                    .      .
                    .      .
                    .      .
                    |      |
        ypos        +------+
                               >
                       0       >  delta_u
           s        ........


      horizontal
      ----------
      
      Here::

            delta_l                delta_r

           
           .    +---- .... ------+    .
           .min |                | max.
           .    +---- .... ------+    .

           |                     | 
           xpos                  xpos+width
 
        # At each end we have to determine the height of the label and
        # add a bit as white space.
        # At each end we have to determine the width of the label
        # add a bit as white space.  (FIXME!!!)

    """
    if position not in ["right", "middle", "left"]:
        raise ValueError("invalid  `position`: <%s>" % position)
    if orientation not in ["vertical", "vertical2",
                           "horizontal", "horizontal2"]:
        raise ValueError("invalid `orientation`: <%s>" % orientation)

    if orientation in ["vertical", "vertical2"]:
        if width is None:
            width = 1
        if height is None:
            height = 3
    else:
        if width is None:
            width = 3
        if height is None:
            height = 1

    #print "ORIENT:", orientation, width, height
        

    def minmaxlabel(label, value):
        """Shorthand to determine the text at the colorbar"""
        if type(label) is types.StringType:
            txt = label
        else:
            if value != None:
                txt = "%g" % value
            else:
                txt = "%g" % 47.11
        return txt

    mintxt = minmaxlabel(minlabel, minvalue)
    maxtxt = minmaxlabel(maxlabel, maxvalue)

    # for position == "middle"  we need to know the height
    # of the resulting text:
    #
    # delta_u(nten) and delta_o(ben) determe the lower and upper
    # distance of the colorbar from the upper and lower edge
    # determine by the y component of `pos` and `height`.

    # --- determine size of an "O" and labels
    tO =  pyx.text.text(0, 0, "O", textattrs=textattrs)
    delta_u, delta_o = 0, 0  # offsets for vertical orientation
    delta_l, delta_r = 0, 0  # offsets for horizontal orientation

    if orientation=="vertical" and position == "middle":
        tu = pyx.text.text(0, 0, mintxt, textattrs=textattrs)
        #delta_u = tu.height+0.5*tO.height
        delta_u = tu.height+0.75*tO.height*label_dist_factor
        to = pyx.text.text(0, 0, maxtxt, textattrs=textattrs)
        #delta_o = to.height+0.5*tO.height
        delta_o = to.height+0.5*tO.height*label_dist_factor

    if orientation=="horizontal" and position == "middle":
        tl = pyx.text.text(0, 0, mintxt, textattrs=textattrs)
        delta_l = tl.width-tO.width
        tr = pyx.text.text(0, 0, maxtxt, textattrs=textattrs)
        delta_r = tr.width
        
    Nq, Np = 2, 256
    colbararr = transpose((Np-arange(Np)) * ones((Nq, Np), "d"))
    if orientation in ["horizontal", "horizontal2"]:
        colbararr = arange(Np) * ones((Nq, Np), "d")

    # If possible pos is in relative coordinates in the
    # frame into which this stuff should go ....
    xpos, ypos = pos[0], pos[1]
    if frame is not None:
        xpos = frame.xpos+pos[0]*frame.width
        ypos = frame.ypos+pos[1]*frame.height

    if border_style is None:
        border_style = [pyx.style.linewidth.normal]
       
    border_painter = pyx.graph.axis.painter.regular(
        basepathattrs=border_style)
    ax = pyx.graph.axis.linear(min=0, max=1, painter=border_painter,
                               parter=None)

    if orientation == "vertical":   # labels are within the box
        gr = pyxgraph(xpos=xpos, ypos=ypos+delta_u, width=width, key=False,
                      height=height-delta_u-delta_o,
                      xaxistype=ax, yaxistype=ax, x2axistype=ax, y2axistype=ax)
    if orientation == "vertical2": 
        gr = pyxgraph(xpos=xpos, ypos=ypos+delta_u, width=width, key=False,
                      height=height-delta_u-delta_o,
                      xaxistype=ax, yaxistype=ax, x2axistype=ax, y2axistype=ax)
    elif orientation == "horizontal": # labels are within the box
        gr = pyxgraph(xpos=xpos+delta_l, ypos=ypos,
                      width=width-delta_l-delta_r, key=False,
                      height=height,
                      xaxistype=ax, yaxistype=ax, x2axistype=ax, y2axistype=ax)
    elif orientation == "horizontal2":
        gr = pyxgraph(xpos=xpos+delta_l, ypos=ypos,
                      width=width-delta_l-delta_r, key=False,
                      height=height,
                      xaxistype=ax, yaxistype=ax, x2axistype=ax, y2axistype=ax)

    pilbitmap = ColMapper.Array2PIL(colbararr, lut=lut, minvalue=minvalue,
                                    maxvalue=maxvalue)
    gr.pyxbitmap(pilbitmap)
    gr.finish()

    # Get coordinates
    x0, y0 = gr.pos(0.0, 0.0)
    x1, y1 = gr.pos(1.0, 1.0)

    # add tick-lines
    if position == "right":
        delta = 0.25
        for ypos in [y0, y1]:
            gr.stroke(pyx.path.line(x1, ypos, x1+delta, ypos), border_style)

    if position == "left":
        delta = 0.25
        for ypos in [y0, y1]:
            gr.stroke(pyx.path.line(x0, ypos, x0-delta, ypos), border_style)

    #if position == "top":
    #    raise NotImplementedError("your help is needed here")
    #if position == "bottom":
    #    raise NotImplementedError("your help is needed here")


    # --- add labels
    if orientation in ["vertical", "vertical2"] :
        if position == "right":
            gr.text(x1+1.2*delta, y0, mintxt, [pyx.text.valign.middle]+textattrs)
            gr.text(x1+1.2*delta, y1, maxtxt, [pyx.text.valign.middle]+textattrs)
            #pyx.text.vshift(-0.25)])
        elif position == "left":
            gr.text(x0-1.2*delta, y0, mintxt, [pyx.text.valign.middle,
                                               pyx.text.halign.right]+textattrs)
            gr.text(x0-1.2*delta, y1, maxtxt, [pyx.text.valign.middle,
                                               pyx.text.halign.right]+textattrs)
            #pyx.text.vshift(-0.25)])
        elif position == "middle":
            if orientation == "vertical":
                gr.text((x0+x1)/2.0, ypos, mintxt, [pyx.text.valign.bottom,
                                                    pyx.text.halign.center]+textattrs)
                gr.text((x0+x1)/2.0, ypos+height, maxtxt,
                        [pyx.text.valign.top, pyx.text.halign.center]+textattrs)
            else:
                gr.text((x0+x1)/2.0, ypos-0.75*tO.height*label_dist_factor,
                        mintxt, [pyx.text.valign.top, pyx.text.halign.center]+textattrs)
                gr.text((x0+x1)/2.0,
                        ypos+height+0.5*tO.height*label_dist_factor, maxtxt,
                        [pyx.text.valign.bottom, pyx.text.halign.center]+textattrs)
                
    else:  # orientation in ["horizontal", "horizontal2":
        if position == "right":
            print "right: NotImplementedErorr"
            #raise NotImplementedErorr("your help is needed here")
        elif position == "left":
            print "left: NotImplementedErorr"
            #raise NotImplementedErorr("your help is needed here")
        elif position == "middle":
            if orientation == "horizontal":
                gr.text(x0-delta_l, (y0+y1)/2.0, mintxt,
                        [pyx.text.valign.middle, pyx.text.halign.right]+textattrs)
                gr.text(x1+delta_r, (y0+y1)/2.0, maxtxt,
                        [pyx.text.valign.middle, pyx.text.halign.right]+textattrs)
            else:
                gr.text(x0-delta_l-tO.width*label_dist_factor,
                        (y0+y1)/2.0, mintxt,
                        [pyx.text.valign.middle, pyx.text.halign.right]+textattrs)
                gr.text(x1+delta_r+tO.width*label_dist_factor,
                        (y0+y1)/2.0, maxtxt,
                        [pyx.text.valign.middle, pyx.text.halign.left]+textattrs)
                
    return gr

