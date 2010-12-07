"""
Additional symbols and color sequences, and line pattern sequences.
"""

import pyx


def _scaled_symbol(sym, sym_attrs=None, factor=1.0):
    """Return symbol with a specified size and additional attributes."""
    if sym_attrs == None:
        sym_attrs = []
    return pyx.graph.style.symbol(sym,
                                  symbolattrs=sym_attrs,
                                  size=factor*0.15*pyx.unit.cm)

#-------------------------------------------------------------------------------
globalscalefactor = 0.8

def _triangle_u_symbol(c, x_pt, y_pt, size_pt, attrs):
   size_pt=size_pt*globalscalefactor
   c.draw(pyx.path.path(pyx.path.moveto_pt(x_pt+0.759835685*size_pt,
                                   y_pt-0.438691337*size_pt),
                        pyx.path.lineto_pt(x_pt-0.759835685*size_pt,
                                   y_pt-0.438691337*size_pt),
                        pyx.path.lineto_pt(x_pt,
                                   y_pt+0.877382675*size_pt),
                        pyx.path.closepath()), attrs)

def _triangle_d_symbol(c, x_pt, y_pt, size_pt, attrs):
    size_pt=size_pt*globalscalefactor
    c.draw(pyx.path.path(pyx.path.moveto_pt(x_pt+0.759835685*size_pt,
                                    y_pt+0.438691337*size_pt),
                         pyx.path.lineto_pt(x_pt-0.759835685*size_pt,
                                    y_pt+0.438691337*size_pt),
                         pyx.path.lineto_pt(x_pt,
                                    y_pt-0.877382675*size_pt),
                         pyx.path.closepath()), attrs)
                         
def _triangle_r_symbol(c, x_pt, y_pt, size_pt, attrs):
    size_pt=size_pt*globalscalefactor
    c.draw(pyx.path.path(pyx.path.moveto_pt(x_pt-0.438691337*size_pt,
                                    y_pt-0.759835685*size_pt),
                         pyx.path.lineto_pt(x_pt-0.438691337*size_pt,
                                    y_pt+0.759835685*size_pt),
                         pyx.path.lineto_pt(x_pt+0.877382675*size_pt,
                                    y_pt),
                         pyx.path.closepath()), attrs)
                         
def _triangle_l_symbol(c, x_pt, y_pt, size_pt, attrs):
    size_pt=size_pt*globalscalefactor
    c.draw(pyx.path.path(pyx.path.moveto_pt(x_pt+0.438691337*size_pt,
                                    y_pt-0.759835685*size_pt),
                         pyx.path.lineto_pt(x_pt+0.438691337*size_pt,
                                    y_pt+0.759835685*size_pt),
                         pyx.path.lineto_pt(x_pt-0.877382675*size_pt,
                                    y_pt),
                         pyx.path.closepath()), attrs)
                                                
def _star_symbol(c, x_pt, y_pt, size_pt, attrs):
    c.draw(pyx.path.path(pyx.path.moveto_pt(x_pt-0.707106781*size_pt, y_pt), 
                         pyx.path.lineto_pt(x_pt+0.707106781*size_pt, y_pt),
                         pyx.path.moveto_pt(x_pt, y_pt-0.707106781*size_pt),
                         pyx.path.lineto_pt(x_pt, y_pt+0.707106781*size_pt), 
                         # plus

                         pyx.path.moveto_pt(x_pt-0.5*size_pt, y_pt-0.5*size_pt),
                         pyx.path.lineto_pt(x_pt+0.5*size_pt, y_pt+0.5*size_pt),
                         pyx.path.moveto_pt(x_pt-0.5*size_pt, y_pt+0.5*size_pt),
                         pyx.path.lineto_pt(x_pt+0.5*size_pt, y_pt-0.5*size_pt)
                         # cross
                         ), attrs)
                         
def _squaresymbol2(c, x_pt, y_pt, size_pt, attrs):
    c.draw(pyx.path.path(pyx.path.moveto_pt(x_pt, y_pt+0.707106781*size_pt),
                         pyx.path.lineto_pt(x_pt+0.707106781*size_pt, y_pt),
                         pyx.path.lineto_pt(x_pt, y_pt-0.707106781*size_pt),
                         pyx.path.lineto_pt(x_pt-0.707106781*size_pt, y_pt),
                         pyx.path.closepath()), attrs)
    
                                              
def _circletriangle_u_symbol(c, x_pt, y_pt, size_pt, attrs):   
    size_pt=size_pt*globalscalefactor
    c.draw(pyx.path.path(pyx.path.moveto_pt(x_pt-0.759835685*size_pt,
                                    y_pt-0.438691337*size_pt),
                         pyx.path.lineto_pt(x_pt+0.759835685*size_pt,
                                    y_pt-0.438691337*size_pt),
                         pyx.path.lineto_pt(x_pt,
                                    y_pt+0.877382675*size_pt),
                         pyx.path.closepath(),
                         # triangle up

                         pyx.path.moveto_pt(x_pt+1.7*0.564189583*size_pt,y_pt), 
                         pyx.path.arc_pt(x_pt, y_pt, 1.7*0.564189583*size_pt,
                                         0, 360),
                         pyx.path.closepath()
                         # circle
                         ), attrs)
                         
def _circletriangle_d_symbol(c, x_pt, y_pt, size_pt, attrs):   
    size_pt=size_pt*globalscalefactor
    c.draw(pyx.path.path(pyx.path.moveto_pt(x_pt+0.759835685*size_pt,
                                    y_pt+0.438691337*size_pt),
                         pyx.path.lineto_pt(x_pt-0.759835685*size_pt,
                                    y_pt+0.438691337*size_pt),
                         pyx.path.lineto_pt(x_pt,
                                    y_pt-0.877382675*size_pt),
                         pyx.path.closepath(),
                         # triangle down

                         pyx.path.moveto_pt(x_pt+1.7*0.564189583*size_pt,y_pt), 
                         pyx.path.arc_pt(x_pt, y_pt, 1.7*0.564189583*size_pt,
                                         0, 360),
                         pyx.path.closepath()
                         # circle
                         ), attrs)
                         
def _circletriangle_l_symbol(c, x_pt, y_pt, size_pt, attrs): 
    size_pt=size_pt*globalscalefactor  
    c.draw(pyx.path.path(pyx.path.moveto_pt(x_pt+0.438691337*size_pt,
                                    y_pt-0.759835685*size_pt),
                         pyx.path.lineto_pt(x_pt+0.438691337*size_pt,
                                    y_pt+0.759835685*size_pt),
                         pyx.path.lineto_pt(x_pt-0.877382675*size_pt,
                                    y_pt),
                         pyx.path.closepath(),
                         # triangle left

                         pyx.path.moveto_pt(x_pt+1.7*0.564189583*size_pt,y_pt), 
                         pyx.path.arc_pt(x_pt, y_pt, 1.7*0.564189583*size_pt,
                                         0, 360),
                         pyx.path.closepath()
                         # circle
                         ), attrs)
                         
def _circletriangle_r_symbol(c, x_pt, y_pt, size_pt, attrs):   
    size_pt=size_pt*globalscalefactor
    c.draw(pyx.path.path(pyx.path.moveto_pt(x_pt-0.438691337*size_pt,
                                    y_pt-0.759835685*size_pt),
                         pyx.path.lineto_pt(x_pt-0.438691337*size_pt,
                                    y_pt+0.759835685*size_pt),
                         pyx.path.lineto_pt(x_pt+0.877382675*size_pt,
                                    y_pt),
                         pyx.path.closepath(),
                         # triangle right

                         pyx.path.moveto_pt(x_pt+1.7*0.564189583*size_pt,y_pt), 
                         pyx.path.arc_pt(x_pt, y_pt, 1.7*0.564189583*size_pt,
                                         0, 360),
                         pyx.path.closepath()
                         # circle
                         ), attrs)
                         
def _circlesquare_symbol(c, x_pt, y_pt, size_pt, attrs):   
    size_pt=size_pt*globalscalefactor
    c.draw(pyx.path.path(pyx.path.moveto_pt(x_pt-0.5*size_pt, y_pt-0.5*size_pt),
                         pyx.path.lineto_pt(x_pt+0.5*size_pt, y_pt-0.5*size_pt),
                         pyx.path.lineto_pt(x_pt+0.5*size_pt, y_pt+0.5*size_pt),
                         pyx.path.lineto_pt(x_pt-0.5*size_pt, y_pt+0.5*size_pt),
                         pyx.path.closepath(),
                         # square

                         pyx.path.moveto_pt(x_pt+1.7*0.564189583*size_pt,y_pt), 
                         pyx.path.arc_pt(x_pt, y_pt, 1.7*0.564189583*size_pt,
                                         0, 360),
                         pyx.path.closepath()
                         # circle
                         ), attrs)
 
def _circlesquare_symbol2(c, x_pt, y_pt, size_pt, attrs): 
    size_pt=size_pt*globalscalefactor  
    c.draw(pyx.path.path(pyx.path.moveto_pt(x_pt, y_pt+0.707106781*size_pt),
                         pyx.path.lineto_pt(x_pt+0.707106781*size_pt, y_pt),
                         pyx.path.lineto_pt(x_pt, y_pt-0.707106781*size_pt),
                         pyx.path.lineto_pt(x_pt-0.707106781*size_pt, y_pt),
                         pyx.path.closepath(),
                         # rotated square

                         pyx.path.moveto_pt(x_pt+1.7*0.564189583*size_pt,y_pt), 
                         pyx.path.arc_pt(x_pt, y_pt, 1.7*0.564189583*size_pt,
                                         0, 360),
                         pyx.path.closepath()
                         # circle
                         ), attrs)                         
                                             
class mysymbols(pyx.graph.style.symbol):
    triangle_u = pyx.attr.changelist([ _triangle_u_symbol])
    triangle_d = pyx.attr.changelist([ _triangle_d_symbol])
    triangle_r = pyx.attr.changelist([ _triangle_r_symbol])
    triangle_l = pyx.attr.changelist([ _triangle_l_symbol])
    square2 = pyx.attr.changelist([ _squaresymbol2])
    star = pyx.attr.changelist([ _star_symbol])
    circletriangle_u = pyx.attr.changelist([ _circletriangle_u_symbol])
    circletriangle_d = pyx.attr.changelist([ _circletriangle_d_symbol])
    circletriangle_r = pyx.attr.changelist([ _circletriangle_r_symbol])
    circletriangle_l = pyx.attr.changelist([ _circletriangle_l_symbol])
    circlesquare = pyx.attr.changelist([ _circlesquare_symbol])
    circlesquare2 = pyx.attr.changelist([ _circlesquare_symbol2])
    

COLOR_SEQ_DEFAULT=[pyx.color.rgb.black,
                   pyx.color.rgb.blue,
                   pyx.color.rgb.red,
                   pyx.color.rgb.green,
                   pyx.color.rgb(0.0,1.0,1.0)]
                   
COLOR_SEQ_COLOR11=[pyx.color.cmyk.Black,
                   pyx.color.cmyk.Red,
                   pyx.color.cmyk.OliveGreen,
                   pyx.color.cmyk.Blue,
                   pyx.color.cmyk.Magenta,
                   pyx.color.cmyk.Cerulean,
                   pyx.color.cmyk.RawSienna,
                   pyx.color.cmyk.LimeGreen,
                   pyx.color.cmyk.Plum,
                   pyx.color.cmyk.BurntOrange,
                   pyx.color.cmyk.Gray,
                   pyx.color.rgb(0.65,0.65,0.65),
                   pyx.color.rgb(1.0,1.0,1.0)]
                   
COLOR_SEQ_RAINBOW=[pyx.color.cmyk.Red,
                   pyx.color.cmyk.BurntOrange,
                   pyx.color.cmyk.Goldenrod,
                   pyx.color.cmyk.LimeGreen,
                   pyx.color.cmyk.PineGreen,
                   pyx.color.cmyk.BlueGreen,
                   pyx.color.cmyk.Cerulean,
                   pyx.color.cmyk.NavyBlue,
                   pyx.color.cmyk.Violet,
                   pyx.color.cmyk.Plum,
                   pyx.color.cmyk.Black]
                 
COLOR_SEQ_COLOR6=[pyx.color.cmyk.Black,
                  pyx.color.cmyk.Red,
                  pyx.color.cmyk.OliveGreen,
                  pyx.color.cmyk.Blue,
                  pyx.color.cmyk.Magenta,
                  pyx.color.cmyk.Cerulean]
 
COLOR_SEQ_GREY5=[pyx.color.rgb(0.0,0.0,0.0),
                 pyx.color.rgb(0.25,0.25,0.25),
                 pyx.color.rgb(0.45,0.45,0.45),
                 pyx.color.rgb(0.65,0.65,0.65),
                 pyx.color.rgb(0.8,0.8,0.8)]
  
COLOR_SEQ_GREY10=[pyx.color.rgb(0.0,0.0,0.0),
                  pyx.color.rgb(0.15,0.15,0.15),
                  pyx.color.rgb(0.25,0.25,0.25),
                  pyx.color.rgb(0.35,0.35,0.35),
                  pyx.color.rgb(0.43,0.43,0.43),
                  pyx.color.rgb(0.50,0.50,0.50),
                  pyx.color.rgb(0.56,0.56,0.56),
                  pyx.color.rgb(0.64,0.64,0.64),
                  pyx.color.rgb(0.72,0.72,0.72),
                  pyx.color.rgb(0.80,0.80,0.80)]                  
                  
                  
def linepattern_factory(dl=1, offset=1, rellengths=0):
    """`dl`: dashlength
       `offset`:
       `rellength`: if the line is wider, the distances between
                    the parts of the dash is adjusted as well

       dash: (length of line, length of free space, lenth of line, ...)
    """
    return [pyx.style.linestyle.solid,  
            pyx.style.linestyle(pyx.style.linecap.butt,    
                                pyx.style.dash([dl*2], offset, rellengths)),
            pyx.style.linestyle(pyx.style.linecap.round, 
                                pyx.style.dash([0, dl*2], offset, rellengths)),
            pyx.style.linestyle(pyx.style.linecap.round, 
                                pyx.style.dash([0, dl*2, dl*2, dl*2],
                                               offset, rellengths)),
            
            pyx.style.dash((dl*4, dl*1.5), offset, rellengths),
            pyx.style.dash((dl*2.5, dl*2), offset, rellengths),
            pyx.style.dash((dl*1.5, dl*1), offset, rellengths),
            pyx.style.dash((dl*5, dl*2, dl*1, dl*2), offset, rellengths),
            pyx.style.dash((dl*3, dl*2.5, dl*1, dl*2.5), offset, rellengths),
            pyx.style.dash((dl*2, dl*1, dl*2, dl*3), offset, rellengths),
            pyx.style.dash((dl*2, dl*1, dl*2,  dl*1, dl*2,  dl*3),
                           offset, rellengths), 
            pyx.style.dash((dl*2, dl*1,  dl*2,  dl*1, dl*2, dl*1, dl*2, dl*3),
                           offset, rellengths),
            
            ## my new linepattern : combine to make a colored dash-sequence                           
            pyx.style.dash((dl*2, dl*2), offset, rellengths),
            pyx.style.dash((dl*0, dl*2, dl*2, dl*0), offset, rellengths),]

# FIXME: maybe find a better place for this?
def linepattern_from_string(s, dl=1, offset=1, rellengths=0):
    '''create a line pattern from a string.
    
    You can use the following chars in the string:
            "  -> #_#__
            '  -> ##__
            .  -> #__
            -  -> ####__
            _  -> ####
               -> ____
    (# - length=1, _ - space with length=1)
    Also, you can use "x_" and "x " where x is a digit for a line or space
    of length x.
    All lengths are multiplied with dl (dashlength).

    Example: linepattern_from_string('- . ', 0.3)
    '''
    pattern = [0]
    atdot = True
    nextlength = None
    for char in s:
        if char in '"\'.-_':
            if not atdot:
                pattern.append(0)
            atdot = False
            if char == '"':
                pattern[-1] += 1
                pattern += [1, 1, 2]
            elif char == "'":
                pattern[-1] += 2
                pattern += [2]
            elif char == '.':
                pattern[-1] += 1
                pattern.append(2)
            elif char == '-':
                pattern[-1] += 4
                pattern.append(2)
            elif char == '_':
                if nextlength is None:
                    nextlength = 4
                pattern[-1] += nextlength
                nextlength = None
                atdot = True
        elif char in ' ':
            if atdot:
                pattern.append(0)
            if nextlength is None:
                nextlength = 4
            pattern[-1] += nextlength
            nextlength = None
            atdot = False
        elif char in '1234567890':
            nextlength = eval(char)
    pattern = [dl*length for length in pattern]
    if len(pattern) == 1:
        pattern=[]
    return pyx.style.dash(tuple(pattern), offset, rellengths)
                                    
SYMBOL_SEQ_DEFAULT=[                   
                    (pyx.graph.style.symbol.plus, []),
                    (pyx.graph.style.symbol.cross, []),
                    (pyx.graph.style.symbol.circle, []),
                    (pyx.graph.style.symbol.square, []),                    
                    (mysymbols.square2, []), 
                    (mysymbols.triangle_u, []),                   
                    (mysymbols.star, []),
                    (mysymbols.triangle_d, []),                    
                    (mysymbols.triangle_r, []),                    
                    (mysymbols.triangle_l, []),  
                    (pyx.graph.style.symbol.diamond, []),
                    (mysymbols.circletriangle_u, []),
                    (mysymbols.circletriangle_d, []),
                    (mysymbols.circletriangle_r, []),
                    (mysymbols.circletriangle_l, []),
                    (mysymbols.circlesquare, []),
                    (mysymbols.circlesquare2, []),
                    (pyx.graph.style.symbol.circle, [pyx.deco.filled]),
                    (mysymbols.triangle_u, [pyx.deco.filled]),
                    (mysymbols.triangle_d, [pyx.deco.filled]),
                    (mysymbols.triangle_r, [pyx.deco.filled]),
                    (mysymbols.triangle_l, [pyx.deco.filled]),
                    (pyx.graph.style.symbol.square, [pyx.deco.filled]),
                    (mysymbols.square2, [pyx.deco.filled]),
                    (pyx.graph.style.symbol.diamond, [pyx.deco.filled]),
                    ]
                    
# [pyx.deco.filled,pyx.deco.stroked([pyx.color.rgb.red]

def provide_styles(dashlength=2, offset=1, rellengths=0):
    """`dashlength`: distance between parts of a dash,
        offset ?
        rellenghts: if the line is wider, the distances between
                    the parts of the dash is adjusted as well
    """                    
    color_dict={"default" : COLOR_SEQ_DEFAULT,
                "color6" : COLOR_SEQ_COLOR6,
                "color11" : COLOR_SEQ_COLOR11,
                "rainbow" : COLOR_SEQ_RAINBOW,
                "grey5" : COLOR_SEQ_GREY5,
                "grey10" : COLOR_SEQ_GREY10,
                }
    linepattern_dict={"default" : linepattern_factory(dashlength, offset,
                                                      rellengths)}
    symbol_dict={"default" : SYMBOL_SEQ_DEFAULT}
    return color_dict, linepattern_dict, symbol_dict


if __name__ == "__main__":
    color_dict, linepattern_dict, symbol_dict = provide_styles(dashlength=1)
    
    for col_seq in color_dict:
        print col_seq, "  no. members:", len(color_dict[col_seq])
    for line_seq in linepattern_dict:
        print line_seq, "  no. members:", len(linepattern_dict[line_seq])
    for symbol_seq in symbol_dict:
        print symbol_seq, "  no. members:", len(symbol_dict[symbol_seq])
