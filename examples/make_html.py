"""
Generate examples.html and examples.ps


Requirements:

- convert (from imagemagick, to convert from .eps to .png)
- rst2html (`aptitude install python-docutils`)
- latex


"""
import sys
import os

from doc_string_extract import get_doc_string

# generate data:
import gendata
gendata.gen_data_all()


# this list determines the order in which the examples are included:
files = [
    "simple1.py",
    "simple2_arangeplots.py",
    "simple3_inset.py",
    "simple4_arrows_labels.py",
    "colors.py",
    "colors1.py",
    "symbols.py",
    "styles_example.py",
    "styles_example2.py",
    "styles_example3.py",
    "axes1.py",
    "axes2.py",
    "axes3.py",
    "axes4.py",
    "axes5.py",
    "axes6.py",
    "axes7.py",
    "axes8.py",
    "axes9.py",
    "axes10.py",
    "axes11.py",
    "axes12.py",
    "axes13.py",
    "axes14.py",
    "axes15.py",
    "axes16.py",
    "array1.py",
    "array2.py",
    "array3.py",
    "array4.py",
    "array5.py",
    "histogram.py",
    "errorbars.py",
    "bitmap1.py",
    "bitmap2.py",
    "bitmap3.py",
    "bitmap4.py",
    "matplotlib_pyx.py",
    "make_arrows.py",
    "make_labels_with_arrows.py",
    "amsmath_and_xscale.py",
    "sans_serif_fonts.py",
    "sans_serif_fonts2.py",
    "filled_regions.py",
    "colorbars.py",
    "plot_3d_1.py",
    "plot_3d_2.py",
    ]

exclude_files = ["gendata.py", "make_html.py", "doc_string_extract.py"]



# check for all .py files in this directory
# and append those which are not in the above `files`
for f in os.listdir("."):
    if (not f in files) and (not f in exclude_files):
        if os.path.splitext(f)[1] == ".py":
            print "This file ****%s*** is missing in the list of files here" % f
            print "Could you please add this file at the appropriate place"
            print "in the `files` list of `make_html.py`!"
            print 
            # we don't automatically append because this could include
            # confusing work in progress examples.
            #files.append(f)

print "Running all examples (may take some time)"
os.system("./run_all_examples")

print "######################################################################"
print "Convert all eps to png (may take some time - requires `convert`)"
for f in os.listdir("."):
    if os.path.splitext(f)[1] == ".eps":
        os.system("convert %s %s" % (f,os.path.splitext(f)[0]+".png"))
print "Conversion done"


outdat = "examples.txt"
fpout = open(outdat,"w")
fpout.write(".. contents::")

for f in files:
    fpout.write(".. raw:: LaTeX\n\n")
    fpout.write(r"    \newpage")
    fpout.write("\n\n")

    fpout.write("\n%s\n" % f )
    fpout.write("="*len(f)+"\n\n")
    fpout.write("::\n\n")

    # get the doc-string:
    doc_string = get_doc_string(f)
    for line in doc_string.split("\n"):
        fpout.write("    "+line+"\n")
        
    #example = __import__(fname)
    #if example.__doc__:
    #    for line in example.__doc__.split("\n"):
    #        fpout.write("    "+line+"\n")
    #else:
    #    fpout.write("    PLEASE ADD A DOCSTRING AT THE TOP OF THIS FILE: %s\n"
    #                     % f)
    fname = os.path.splitext(f)[0]
    fpout.write("\n\n\n")
    fpout.write(".. image:: %s\n" % (fname+".png"))
    fpout.write("\n`src <%s>`_ `eps <%s>`_ \n\n\n" % (f,fname+".eps"))
    fpout.write(".. raw:: LaTeX\n\n")
    fpout.write(r"     \VerbatimInput[frame=lines,fontshape=sl,fontsize=\footnotesize]{%s}" % f )
    fpout.write("\n\n")



fpout.write("\n\n")
fpout.close()

print "The following requires rst2html (`apt-get install python-docutils`)"
os.system("rst2html --quiet  %s > examples.html" % outdat)
os.system("rst2latex --stylesheet examples.sty --quiet  %s > tmp_examples.tex" % outdat)
os.system(r"cat tmp_examples.tex | sed 's/.png/.eps/g' > examples.tex")
os.system("latex examples.tex; latex examples.tex; dvips examples ; gv examples.ps &")


