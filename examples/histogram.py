"""Plot a histogram."""


from pyxgraph import *
from scipy import io

def plot_histogram(epsoutfile, x):
    
    g = pyxgraph(width=6, height=6,
                 key=None,
                 xlabel="x", 
                 xlimits=(min(x),max(x))
                )
    g.pyxplothist(x, Nbins = 100, bin_range=(min(x),max(x)), bars=0)
    
    g.pyxsave(epsoutfile)


if __name__=="__main__":    
    x = io.read_array("data_histogram.dat")
    plot_histogram("histogram.eps", x)
