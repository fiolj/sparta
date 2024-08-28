
.. _history:




.. _history-future:



##################
Future and history
##################




This section lists features we are planning to add to SPARTA, features
of previous versions of SPARTA, and features of other parallel
molecular dynamics codes I've distributed.



:ref:`Coming attractions<history-coming-attraction>`
:ref:`Past versions<history-past-versions>`







.. _history-coming-attraction:



******************
Coming attractions
******************




The `wish list link <http://sparta.sandia.gov/future.html>`__ on the
SPARTA web page gives a list of features we are planning to add to
SPARTA in the future.  Please contact the
`developers <_http://sparta.sandia.gov/authors.html>`__ you are interested
in contributing to the those developments or would be a future user of
that feature.



You can also send `email to the developers <http://sparta.sandia.gov/authors.html>`__ if you want to add
your wish to the list.






.. _history-past-versions:



*************
Past versions
*************




Sandia's predecessor to SPARTA is a DSMC code called ICARUS.  It was
developed in the early 1990s by Tim Bartel and `Steve Plimpton <http>`__://www.sandia.gov/~sjplimp.  It was later modified and
extended by Michael Gallis.



ICARUS is a 2d code, written in Fortran, which models the flow
geometry around bodies with a collection of adjoining body-fitted grid
blocks.  The geometry of the grid cells within in a single block is
represented with analytic equations, which allows for fast particle
tracking.



Some details about ICARUS, including simulation snapshots and papers,
are discussed on `this page <http>`__://www.sandia.gov/~sjplimp/dsmc.html



Performance-wise ICARUS scaled quite well on several generations of
parallel machines, and is still used by Sandia researchers today.
ICARUS was export-controlled software, and so was not distributed
widely outside of Sandia.



SPARTA development began in late 2011.  In contrast to ICARUS, it is a
3d code, written in C++, and uses a hierarchical Cartesian grid to
track particles.  Surfaces are embedded in the grid, which cuts and
splits their flow volumes.



The `Authors link <http://sparta.sandia.gov/history.html>`__ on the SPARTA
web page gives a timeline of features added to the code since it's
initial open-source release.



