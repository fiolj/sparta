:orphan:

.. index:: print



.. _command-print:

#############
print command
#############


**Syntax:**

print string keyword value:pre

-  string = text string to print, which may contain variables
-  zero or more keyword/value pairs may be appended
-  keyword = *file* or *append* or *screen*

   ::

        file value = filename
        append value = filename
        screen value = yes or no 

**Examples:**

::

   print "Done with equilibration"
   print 'Done with equilibration'
   print "Done with equilibration" file info.dat 

::

   compute myTemp temp
   variable t equal c_myTemp
   print "The system temperature is now $t" 

**Description:**

Print a text string to the screen and logfile. One line of output is
generated. The text string must be a single argument, so it should be
enclosed in quotes if it is more than one word. If it contains
variables, they will be evaluated and their current values printed.

If the *file* or *append* keyword is used, a filename is specified to
which the output will be written. If *file* is used, then the filename
is overwritten if it already exists. If *append* is used, then the
filename is appended to if it already exists, or created if it does not
exist.

If the *screen* keyword is used, output to the screen and logfile can be
turned on or off as desired.

If you want the print command to be executed multiple times (e.g. with
changing variable values), there are 3 options. First, consider using
the :ref:`fix print<command-fix-print>` command, which will print a string
periodically during a simulation. Second, the print command can be used
as an argument to the *every* option of the :ref:`run<command-run>` command.
Third, the print command could appear in a section of the input script
that is looped over (see the :ref:`jump<command-jump>` and
:ref:`next<command-next>` commands).

See the :ref:`variable<command-variable>` command for a description of
*equal* style variables which are typically the most useful ones to use
with the print command. Equal-style variables can calculate formulas
involving mathematical operations, global values calculated by a
:ref:`compute<command-compute>` or :ref:`fix<command-fix>`, or references to other
:ref:`variables<command-variable>`.

**Restrictions:** none

**Related commands:**

:ref:`command-fix-print`,
:ref:`command-variable`

**Default:**

The option defaults are no file output and screen = yes.
