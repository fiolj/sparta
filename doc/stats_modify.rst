:orphan:

.. index:: stats_modify



.. _command-stats-modify:

####################
stats_modify command
####################


*******
Syntax:
*******

::

   stats_modify keyword value ... 

-  one or more keyword/value pairs may be listed
-  keyword = *flush* or *format* or *every*

   ::

        flush value = yes or no
        format values = line string, int string, float string, M string, or none
          string = C-style format string
          M = integer from 1 to N, where N = # of quantities being output
        every value = v_name
          v_name = an equal-style variable name 

*********
Examples:
*********

::

   stats_modify flush yes
   stats_modify format 3 %15.8g
   stas_modify format line "%ld %g %g %15.8g" 

************
Description:
************

Set options for how statistical information is computed and printed by
SPARTA.

The *flush* keyword invokes a flush operation after statistical info is
written to the log file. This insures the output in that file is current
(no buffering by the OS), even if SPARTA halts before the simulation
completes.

The *format* keyword can be used to change the default numeric format of
any of quantities the :ref:`stats_style<command-stats-style>` command
outputs. All the specified format strings are C-style formats, e.g. as
used by the C/C++ printf() command. The *line* keyword takes a single
argument which is the format string for the entire line of stats output,
with N fields, which you must enclose in quotes if it is more than one
field. The *int* and *float* keywords take a single format argument and
are applied to all integer or floating-point quantities output. The
setting for *M string* also takes a single format argument which is used
for the Mth value output in each line, e.g. the 5th column is output in
high precision for "format 5 %20.15g".

The *format* keyword can be used multiple times. The precedence is that
for each value in a line of output, the *M* format (if specified) is
used, else the *int* or *float* setting (if specified) is used, else the
*line* setting (if specified) for that value is used, else the default
setting is used. A setting of *none* clears all previous settings,
reverting all values to their default format.

.. note:: The stats output values *step* and *atoms* are stored internally as 8-byte signed integers, rather than the usual 4-byte signed integers.  When specifying the *format int* option you can use a "%d"-style format identifier in the format string and SPARTA will convert this to the corresponding 8-byte form when it is applied to those keywords. However, when specifying the *line* option or *format M string* option for *step* and *natoms*, you should specify a format string appropriate for an 8-byte signed integer, e.g. one with "%ld".

The *every* keyword allows a variable to be specified which will
determine the timesteps on which statistical output is generated. It
must be an :ref:`equal-style variable<command-variable>`, and is specified as
v_name, where name is the variable name. The variable is evaluated at
the beginning of a run to determine the next timestep at which a dump
snapshot will be written out. On that timestep, the variable will be
evaluated again to determine the next timestep, etc. Thus the variable
should return timestep values. See the stagger() and logfreq() math
functions for :ref:`equal-style variables<command-variable>`, as examples of
useful functions to use in this context. Other similar math functions
could easily be added as options for :ref:`equal-style variables<command-variable>`. In addition, statistical output will
always occur on the first and last timestep of each run.

For example, the following commands will output statistical info at
timesteps 0,10,20,30,100,200,300,1000,2000,etc:

::

   variable   s equal logfreq(10,3,10)
   stats_modify    1 every v_s 

Note that the *every* keyword overrides the output frequency setting
made by the :ref:`stats<command-stats>` command, by setting it to 0. If the
:ref:`stats<command-stats>` command is later used to set the output frequency
to a non-zero value, then the variable setting of the stats_modify every
command will be overridden.

*************
Restrictions:
*************
 none

*****************
Related commands:
*****************

:ref:`command-stats`,
:ref:`command-stats-style`

********
Default:
********


The option defaults are flush = no, format int = "%8d", format float =
"%12.8g", and every = non-variable setting provided by the
:ref:`stats<command-stats>` command.
