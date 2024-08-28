
:orphan:



.. index:: include



.. _include:




.. _include-command:



###############
include command
###############




.. _include-syntax:



*******
Syntax:
*******





::



   include file




file = filename of new input script to switch to




.. _include-examples:



*********
Examples:
*********





::



   include newfile
   include in.run2




.. _include-descriptio:



************
Description:
************




This command opens a new input script file and begins reading SPARTA
commands from that file.  When the new file is finished, the original
file is returned to.  Include files can be nested as deeply as
desired.  If input script A includes script B, and B includes A, then
SPARTA could run for a long time.



If the filename is a variable (see the :ref:`variable<variable>`
command), different processor partitions can run different input
scripts.



.. _include-restrictio:



*************
Restrictions:
*************




none



.. _include-related-commands:



*****************
Related commands:
*****************




:ref:`variable<variable>`, :ref:`jump<jump>`



.. _include-default:



********
Default:
********




none



