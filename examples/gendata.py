
from scipy import *
        
        
        
def gen_data(fname="test_data.dat"):
    """Generate some moderately interesting data."""
    x = arange(0.0+1e-6, 10.1, 0.2)
    y1 = 0.2*x*sin(x)
    y2 = 0.3*x**2*cos(x)
    y3 = 0.01*x**3*cos(x)
    y4 = 3.0*x*sin(x)/x
    y5 = 2.0*x*sin(x)/x
    io.write_array(fname, zip(x, y1, y2, y3, y4, y5))

def gen_data2(fname="test_data2.dat"):
    """Generate some really interesting data."""
    x = arange(0.0+1e-6, 10.1, 0.2)
    y1 = x**2
    y2 = x**4
    y3 = exp(x)
    y4 = exp(-x)
    y5 = sqrt(x)
    io.write_array(fname, zip(x, y1, y2, y3, y4, y5))


def gen_data_all():
    """Generate all data."""
    gen_data()
    gen_data2()


if __name__=="__main__":
    gen_data_all()

