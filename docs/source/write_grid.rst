
:orphan:

.. index:: write_grid

.. _write-grid:

.. _write-grid-command:

##################
write_grid command
##################

.. _write-grid-syntax:

*******
Syntax:
*******

::

   write_grid filename keyword arg ...

- filename = name of file to write grid info to 

- zero or more keyword/args pairs may be appended

- keyword = *custom*

::

   *custom* arg = name
   name = name of custom per-surf vector or array

.. _write-grid-examples:

*********
Examples:
*********

::

   write_grid data.grid
   write_grid data.grid custom flags

.. _write-grid-descriptio:

************
Description:
************

.. note::

  that if
  the grid is hierarchical, grid cell IDs are not simply numbered from 1
  to N.  They also encode the cell's logical position within the grid
  hierarchy.

The file is in the following format which is the same as the input
file used by the "read_grid"_read_grid.html" command.  Thus the file
can be used to start a subsequent simulation with the same grid
topology.

::

   Description line

::

   N cells
   M levels
   n1 n2 n3 level-1
   n1 n2 n3 level-2
   ...
   n1 n2 n3 level-M

::

   Cells

::

   id1 (custom1a) (custom1b) ...
   id2 (custom2a) (custom2b) ...
   ...
   idN (customNa) (customNb) ...

The file begins with an arbitrary description line followed by zero or
more blank lines.  The header section of the file then lists the
number of grid cells N and the number of levels M in the hierarchical
grid.  For each level the n1, n2, n3 values give the size of the
sub-grid that parent cells (one level lower) are sub-divided into at
this level.  The lines in the header section can be in any order
except the the number of levels M must appear before any of the
level-\* lines.  A blank line ends the header section.

The Cells section of the file lists all the grid cell IDs, one per
line.  They may be in arbitrary order, particularly if the file is
written in parallel, where each processor contributes a subset of the
grid cell IDs.

If the optional *custom* keyword is specified along with the *name* of
a custom per-grid vector or array, then the per-grid values for that
vector or array are added following the grid cell ID.  A per-grid
vector is a single value per grid cell; a per-grid array is 1 or more
values per grid cell, depending on how it was defined.  If the
*custom* keyword is used multiple times, then the value(s) for each
*name* are appended in the order the *custom* keywords are specified.

.. _write-grid-restrictio:

*************
Restrictions:
*************

none

.. _write-grid-related-commands:

*****************
Related commands:
*****************

:ref:`read_grid<read-grid>`, :ref:`create_grid<create-grid>`

.. _write-grid-default:

********
Default:
********

none

