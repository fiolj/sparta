
:orphan:

.. index:: python

.. _python:

.. _python-mixture-command:

###############
mixture command
###############

.. _python-syntax:

*******
Syntax:
*******

::

   python mode keyword args ...

- mode = *source* or *name* of a Python function 

- if mode is *source*:

  keyword = *here* or name of a *Python file*
    *here* arg = inline
       inline = one or more lines of Python code which will be executed immediately
                  must be a single argument, typically enclosed between triple quotes
    *Python file* = name of a file with Python code which will be executed immediately

- if mode is *name* of a Python function:

::

     one or more keywords with/without arguments must be appended
     keyword = *invoke* or *input* or *return* or *format* or *length* or *file* or *here* or *exists*
       *invoke* arg = logreturn (optional)
          invoke the previously-defined Python function
          if logreturn is specified, print the return value of the invoked function to the screen and logfile
       *input* args = N i1 i2 ... iN
         N = # of inputs to function
         i1,...,iN = value, SELF, or SPARTA variable name
           value = integer number, floating point number, or string
           SELF = reference to SPARTA itself which can then be accessed by Python function
           variable = v_name, where name = name of SPARTA variable, e.g. v_abc
           internal variable = iv_name, where name = name of a SPARTA internal-style variable, e.g. iv_xyz
       *return* arg = varReturn
         varReturn = v_name  = SPARTA variable name which the return value of the Python function will be assigned to
       *format* arg = fstring with M characters
         M = N if no return value, where N = # of inputs
         M = N+1 if there is a return value
         fstring = each character (i,f,s,p) corresponds (in order) to an input or return value
           'i' = integer, 'f' = floating point, 's' = string, 'p' = SELF
        *length* arg = Nlen
          Nlen = max length of string returned from Python function
        *file* arg = filename
          filename = file of Python code, which defines the Python function
        *here* arg = one or more lines of Python code which defines the Python function
                     must be a single argument, typically enclosed between triple quotes
        *exists* arg = none = Python code has been loaded by previous python command

.. _python-examples:

*********
Examples:
*********

::

   python source funcdef.py
   python pForce input 2 v_x 20.0 return v_f format fff file force.py
   python pForce invoke

::

   python factorial input 1 myN return v_fac format ii here """
   def factorial(n):
     if n == 1: return n
     return n \* factorial(n-1)
   """

::

   python source funcdef.py
   python source here "from sparta import sparta"

.. _python-descriptio:

************
Description:
************

The *python* command interfaces SPARTA with an embedded Python
interpreter and enables executing arbitrary python code in that
interpreter.  This can be done immediately, by using *mode* =
*source*.  Or execution can be deferred, by registering a Python
function for later execution, by using *mode* = *name* of a Python
function.

Later execution can be triggered in one of two ways.  One is to use
the python command again with its *invoke* keyword.  The other is to
trigger the evaluation of a python-style, equal-style, particle-style,
grid-style, or surf-style variable.  A python-style variable invokes
its associated Python function; its return value becomes the value of
the python-style variable.  Equal-, particle-, grid-, and surt-style
variables can use a Python function wrapper in their formulas which
encodes the Python function name, and specifies arguments (which
themselves can be numeric formulas) to pass to the Python function
associated with the python-style variable.

As explained on the :ref:`variable<variable>` doc page, the definition
of a python-style variable associates a Python function name with the
variable.  Its specification must match the *mode* argument of the
*python* command for the Python function name.  For example these two
commands would be consistent:

::

   variable foo python myMultiply
   python myMultiply return v_foo format f file funcs.py

The two commands can appear in either order in the input script so
long as both are specified before the Python function is invoked for
the first time.

.. note::

  that python-style, equal-style, particle-style, grid-style, and
  surf-style variables can be used in many different ways within SPARTA.
  They can be evaulated directly in an input script, effectively
  replacing the variable with its value.  Or they can be passed to
  various commands as arguments, so that the variable is evaluated
  multiple times during a simulation run.  See the
  :ref:`variable<variable>` command for more details on variable styles
  which enable Python function evaluation.

The Python code for the function can be included directly in the input
script or in a separate Python file.  The function can be standard
Python code or it can make "callbacks" to SPARTA through its library
interface to query or set internal values within SPARTA.  This is a
powerful mechanism for performing complex operations in a SPARTA input
script that are not possible with the simple input script and variable
syntax which SPARTA defines.  Thus your input script can operate more
like a true programming language.

Use of this command requires building SPARTA with the PYTHON package
which links to the Python library so that the Python interpreter is
embedded in SPARTA.  More details about this process are given below.

A broader overview of how Python can be used with SPARTA is given on
the :ref:`Python interface to SPARTA<python>` doc page.  There
is also an ``examples/python`` directory which illustrates use of the
python command.

----------

The first argument to the *python* command is the *mode* setting,
which is either *source* or the *name* of a Python function.

If *source* is used, it is followed by either the *here* keyword or a
file name containing Python code.  The *here* keyword is followed by a
single *inline* argument which is a string containing one or more
python commands.  The string can either be on the same line as the
*python* command, enclosed in quotes, or it can be multiple lines
enclosed in triple quotes.

.. note::

  that no arguments can be passed to the executed
  Python code.

.. note::

  that only one of those 4 keywords
  is allowed since their operations are mutually exclusive.

.. note::

  that return values of python functions are
  otherwise *only* accessible when the function is invoked indirectly by
  evaluating its associated :ref:`python style variable<variable>`, as
  described below.

.. note::

  that Python code which contains a function definition does NOT
  "execute" the function when it is run; it simply defines the function
  so that it can be invoked later.

The *here* keyword does the same thing, except that the Python code
follows as a single argument to the *here* keyword.  This can be done
using triple quotes as delimiters, as in the examples above and below.
This allows Python code to be listed verbatim in your input script,
with proper indentation, blank lines, and comments, as desired.  See
the :doc:`Commands parse <Commands_parse>` doc page, for an
explanation of how triple quotes can be used as part of input script
syntax.

The *exists* keyword takes no argument.  It simply means that Python
code containing the needed Python function has already been loaded
into the SPARTA Python interpreter, for example by previous *python
source* command or in a file that was loaded previously with the
*file* keyword. This allows use of a single file of Python code which
contains multiple functions, any of which can be used in the same (or
different) input scripts (see below).

.. note::

  that the Python code that is loaded and run by the *file* or
  *here* keyword must contain a function with the specified function
  *name*.  To operate properly when the function is later invoked, the
  code for the function must match the *input* and *return* and *format*
  keywords specified by the python command.  Otherwise Python will
  generate an error.

The other keywords which can be used with the *python* command are
*input*, *return*, *format*, and *length*.

The *input* keyword defines how many arguments *N* the Python function
expects.  If it takes no arguments, then the *input* keyword should
not be used.  Each argument can be specified directly as a value,
e.g. '6' or '3.14159' or 'abc' (a string of characters).  The type of
each argument is specified by the *format* keyword as explained below,
so that Python will know how to interpret the value.  If the word SELF
is used for an argument it has a special meaning.  A pointer is passed
to the Python function which it can convert into a reference to SPARTA
itself using the :ref:`SPARTA Python module<python>`.  This
enables the function to call back to SPARTA through its library
interface as explained below.  This allows the Python function to
query or set values internal to SPARTA which can affect the subsequent
execution of the input script.

.. note::

  that a python-style variable can be used as an
  argument, which means that the a Python function can use arguments
  which invoke other Python functions.

A SPARTA internal-style variable can also be used as an *input*
argument, specified as iv_name, where "name" is the name of the
internal-style variable.  The internal-style variable does not have to
be defined in the input script (though it can be); if it is not
defined, this command creates an :ref:`internal-style variable<variable>` with the specified name.

An internal-style variable must be used when an equal-style,
vector-style, or atom-style variable triggers the invocation of the
Python function defined by this command, by including a Python function
wrapper with arguments in its formula.  Each of the arguments must be
specified as an internal-style variable via the *input* keyword.

.. note::

  that the Python
  function can also have additional inputs, also specified by the *input*
  keyword, which are NOT arguments in the Python function wrapper.  See
  the example below for the ``mixedargs`` Python function.

.. note::

  that as explained
  above with python-style variables, Python function wrappers can be
  nested; a sub-formula for an argument can contain its own Python
  function wrapper which invokes another Python function.

The *return* keyword is only needed if the Python function returns a
value.  The specified *varReturn* is of the form v_name, where "name"
is the name of a python-style SPARTA variable, defined by the
:ref:`variable<variable>` command.  The Python function can return a
numeric or string value, as specified by the *format* keyword.  This
return value is *only* accessible when its associated python-style
variable is evaluated.  When the *invoke* keyword is used, the return
value of the python function is ignored unless the optional
*logreturn* argument is specified.

.. note::

  that it is permissible to use a :ref:`python-style   variable<variable>` in a SPARTA command that allows for an
  equal-style variable as an argument, but only if the output of the
  Python function is flagged as a numeric value ("i" or "f") via the
  *format* keyword.

If the *return* keyword is used and the *format* keyword specifies the
output as a string, then the default maximum length of that string is
63 characters (64-1 for the string terminator).  If you want to return
a longer string, the *length* keyword can be specified with its *Nlen*
value set to a larger number.  SPARTA will then allocate Nlen+1 space
to include the string terminator.  If the Python function generates a
string longer than the default 63 or the specified *Nlen*, it will be
truncated.

This section describes how Python code can be written to work with
SPARTA.

Whether you load Python code from a file or directly from your input
script, via the *file* and *here* keywords, the code can be identical.
It must be indented properly as Python requires.  It can contain
comments or blank lines.  If the code is in your input script, it cannot
however contain triple-quoted Python strings, since that will conflict
with the triple-quote parsing that the SPARTA input script performs.

All the Python code you specify via one or more python commands is
loaded into the Python "main" module, i.e. ``__name__ == '__main__'``.
The code can define global variables, define global functions, define
classes or execute statements that are outside of function
definitions.  It can contain multiple functions, only one of which
matches the name of the Python function specified in the python
command.  This means you can use the *file* keyword once to load
several functions, and the *exists* keyword thereafter in subsequent
python commands to register the other functions that were previously
loaded with SPARTA.

A Python function you define (or more generally, the code you load)
can import other Python modules or classes, it can make calls to other
system functions or functions you define, and it can access or modify
global variables (in the "main" module) which will persist between
successive function calls.  The latter can be useful, for example, to
prevent a function from being invoked multiple times per timestep by
different commands in a SPARTA input script that accesses the returned
python-style variable associated with the function.  For example,
consider this function loaded with two global variables defined
outside the function:

::

   nsteplast = -1
   nvaluelast = 0

::

   def expensive(nstep):
     global nsteplast,nvaluelast
     if nstep == nsteplast: return nvaluelast
     nsteplast = nstep
     # perform complicated calculation
     nvalue = ...
     nvaluelast = nvalue
     return nvalue

The variable 'nsteplast' stores the previous timestep the function was
invoked (passed as an argument to the function).  The variable
'nvaluelast' stores the return value computed on the last function
invocation.  If the function is invoked again on the same timestep, the
previous value is simply returned, without re-computing it.  The
"global" statement inside the Python function allows it to overwrite the
global variables from within the local context of the function.

Also note that if you load Python code multiple times (via multiple
python commands), you can overwrite previously loaded variables and
functions if you are not careful.  E.g. if the code above were loaded
twice, the global variables would be re-initialized, which might not
be what you want.  Likewise, if a function with the same name exists
in two chunks of Python code you load, the function loaded second will
override the function loaded first.

It's important to realize that if you are running SPARTA in parallel,
each MPI task will load the Python interpreter and execute a local
copy of the Python function(s) you define.  There is no connection
between the Python interpreters running on different processors.
This implies three important things.

First, if you put a print or other statement creating output to the
screen in your Python function, you will see P copies of the output,
when running on P processors.  If the prints occur at (nearly) the same
time, the P copies of the output may be mixed together.

It is possible to avoid this issue, by passing the pointer to the
current SPARTA class instance to the Python function via the *input*
SELF argument described above.  The Python function can then use the
Python interface to the SPARTA library interface, and determine the
MPI rank of the current process.  The Python code can then ensure
output will only appear on MPI rank 0.  The following SPARTA input
demonstrates how this could be done. The text 'Hello, SPARTA!' should
be printed only once, even when running SPARTA in parallel.

::

   python python_hello input 1 SELF format p here """
   def python_hello(handle):
     from SPARTA import SPARTA
     sparta = SPARTA(ptr=handle)
     me = sparta.extract_setting('world_rank')
     if me == 0: print('Hello, SPARTA!')
   """
   python python_hello invoke

Second, if your Python code loads Python modules that are not
pre-loaded by the Python library, then it will load the module from
disk.  This may be a bottleneck if 1000s of processors try to load a
module at the same time.  On some large supercomputers, loading of
modules from disk by Python may be disabled.  In this case you would
need to pre-build a Python library that has the required modules
pre-loaded and link SPARTA with that library.

Third, if your Python code calls back to SPARTA (discussed in the next
section) and causes SPARTA to perform an MPI operation requiring
global communication (e.g. via MPI_Allreduce), such as computing the
global temperature of the system, then you must ensure all your Python
functions (running independently on different processors) call back to
SPARTA.  Otherwise the code may hang.

As mentioned above, your Python function can "call back" to SPARTA
through its library interface, if you use the SELF input to pass
Python a pointer to SPARTA.  The mechanism for doing this in your
Python function is as follows:

::

   def foo(handle,...):
      from SPARTA import SPARTA
      sparta = SPARTA(ptr=handle)
      sparta.command('print "Hello from inside Python"')
      ...

The function definition must include a variable ('handle' in this
case) which corresponds to SELF in the *python* command.  The first
line of the function imports the SPARTA Python module <Python_module>.
The second line creates a Python object "sparta" which wraps the
instance of SPARTA that called the function.  The 'ptr=handle'
argument is what makes that happen.  The third line invokes the
command() function in the SPARTA library interface.  It takes a single
string argument which is a SPARTA input script command for SPARTA to
execute, the same as if it appeared in your input script.  In this
case, SPARTA should output

::

   Hello from inside Python

.. note::

  that since the SPARTA print command
  itself takes a string in quotes as its argument, the Python string
  must be delimited with a different style of quotes.

The :ref:`Section python<python>` doc page describes the syntax
for how Python wraps the various functions included in the SPARTA
library interface.

In general, Python can be used to implement a loop with complex logic,
much more so than can be created using the SPARTA :ref:`jump<jump>` and
:ref:`if<if>` commands.

.. important::

  When using the callback mechanism just described,
  recognize that there are some operations you should not attempt
  because SPARTA cannot execute them correctly.  If the Python function
  is invoked between runs in the SPARTA input script, then it should be
  OK to invoke any SPARTA input script command via the library interface
  command() or file() functions, so long as the command would work if it
  were executed in the SPARTA input script directly at the same point.

As noted above, a Python function can be invoked during a run,
whenever an associated python-style variable it is assigned to is
evaluated.

If the variable is an input argument to another SPARTA command
(e.g. :ref:`fix custom<fix-custom>`), then the Python function will be
invoked inside the class for that command, possibly in one of its
methods that is invoked in the middle of a timestep.  You cannot
execute arbitrary input script commands from the Python function
(again, via the command() or file() functions) at that point in the
run and expect it to work.  Other library functions such as those that
invoke computes or other variables may have hidden side effects as
well.  In these cases, SPARTA has no simple way to check that
something illogical is being attempted.

As noted above, a Python function can also be invoked within the
formula for an equal-style, particle-style, grid-style, or surf-style
variable.  This means the Python function will be invoked whenever the
variable is invoked.  In the case of a particle-, grid-, or
surf--style variable, the Python function can be invoked once per
particle, grid cell, or surface element.

Here are three simple examples using equal-style, particle-style, and
grid-style variables to trigger execution of a Python function.  See
the examples/python/in.circle.pyvar input script for more details.
Assume the file truncate.py includes this Python code:

::

   def truncate(x):
     return int(x)

Then consider these input script lines:

variable        foo python truncate
python          truncate return v_foo input 1 iv_arg format fi file truncate.py
variable        scalar equal py_foo(vol)
print           "TRUNCATED volume $*vol+2.5*"

.. note::

  that the *input* keyword for
  the *python* command, specifies an internal-style variable named "arg"
  as iv_arg which is required to invoke the Python function from a
  Python function wrapper.

The last 2 lines of the equal-style variable example can be replaced
by these to define grid-style variables which invoke the same Python
"truncate" function:

::

   compute         1 property/grid all xc yc
   variable        xnew grid py_foo(c_1**1**)
   variable        ynew grid py_foo(c_1**2**)
   dump            1 grid all 1000 dump.grid.pyvar id xc yc v_xnew v_ynew

When the dump command invokes the 2 grid-style variables, their
arguments c_1\[1\] and c_1\[2\] Python function wrapper are the cell
center coordinates of each grid cell.  The Python "truncate" function
is thus invoked twice for each grid cell, and the truncated coordinate
values for each grid cell are written to the dump file.

The last 2 lines of the equal-style variable example can be replaced
by these to define particle-style variables which invoke the same
Python "truncate" function:

variable        xx particle py_foo(x)
variable        yy particle py_foo(y)
dump            2 particle all 1000 dump.particle.pyvar id x y v_xx v_yy

When the dump command invokes the 2 particle-style variables, their
arguments x and y in the Python function wrapper are the x,y
coordinates of each particle.  The Python "truncate" function is thus
invoked twice for each particle, and the truncated coordinate values
for each particle are written to the dump file.

.. note::

  that when using a Python function wrapper in a variable,
  arguments can be passed to the Python function either from the
  variable formula or by *input* keyword to the *python command.

Assume the file mixedargs.py includes this Python code:

::

   def mixedargs(a,b,x,y,z,flag):
     ...
     return result

Now consider these (made up) commands:

::

   variable        foo python mixedargs
   python          mixedargs return v_foo input 6 7.5 v_myValue iv_arg1 iv_argy iv_argz v_flag &
                   format fffffsf file mixedargs.pt
   variable        flag string optionABC
   variable        myValue equal "2.0\*np"
   compute         1 property/grid all xc yc zc
   compute         2 grid all n
   variable        field grid py_foo(c_1**1**+3.0,sqrt(c_1**2**),(c_1**3**-zlo)\*c_2**1**)

They define a Python "mixedargs" function with 6 arguments.  Three of
them are internal-style variables, which the variable formula
calculates as numeric values for each grid cell and passes to the
function.  In this example, these arguments are themselves small
formulas containing the x,y,z coordinates of each grid cell as well as
a per-grid compute (c_2) and stats keyword (zlo).

The other three arguements (7.5,v_myValue,v_flag) are defined by the
{python* command.  The first and last are constant values (7.5 and the
optionABC string).  The second argument (myValue) is the result of an
equal-style variable formula which accesses the total particle count
(np).

The "result" returned by each invocation of the Python "mixedargs"
function becomes the per-grid value in the grid-style "field"
variable, which could be output to a dump file or used elsewhere in
the input script.

If you run Python code directly on your workstation, either
interactively or by using Python to launch a Python script stored in a
file, and your code has an error, you will typically see informative
error messages.  That is not the case when you run Python code from
SPARTA using an embedded Python interpreter.  The code will typically
fail silently.  SPARTA will catch some errors but cannot tell you
where in the Python code the problem occurred.  For example, if the
Python code cannot be loaded and run because it has syntax or other
logic errors, you may get an error from Python pointing to the
offending line, or you may get one of these generic errors from
SPARTA:

   - Could not process Python file 
   - Could not process Python string

When the Python function is invoked, if it does not return properly,
you will typically get this generic error from SPARTA:

   - Python function evaluation failed

Here are three suggestions for debugging your Python code while
running it under SPARTA.

First, don't run it under SPARTA, at least to start with!  Debug it
using plain Python.  Load and invoke your function, pass it arguments,
check return values, etc.

Second, add Python print statements to the function to check how far
it gets and intermediate values it calculates.  See the discussion
above about printing from Python when running in parallel.

Third, use Python exception handling.  For example, say this statement
in your Python function is failing, because you have not initialized the
variable foo:

::

   foo += 1

If you put one (or more) statements inside a "try" statement,
like this:

::

   import exceptions
   print("Inside simple function")
   try:
     foo += 1      # one or more statements here
   except Exception as e:
     print("FOO error:", e)

then you will get this message printed to the screen:

::

   FOO error: local variable 'foo' referenced before assignment

If there is no error in the try statements, then nothing is printed.
Either way the function continues on (unless you put a return or
sys.exit() in the except clause).

.. _python-restrictio:

*************
Restrictions:
*************

This command is part of the PYTHON package.  It is only enabled if
SPARTA was built with that package.  See the :ref:`Section start 3<start-making-sparta-optional-packages>` doc page for more info.

Building SPARTA with the PYTHON package will link SPARTA with the Python
library on your system.  Settings to enable this are in the
lib/python/Makefile.SPARTA file.  See the lib/python/README file for
information on those settings.

If you use Python code which calls back to SPARTA, via the SELF input
argument explained above, there is an extra step required when
building SPARTA.  SPARTA must also be built as a shared library; see the
:ref:`Section start 2.4<start-building-sparta-library>` doc page.
And your Python function must be able to load the Python module that
wraps the SPARTA library interface.

.. note::

  that it is important that
  the stand-alone SPARTA executable and the SPARTA shared library be
  consistent (built from the same source code files) in order for this
  to work.  If the two have been built at different times using
  different source files, problems may occur.

Another limitation of calling back to Python from the SPARTA module
using the python command in a SPARTA input is that both the Python
interpreter and SPARTA, must be linked to the same Python runtime as a
shared library.  If the Python interpreter is linked to Python
statically (which seems to happen with Conda) then loading the shared
SPARTA library will create a second python "main" module that hides
the one from the Python interpreter and all previous defined function
and global variables will become invisible.

.. _python-related-commands:

*****************
Related commands:
*****************

:ref:`shell<shell>`, :ref:`variable<howto-variables-generate-values-output>`,html

.. _python-default:

********
Default:
********

none

