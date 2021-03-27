:orphan:

.. index:: read_grid



.. _command-read-grid:

#################
read_grid command
#################


*******
Syntax:
*******

::

   read_grid filename 

-  filename = name of grid file

*********
Examples:
*********

::

   read_grid data.grid 

************
Description:
************

Read a grid file in text format which lists the grid cell IDs to be
used to construct a hierarchical grid that overalys the simulation
domain defined by the :ref:`command-create-box`.
The grid can also be defined by the :ref:`command-create-grid`.

The grid file can be written by the :ref:`command-write-grid` in a previous simulation, or be created by some pre-processing 
tool.  See :ref:`Section 6.8<howto-grids>` of the manual for
a definition of hierarchical grids and grid cell IDs as used by
SPARTA.

The specified file can be a text file or a gzipped text file (detected
by a .gz suffix).  See the :ref:`command-write-grid` for a
description of the format of the file.

The grid cell IDs read from the file to processors in a round-robin
fashion, which means in general the set of cells a processor owns will
not be contiguous in a geometric sense.  They are thus assumed to be a
"dispersed" assignment of grid cells to each processor.


.. important:: See :ref:`Section 6.8<howto-grids>` of the manual for an explanation of clumped and dispersed grid cell assignments and their relative performance trade-offs.
	       The :ref:`balance_grid<command-balance-grid>` command can be used after the grid is read, to assign child cells to processors in different ways.
	       The :ref:`command-fix-balance` can be used to re-assign them in a load-balanced manner periodically during a running simulation.


*************
Restrictions:
*************


This command can only be used after the simulation box is defined by the
:ref:`create_box<command-create-box>` command.

To read gzipped grid files, you must compile SPARTA with the
-DSPARTA_GZIP option - see :ref:`Section 2.2<start-steps-build-make>`
of the manual for details.

*****************
Related commands:
*****************

- :ref:`command-create-box`,
- :ref:`command-create-grid`

********
Default:
********
 none
