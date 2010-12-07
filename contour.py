from numerix import arange, array, where, any, nonzero

def contour_gencoords(x_grid, y_grid, z, levels):
    '''calculate the contours of z on the coordinate grid x_grid, y_grid at
    levels.

    Let the 2d plane be parametrized by p and q.
    x_grid[p, q] and y_grid[p,q] have to contain the cartesic coordinates of
    the point (p, q). z[p, q] holds the value of some scalar function on that
    grid. levels is a list of float values for which the contours shall be
    calculated.

    Returns a list of equal length to levels. Each entry is a set of contour
    lines for the corresponding level value.

    A set of contour lines is a list which contains 2-element lists
    [xarr, yarr]. xarr and yarr hold the points of one contour line in cartesic
    coordinates.
    
    xarr = result[levidx][lineidx][0]
    yarr = result[levidx][lineidx][1]'''
    result = []
    maxy, maxx = z.shape
    for level in levels:
        lines = contour_graph(z, level)
        coordinates = []
        for line in lines:
            interp_y, x, y, weights = map(array, line)
            line_translated = []
            for grid in x_grid, y_grid:
                line_translated.append(where(interp_y,
                    # The % operation does not affect the result!
                    # It will avoid index errors but the corresponding
                    # entries will be eaten by where.
                    grid[y,x]*(1-weights) + grid[(y+1)%maxy,x]*weights,
                    grid[y,x]*(1-weights) + grid[y,(x+1)%maxx]*weights ))
            coordinates.append(line_translated)
        result.append(coordinates)
    return result  # result[lev][line][0 or 1] -> x / y (interpol. x_grid / y_grid)

def contour_rectgrid(x_grid, y_grid, z, levels):
    '''calculate the contours of z on the rectangular grid x_grid, y_grid at
    levels.

    xarr and yarr are 1d arrays which hold the x/y coordinates of the grid.
    They do not need to be equispaced nor of same length.

    z[y, x] holds the value of some scalar function on that
    grid.
    
    levels is a list of float values for which the contours shall be
    calculated.

    Returns a list of equal length to levels. Each entry is a set of contour
    lines for the corresponding level value.

    A set of contour lines is a list which contains 2-element lists
    [xarr, yarr]. xarr and yarr hold the points of one contour line in cartesic
    coordinates.
    
    xarr = result[levidx][lineidx][0]
    yarr = result[levidx][lineidx][1]'''
    result = []
    dx_grid = x_grid[1:] - x_grid[:-1]  # x_n+1 - x_n
    dy_grid = y_grid[1:] - y_grid[:-1]  # y_n+1 - y_n
    for level in levels:
        lines = contour_graph(z, level)
        translated_lines = []
        for line in lines:
            interp_y, xind, yind, weights = map(array, line)
            xcoord = where(interp_y,
                        x_grid[xind],
                        x_grid[xind] + weights*dx_grid[xind-1])
            ycoord = where(interp_y,
                        y_grid[yind] + weights*dy_grid[yind-1],
                        y_grid[yind])
            translated_lines.append([xcoord, ycoord])
        result.append(translated_lines)
    return result

def contour_nogrid(z, levels):
    '''calculate the contours of z on a rectangular, equispaced grid at levels.

    z[y, x] holds the value of some scalar function on that
    grid. y and x are taken equispaced with a step length of 1.
    
    levels is a list of float values for which the contours shall be
    calculated.

    Returns a list of equal length to levels. Each entry is a set of contour
    lines for the corresponding level value.

    A set of contour lines is a list which contains 2-element lists
    [xarr, yarr]. xarr and yarr hold the points of one contour line in cartesic
    coordinates.
    
    xarr = result[levidx][lineidx][0]
    yarr = result[levidx][lineidx][1]'''
    return contour_rectgrid(arange(z.shape[1]), arange(z.shape[0]), z, levels)
        
def contour_graph(z, level):
    '''calculate contour of z at level.

    z[y,x] has to be a 2d array.

    Returns a list of 4-element lists. Each entry represents one contour.
    Each entry is [interp_y, xind, yind, weight] where all four are 1d lists
    of equal size.
    
    Imagine a rectangular grid where the crossings are the points of z. All
    points of the result are located on this grid. For point n:
    if interp_y[n] is True, the point is on a vertical line, else on a
    horizontal line.
    
    If it is on a vertical line, xind[n] gives the corresponding index into z.
    The y position is between yind[n] and yind[n]+1. weight[n] is a number
    between 0.0 and 1.0 giving the position: 0 means the point is on yind[n]
    exactly, 1.0 means the point is on yind[n]+1 exactly.
    
    If the point is on a horizontal line, weight[n] denotes the position
    between xind[n] and xind[n]+1.

    result[lineidx][0..3][pointidx]
    '''
    bw = (z>level)                  # "black and white" image of z
    horiz = (bw[:,:-1] != bw[:,1:]) # True where a contour crosses rows
    vert = (bw[:-1] != bw[1:])      # True where a contour crosses columns
    # for later readability
    up, down, left, right = 1, 4, 2, 8
    # adjacency & up means crosspoint at y (top), & left: at x (left),
    # & down: at y+1, & right: at x+1
    # adjacency[y, x] is the cell between x...x+1 and y...y+1
    adjacency = (horiz[:-1,:]*up | vert[:,:-1]*left |
                 horiz [1:,:]*down | vert[:,1:]*right)

    # calculate interpolation weights and store in horiz, vert
    # weight = (level - z[n])/(z[n+1]-z[n])
    # -1 => dummy value (no crossing)
    horiz = where(horiz, (level-z[:,:-1]) / (z[:,1:]-z[:,:-1]), -1)
    vert = where(vert, (level-z[:-1]) / (z[1:]-z[:-1]), -1)
    
    result = []
    def _appendpoint(line, x, y, direction):
        '''append the point adjacency[y,x], direction translated into grid
        coordinates and remove from adjacency.
        returns tuple (bool, x, y, weight)
        bool: False means on horizontal grid, True on vertical grid
        weight is the position between x and x+1 resp y and y+1'''
        adjacency[y, x] ^= direction   # XOR out direction
        if direction & (up|down):
            if direction & down:
                y += 1
            assert horiz[y,x] > -1      # for debugging
            line[0].append(False)
            line[1].append(x)
            line[2].append(y)
            line[3].append(horiz[y, x])
        else:
            # direction is left or right
            if direction & right:
                x += 1
            assert vert[y, x] > -1      # for debugging
            line[0].append(True)
            line[1].append(x)
            line[2].append(y)
            line[3].append(vert[y,x])
    # end def
    opposite = {up:down, down:up, left:right, right:left}
    while any(adjacency != 0):
        # first look if there are any contours ending at the borders of z
        border = True
        # top border
        if any(adjacency[0] & up):
            x0 = nonzero(adjacency[0] & up)[0][0]  # just take first one
            y0 = 0
            orig = up                   # where we come from
        # bottom
        elif any(adjacency[-1] & down):
            x0 = nonzero(adjacency[-1] & down)[0][0]
            y0 = adjacency.shape[0] - 1
            orig = down
        # left
        elif any(adjacency[:,0] & left):
            x0 = 0
            y0 = nonzero(adjacency[:,0] & left)[0][0]
            orig = left
        # right border
        elif any(adjacency[:,-1] & right):
            x0 = adjacency.shape[1] - 1
            y0 = nonzero(adjacency[:,-1] & right)[0][0]
            orig = right
        else:  # pick an arbitrary point (all contours are closed loops now)
            m = adjacency.argmax()
            # FIXME: This is not very pretty! forward compatible?!
            x0, y0 = m%adjacency.shape[1], m/adjacency.shape[1]
            border = False              # did not start from border
            adj = adjacency[y0, x0]
            if adj & up:
                orig = up
            elif adj & down:
                orig = down
            elif adj & left:
                orig = left
            else:
                # There can be only 2 or 4 ends, so adj&right only is an error
                raise 'Dead end at r%d,c%d -- should be impossible!'%(y0,x0)
        # okay now we have starting cell x0,y0 and direction orig.
        endofcontour = False   # set when border reached or closed
        line = [[], [], [], []]
        while not endofcontour:
            # append last point
            _appendpoint(line, x0, y0, orig)
            # find next point
            adj = adjacency[y0, x0]
            if (adj | orig) == 15:      # all directions possible, hm...
                # lets connect cross-wise
                # this might create weird results with multiple contours
                cont = opposite[orig]
            else:   # only one continuation - no problem :-D
                cont = adj
            newx0 = x0 + {up:0, down:0, left:-1, right:1}[cont]
            newy0 = y0 + {up:-1, down:1, left:0, right:0}[cont]
            orig = opposite[cont]
            # out of bounds
            if border and ((not 0<=newx0<adjacency.shape[1]) or
                           (not 0<=newy0<adjacency.shape[0])):
                _appendpoint(line, x0, y0, cont)
                endofcontour = True
            else:
                adjacency[y0, x0] ^= cont
                x0, y0 = newx0, newy0
                # loop closed
                if adjacency[y0, x0] & orig == 0:
                    _appendpoint(line, x0, y0, orig)
                    adjacency[y0, x0] ^= orig
                    endofcontour = True
        result.append(line)
    return result
