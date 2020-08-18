:orphan:

.. index:: include



.. _command-include:

###############
include command
###############


*******
Syntax:
*******

::

   include file 

-  file = filename of new input script to switch to

*********
Examples:
*********

::

   include newfile
   include in.run2 

************
Description:
************

This command opens a new input script file and begins reading SPARTA
commands from that file. When the new file is finished, the original
file is returned to. Include files can be nested as deeply as desired.
If input script A includes script B, and B includes A, then SPARTA could
run for a long time.

If the filename is a variable (see the :ref:`command-variable`), different processor partitions can run different input scripts.

*************
Restrictions:
*************
 none

*****************
Related commands:
*****************

:ref:`command-variable`,
:ref:`command-jump`

********
Default:
********
 none
