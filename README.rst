
========
PyXgraph
========


Introduction
============

`PyX <http://pyx.sourceforge.net/>`_
allows to generate publication quality postscript and pdf.
Convince yourself by looking at the 
`examples <http://pyx.sourceforge.net/examples/index.html>`_

PyX is extremely flexible and well designed,
see the `documentation <http://pyx.sourceforge.net/documentation.html>`_
(pdf and FAQ).

However, for slightly more complicated graphs
the code can become very extensive.
PyXgraph tries to address this problem by setting up
some routines to make plotting simpler.


Notes:

- documentation needs to be written
- not everything is implemented yet
- addition of new features etc. is very welcome
- the file TODO contains a list of things which should be done.
  In addition many FIXMEs are scattered throughout the code...

These are the places where **your** contributions are needed!!


Usage
=====

Just set your ``PYTHONPATH`` accordingly::

  export PYTHONPATH=path_to_the_PyXGraph_directory:$PYTHONPATH

(You can put the above line into your ``.zshrc``)

Note that the examples work without this.


Documentation
=============

So far none. 
Study the examples in the ``examples`` directory.

Overview of all examples
------------------------

If ``imagemagick`` (for ``convert``) and ``rest2html`` 
are installed, on Linux just do::

  cd examples
  python make_html.py
  
and point your web-browser at the resulting ``examples.html``.



Notes on Installing PyX
=======================

Get the latest release (currently 0.10) from http://pyx.sourceforge.net/
(or from your linux distribution).

Installation from source:
  cd /tmp 
  tar xzf PyX-0.10.tar.gz
  cd PyX-0.10
  # Instalation instructions:
  more INSTALL
  # edit setup.cfg accordingly (optional!):
  #    build_t1code=1
  #    build_pykpathsea=1
  # install the dev package for libkpathsea   (on debian ;-)
  aptitude install libkpathsea-dev
  xemacs setup.cfg &
  export PYXDIR=$HOME/Python/Modules
  python setup.py install --prefix=$PYXDIR
