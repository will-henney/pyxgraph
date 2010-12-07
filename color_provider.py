"""Routines to provide a reasonable color for almost any input."""

import pyx

def _to_pyxcolor_eval(val):
    """ helper function for _to_pyxcolor: take int or float, return a float
    from interval [0.0, 1.0]
    """
    if isinstance(val, float):
        if val < 0.0 or val > 1.0:
            val %= 1.0
        return val
    if isinstance(val, int):
        return (val%256)/255.0
    if type(val) is str or type(val) is unicode:
        try:
            return _to_pyxcolor_eval(eval(val))
        except:
            return 0.0
    print 'Not a number:', repr(val)
    return 0.0

def _chkattrs(checkfunc, retrfunc):
    """helper function for _to_pyxcolor. checks for a possible color definition
    via checkfunc, retrieves the values with retrfunc and (if applicable)
    returns a pyx.color.color. Otherwise returns None.
    checkfunc: checkfunc('r') -> True if attribute/ entry/ whatever called
    'r' exists.
    retrfunc: retrfunc('r') -> retrieve value associated to 'r'.
    """
    def chkcolorsys(kwlist):
        """ checks if attributes corresponding to kwlist exist. If yes, return
        tuple of values. Case insensitive."""
        retlist = [][:]   # [:] is important here because [] is mutable!
        for sublist in kwlist:
            values = [retrfunc(i) for i in sublist if checkfunc(i)]
            if len(values) == 0:
                return None
            if len(values) > 1:
                print "Multiple values for %s given, taking the 1st one" % \
                      sublist[0]
            retlist.append(_to_pyxcolor_eval(values[0]))
        return retlist
    # ordering of arguments r,g,b given by ordering in pyx function call!
    rgbvals = chkcolorsys([['r', 'red'], ['g', 'green'], ['b', 'blue']])
    if rgbvals:
        return pyx.color.rgb(*rgbvals)
    cmykvals = chkcolorsys([['c', 'cyan'], ['m', 'mag', 'magenta'], 
                            ['y', 'yellow'], ['b', 'k', 'black', 'key']])
    if cmykvals:
        return pyx.color.cmyk(*cmykvals)
    hsbvals = chkcolorsys([['h', 'hue'], ['s', 'sat', 'saturation'],
                           ['b', 'brightness', 'l', 'lum', 'luminance', 
                            'lightness', 'v', 'val', 'value']])
    if hsbvals:
        return pyx.color.hsb(*hsbvals)
    greyval = chkcolorsys([['g', 'gray', 'grey']])
    if greyval:
        return pyx.color.gray(*greyval)
    return None
    
             
def _to_pyxcolor(ident, color_seq=[]):
    """takes ident and returns a pyx.color.color object.

    ident can be almost anything:
    - a pyx.color.color object: returned unchanged
    - a string: assumed to be (part of) the colors name
        e.g.: "yellow", "GREEN", "yel", "v"
    - an integer: used as index into color_seq
        if color_seq is empty: taken as greyscale value (0 ... 255)
    - a float: taken as greyscale value (0.0 ... 1.0)
    - a list / a tuple / anything sliceable of length 4 (CMYK) or 3 (RGB)
      - if integers: taken as values for C, M, Y, K (0 ... 255)
      - if floats: taken as values for C, M, Y, K (0.0 ... 1.0)
      for a sliceable object of length!=4, we take the first 3 as rgb values.
    - a dictionary:
      - if containing keys 'r', 'g', 'b' or 'red', 'green', 'blue':
        interpreted as RGB color
      - if containing keys 'c', 'm', 'y', 'k' or 'cyan', 'magenta',
        'yellow', 'black':
        interpreted as CMYK color
      - if containing keys 'h', {'l' or 'v' or 'b'}, 's' or
        'hue', {'luminance' or 'value' or 'brightness}, 'saturation' or
        similar: interpreted as HSB color (note that HLS!=HSB, but L will be
        treated as if it was B).
      - if containing key 'g' or 'gray' or 'grey': interpreted as gray value
    - some other object:
      - we will look for attributes like 'r', 'g', 'b' etc. of correct
        type. Treated like the dictionary case.
    If ident absolutely cannot be evaluated, pyx.color.cmyk.Black
    will be returned.
    """
    if isinstance(ident, pyx.color.color):
        return ident
    if type(ident) is str or type(ident) is unicode:
        # assume to be color name or part of it
        name = ident.upper()
        # get the predefined colors from pyx.color.cmyk
        cmykattrs = dir(pyx.color.cmyk)

        # take only items that are no colors
        # that is, all items not starting with a capital letter
        colornames = [(n.upper(), n) for n in cmykattrs
                      if ord(n[:1]) in range(ord('A'),ord('Z')+1) ]
        # build dictionary which matches the uppercase name to the real
        # name
        namedict = dict(colornames)
        if name not in namedict:
            # check if part of the name occurs in the color names
            colornames = [capn for capn, n in colornames]
            # sort by string length
            # reason: if you give 'g', you likely mean 'gray' and not
            # 'LimeGreen'.
            colornames.sort(lambda s1, s2: cmp(len(s1), len(s2)))
            matches = [(name in n) for n in colornames]
            if True in matches:
                name = colornames[matches.index(True)]
                print "I don't know the color %s. You get %s instead." % \
                      (ident, namedict[name])
            else:
                print 'Did not understand color name', ident
                return pyx.color.cmyk.Black
        return getattr(pyx.color.cmyk, namedict[name])
    if isinstance(ident, int):
        if len(color_seq) > 0:
            c = color_seq[ident % len(color_seq)]
            return _to_pyxcolor(c, [])
        else:
            # assume ident = gray scale value [0 .. 255]
            return pyx.color.gray(_to_pyxcolor_eval(ident))
    if type(ident) is float:
        return pyx.color.gray(_to_pyxcolor_eval(ident))
    try:
        l=len(ident)
    except:
        l=0
    if l != 0:
        if len(ident) == 4:
            # map(.., ident) makes sure that each element of ident is a valid
            # number. map(f, [1,2]) == [f(1), f(2)]
            return pyx.color.cmyk(*map(_to_pyxcolor_eval, ident))
        return pyx.color.rgb(*map(_to_pyxcolor_eval, ident[:3]))
    if type(ident) is dict:
        # first argument is a function that checks if the dict contains s
        # second argument is a function that retrieves s's value
        c = _chkattrs(lambda s: s in ident, lambda s: ident[s])
        if c is not None:
            return c
    c = _chkattrs(lambda s: hasattr(ident, s), lambda s: getattr(ident, s))
    if c is not None:
        return c
    return pyx.color.cmyk.Black

