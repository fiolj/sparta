:orphan:

.. index:: write_grid



.. _command-write-grid:

##################
write_grid command
##################


*******
Syntax:
*******

::

   write_grid filename

-  filename = name of file to write grid info to

*********
Examples:
*********

::

   write_grid data.grid


************
Description:
************

Write a grid file in text format listing the grid cell IDs in the
current hierarchical grid.  See the :ref:`read_grid<command-read-grid>` and
:ref:`create_grid<command-create-grid>` commands, as well as :ref:`Section 6.8<howto-grids>` of the manual for a definition of
hierarchical grids and grid cell IDs as used by SPARTA.

The file is in the following format which is the same as the input
file used by the :ref:`command-read-grid`.  Thus the file
can be used to start a subsequent simulation with the same grid
topology.

.. code-block:: none

   Description line 

   N cells
   M levels
   n1 n2 n3 level-1
   n1 n2 n3 level-2
   ...
   n1 n2 n3 level-M

   Cells 

   id1
   id2
   ...
   idN ... 
   

The file begins with an arbitrary description line followed by zero or
more blank lines.  The header section of the file then lists the
number of grid cells N and the number of levels M in the hierarchical
grid.  For each level the n1, n2, n3 values give the size of the
sub-grid that parent cells (one level lower) are sub-divided into at
this level.  The lines in the header section can be in any order
except the the number of levels M must appear before any of the
level-* lines.  A blank line ends the header section.

The Cells section of the file lists all the grid cell IDs, one per
line.  They may be in arbitrary order, particularly if the file is
written in parallel, where each processor contributes a subset of the
grid cell IDs.

*************
Restrictions:
*************
 none

*****************
Related commands:
*****************

- :ref:`command-read-grid`
- :ref:`command-create-grid`

********
Default:
********
 none
