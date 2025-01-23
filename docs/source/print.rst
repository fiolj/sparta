
:orphan:

.. index:: print

.. _print:

.. _print-command:

#############
print command
#############

.. _print-syntax:

*******
Syntax:
*******

::

   print string keyword value

- string = text string to print, which may contain variables

- zero or more keyword/value pairs may be appended

- keyword = *file* or *append* or *screen*

::

     *file* value = filename
     *append* value = filename
     *screen* value = *yes* or *no*

.. _print-examples:

*********
Examples:
*********

::

   print "Done with equilibration"
   print 'Done with equilibration'
   print "Done with equilibration" file info.dat

::

   compute myTemp temp
   variable t equal c_myTemp
   print "The system temperature is now $t"

.. _print-descriptio:

************
Description:
************

Print a text string to the screen and logfile.  One line of output is
generated.  The text string must be a single argument, so it should be
enclosed in quotes if it is more than one word.  If it contains
variables, they will be evaluated and their current values printed.

If the *file* or *append* keyword is used, a filename is specified to
which the output will be written.  If *file* is used, then the
filename is overwritten if it already exists.  If *append* is used,
then the filename is appended to if it already exists, or created if
it does not exist.

If the *screen* keyword is used, output to the screen and logfile can
be turned on or off as desired.

If you want the print command to be executed multiple times (e.g. with
changing variable values), there are 3 options.  First, consider using
the :ref:`fix print<fix-print>` command, which will print a string
periodically during a simulation.  Second, the print command can be
used as an argument to the *every* option of the :ref:`run<run>`
command.  Third, the print command could appear in a section of the
input script that is looped over (see the :ref:`jump<jump>` and
:ref:`next<next>` commands).

See the :ref:`variable<variable>` command for a description of *equal*
style variables which are typically the most useful ones to use with
the print command.  Equal-style variables can calculate formulas
involving mathematical operations, global values calculated by a
:ref:`compute<compute>` or :ref:`fix<fix>`, or references to other
:ref:`variables<variable>`.

.. _print-restrictio:

*************
Restrictions:
*************

none

.. _print-related-commands:

*****************
Related commands:
*****************

:ref:`fix print<fix-print>`, :ref:`variable<variable>`

.. _print-default:

********
Default:
********

The option defaults are no file output and screen = yes.

