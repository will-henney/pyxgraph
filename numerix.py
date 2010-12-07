"""
Try to get Numeric or numpy.

"""

import sys

found = False


def any():
    print "Not defined for Numeric ..."
    
if "numpy" in sys.modules:    
    from numpy import *
    print "Using numpy because it is already imported"
    import ColMapper
    found = True


if "Numeric" in sys.modules:
    if found:
        print "Autsch, both Numeric and numpy are already imported"
        print "not sure if you should really do this"
    from Numeric import *
    print "Using Numeric because it is already imported"
    import ColMapperNumeric as ColMapper
    found = True





if not found:
    try:
        from numpy import *
        found = True
        print "Using numpy..."
    except ImportError:
        pass

    if found:
        import ColMapper

def not_available_in_Numeric():
    print "problem, this routine is not available in Numeric"
    

if not found:
    try:
        from Numeric import *
        found = True
        print "Using Numeric"
        any = not_available_in_Numeric
    except ImportError:
        pass

    if found:
        import ColMapperNumeric as ColMapper


##if not found:
##    try:
##        from numarray import *
##        found = True
##    except ImportError:
##        pass

if not found:
    print "No numpy, no Numeric? poor guy ...."
    print "PyXgraph needs one of these ..."

try:
    NewAxis = newaxis
except:  # Numeric
    pass
