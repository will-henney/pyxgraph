"""
Helper functions to setup an axis for pyxgraph.py
"""

import pyx
import types
from numerix import *

from pyx.graph.axis.texter import _Itexter


class empty_texter:
    """a texter creating empty labels.

     A texter which does not produce text is not a texter - so why
     do we need this: we want to create a full copy of all properties,
     for example from x to x2, but without any tick labels.
    """
    __implements__ = _Itexter    # what is this for?
    
    def labels(self, ticks):
        for tick in ticks:
            tick.label=""



def _setup_manualticks(whichaxis, caxis, cticks, ticksformat=None,
                       cmin=None, cmax=None):
    """FIXME: doku...

    cticks=(0.0, 4.0, 2.0)
    cticks=(0.0, 4.0, 2.0, 10)      # 10 subticks between ticks.
    cticks=(0.0, 4.0, 2.0, 10, 4)   # 10 subticks between ticks and
                                    # only every fourth tick is labeled.

    If you want no subticks, but labeling of every 2nd tick only, then choose:
    cticks=(0.0, 4.0, 1.0, 0, 2)
    (UMPF, this looks quite un-intuitive now (but it is really special
    casing anyway ...))
    

    For linear axes (``caxis=="linear"``) the subticks are placed
    at equidistant intervals between the major ticks.

    # this is solved by the above:
    #For logarithmic axes the minor ticks are at equidistant values
    #between the major ticks (so visually, they are not equidistant).
    #Problem: e.g. if we have ticks with labels at 10^0 and 10^4 and 10^8
    #and we want to have ticsk without labels at 10^1, 10^2 and 10^3,
    #and 10^5, ... this is not possible.

    """
    pgat = pyx.graph.axis.tick
    manualticks = []
    if (cticks is None) or (cticks == False):        # no manualticks
        return manualticks

    if type(cticks) is types.ListType:  # list with pgat.ticks entries ...
        if not isinstance(cticks[0], pyx.graph.axis.tick.tick):
            raise ValueError("Entries of %sticks should be"
                             "pyx.graph.axis.tick.tick instances" % whichaxis )
        return cticks 

    if type(cticks) is types.TupleType:
        if len(cticks) >= 3:
            tmin = cticks[0]
            tmax = cticks[1]
            tstep = cticks[2]

            cmticks=None
            if len(cticks) == 4 and cticks[3]!=0:
                cmticks = cticks[3]
            every = 1
            if len(cticks) == 5:
                every = cticks[4]   # on label every `every` tick

            if caxis == "linear" or caxis == "pi" or caxis == "frac":
                for nr, tick in enumerate(arange(tmin, tmax+tstep/2.0, tstep)):
                    if nr%every!=0:           # just a tick and no label
                        label = ""
                    if ticksformat is None:   # automatic formatting
                        label = None
                    else:
                        label = ticksformat % (tick)
                    manualticks.append(pgat.tick(tick, label=label))


                # deal with minor ticks:
                if cmticks is not None:
                    for nr,tick in enumerate(arange(tmin,
                                                    tmax+tstep/2.0/cmticks,
                                                    1.0*tstep/cmticks)):
                        if not (nr % cmticks==0):
                            manualticks.append(pgat.tick(tick, label="",
                                                         ticklevel=1))

            elif caxis in ["log", "log10", "ln"]:
                tick = tmin
                nr = 0
                while tick <= tmax+tmin:
                    if nr%every!=0:              # just a tick, but no label
                        label = ""
                    elif ticksformat is None:  # automatic formatting
                        label = None
                    else:
                        label = ticksformat % (tick)
                    manualticks.append(pgat.tick(tick, label=label))
                    tick = tick*tstep
                    nr = nr + 1
                    
                # deal with minor ticks:
                if cmticks is not None:
                    tick = tmin
                    while tick <= tmax*tstep+tmin: 
                        mtick = tick
                        mtstep  = 1.0*(tick*tstep-tick)/(cmticks-1)
                        for i in xrange(1, cmticks-1):
                            mtick = tick+i*mtstep
                            if mtick >= tmax+tmin: 
                                break
                            manualticks.append(pgat.tick(mtick, label="",
                                                         ticklevel=1))

                        tick = tick*tstep


                    
                    #factor = tstep**(1.0/cmticks)
##                    while tick < tmax+tstep/2.0:

##                        # ..... FCK how to do that .....
                        
##                        #if not (nr % cmticks==0):
##                        #    manualticks.append(pgat.tick(tick, label="",
##                        #                                 ticklevel=1))
##                        #tick = tick*factor
##                        #nr = nr +1
            else:
                print "what kind of axis should this be:", caxis

        elif len(cticks) == 2:              # (tmin, tstep) situation
            raise NotImplementedError     # FIXME: tobewritten (easy, if needed)
        else:
            raise ValueError("invalid ticks for %saxis: " % (whichaxis,
                                                             str(cticks)))
    else:
        raise ValueError("invalid ticks for %saxis: " %
                         (whichaxis, str(cticks)))

    return manualticks
    


def _setup_axis(whichaxis, caxis, climits, cticks, cpaint, cticksformat,
                ctexter, label, linkpainter=None):
    """Internal routine to setup an axis.

         caxis  : False, "linear", "log", "log10", "ln", "pi",
                  or PyX axis instance: pyx.graph.axis.axis._axis 
         climits: (0, 10), (0, None), (None, 10)
         cticks : False, None, (0, 2), (0.0, 5.0, 1.0), or manualticks
         cticksformat: None, or format string "%5.4f"
         cpaint : False,  PyX painter instance
         
         Thus:
            - False for cticks : ticks are not shown
              (None means automatic ticking ...)
            - False for caxis  : whole axis is not shown
            - False for cpaint : whole axis is not shown

         ctexter: - False:  no text at ticks
                  - None: do something automaticlaly
                  - texter instance 
         
       """
    cparter_dict=None       # not used at the moment (maybe kick out again)
    if False:
        print "===================="
        print "Setting up axis: ", whichaxis
        print "caxis       : ", caxis
        print "climits     : ", climits
        print "cticks      : ", cticks
        print "cpaint      : ", cpaint
        print "cticksformat: ", cticksformat
        print "ctexter     : ", ctexter
        print "cparter_dict: ", cparter_dict
        print "label       : ", label
        print "===================="

    # Problem is that in these cases the painter is ignored!!!
    if ( (climits[0] is None) and (climits[1] is None) and
         (cticks is None) and (ctexter==False)):
        #print "rejected axis %s: Reason 1"  % whichaxis
        return False           # insufficient axis specification

    #if (cticks is None) and (ctexter==False):
        #print "rejected axis %s: Reason 2"  % whichaxis
    #    return False           # insufficient axis specification


    cmin, cmax = climits
    if cticks == False:
        if cmin is None:
            cmin = 0
        if cmax is None:
            cmax = 0
        if caxis=="linear" or caxis is None:
            return pyx.graph.axis.linear(min=cmin, max=cmax,
                                         painter=cpaint,
                                         parter=None, rater=None,
                                         texter=empty_texter())
        elif caxis in ["log", "log10"]:
            return pyx.graph.axis.logarithmic(min=cmin, max=cmax,
                                              painter=cpaint,
                                              parter=None, rater=None,
                                              texter=empty_texter())
        else:
            print "Axis: %s not supported here ..." % caxis
            print "und nun ?? ;-)"
        

    if caxis is None:
        return False

    if ctexter==False:
        ctexter = empty_texter()

    if (caxis == False) or (cpaint == False):  # whole axis is not shown
        return False
        
    if isinstance(caxis, pyx.graph.axis.axis._axis):
        return caxis
    
#     if caxis not in ["linear", "log", "log10", "pi", "frac"]:
#         raise ValueError("invalid %saxis '%s'" % (whichaxis, caxis))

    manual_ticks = _setup_manualticks(whichaxis, caxis, cticks, cticksformat,
                                      cmin=cmin, cmax=cmax)

    if linkpainter is not None:
        linkpainterspec = dict(linkpainter=linkpainter)
    else:
        linkpainterspec = dict()

    #print "linkpainterspec=", linkpainterspec, linkpainter

    if cparter_dict is None:
        cparter_dict = dict()


    pga = pyx.graph.axis   # shorthand
    if caxis == "linear":
        parter = pga.parter.autolinear(**cparter_dict)
        #parter = pga.parter.linear(**cparter_dict)
        rater = pga.rater.linear()
        if len(manual_ticks)>0 or  cticks == False:
            parter = None             # no additional automatic ticks
            rater = None              # and no rating

        if cticks == False:
            manual_ticks = []

        # E.g.: for 0.00, 0.05, 0.10, ...
        if ctexter is None:
            ctexter = pyx.graph.axis.texter.decimal(equalprecision=True)
            
        curr_axis = pga.linear(min=cmin, max=cmax,
                               painter=cpaint,
                               parter=parter, rater=rater,
                               manualticks=manual_ticks,
                               title=label,
                               texter=ctexter,
                               **linkpainterspec
                               )
    elif caxis == "log" or caxis == "log10":
        parter = pga.parter.autologarithmic(**cparter_dict)
        rater = pga.rater.logarithmic()
        if len(manual_ticks)>0 or  cticks == False:
            parter = None             # no additional automatic ticks
            rater = None              # and no rating
        if cticks == False:
            manual_ticks = []
        if ctexter is None:
            #ctexter = pyx.graph.axis.texter.exponential()
            ctexter = pyx.graph.axis.texter.mixed()
        curr_axis = pga.logarithmic(min=cmin, max=cmax, painter=cpaint,
                                    parter=parter, rater=rater,
                                    manualticks=manual_ticks, title=label,
                                    texter=ctexter,
                                    **linkpainterspec)
    elif caxis == "ln":
        raise NotImplementedError
    elif caxis == "pi":
        parter = pga.parter.autolinear(**cparter_dict)
        rater = pga.rater.linear()
        if len(manual_ticks)>0 or  cticks == False:
            parter = None             # no additional automatic ticks
            rater = None              # and no rating

        if ctexter is None:
            ctexter = pga.texter.rational(suffix=r"\pi") 
            
        curr_axis  = pga.linear(min=cmin, max=cmax, divisor=pi,
                                texter=ctexter,
                                painter=cpaint,
                                parter=parter, rater=rater,
                                manualticks=manual_ticks,
                                title=label,
                                **linkpainterspec)
                                
    elif caxis == "frac":
        parter = pga.parter.autolinear(**cparter_dict)
        rater = pga.rater.linear()
        if len(manual_ticks)>0 or  cticks == False:
            parter = None             # no additional automatic ticks
            rater = None              # and no rating

        if ctexter is None:
            ctexter = pga.texter.rational(suffix=r"") 
            
        curr_axis  = pga.linear(min=cmin, max=cmax, divisor=1,
                                texter=ctexter,
                                painter=cpaint,
                                parter=parter, rater=rater,
                                manualticks=manual_ticks,
                                title=label,
                                **linkpainterspec)
    else:
         #raise NotImplementedError       # should not get here!
        curr_axis = caxis  
  
    return curr_axis
