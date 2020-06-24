:orphan:

.. index:: create_grid



.. _command-create-grid:

###################
create_grid command
###################


**Syntax:**

::

   create_grid Nx Ny Nz keyword args ... 

-  Nx,Ny,Nz = size of 1st-level grid in each dimension
-  zero or more keywords/args pairs may be appended
-  keyword = *level* or *region* or *stride* or *clump* or *block* or
   *random* or *inside*

   ::

        level args = Nlevel Px Py Pz Cx Cy Cz 
          Nlevel = level from 2 to M, must be in ascending order
          Px Py Pz = range of parent cells in each dimension in which to create child cells
          Cx Cy Cz = size of child grid in each dimension within parent cells
        region args = Nlevel reg-ID Cx Cy Cz 
          Nlevel = level from 2 to M, must be in ascending order
          reg-ID = ID of region which parent cells must be in to create child cells
          Cx Cy Cz = size of child grid in each dimension within parent cells
        stride arg = xyz or xzy or yxz or yzx or zxy or zyx
        clump arg = xyz or xzy or yxz or yzx or zxy or zyx
        block args = Px Py Pz
          Px,Py,Pz = # of processors in each dimension
        random args = none
        inside args = any or all 

**Examples:**

::

   create_grid 10 10 10
   create_grid 10 10 10 block * * *
   create_grid 10 10 10 block 4 2 5
   create_grid 10 10 10 level 2 * * * 2 2 3
   create_grid 20 10 1 level 2 10*15 3*7 1 2 2 1
   create_grid 20 10 1 region 2 b2 2 2 1 region 3 b3 2 3 1 inside any
   create_grid 20 10 1 level 2 10*15 3*7 1 2 2 1 region 3 b3 2 3 1
   create_grid 8 8 10 level 2 5* * * 4 4 4 level 3 1 2*3 3* 2 2 1 

**Description:**

Overlay a grid over the simulation domain defined by the
:ref:`create_box<command-create-box>` command. The grid can also be defined
by the :ref:`read_grid<command-read-grid>` command.

The grid in SPARTA is hierarchical, as described in :ref:`Section howto 4.8<howto-grids>`. The entire simulation box is a
single parent grid cell at level 0. It is subdivided into Nx by Ny by Nz
cells at level 1. Each of those cells can be a child cell (no further
sub-division) or can be a parent cell which is further subdivided into
Nx by Ny by Nz cells at level 2. This can recurse to as many levels as
desired. Different cells can stop recursing at different levels. Each
parent cell can define its own unique Nx, Ny, Nz values for subdivision.
Note that a grid with a single level is simply a uniform grid with Nx by
Ny by Nz cells in each dimension.

In the current SPARTA implementation, all processors own a copy of all
parent cells. Each child cell is owned by a unique processor. The
details of how child cells are assigned to processors by the various
options of this command are described below. The cells assigned to each
processor will either be "clumped" or "dispersed".

The *clump* and *block* keywords will produce clumped assignments of
child cells to each processor. This means each processor's cells will be
geometrically compact. The *stride* and *random* keywords, as well as
the round-robin assignment scheme for grids with multiple levels
(described below), will produce dispersed assignments of child cells to
each processor.

.. important:: See :ref:`Section 6.8<howto-grids>` of the manual for an explanation of clumped and dispersed grid cell assignments and their relative performance trade-offs.
	       The :ref:`balance_grid<command-balance-grid>` command can be used after the grid is created, to assign child cells to processors in different ways. The "fix balance" command can be used to re-assign them in a load-balanced manner periodically during a running simulation.

--------------

A single-level grid is defined by specifying only the arguments *Nx*,
*Ny*, *Nz*, with no additional *level* or *region* keywords. This will
create a uniform Nx by Ny by Nz grid of child cells. For 2d simulations,
*Nz* must equal 1.

For single-level grids, one of the keywords *stride*, *clump*, *block*,
or *random* can be used to determine which processors are assigned which
cells in the grid. The *inside* keyword is ignored for single-level
grids. If no keyword is used, the cells are assigned in round-robin
fashion, so that each processor is assigned every Pth grid cell, where P
= the number of processors. This is the same as "stride xyz" in the
discussion below.

The *stride* keyword means that every Pth cell is assigned to the same
processor, where P is the number of processors. E.g. if there are 100
cells and 10 processors, then the 1st processor (proc 0) will be
assigned cells 1,11,21, ..., 91. The 2nd processor (proc 1) will be
assigned cells 2,12,22 ..., 92. The 10th processor (proc 9) will be
assigned cells 10,20,30, ..., 100.

The *clump* keyword means that the Pth clump of cells is assigned to the
same processor, where P is the number of processors. E.g. if there are N
= 100 cells and 10 processors, then the 1st processor (proc 0) will be
assigned cells 1 to 10. The 2nd processor (proc 1) will be assigned
cells 11 to 20. And The 10th processor (proc 9) will be assigned cells
91 to 100.

The argument for *stride* and *clump* determines how the N grid cells
are ordered and is some permutation of the letters *x*, *y*, and *z*.
Each of the N cells has 3 indices (I,J,K) to describe its location in
the 3d grid. If the stride argument is yxz, then the cells will be
ordered from 1 to N with the y dimension (J index) varying fastest, the
x dimension next (I index), and the z dimension slowest (K index).

The *block* keyword maps the P processors to a *Px* by *Py* by *Pz*
logical grid that overlays the actual *Nx* by *Ny* by *Nz* grid. This
effectively assigns a contiguous 3d sub-block of cells to each
processor.

Any of the *Px*, *Py*, *Pz* parameters can be specified with an asterisk
"*", in which case SPARTA will choose the number of processors in that
dimension. It will do this based on the size and shape of the global
grid so as to minimize the surface-to-volume ratio of each processor's
sub-block of cells.

The product of Px, Py, Pz must equal P, the total # of processors SPARTA
is running on. For a 2d simulation, Pz must equal 1. If multiple
partitions are being used then P is the number of processors in this
partition; see :ref:`Section 2.6<start-command-line-options>` for an
explanation of the -partition command-line switch.

Note that if you run on a large, prime number of processors P, then a
grid such as 1 x P x 1 will be required, which may incur extra
communication costs.

The *random* keyword means that each grid cell will be assigned randomly
to one of the processors. Note that in this case different processors
will typically not be assigned exactly the same number of cells.

--------------

A hierarchical grid with more than one level can be defined using the
*level* or *region* keywords one or more times with *Nlevel* in
ascending order, starting with *Nlevel* = 2. At each level the *level*
or *region* keyword can be used interchangeably. Child cells (at any
level) are assigned to processors in round-robin fashion, so that each
processor is assigned every Pth grid cell, where P = the number of
processors.

Note that the keywords *stride*, *clump*, *block*, or *random* cannot be
used with a hierarchical grid. The keyword *inside* can be used, but it
must come after all the *level* or *region* keywords.

For the *level* keyword, the Px, Py, Pz arguments specify which cells in
the previous level are flagged as parents and sub-divided to create
cells at the new level. For example, if the level 1 grid is 100x100x100,
then Px, Py, Pz for level 2 could select any contiguous range of cells
from 1 to 100 in x, y, or z. If the level 2 grid is 4x4x2 within any
level 1 cell (as set by Cx, Cy, Cz), then Px, Py, Pz for level 3 could
select any contiguous range of cells from 1 to 4 in x, y and 1 to 2 in
z.

Each of the Px, Py, Pz arguments can be a single number or be specified
with a wildcard asterisk, as in the examples above. For example, Px can
be specified as "*" or "*n" or "n*" or "m*n". If N = the number of grid
cells in the x-direction in the previous level as defined by Nx (or Cx),
then an asterisk with no numeric values means all cells with indices
from 1 to N. A leading asterisk means all indices from 1 to n
(inclusive). A trailing asterisk means all indices from n to N
(inclusive). A middle asterisk means all indices from m to n
(inclusive).

The Cx, Cy, Cz arguments are the number of new cells (in each dimension)
to partition each selected parent cell into. For 2d simulations, *Cz*
must equal 1. Note that for each new level, only grid cells that exist
in the previous level are partitioned further. E.g. level 3 cells are
only added to level 2 cells that exist, since some level 1 cells may not
have been partitioned into level 2 cells.

This command creates a two-level grid:

::

   create_grid 10 10 10 level 2 * * * 2 2 3 

The 1st level is 10x10x10. Each of the 1000 level 1 cells is further
partitioned into 2x2x3 cells. This means the total number of level 2
cells is 1000 \* 12 = 12000. The resulting grid thus has 1001 parent
cells (the simulation box plus the 1000 level 1 cells), and 12000 child
cells.

This command creates a 3-level grid:

::

   create_grid 8 8 10 level 2 5* * * 4 4 4 level 3 1 2*3 3* 2 2 1 

The last example above creates a 3-level grid. The first level is
8x8x10. The second level is 4x4x4 within each 1st level cell, but only
half or 320 of the 640 level 1 cells are partitioned, namely those with
x indices from 5 to 8. Those with x indices from 1 to 4 remain as level
1 cells. Some of the level 2 cells are further partitioned into 2x2x1
level 3 cells. For the 4x4x4 level 2 grid within 320 or the level 1
cells, only the level 2 cells with x index = 1, y index = 2-3, and
z-index = 3-4 are further partitioned into level 3 cells, which is just
4 of the 64 level 2 cells.

The resulting grid thus has 1601 parent cells: 1 for the simulation box,
320 level 1 cells, and 1280 level 2 cells. It has 24640 child cells: 320
level 1 cells, 19200 level 2 cells, and 5120 level 3 cells.

For the *region* keyword, the subset of cells in the previous level
which are flagged as parents and sub-divided is determined by which of
them are in the geometric region specified by *reg-ID*.

The :ref:`region<command-region>` command can define volumes for simple
geometric objects such as a sphere or rectangular block. It can also
define unions or intersections of simple objects or other union or
intersection objects. by defining an appropriate region, a complex
portion of the simulation domain can be refined to a new level.

Each grid cell at the previous level is tested to see whether it is "in"
the region. The *inside* keyword determines how this is done. If
*inside* is set to *any* which is the default, then the grid cell is in
the region if any of its corner points (4 in 2d, 8 in 3d) is in the
region. If *inside* is set to *all*, then all 4 or 8 corner points must
be in the region for the grid cell itself to be in the region. Note that
the *side* option for the :ref:`region<command-region>` command can be used
to define whether the inside or outside of the geometric region is
considered to be "in" the region.

If the grid cell is in the region, then it is refined using the Cx, Cy,
Cz arguments in the same manner that the *level* keyword uses them.
Examples for the use of the *region* keyword are given above.

--------------

**Restrictions:**

This command can only be used after the simulation box is defined by the
:ref:`create_box<command-create-box>` command.

The hierarchical grid used by SPARTA is encoded in a 32-bit or 64-bit
integer ID. The precision is set by the -DSPARTA_BIG or -DSPARTA_SMALL
or -DSPARTA_BIGBIG compiler switch, as described in :ref:`Section 2.2<start-steps-build>`. The number of grid levels that can
be used depends on the resolution of the grid at each level. For a
minimal refinement of 2x2x2, a level uses 4 bits of the integer ID. Thus
for this style of refinement a maximum of 7 levels can be used for
32-bit IDs and 15 levels for 64-bit IDs.

**Related commands:**

:ref:`command-create-box`,
:ref:`command-read-grid`

**Default:**

The only keyword with a default setting is inside = any.
