

.. _python-11-interface-sparta:

##############################
11. Python interface to SPARTA
##############################

This section describes various ways that SPARTA and Python can be used
together.

   - 11.1 :ref:`Building SPARTA as a shared library<python-building-sparta-shared-library>`
   - 11.2 :ref:`Installing the Python wrapper into Python<python-installing-wrapper-into>`
   - 11.3 :ref:`Extending Python with MPI to run in parallel<python-extending-mpi-run-parallel>`
   - 11.4 :ref:`Testing the Python-SPARTA interface<python-testing-pythonspar-interface>`
   - 11.5 :ref:`Using SPARTA from Python<python-sparta>`
   - 11.6 :ref:`Example Python scripts that use SPARTA<python-example-scripts-sparta>`
   - 11.7 :ref:`Calling Python from SPARTA<python-calling-sparta>`

If you are not familiar with `Python <https://www.python.org>`_, it is
a powerful scripting and programming language which can do almost
everything that compiled languages like C, C++, or Fortran can do in
fewer lines of code. It also comes with a large collection of add-on
modules for many purposes (either bundled or easily installed from
Python code repositories).  The major drawback is slower execution
speed of the script code compared to compiled programming languages.
But when the script code is interfaced to optimized compiled code,
performance can be on par with a standalone executable, so long as the
scripting is restricted to high-level operations.  Thus Python is also
convenient to use as a "glue" language to "drive" a program like
SPARTA through its library interface, or to hook multiple pieces of
software together, such as a simulation code and a visualization tool,
or to run a coupled multi-scale or multi-physics model.

The SPARTA distribution includes the file python/sparta.py which wraps
the library interface to SPARTA.  That interface is exposed to Python
either when calling SPARTA from Python or when calling Python from a
SPARTA input script and then calling back to SPARTA from Python code.
It is a C-library interface which is designed to be easy to add
functionality to, thus the Python interface to SPARTA is easy to
extend as well.

The Python wrapper for SPARTA uses the amazing "ctypes" package in
Python, which auto-generates the interface code needed between Python
and a set of C interface routines for a library.  Ctypes is part of
standard Python for versions 2.5 and later.  You can check which
version of Python you have installed, by simply typing "python" at a
shell prompt.

If you create interesting Python scripts that run SPARTA or
interesting Python functions that can be called from a SPARTA input
script, that you think would be generally useful, please post them as
a pull request to our `GitHub site
<https://github.com/sparta/sparta>`_, and they can be added to the
SPARTA distribution or web page.

Before using SPARTA from a Python script, you need to do two things.
You need to build SPARTA as a dynamic shared library, so it can be
loaded by Python.  And you need to tell Python how to find the library
and the Python wrapper file python/sparta.py.  Both these steps are
discussed next.  If you wish to run SPARTA in parallel from Python,
you also need to extend your Python with MPI.  This is also discussed
below.

.. _python-building-sparta-shared-library:

***********************************
Building SPARTA as a shared library
***********************************

Instructions on how to build SPARTA as a shared library are given in
:ref:`Section 2.4<start-building-sparta-library>`.  A shared library is one
that is dynamically loadable, which is what Python requires.  On Linux
this is a library file that ends in ".so", not ".a".

For make, from the src directory, type

::

   make mode=shlib foo

For CMake, from the build directory, tyoe

::

   cmake -C /path/to/sparta/cmake/presets/foo.cmake -DBUILD_SHARED_LIBS=ON /path/to/sparta/cmake
   make

.. note::

  that if you are building multiple machine
  versions of the shared library, the soft link is always set to the
  most recently built version.

If this fails, see :ref:`Section 2.3<start-making-sparta-optional-packages>` for more
details, especially if your SPARTA build uses auxiliary libraries like
MPI which may not be built as shared libraries on your system.

.. _python-installing-wrapper-into:

*****************************************
Installing the Python wrapper into Python
*****************************************

For Python to invoke SPARTA, there are 2 files it needs to know about:

   - python/sparta.py
   - src/libsparta.so

Sparta.py is the Python wrapper on the SPARTA library interface.
Libsparta.so is the shared SPARTA library that Python loads, as
described above.

You can insure Python can find these files in one of two ways:

   - set two environment variables
   - run the python/install.py script

If you set the paths to these files as environment variables, you only
have to do it once.  For the csh or tcsh shells, add something like
this to your ~/.cshrc file, one line for each of the two files:

::

   setenv PYTHONPATH $*PYTHONPATH*:/home/sjplimp/sparta/python
   setenv LD_LIBRARY_PATH $*LD_LIBRARY_PATH*:/home/sjplimp/sparta/src

If you use the python/install.py script, you need to invoke it every
time you rebuild SPARTA (as a shared library) or make changes to the
python/sparta.py file.

You can invoke install.py from the python directory as

::

   % python install.py \[libdir\] \[pydir\]

The optional libdir is where to copy the SPARTA shared library to; the
default is /usr/local/lib.  The optional pydir is where to copy the
sparta.py file to; the default is the site-packages directory of the
version of Python that is running the install script.

.. note::

  that libdir must be a location that is in your default
  LD_LIBRARY_PATH, like /usr/local/lib or /usr/lib.  And pydir must be a
  location that Python looks in by default for imported modules, like
  its site-packages dir.  If you want to copy these files to
  non-standard locations, such as within your own user space, you will
  need to set your PYTHONPATH and LD_LIBRARY_PATH environment variables
  accordingly, as above.

If the install.py script does not allow you to copy files into system
directories, prefix the python command with "sudo".  If you do this,
make sure that the Python that root runs is the same as the Python you
run.  E.g. you may need to do something like

::

   % sudo /usr/local/bin/python install.py \[libdir\] \[pydir\]

You can also invoke install.py from the make command in the src
directory as

::

   % make install-python

In this mode you cannot append optional arguments.  Again, you may
need to prefix this with "sudo".  In this mode you cannot control
which Python is invoked by root.

.. note::

  that if you want Python to be able to load different versions of
  the SPARTA shared library (see :ref:`this section<python-sparta>` below), you will
  need to manually copy files like libsparta_g++.so into the appropriate
  system directory.  This is not needed if you set the LD_LIBRARY_PATH
  environment variable as described above.

.. _python-extending-mpi-run-parallel:

********************************************
Extending Python with MPI to run in parallel
********************************************

If you wish to run SPARTA in parallel from Python, you need to extend
your Python with an interface to MPI.  This also allows you to
make MPI calls directly from Python in your script, if you desire.

There are several Python packages available that purport to wrap MPI
as a library and allow MPI functions to be called from Python.

These include

   - `pyMPI <http://pympi.sourceforge.net/>`__
   - `maroonmpi <http://code.google.com/p/maroonmpi/>`__
   - `mpi4py <http://code.google.com/p/mpi4py/>`__
   - `myMPI <http>`__://nbcr.sdsc.edu/forum/viewtopic.php?t=89&sid=c997fefc3933bd66204875b436940f16
   - `Pypar <http://code.google.com/p/pypar>`__

All of these except pyMPI work by wrapping the MPI library and
exposing (some portion of) its interface to your Python script.  This
means Python cannot be used interactively in parallel, since they do
not address the issue of interactive input to multiple instances of
Python running on different processors.  The one exception is pyMPI,
which alters the Python interpreter to address this issue, and (I
believe) creates a new alternate executable (in place of "python"
itself) as a result.

In principle any of these Python/MPI packages should work to invoke
SPARTA in parallel and MPI calls themselves from a Python script which
is itself running in parallel.  However, when I downloaded and looked
at a few of them, their documentation was incomplete and I had trouble
with their installation.  It's not clear if some of the packages are
still being actively developed and supported.

The one I recommend, since I have successfully used it with SPARTA, is
Pypar.  Pypar requires the ubiquitous `Numpy package <http://numpy.scipy.org>`__ be installed in your Python.  After
launching python, type

::

   import numpy

to see if it is installed.  If not, here is how to install it (version
1.3.0b1 as of April 2009).  Unpack the numpy tarball and from its
top-level directory, type

::

   python setup.py build
   sudo python setup.py install

The "sudo" is only needed if required to copy Numpy files into your
Python distribution's site-packages directory.

To install Pypar (version pypar-2.1.4_94 as of Aug 2012), unpack it
and from its "source" directory, type

::

   python setup.py build
   sudo python setup.py install

Again, the "sudo" is only needed if required to copy Pypar files into
your Python distribution's site-packages directory.

If you have successully installed Pypar, you should be able to run
Python and type

::

   import pypar

without error.  You should also be able to run python in parallel
on a simple test script

::

   % mpirun -np 4 python test.py

where test.py contains the lines

::

   import pypar
   print "Proc %d out of %d procs" % (pypar.rank(),pypar.size())

and see one line of output for each processor you run on.

.. important::

  To use Pypar and SPARTA in parallel from Python, you
  must insure both are using the same version of MPI.  If you only have
  one MPI installed on your system, this is not an issue, but it can be
  if you have multiple MPIs.  Your SPARTA build is explicit about which
  MPI it is using, since you specify the details in your lo-level
  src/MAKE/Makefile.foo file.  Pypar uses the "mpicc" command to find
  information about the MPI it uses to build against.  And it tries to
  load "libmpi.so" from the LD_LIBRARY_PATH.  This may or may not find
  the MPI library that SPARTA is using.  If you have problems running
  both Pypar and SPARTA together, this is an issue you may need to
  address, e.g. by moving other MPI installations so that Pypar finds
  the right one.

.. _python-testing-pythonspar-interface:

***********************************
Testing the Python-SPARTA interface
***********************************

To test if SPARTA is callable from Python, launch Python interactively
and type:

::

   >>> from sparta import sparta
   >>> spa = sparta()

If you get no errors, you're ready to use SPARTA from Python.  If the
2nd command fails, the most common error to see is

::

   OSError: Could not load SPARTA dynamic library

which means Python was unable to load the SPARTA shared library.  This
typically occurs if the system can't find the SPARTA shared library or
one of the auxiliary shared libraries it depends on, or if something
about the library is incompatible with your Python.  The error message
should give you an indication of what went wrong.

You can also test the load directly in Python as follows, without
first importing from the sparta.py file:

::

   >>> from ctypes import CDLL
   >>> CDLL("libsparta.so")

If an error occurs, carefully go thru the steps in :ref:`Section 4<start-building-sparta-library>` and above about building a shared
library and about insuring Python can find the necessary two files it
needs.

.. _python-test-sparta-serial:

Test SPARTA and Python in serial:
=================================

.. _python:

To run a SPARTA test in serial, type these lines into Python
interactively from the bench directory:

::

   >>> from sparta import sparta
   >>> spa = sparta()
   >>> spa.file("in.free")

Or put the same lines in the file test.py and run it as

::

   % python test.py

Either way, you should see the results of running the in.free
benchmark on a single processor appear on the screen, the same as if
you had typed something like:

::

   spa_g++ < in.free

You can also pass command-line switches, e.g. to set input script
variables, through the Python interface.

Replacing the "spa = sparta()" line above with

::

   spa = sparta("",**"-v","x","100","-v","y","100","-v","z","100"**)

is the same as typing

::

   spa_g++ -v x 100 -v y 100 -v z 100 < in.free

from the command line.

.. _python-test-sparta-parallel:

Test SPARTA and Python in parallel:
===================================

To run SPARTA in parallel, assuming you have installed the
`Pypar <http>`__://datamining.anu.edu.au/~ole/pypar package as discussed
above, create a test.py file containing these lines:

::

   import pypar
   from sparta import sparta
   spa = sparta()
   spa.file("in.free")
   print "Proc %d out of %d procs has" % (pypar.rank(),pypar.size()),lmp
   pypar.finalize()

You can then run it in parallel as:

::

   % mpirun -np 4 python test.py

and you should see the same output as if you had typed

::

   % mpirun -np 4 spa_g++ < in.lj

.. note::

  that if you leave out the 3 lines from test.py that specify Pypar
  commands you will instantiate and run SPARTA independently on each of
  the P processors specified in the mpirun command.  In this case you
  should get 4 sets of output, each showing that a SPARTA run was made
  on a single processor, instead of one set of output showing that
  SPARTA ran on 4 processors.  If the 1-processor outputs occur, it
  means that Pypar is not working correctly.

Also note that once you import the PyPar module, Pypar initializes MPI
for you, and you can use MPI calls directly in your Python script, as
described in the Pypar documentation.  The last line of your Python
script should be pypar.finalize(), to insure MPI is shut down
correctly.

.. _python-running-scripts:

Running Python scripts:
=======================

.. note::

  that any Python script (not just for SPARTA) can be invoked in
  one of several ways:

::

   % python foo.script
   % python -i foo.script
   % foo.script

The last command requires that the first line of the script be
something like this:

::

   #!/usr/local/bin/python 
   #!/usr/local/bin/python -i

where the path points to where you have Python installed, and requires
that you have made the script file executable:

::

   % chmod +x foo.script

Without the "-i" flag, Python will exit when the script finishes.
With the "-i" flag, you will be left in the Python interpreter when
the script finishes, so you can type subsequent commands.  As
mentioned above, you can only run Python interactively when running
Python on a single processor, not in parallel.

.. _python-sparta:

************************
Using SPARTA from Python
************************

The Python interface to SPARTA consists of a Python "sparta" module,
the source code for which is in python/sparta.py, which creates a
"sparta" object, with a set of methods that can be invoked on that
object.  The sample Python code below assumes you have first imported
the "sparta" module in your Python script, as follows:

::

   from sparta import sparta

These are the methods defined by the sparta module.  If you look
at the file src/library.cpp you will see that they correspond
one-to-one with calls you can make to the SPARTA library from a C++ or
C or Fortran program.

::

   spa = sparta()           # create a SPARTA object using the default libsparta.so library
   spa = sparta("g++")      # create a SPARTA object using the libsparta_g++.so library
   spa = sparta("",list)    # ditto, with command-line args, e.g. list = \["-echo","screen"\]
   spa = sparta("g++",list)

::

   spa.close()              # destroy a SPARTA object

::

   spa.file(file)           # run an entire input script, file = "in.lj"
   spa.command(cmd)         # invoke a single SPARTA command, cmd = "run 100"

::

   fnum = spa.extract_global(name,type) # extract a global quantity
                                        # name = "dt", "fnum", etc
   				     # type = 0 = int
   				     #        1 = double

::

   temp = spa.extract_compute(id,style,type) # extract value(s) from a compute
                                             # id = ID of compute
   					  # style = 0 = global data
   					  #	    1 = per particle data
   					  #	    2 = per grid cell data
   					  #	    3 = per surf element data
   					  # type = 0 = scalar
   					  #	   1 = vector
   					  #        2 = array

::

   var = spa.extract_variable(name,flag)  # extract value(s) from a variable
   	                               # name = name of variable
   				       # flag = 0 = equal-style variable
   				       #        1 = particle-style variable

.. important::

  Currently, the creation of a SPARTA object from within
  sparta.py does not take an MPI communicator as an argument.  There
  should be a way to do this, so that the SPARTA instance runs on a
  subset of processors if desired, but I don't know how to do it from
  Pypar.  So for now, it runs with MPI_COMM_WORLD, which is all the
  processors.  If someone figures out how to do this with one or more of
  the Python wrappers for MPI, like Pypar, please let us know and we
  will amend these doc pages.

.. note::

  that you can create multiple SPARTA objects in your Python
  script, and coordinate and run multiple simulations, e.g.

::

   from sparta import sparta
   spa1 = sparta()
   spa2 = sparta()
   spa1.file("in.file1")
   spa2.file("in.file2")

The file() and command() methods allow an input script or single
commands to be invoked.

The extract_global(), extract_compute(), and extract_variable()
methods return values or pointers to data structures internal to
SPARTA.

For extract_global() see the src/library.cpp file for the list of
valid names.  New names can easily be added.  A double or integer is
returned.  You need to specify the appropriate data type via the type
argument.

For extract_compute(), the global, per particle, per grid cell, or per
surface element results calulated by the compute can be accessed.
What is returned depends on whether the compute calculates a scalar or
vector or array.  For a scalar, a single double value is returned.  If
the compute or fix calculates a vector or array, a pointer to the
internal SPARTA data is returned, which you can use via normal Python
subscripting.  See :ref:`Section 6.4<howto-64-output-sparta-(stats,>` of the
manual for a discussion of global, per particle, per grid, and per
surf data, and of scalar, vector, and array data types.  See the doc
pages for individual :ref:`computes<compute>` for a description of what
they calculate and store.

For extract_variable(), an :ref:`equal-style or particle-style variable<variable>` is evaluated and its result returned.

For equal-style variables a single double value is returned and the
group argument is ignored.  For particle-style variables, a vector of
doubles is returned, one value per particle, which you can use via
normal Python subscripting.

As noted above, these Python class methods correspond one-to-one with
the functions in the SPARTA library interface in src/library.cpp and
library.h.  This means you can extend the Python wrapper via the
following steps:

- Add a new interface function to src/library.cpp and src/library.h. 

- Rebuild SPARTA as a shared library.

- Add a wrapper method to python/sparta.py for this interface function.

- You should now be able to invoke the new interface function from a Python script.  Isn't ctypes amazing?

.. _python-example-scripts-sparta:

**************************************
Example Python scripts that use SPARTA
**************************************

There are demonstration Python scripts included in the python/examples
directory of the SPARTA distribution, to illustrate what is possible
when Python wraps SPARTA.

See the python/README file for more details.

SPARTA has several commands which can be used to invoke Python
code directly from an input script:

.. _python-calling-sparta:

**************************
Calling Python from SPARTA
**************************

There are SPARTA input script commands which can invoke Python code directly.

   - :ref:`python<python>`
   - :ref:`python-style variables<varaible>`
   - :ref:`equal-style and grid-style variables with formulas containing Python function wrappers<variable>`

The :ref:`python<python>` command can be used to define and execute a
Python function that you write the code for.  The Python function can
also be assigned to a SPARTA python-style variable via the
:ref:`variable<variable>` command.  Each time the variable is
evaluated, either in the SPARTA input script itself, or by another
SPARTA command that uses the variable, this will trigger the Python
function to be invoked.

The Python function can also be referenced in the formula used to
define an :ref:`equal-style or grid-style variable<variable>`, using
the syntax for a :ref:`Python function wrapper<variable>`.  This make
it easy to pass SPARTA-related arguments to the Python function, as
well as to invoke it whenever the equal- or grid-style variable is
evaluated.  For a grid-style variable it means the Python function can
be invoked once per grid cell, using per-grid properties as arguments
to the function.

The Python code for the function can be included directly in the input
script or in an auxiliary file.  The function can have arguments which
are mapped to SPARTA variables (also defined in the input script) and
it can return a value to a SPARTA variable.  This is thus a mechanism
for your input script to pass information to a piece of Python code,
ask Python to execute the code, and return information to your input
script.

.. note::

  that a Python function can be arbitrarily complex.  It can import
  other Python modules, instantiate Python classes, call other Python
  functions, etc.  The Python code that you provide can contain more
  code than the single function.  It can contain other functions or
  Python classes, as well as global variables or other mechanisms for
  storing state between calls from SPARTA to the function.

The Python function you provide can consist of "pure" Python code that
only performs operations provided by standard Python.  However, the
Python function can also "call back" to SPARTA through its
Python-wrapped library interface, in the manner described above.  This
means it can issue SPARTA input script commands or query and set
internal SPARTA state.  As an example, this can be useful in an input
script to create a more complex loop with branching logic, than can be
created using the simple looping and branching logic enabled by the
:ref:`next<next>` and :ref:`if<if>` commands.

See the :ref:`python<python>` and :ref:`variable<>` <variable>`
command doc pages for more info on using Python from a SPARTA input
script including examples of Python code you can write for both pure
Python operations and callbacks to SPARTA.

