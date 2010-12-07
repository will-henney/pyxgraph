#!/usr/bin/env python
"""
   General color mapper.

   



   Variant which creates three arrays of length 256
   corresponding to the r,g,b values
   
   Version 0.0.2, 29.10.2003
   Version 0.0.3, 08.06.2004
   Version 0.0.4, 09.04.2005: support for normalized rgb triples
                              (for matplotlib)


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
   
"""

__author__="Arnd Baecker"


import scipy    # maybe we could use the normal math gauss here ???

import Numeric

from math import *
import os    


DEG2RAD= (Numeric.pi / 180.0)

def pm3d_formula(x,formula):
    """   the input gray x is supposed to be in interval [0,1] """
    
    if(formula<0):		
	x=1.0-x
	formula=-formula

    if(formula==0): return 0
    elif(formula==1): return 0.5
    elif(formula==2): return 1
    elif(formula==3): return x
    elif(formula==4): return(x * x)
    elif(formula==5): return(x * x * x)
    elif(formula==6): return(x * x * x * x)
    elif(formula==7): return(Numeric.sqrt(x))
    elif(formula==8): return(x**0.25)
    elif(formula==9): return(Numeric.sin(90.0 * x * DEG2RAD))
    elif(formula==10): return(Numeric.cos(90 * x * DEG2RAD))
    elif(formula==11): return(Numeric.fabs(x - 0.5))
    elif(formula==12): return((2 * x - 1) * (2.0 * x - 1))
    elif(formula==13): return(Numeric.sin(180 * x * DEG2RAD))
    elif(formula==14): return(Numeric.fabs(cos(180 * x * DEG2RAD)))
    elif(formula==15): return(Numeric.sin(360 * x * DEG2RAD))
    elif(formula==16): return(Numeric.cos(360 * x * DEG2RAD))
    elif(formula==17): return(Numeric.fabs(Numeric.sin(360 * x * DEG2RAD)))
    elif(formula==18): return(Numeric.fabs(Numeric.cos(360 * x * DEG2RAD)))
    elif(formula==19): return(Numeric.fabs(Numeric.sin(720 * x * DEG2RAD)))
    elif(formula==20): return(Numeric.fabs(Numeric.cos(720 * x * DEG2RAD)))
    elif(formula==21): return(3 * x)           # ???????
    elif(formula==22): return(3 * x - 1)
    elif(formula==23): return(3 * x - 2)
    elif(formula==24): return(Numeric.fabs(3 * x - 1))
    elif(formula==25): return(Numeric.fabs(3 * x - 2))
    elif(formula==26): return((1.5 * x - 0.5))
    elif(formula==27): return((1.5 * x - 1))
    elif(formula==28): return(Numeric.fabs(1.5 * x - 0.5))
    elif(formula==29): return(Numeric.fabs(1.5 * x - 1))
    elif(formula==30):
        if (x <= 0.25): return 0.0
        if (x >= 0.57): return 1.0
	return(x / 0.32 - 0.78125)
    elif(formula==31):
        if (x <= 0.42): return 0.0
        if (x >= 0.92): return 1.0
	return(2 * x - 0.84)
    elif(formula==32):
        if (x <= 0.42): return(4*x)
        if (x <= 0.92):  return(-2 * x + 1.84)
        return(x / 0.08 - 11.5)
    elif(formula==33): return(Numeric.fabs(2 * x - 0.5))
    elif(formula==34): return(2 * x)
    elif(formula==35): return(2 * x - 0.5)
    elif(formula==36): return(2 * x - 1)
    return(0)







class ColorMapper:
    """Define rgb color-mapping function

       Usage:
       import ColorMapper
       colmap=ColorMapper.ColorMapper("typus", <parameter>)
 
       r,g,b=colmap.colfct(z)

       where z\in[0,1].

       Concrete example:
         colmap=ColorMapper.ColorMapper("pm3d",pm3d=[7,5,15])
         r,g,b=colmap.colfct(z)
       
       """
    def __init__(self,typus,widths=[0.4,0.4,0.4],gausspos=[0.0,0.5,1.0],
                 exponent=1.0,invert=0,
                 hls_l=0.5,hls_s=1.0,hls_hls=0,
                 pm3d=[7,5,15],
                 brightness=0.0,
                 lutfile=None):
        self.widths=widths
        self.exponent=exponent
        self.invert=invert
        self.hls_l=hls_l
        self.hls_s=hls_s
        self.hls_hls=hls_hls
        self.pm3d=pm3d
        self.gausspos=gausspos
        self.brightness=brightness
        
        if(typus=="gauss"):
            self.colfct=self._gauss_color
        elif(typus=="hls"):
            self.colfct=self._hls2rgb
        elif(typus=="pm3d"):
            self.colfct=self._pm3d
        elif(typus=="red"):
            self.colfct=self._red
        elif(typus=="red2"):
            self.colfct=self._red2
        elif(typus=="green"):
            self.colfct=self._green
        elif(typus=="blue"):
            self.colfct=self._blue
        elif(typus=="blue2"):
            self.colfct=self._blue2
        elif(typus=="yellow-red"):
            self.colfct=self._yellow_red
        elif(typus=="yellow-blue"):
            self.colfct=self._yellow_blue
        elif(typus=="white-yellow-red-black"):
            self.colfct=self._white_yellow_red_black
        elif(typus=="yellow-green-blue-red"):
            self.colfct=self._yellow_green_blue_red
        elif(typus=="lut"):
            self.colfct=self._vtk_lut
            if self.lutfile==None:
                print "Please supply a LUT file"
            else:
                self._initialize_from_lutfile(self.lutfile)

                
        else:
            print "Please supply a correct color mapper"
            print "Now we use a gauss as default"
            self.colfct=self._gauss_color



    def _initialize_from_lutfile(self,lutfile):
        fp=open(lutfile,"r")
        #parse: LOOKUP_TABLE ./luts/pm3d_24.lut 256
        firstline=fp.readline()
        anz=firstline.split()[2]
        
        r,g,b=(Numeric.zeros(anz,"d"),Numeric.zeros(anz,"d"),
               Numeric.zeros(anz,"d"))
        for i in xrange(anz):
            zeile=fp.readline()
            rgb=zeile.split()
            r[i]=string.atof(rgb[0])
            g[i]=string.atof(rgb[1])
            b[i]=string.atof(rgb[2])
        fp.close()
        
        self.r=r
        self.g=g
        self.b=b



    def write_vtk_lutfile(self,lutfile):
        fp=open(lutfile,"w")
        lutfile_=os.path.split(lutfile)[1]
        fp.write("LOOKUP_TABLE %s %d" % (lutfile_,256))

        r,g,b=self.generate_normalized_rgb()
        
        for i in xrange(len(r)):
            fp.write("%5.4f %5.4f %5.4f 1.0\n" % (r[i],g[i],b[i]))
        fp.close()
        


        

    def generate_lut(self):
        """Return triple of rgb arrays with values in [0,255]. """
        r,g,b=(Numeric.zeros(256),Numeric.zeros(256),Numeric.zeros(256))
        for i in Numeric.arange(256):
               r_,g_,b_=self.colfct(i/255.0) # these are from [0,1]
               r[i],g[i],b[i]=int(255*r_),int(255*g_),int(255*b_)
        return r,g,b

    def generate_normalized_rgb(self):
        """Return normalized, [0.0,1.0], triple of rgb arrays."""
        
        r,g,b=(Numeric.zeros(256),Numeric.zeros(256),Numeric.zeros(256))
        for i in Numeric.arange(256):
               r_,g_,b_=self.colfct(i/255.0) # these are from [0,1]
               r[i],g[i],b[i]=int(255*r_),int(255*g_),int(255*b_)
        return r/256.0,g/256.0,b/256.0

              
##    def generate_lut(self):
##        r,g,b=(zeros(256),zeros(256),zeros(256)
##        for x in Numeric.arange(256)
               
##               r,g,b=self.colfct(x/255.0) # these are from [0,1]
##        print r,g,b
##        r=Numeric.where(r>0,r,0*r)
##        g=Numeric.where(g>0,g,0*g)
##        b=Numeric.where(b>0,b,0*b)
##        r=Numeric.where(r>1,0*r,r)
##        g=Numeric.where(g>1,0*g,g)
##        b=Numeric.where(b>1,0*b,b)
##        return((255.0*r).astype(Numeric.UInt8),
##               (255.0*g).astype(Numeric.UInt8),
##               (255.0*b).astype(Numeric.UInt8))        
            
 
    def _gauss(self,x,x0,sigma):        # do we need scipy here ?
        return(scipy.exp(-(x-x0)*(x-x0)/(2.0*sigma*sigma)))


    def _gauss_color(self,x):
        if(self.invert): x=1.0-x
        x=x**self.exponent
        return(self._gauss(x,self.gausspos[0],self.widths[0]),
               self._gauss(x,self.gausspos[1],self.widths[1]),
               self._gauss(x,self.gausspos[2],self.widths[2]))

    def normalize(self,rgb):
        """Normalize an rgb triplet to the 0,1 range"""

        rgb = Numeric.array(rgb)
        return Numeric.clip(rgb,0,1).tolist()
 
    def _gauss(self,x,x0,sigma):        # do we need scipy here ?
        return (scipy.exp(-(x-x0)*(x-x0)/(2.0*sigma*sigma)))



    def _pm3d(self,x):
        if(self.invert): x=1.0-x
        x=x**self.exponent

        return self.normalize([pm3d_formula(x,self.pm3d[0]),
                               pm3d_formula(x,self.pm3d[1]),
                               pm3d_formula(x,self.pm3d[2]) ])


    def _red(self,x):
        """self.brightness: determines the end color.
           Starting from (r,g,b)=(1,1,1) we go to
                         (r,g,b)=(1-self.brightness,0,0)

           self.brightness=0.2 means darker.
        """
    
        if(self.invert): x=1.0-x
        x=x**self.exponent
        return 1.0-x*self.brightness,1.0-x,1.0-x

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

    def _yellow_red(self,x):
        if(self.invert): x=1.0-x
        x=x**self.exponent
        
        return 1.0,1.0-x,self.brightness*(1.0-x)

    def _yellow_green(self,x):
        if(self.invert): x=1.0-x
        x=x**self.exponent
        
        return 1.0-x,1.0,self.brightness*(1.0-x)


    def _yellow_blue(self,x):
        # FIXME: we don't have this !!!!
        if(self.invert): x=1.0-x
        x=x**self.exponent
        
        return 1.0-x**1.5,1.0-x**1.5,x



    def  __white_yellow_red_black1(self,x):
        if(self.invert): x=1.0-x
        x=x**self.exponent
        if x<0.5:
            b=0.0
        else:
            b=(x-0.5)*2.0

        if x<0.25:
            g=0.0
        elif x<0.75:
            g=(x-0.25)*2.0
        else:
            g=1.0

        if x>0.5:
            r=1.0
        else:
            r=x*2.0

        return (r,g,b)
       
        
    def  __white_yellow_red_black(self,x):
        if(self.invert): x=1.0-x
        x=x**self.exponent
        if x<0.5:
            b=0.0
        else:
            b=(x-0.5)*2.0

        if x<0.15:
            g=0.0
        elif x<0.75:
            g=(x-0.15)/(0.75-0.15)
        else:
            g=1.0


        if x>0.3:
            r=1.0
        else:
            r=x/0.3

        return (r,g,b)




    def _white_yellow_red_black(self,x):
        import scipy
        tmp_fkt=scipy.vectorize(self.__white_yellow_red_black)
        return tmp_fkt(x) 

    def _yellow_green_blue_red(self,x):
        if(self.invert): x=1.0-x
        x=x**self.exponent
        w=0.15
        return(self._gauss(x,0.0,w)+self._gauss(x,1.0,w*1.4),
               (self._gauss(x,0.0,w)+self._gauss(x,0.3333,w))/1.1137,
               self._gauss(x,0.6,w/1.1))
        

    def _pm3d2(self,x):
        if(self.invert): x=1.0-x
        x=x**self.exponent        
        return(x**0.35, x**0.5, x**0.8)

    def _hls2rgb(self,h):
        """
        We use a rescaled h \in [0,1]

        h von 0 .. 360 

       letztes argument ist ein flag 0 oder 1, der entscheided ob
       die gruenen farben noch staerker auseinandergezogen werden,
       da wir gruen so gut sehen koennen.
       sonst: l = 0.5, s = 1 ist meist sinnvoll,
                    l = 0: schwarz, l=1 weiss, s: saettigung

        """
        h=h**self.exponent
        if(self.invert): h=1.0-h
        h=h*360.0
        h=Numeric.fmod(h,360.0)
        if(self.hls_hls):
            h=h/60.0
        else:
            if(h<120):
                h=h/120.0       #    /* 0..1 Rot..(Orange)..Gelb */
            elif(h<180):
                h=h/60.0 - 1.0  #     /* 1..2 Gelb..Gruen */
            elif(h<240):
                h=h/30.0 - 4.0 #     /* 2..4 Gruen..Blaugruen..Blau*/
            else:
                h=h/60.0        #     /* 4..6 Blau..Purpur..Rot */
        c=int(h)
        frac=h-c
        if (self.hls_l<=0.5):
            maxi=self.hls_l*(1.0+self.hls_s)
        else:
            maxi=self.hls_l+self.hls_s-self.hls_l*self.hls_s
        mini=2*self.hls_l-maxi;
        diff=maxi-mini;
        if(self.hls_s==0):            #                            /* grau */
            return(1.0,1.0,1.0) 
        else:
            if(c==0):
                return(maxi,mini+frac*diff,mini)
            elif(c==1):
                return(mini+(1.0-frac)*diff,maxi,mini)
            elif(c==2):
                return(mini,maxi,mini+frac*diff)
            elif(c==3):
                return(mini,mini+(1.0-frac)*diff,maxi)
            elif(c==4):
                return(mini+frac*diff,mini,maxi)
            else:
                return(maxi,mini,mini+(1.0-frac)*diff)


    def plotpm3d(self):
        x=Numeric.arange(0,1.0,0.01)
        #qqscipy.xplt.window()
        #qscipy.xplt.limits(0.0,0.0,1.0,1.0)
        #scipy.xplt.hold("on")
        scipy.xplt.plg(pm3d_formula(x,self.pm3d[0]),x,color=-5)
        scipy.xplt.plg(pm3d_formula(x,self.pm3d[1]),x,color=-4)
        scipy.xplt.plg(pm3d_formula(x,self.pm3d[2]),x,color=-3)
        #scipy.xplt.plg(Numeric.sin(x),x)
        #print x,Numeric.sin(x)
        #scipy.xplt.pause(1)



def Array2PIL(a,lut=None,minvalue=None,maxvalue=None,width=None,height=None,
              flip=None):
    """Plot a 2D array as a bitmap.

       what about width,height?????

       - flip:  None: no flip
                "ud": up-down exchange

    """
    import Image   # we only need it here ...

    if flip=="ud":  #up-down exchange
        a=a[::-1,:]
    h,w=Numeric.shape(a)
##    a_min=Numeric.minimum.reduce((Numeric.ravel(a)))
##    a_max=Numeric.maximum.reduce((Numeric.ravel(a)))
    a_min=min(Numeric.ravel(a))
    a_max=max(Numeric.ravel(a))

    # allow for an user-specified maximal value:
    if maxvalue!=None and maxvalue>a_max:
        a_max=maxvalue
    # allows for an user-specified minimal value:
    if minvalue!=None and minvalue<a_min:
        a_min=minvalue

    if lut is not None:
        if len(lut[0]) == 256:
            
            a=(Numeric.ravel(255.0*(a-a_min)/
                             (a_max-a_min))).astype(Numeric.UInt8)

            rgb=Numeric.zeros( (len(a),3),typecode=Numeric.UInt8)


            lut_=Numeric.zeros( (3,len(lut[0])),Numeric.UInt8)
            lut_[0]=lut[0].astype(Numeric.UInt8)
            lut_[1]=lut[1].astype(Numeric.UInt8)
            lut_[2]=lut[2].astype(Numeric.UInt8)

            # This is much faster than the original zip/ravel variant ...
            rgb[:,0]=Numeric.take(lut_[0],a)
            #print "rtake"
            rgb[:,1]=Numeric.take(lut_[1],a)
            #print "gtake"
            rgb[:,2]=Numeric.take(lut_[2],a)
            #print "btake"
            #rgb=Numeric.ravel(((Numeric.array(zip(r,g,b),
            #                                  typecode=Numeric.UInt8))))

            #print "rgb done"
        else:
            N =  len(lut[0])
            print "LUT with N=%d entries" % N
            if N>=256*256:
                print "UUPS, more than uint16 colors??", N
                raise ValueError("N too large")
                
            a = (Numeric.ravel((N-1)*(a-a_min)/
                             (a_max-a_min))).astype(Numeric.UInt16)

            rgb = Numeric.zeros( (len(a), 3), typecode=Numeric.UInt16)

            lut_ = Numeric.zeros( (3,len(lut[0])), Numeric.UInt16)
            lut_[0] = lut[0].astype(Numeric.UInt16)
            lut_[1] = lut[1].astype(Numeric.UInt16)
            lut_[2] = lut[2].astype(Numeric.UInt16)

            # This is much faster than the original zip/ravel variant ...
            rgb[:,0] = Numeric.take(lut_[0],a)
            rgb[:,1] = Numeric.take(lut_[1],a)
            rgb[:,2] = Numeric.take(lut_[2],a)

            rgb = (rgb*256.0/N).astype(Numeric.UInt8)

    else:  # simple grey scale ramp...
        a=(Numeric.ravel(255.0*(a-a_min)/
                         (a_max-a_min))).astype(Numeric.UInt8)
        # convert to (r_0,g_0,b_0,r_1,g_1,b_1,....)
        rgb=Numeric.ravel(Numeric.array(zip(a,a,a)))

    # create a PIL RGB image
    #print "w/h",w,h
    im=Image.new("RGB",(w,h))
    #print "imfromstring:"
    im.fromstring(rgb.tostring())
    #print "done ..."
    
    # scale image ?
    if height!=None and width==None:
        im=im.resize(w/h*height,height)
    elif height==None and width!=None:
        im=im.resize(width,h/w*width)
    elif height!=None and width!=None:
        im=im.resize(width,height)

    return(im)
    
    
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
        r, g, b = (Numeric.zeros(N), Numeric.zeros(N), Numeric.zeros(N))
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
