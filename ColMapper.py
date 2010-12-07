"""General color mapper.

FIXME: FIXMEs
FIXME: docu
FIXME: style (try pylint ;-)
FIXME: example of colormaps for the examples ....
FIXME: do alpha stuff properly
FIXME: interface with MPL color maps: use: ColorMapsMatplotlib.py
FIXME: segmented color maps

For the graphical representation of some function f(x,y)
there are different possibilities.
One of the simplest is a 2D false color plot
where one associates with
each value of the range of f a shade of grey ranging from white to black.
In addition one might have a nonlinear scaling
in this association.

Even more pronounced effects can be obtained by arbitrary
associations of
  z\in[0,1] \to (r, g, b)
This is the purpose of this color mapper.
Note: use this with caution!!

In particular, a result might look nice on screen,
but when printed in black-and-white, the color scale might
be just one shade of grey, i.e. essentially useless
Many people don't have access to color printers, or will
print out your picture/paper without color anyway!.

In all cases when using such a color map, a corresponding
color-bar should be shown. Everything else is quite a bit of
cheating IMHO!



FIXME: adapt documentation here:

Some of the color maps below ...


-------------------------



   Variant which creates three arrays of length 256
   corresponding to the r,g,b values


   

   In addition a short routine to convert an array to a PIL image
   is provided.


   Some good color scales:

   white-blue-black:   -36,-36,-9
                    or -36,-36,-8
                    or -36,-36,-7
   

   WANTED: white to black via yellow-red   or yellow-green-blue
   (We might need the brightness for a grey scale interpretation
   of rgb colors ...)


   TODO:
     - add rgba mappings (for mayavi and matplotlib)
     - import and export of mayavi type color mappings
     - import and export of grad-files (mayavi, Create LUT)



   Version 0.0.2, 29.10.2003
   Version 0.0.3, 08.06.2004
   Version 0.0.4, 09.04.2005: support for normalized rgb triples
                              (for matplotlib)

   Version 0.0.5, 13.04.2006: conversion to numpy



Note: very interesting document on colors is:
  http://www.tug.org/tex-archive/macros/latex/contrib/xcolor/xcolor.pdf

   
"""

__author__ = "Arnd Baecker"


import os    
import numpy
#from math import *  # do we need this ?

DEG2RAD = numpy.pi/180.0

def pm3d_formula(x, formula):
    """Map the value `x` from [0, 1] according to `formula` to [0, 1]

       The formulae are taken from Peter Mikulik's pm3d from gnuplot.
       
    """
    
    if formula<0:		   # inverted range
	x = 1.0-x
	formula = -formula

    if formula==0: return 0
    elif formula==1: return 0.5
    elif formula==2: return 1
    elif formula==3: return x
    elif formula==4: return x*x
    elif formula==5: return x**3
    elif formula==6: return x**4
    elif formula==7: return numpy.sqrt(x)
    elif formula==8: return x**0.25
    elif formula==9: return numpy.sin(90.0*x*DEG2RAD)
    elif formula==10: return numpy.cos(90*x*DEG2RAD)
    elif formula==11: return numpy.fabs(x - 0.5)
    elif formula==12: return (2*x - 1)*(2.0*x - 1)
    elif formula==13: return numpy.sin(180*x*DEG2RAD)
    elif formula==14: return numpy.fabs(cos(180*x*DEG2RAD))
    elif formula==15: return numpy.sin(360*x*DEG2RAD)
    elif formula==16: return numpy.cos(360*x*DEG2RAD)
    elif formula==17: return numpy.fabs(numpy.sin(360*x*DEG2RAD))
    elif formula==18: return numpy.fabs(numpy.cos(360*x*DEG2RAD))
    elif formula==19: return numpy.fabs(numpy.sin(720*x*DEG2RAD))
    elif formula==20: return numpy.fabs(numpy.cos(720*x*DEG2RAD))
    elif formula==21: return 3*x
    elif formula==22: return 3*x - 1
    elif formula==23: return 3*x - 2
    elif formula==24: return numpy.fabs(3*x - 1)
    elif formula==25: return numpy.fabs(3*x - 2)
    elif formula==26: return (1.5*x - 0.5)
    elif formula==27: return (1.5*x - 1)
    elif formula==28: return numpy.fabs(1.5*x - 0.5)
    elif formula==29: return numpy.fabs(1.5*x - 1)
    elif formula==30:
        if x<=0.25: return 0.0
        if x>=0.57: return 1.0
	return x/0.32 - 0.78125
    elif formula==31:
        if x <= 0.42: return 0.0
        if x >= 0.92: return 1.0
	return 2*x - 0.84
    elif formula==32:
        if x <= 0.42: return 4*x
        if x <= 0.92:  return -2*x + 1.84
        return x/0.08 - 11.5
    elif formula==33: return numpy.fabs(2*x) - 0.5
    elif formula==34: return 2*x
    elif formula==35: return 2*x - 0.5
    elif formula==36: return 2*x - 1
    return 0.0



class ColorMapper(object):
    """Define rgb color-mapping function

       Usage::
       
         import ColorMapper
         colmap = ColorMapper.ColorMapper("typus", <parameter>)
         # get r, g, b associated with z
         r, g, b = colmap.colfct(z)

       where z\in[0,1].

       FIXME: use different one than pm3d:
       Concrete example::
       
         import ColorMapper
         colmap = ColorMapper.ColorMapper("pm3d", pm3d=[7,5,15])
         r, g, b = colmap.colfct(z)
       
       """
    def __init__(self, typus, widths=[0.4, 0.4, 0.4], gausspos=[0.0, 0.5, 1.0],
                 exponent=1.0, invert=0,
                 hls_l=0.5, hls_s=1.0, hls_hls=0,
                 pm3d=[7, 5, 15],
                 brightness=0.0,
                 lutfile=None):
        self.widths = widths
        self.exponent = exponent
        self.invert = invert
        self.hls_l = hls_l
        self.hls_s = hls_s
        self.hls_hls = hls_hls
        self.pm3d = pm3d
        self.gausspos = gausspos
        self.brightness = brightness
        
        functions = {"gauss": self._gauss_color,
                     "hls": self._hls2rgb,
                     "pm3d": self._pm3d,
                     "red": self._red,
                     "red2": self._red2,
                     "green": self._green,
                     "blue": self._blue,
                     "blue2": self._blue2,
                     "yellow-red": self._yellow_red,
                     "yellow-blue": self._yellow_blue,
                     "white-yellow-red-black": self._white_yellow_red_black,
                     "yellow-green-blue-red": self._yellow_green_blue_red,
                     #"lut": self._vtk_lut
                     }
                         
        try:
            self.colfct = functions[typus]  #.replace("-","_")]
        except KeyError:
            print "Please supply a correct color mapper instead of <%s>" % typus
            print "Now we use a gauss as default"
            print "Possible values are:",
            for key in functions.keys():
                print key,
            print
            self.colfct = self._gauss_color

        # FIXME: self.colfct is a function which associates
        # FIXME: any value from [0.0, 1.0] an rgb triplet.
        # FIXME: Is this description correct?

        if typus == "lut":
            if self.lutfile is None:
                print "Please supply a LUT file"
            else:
                self._initialize_from_lutfile(self.lutfile)



    def _initialize_from_lutfile(self,lutfile):
        """Load a rgba lookup tabel from a vtk lut file"""
        fp = open(lutfile, "r")
        #parse: LOOKUP_TABLE ./luts/pm3d_24.lut 256
        firstline = fp.readline()
        anz = firstline.split()[2]
        
        r, g, b, alpha = (numpy.zeros(anz, dtype=numpy.Float),
                          numpy.zeros(anz, dtype=numpy.Float),
                          numpy.zeros(anz, dtype=numpy.Float),
                          numpy.zeros(anz, dtype=numpy.Float))
        for i in xrange(anz):
            zeile = fp.readline()
            rgba = zeile.split()
            r[i] = float(rgba[0])
            g[i] = float(rgba[1])
            b[i] = float(rgba[2])
            if len(rgba)==4:
                alpha[i] = float(rgba[3])
            else:
                alpha[i] = 1.0
        fp.close()
        
        self.r = r
        self.g = g
        self.b = b
        self.alpha = alpha



    def write_vtk_lutfile(self,lutfile):
        """Write a vtk lutfile from the current lookup table"""
        fp = open(lutfile, "w")
        lutfile_ = os.path.split(lutfile)[1]

        r, g, b, alpha = self.generate_normalized_rgba()

        fp.write("LOOKUP_TABLE %s %d" % (lutfile_, len(r)))    
        for i in xrange(len(r)):
            fp.write("%5.4f %5.4f %5.4f %5.4f\n" % (r[i], g[i], b[i], alpha[i]))
        fp.close()

        
    def generate_lut(self, N=256):
        """Return triple of rgb arrays with values in [0, N-1]. """
        r, g, b = (numpy.zeros(N), numpy.zeros(N), numpy.zeros(N))
        N_ = N - 1.0
        for i in xrange(N):
               r_, g_, b_ = self.colfct(i/N_) # these are from [0,1]
               r[i], g[i], b[i] = int(N_*r_), int(N_*g_), int(N_*b_)
        return r, g, b


    def generate_lutalpha(self, N=256):
        """Return triple of rgba arrays with values in [0, N-1]. """
        r, g, b, alpha = (numpy.zeros(N), numpy.zeros(N), numpy.zeros(N),
                          numpy.zeros(N))
        N_ = N - 1.0
        for i in xrange(N):
            r_, g_, b_, alpha_ = self.colfctalpha(i/N_) #  from [0,1]
            r[i], g[i], b[i], alpha[i] = (int(N_*r_), int(N_*g_),
                                          int(N_*b_), int(N_*alpha_))
        return r, g, b, alpha



    def generate_normalized_rgb(self, N=256):
        """Return normalized, [0.0,1.0], triple of rgb arrays."""
        r, g, b = (numpy.zeros(N), numpy.zeros(N), numpy.zeros(N))
        N_ = N - 1.0
        for i in xrange(N):
            r_, g_, b_ = self.colfct(i/N_) # these are from [0,1]
            r[i], g[i], b[i] = int(N_*r_), int(N_*g_), int(N_*b_)
        return 1.0*r/N, 1.0*g/N, 1.0*b/N
        

    def generate_normalized_rgba(self, N=256):
        """Return normalized, [0.0, 1.0] 4-uple of rgba arrays."""
        
        r, g, b, alpha = (numpy.zeros(N), numpy.zeros(N),
                          numpy.zeros(N), numpy.zeros(N))
        N_ = N - 1.0
        for i in xrange(N):
            r_, g_, b_, alpha_ = self.colfctalpha(i/N_) # these are from [0,1]
            r[i], g[i], b[i], alpha[i] = (int(N_*r_), int(N_*g_),
                                          int(N_*b_), int(N_*alpha_))
        return 1.0*r/N, 1.0*g/N, 1.0*b/N, 1.0*alpha/N


              
##    def generate_lut(self):
##        r,g,b = (zeros(256),zeros(256),zeros(256)
##        for x in numpy.arange(256)
               
##               r,g,b = self.colfct(x/255.0) # these are from [0,1]
##        print r,g,b
##        r = numpy.where(r>0,r,0*r)
##        g = numpy.where(g>0,g,0*g)
##        b = numpy.where(b>0,b,0*b)
##        r = numpy.where(r>1,0*r,r)
##        g = numpy.where(g>1,0*g,g)
##        b = numpy.where(b>1,0*b,b)
##        return (255.0*r).astype(numpy.UInt8),
##               (255.0*g).astype(numpy.UInt8),
##               (255.0*b).astype(numpy.UInt8))        
            
 
    def _gauss(self, x, x0, sigma):      
        return numpy.exp(-(x-x0)*(x-x0)/(2.0*sigma*sigma))


    def _gauss_color(self, x):
        if self.invert: x = 1.0-x
        x = x**self.exponent
        return (self._gauss(x, self.gausspos[0], self.widths[0]),
                self._gauss(x, self.gausspos[1], self.widths[1]),
                self._gauss(x, self.gausspos[2], self.widths[2]))


    # FIXME: what does this routine return?
    def normalize(self, rgb):
        """Normalize an rgb triplet to the 0,1 range"""
        rgb  =  numpy.array(rgb)
        return numpy.clip(rgb, 0.0, 1.0).tolist()
 

    def _pm3d(self, x):
        if self.invert: x = 1.0-x
        x = x**self.exponent

        return self.normalize([pm3d_formula(x, self.pm3d[0]),
                               pm3d_formula(x, self.pm3d[1]),
                               pm3d_formula(x, self.pm3d[2]) ])


    def _red(self, x):
        """self.brightness: determines the end color.
           Starting from (r,g,b) = (1,1,1) we go to
                         (r,g,b) = (1-self.brightness,0,0)

           self.brightness = 0.2 means darker.
        """
    
        if self.invert: x = 1.0-x
        x = x**self.exponent
        return 1.0-x*self.brightness, 1.0-x, 1.0-x

    def _red2(self, x):
        """red to black"""
        if self.invert: x = 1.0-x
        x = x**self.exponent
        return x*(1.0-self.brightness), 0.0, 0.0

    def _green(self, x):
        if self.invert: x = 1.0-x
        x = x**self.exponent
        return 1.0-x, 1.0-x*self.brightness, 1.0-x


    def _blue(self, x):
        if self.invert: x = 1.0-x
        x = x**self.exponent
        return 1.0-x, 1.0-x, 1.0-x*self.brightness
        
    def _blue2(self, x):
        if self.invert: x = 1.0-x
        x = x**self.exponent
        return 0.0, 0.0, x*(1.0-self.brightness)


    def _yellow_red(self, x):
        if self.invert: x = 1.0-x
        x = x**self.exponent
        return 1.0, 1.0-x, self.brightness*(1.0-x)


    def _yellow_green(self, x):
        if self.invert: x = 1.0-x
        x = x**self.exponent        
        return 1.0-x, 1.0, self.brightness*(1.0-x)


    def _yellow_blue(self, x):
        # FIXME: we don't have this !!!!
        if self.invert: x = 1.0-x
        x = x**self.exponent        
        return 1.0-x**1.5, 1.0-x**1.5, x


    def  __white_yellow_red_black1(self, x):
        if self.invert: x = 1.0-x
        x = x**self.exponent
        if x<0.5:
            b = 0.0
        else:
            b = (x-0.5)*2.0

        if x<0.25:
            g = 0.0
        elif x<0.75:
            g = (x-0.25)*2.0
        else:
            g = 1.0

        if x>0.5:
            r = 1.0
        else:
            r = x*2.0

        return r, g, b
       
        
    def  __white_yellow_red_black(self, x):
        if self.invert: x = 1.0-x
        x = x**self.exponent
        if x<0.5:
            b = 0.0
        else:
            b = (x-0.5)*2.0

        if x<0.15:
            g = 0.0
        elif x<0.75:
            g = (x-0.15)/(0.75-0.15)
        else:
            g = 1.0

        if x>0.3:
            r = 1.0
        else:
            r = x/0.3

        return r, g, b



    def _white_yellow_red_black(self, x):
        tmp_fkt = numpy.vectorize(self.__white_yellow_red_black)
        return tmp_fkt(x) 


    def _yellow_green_blue_red(self, x):
        if self.invert: x = 1.0-x
        x = x**self.exponent
        w = 0.15
        return (self._gauss(x, 0.0, w) + self._gauss(x, 1.0, w*1.4),
                (self._gauss(x, 0.0, w) + self._gauss(x, 0.3333, w))/1.1137,
                self._gauss(x, 0.6, w/1.1))
        

    def _pm3d2(self, x):
        if self.invert: x = 1.0-x
        x = x**self.exponent        
        return x**0.35, x**0.5, x**0.8


    def _hls2rgb(self, h):
        """
        We use a rescaled h \in [0,1]

        h von 0 .. 360 

       letztes argument ist ein flag 0 oder 1, der entscheided ob
       die gruenen farben noch staerker auseinandergezogen werden,
       da wir gruen so gut sehen koennen.
       sonst: l  =  0.5, s = 1 ist meist sinnvoll,
                    l = 0: schwarz, l=1 weiss, s: saettigung

        """
        h = h**self.exponent
        if self.invert: h = 1.0-h
        h = h*360.0
        h = numpy.fmod(h, 360.0)
        if self.hls_hls:
            h = h/60.0
        else:
            if h<120:
                h = h/120.0       #    /* 0..1 Rot..(Orange)..Gelb */
            elif h<180:
                h = h/60.0 - 1.0  #     /* 1..2 Gelb..Gruen */
            elif h<240:
                h = h/30.0 - 4.0  #      /* 2..4 Gruen..Blaugruen..Blau*/
            else:
                h = h/60.0        #     /* 4..6 Blau..Purpur..Rot */
        c = int(h)
        frac = h-c
        if self.hls_l<= 0.5:
            maxi = self.hls_l*(1.0+self.hls_s)
        else:
            maxi = self.hls_l+self.hls_s-self.hls_l*self.hls_s
        mini = 2*self.hls_l-maxi;
        diff = maxi-mini;
        if self.hls_s==0:            #                            /* grau */
            return 1.0, 1.0, 1.0
        else:
            if c==0:
                return maxi,mini+frac*diff,mini
            elif c==1:
                return mini+(1.0-frac)*diff,maxi,mini
            elif c==2:
                return mini,maxi,mini+frac*diff
            elif c==3:
                return mini,mini+(1.0-frac)*diff,maxi
            elif c==4:
                return mini+frac*diff,mini,maxi
            else:
                return maxi,mini,mini+(1.0-frac)*diff


### FIXME: no plot routines within here IMHO
##    def plotpm3d(self):
##        x=numpy.arange(0,1.0,0.01)
##        #qqscipy.xplt.window()
##        #qscipy.xplt.limits(0.0,0.0,1.0,1.0)
##        #scipy.xplt.hold("on")
##        scipy.xplt.plg(pm3d_formula(x,self.pm3d[0]),x,color=-5)
##        scipy.xplt.plg(pm3d_formula(x,self.pm3d[1]),x,color=-4)
##        scipy.xplt.plg(pm3d_formula(x,self.pm3d[2]),x,color=-3)
##        #scipy.xplt.plg(numpy.sin(x),x)
##        #print x,numpy.sin(x)
##        #scipy.xplt.pause(1)




# FIXME: this syntax should be adapapted to be array2pil,
# or even array_to_pil() or array_to_image()
#
def Array2PIL(a, lut=None, minvalue=None, maxvalue=None,
              width=None, height=None, flip=None):
    """Convert 2D array `a` to a python image library (PIL) bitmap.

       what about width,height?????

       - flip:  None: no flip
                "ud": up-down exchange

    """
    import Image   # we only need it here ...

    if flip=="ud":  #up-down exchange
        a = a[::-1,:]
    if len(a.shape)!=2:
        raise ValueError("Array2PIL needs array with shape=2")
    
    h, w =numpy.shape(a)
##    a_min=numpy.minimum.reduce((numpy.ravel(a)))
##    a_max=numpy.maximum.reduce((numpy.ravel(a)))
    a_min = min(numpy.ravel(a))
    a_max = max(numpy.ravel(a))

    # allow for an user-specified maximal value:
    # if maxvalue is not None and maxvalue>a_max:
    # WJH 17 Sep 2010 - allow setting max that is less than highest data value
    if maxvalue is not None:
        a_max = maxvalue
    # allows for an user-specified minimal value:
    # if minvalue is not None and minvalue<a_min:
    # WJH 17 Sep 2010 - allow setting min that is greater than lowest data value
    if minvalue is not None:
        a_min =  minvalue

    # We should clip all values:    
    # WJH 17 Sep 2010 - fixed to do in-place clip
    a.clip(min=a_min, max=a_max, out=a)
    
    mode = "RGB"
    if lut is not None:
        if len(lut[0]) == 256:
            
            a = (numpy.ravel(255.0*(a-a_min)/
                             (a_max-a_min))).astype(numpy.uint8)

            rgb = numpy.zeros( (len(a),3),dtype=numpy.uint8)

            lut_ = numpy.zeros( (3,len(lut[0])),numpy.uint8)
            lut_[0] = lut[0].astype(numpy.uint8)
            lut_[1] = lut[1].astype(numpy.uint8)
            lut_[2] = lut[2].astype(numpy.uint8)

            # This is much faster than the original zip/ravel variant ...
            rgb[:,0]=numpy.take(lut_[0],a)
            #print "rtake"
            rgb[:,1] = numpy.take(lut_[1],a)
            #print "gtake"
            rgb[:,2] = numpy.take(lut_[2],a)
            #print "btake"
            #rgb = numpy.ravel(((numpy.array(zip(r,g,b),
            #                                  dtype=numpy.uint8))))

            #print "rgb done"
        else:
            N =  len(lut[0])
            print "LUT with N=%d entries" % N
            if N>=256*256:
                print "UUPS, more than uint16 colors??", N
                raise ValueError("N too large")
                
            a = (numpy.ravel((N-1)*(a-a_min)/
                             (a_max-a_min))).astype(numpy.uint16)

            rgb = numpy.zeros( (len(a), 3), dtype=numpy.uint16)

            lut_ = numpy.zeros( (3,len(lut[0])),numpy.uint16)
            lut_[0] = lut[0].astype(numpy.uint16)
            lut_[1] = lut[1].astype(numpy.uint16)
            lut_[2] = lut[2].astype(numpy.uint16)

            # This is much faster than the original zip/ravel variant ...
            rgb[:,0] = numpy.take(lut_[0],a)
            rgb[:,1] = numpy.take(lut_[1],a)
            rgb[:,2] = numpy.take(lut_[2],a)

            rgb = (rgb*256.0/N).astype(numpy.uint8)

    else:  # simple grey scale ramp...
        a = (numpy.ravel(255.0*(a-a_min)/
                         (a_max-a_min))).astype(numpy.uint8)
        # convert to (r_0,g_0,b_0,r_1,g_1,b_1,....)
        rgb = numpy.ravel(numpy.array(zip(a,a,a)))
        
    # create a PIL RGB image
    im = Image.new("RGB", (w,h))
    im.fromstring(rgb.tostring())

    
   
    # scale image and keep aspect ratio if either width or height is given
    if height is not None and width is None:
        im = im.resize(w/h*height, height)
    elif height is None and width is not None:
        im = im.resize(width, h/w*width)
    elif height is not None and width is not None:
        im = im.resize(width, height)

    return im


class SegmentedColorMapping(object):
    """Class of color mapping with different
       color functions on defined intervals (segments)."""
       
    def __init__(self, colmaps, min_value, max_value):
        """colmaps is a list of triples (min, max, colmap),
           where [min, max] defines the interval on which
           colmap is active
           
           min_value: minimal value of plotted 2d-array 
           max_value: maximal value of plotted 2d-array 
        """
       
        self.colmaps = colmaps
        self.anz_seg = len(self.colmaps)
               
        self.xmin = []
        self.xmax = []
        self.colmap = []
        
        # min_value being smaller than the smallest min value
        # of a segment is not allowed (same for max_value)
        if min_value < self.colmaps[0][0]:
            min_value = self.colmaps[0][0]
        
        if max_value > self.colmaps[self.anz_seg-1][1]:
            max_value = self.colmaps[self.anz_seg-1][1]
       
        # scale segment borders to interval [0,1]
        for i in xrange(self.anz_seg):
            x = colmaps[i][0]
            self.xmin.append((x-min_value)/(max_value-min_value))
            
            x = colmaps[i][1]
            self.xmax.append((x-min_value)/(max_value-min_value))
            
            self.colmap.append(colmaps[i][2])
        
        print self.xmin, self.xmax          
                        
    def colfct(self, x):
        """Return rgb(a?) triple for  x in [0,1]"""
        for i in xrange(self.anz_seg):
            # find interval which contains x
            if self.xmin[i]<=x<=self.xmax[i]:
                # normalize to [0, 1]
                x = (x-self.xmin[i])/(self.xmax[i]-self.xmin[i])
                return self.colmap[i].colfct(x)
        print "no interval found for x=%e - should not happen" % x
        return 0.0
        
    def generate_lut(self, N=256):
        """Return triple of rgb arrays with values in [0, N-1]. """
        r, g, b = (numpy.zeros(N), numpy.zeros(N), numpy.zeros(N))
        N_ = N - 1.0
        for i in xrange(N):
               r_, g_, b_ = self.colfct(i/N_) # these are from [0,1]
               r[i], g[i], b[i] = int(N_*r_), int(N_*g_), int(N_*b_)
        return r, g, b


def example_SegmentedColorMapping(min_value, max_value):
    """example of color mapper with four different color functions
       in an interval [-4,4]"""
    
    colmap1 = ColorMapper("red2")
    colmap1.exponent = 0.7
    
    colmap2 = ColorMapper("green")
    
    colmap3 = ColorMapper("green")
    colmap3.invert = True
    
    colmap4 = ColorMapper("blue2")
    colmap4.invert = True
    colmap4.exponent = 0.5
    
    colmap = SegmentedColorMapping([ (-4.0, -2.0, colmap1), (-2.0, 0.0, colmap2),
                                     (0.0, 2.0, colmap3), (2.0, 4.0, colmap4)],
                                     min_value, max_value)
                                    
    return colmap
    

################################################################################
## Test routines
################################################################################
def get_one_PIL(colmap, fname=None, Nx=255):
    """Simple test routine to get color-bar for the colormapper `colmap`.

       If a filename `fname` is provided, the image is written
       as JPEG file.
    """
       
    import Image
    Ny = 50
    im = Image.new("RGB", (Nx, Ny))
    for nx in range(Nx):
        z = nx/(Nx-1.0)
        r,g,b = colmap.colfct(z)
        r = int(255*r)
        g = int(255*g)
        b = int(255*b)
        for ny in range(Ny):
            im.putpixel((nx,ny),(r,g,b))
    if fname:
        print "saving:", fname+".jpg"
        im.save(fname+".jpg", "JPEG")
        im.save(fname+".png", "PNG")
    ## im.show()
    return im



    
def test_several():
    colmap = ColorMapper("hls",hls_l=0.45,hls_s=0.5)   # gauss")
    get_one_PIL(colmap, "hls")
    colmap = ColorMapper("pm3d")
    get_one_PIL(colmap, "pm3d_1")
    colmap = ColorMapper("pm3d",pm3d=[30,31,32])
    get_one_PIL(colmap, "pm3d_2")
    colmap = ColorMapper("pm3d",pm3d=[7,-11,32])
    get_one_PIL(colmap, "pm3d_3")
    colmap = ColorMapper("pm3d",pm3d=[7,5,15])
    get_one_PIL(colmap, "pm3d_4")
    colmap = ColorMapper("pm3d",pm3d=[-36,-36,-34],invert=0,exponent=0.75)
    get_one_PIL(colmap, "pm3d_5")
    colmap = ColorMapper("red",invert=1,exponent=0.25)
    get_one_PIL(colmap, "red")
    colmap = ColorMapper("blue")
    get_one_PIL(colmap, "blue")
    colmap=ColorMapper("green",invert = 1,exponent=0.25,brightness=0.6)
    get_one_PIL(colmap, "green")
       
    colmap = example_SegmentedColorMapping(-4.0,4.0)                                    
    get_one_PIL(colmap, "segmented")


if __name__ == "__main__":
    test_several()
