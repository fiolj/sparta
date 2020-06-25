:orphan:

.. index:: write_grid



.. _command-write-grid:

##################
write_grid command
##################


**Syntax:**

::

   write_grid mode file 

-  mode = *parent* or *geom*
-  file = name of file to write grid info to

**Examples:**

::

   write_grid parent data.grid
   write_grid geom viz.out 

**Description:**

Write a grid file in text format describing the currently defined
hierarchical grid. See the :ref:`read_grid<command-read-grid>` and
:ref:`create_grid<command-create-grid>` commands for a definition of
hierarchical grids and parent/child cells as used by SPARTA.

The file is written in text format in one of two modes.

If *mode* is *parent* then a list of parent cells is written in the same
format as the input file used by the :ref:`read_grid<command-read-grid>`
command. Thus the file can be used to start a subsequent simulation
using the same grid topology.

If *mode* is *geom* then the geometric description of all the child
cells is written in the following format. This file can be used in
conjunction with snapshot files of per-grid properties, written by the
:ref:`dump grid<command-dump>` command, to visualize various properties on
the grid.

::

   Description line 

::

   N points
   M cells 

::

   Points 

::

   1 x y z
   2 x y z
   ...
   N x y z 

::

   Cells 

::

   1 p1 p2 p3 p4 ...
   2 p1 p2 p3 p4 ...
   ...
   M p1 p2 p3 p4 ... 

The file will have N points and M grid cells. For each point the x,y,z
coordinates are output. For each grid cell, the indices of the 4 (in 2d)
or 8 (in 3d) points comprising the corners of the grid cell are output.
Each point index is an integer from 1 to N. The ordering of the point
indices is (LL,LR,UR,UL) or counter-clockwise for 2d grid cells. For 3d
grid cells it is the same where the first 4 indices are the lower-Z
indices, and the next 4 are the upper-Z indices.

.. important:: The points in the output file will not be unique.
	       Instead there will be 4 or 8 for each grid cell, with some (x,y,z) coordinates being duplicated since they are shared by multiple grid cells.
	       Converting the output file to one with a unique list of points is currently a post-processing task.

**Restrictions:** none

**Related commands:**

:ref:`command-read-grid`
:ref:`command-create-grid`

**Default:** none
