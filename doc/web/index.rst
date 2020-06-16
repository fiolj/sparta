####################
SPARTA Documentation
####################


**Version info:**

The SPARTA "version" is the date when it was released, such as 3 Mar
2014. SPARTA is updated continuously. Whenever we fix a bug or add a
feature, we release it immediately, and post a notice on `this page of
the WWW site <http://sparta.sandia.gov/bug.html>`__. Each dated copy of
SPARTA contains all the features and bug-fixes up to and including that
version date. The version date is printed to the screen and logfile
every time you run SPARTA. It is also in the file src/version.h and in
the SPARTA directory name created when you unpack a tarball, and at the
top of the first page of the manual (this page).

-  If you browse the HTML doc pages on the SPARTA WWW site, they always
   describe the most current version of SPARTA.
-  If you browse the HTML doc pages included in your tarball, they
   describe the version you have.
-  The `PDF file <Manual.pdf>`__ on the WWW site or in the tarball is
   updated about once per month. This is because it is large, and we
   don't want it to be part of very patch.
-  At some point, there also will be a `Developer.pdf <Developer.pdf>`__
   file in the doc directory, which describes the internal structure and
   algorithms of SPARTA. NOTE: as of 21 Apr 2015, this file is not yet
   available.

SPARTA stands for Stochastic PArallel Rarefied-gas Time-accurate
Analyzer.

SPARTA is a Direct Simulation Monte Carlo (DSMC) simulator designed to
run efficiently on parallel computers. It was developed at Sandia
National Laboratories, a US Department of Energy facility, with funding
from the DOE. It is an open-source code, distributed freely under the
terms of the GNU Public License (GPL), or sometimes by request under the
terms of the GNU Lesser General Public License (LGPL).

The primary developers of SPARTA are `Steve
Plimpton <http://www.sandia.gov/~sjplimp>`__, and Michael Gallis who can
be contacted at sjplimp,magalli at sandia.gov. The `SPARTA WWW
Site <http://sparta.sandia.gov>`__ at http://sparta.sandia.gov has more
information about the code and its uses.

--------------

The SPARTA documentation is organized into the following sections. If
you find errors or omissions in this manual or have suggestions for
useful information to add, please send an email to the developers so we
can improve the SPARTA documentation.

Once you are familiar with SPARTA, you may want to bookmark :ref:`this
page <commands-individual>` since it gives quick access to
documentation for all SPARTA commands.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :numbered:

   Section_intro

   Section_start

   Section_commands

   Section_packages

   Section_accelerate

   Section_howto

   Section_example

   Section_perf

   Section_tools

   Section_modify

   Section_python

   Section_errors

   Section_history

   commands

.. only:: html
	  
	  *************
	  Command Index
	  *************

* :ref:`Command index <genindex>`

