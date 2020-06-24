:orphan:

.. index:: read_grid



.. _command-read-grid:

#################
read_grid command
#################


**Syntax:**

::

   read_grid filename 

-  filename = name of grid file

**Examples:**

::

   read_grid grid.overlay 

**Description:**

Read in a grid description from a file, which will overlay the
simulation domain defined by the :ref:`create_box<command-create-box>`
command. The grid can also be defined by the
:ref:`create_grid<command-create-grid>` command.

The grid in SPARTA is hierarchical. The entire simulation box is a
single parent grid cell at level 0. It is subdivided into Nx by Ny by Nz
cells at level 1. Each of those cells can be a child cell (no further
sub-division) or can be a parent cell which is further subdivided into
Nx by Ny by Nz cells at level 2. This can recurse to as many levels as
desired. Different cells can stop recursing at different levels. Each
parent cell can define its own unique Nx, Ny, Nz values for subdivision.
Note that a grid with a single level is simply a uniform grid with Nx by
Ny by Nz cells in each dimension.

In the current SPARTA implementation, all processors own a copy of all
parent cells. Each child cell is owned by a unique processor. They are
assigned by this command to processors in a round-robin fashion, as they
are created at each level when the file is read. This is a "dispersed"
assignment of child cells to each processor.

.. important:: See :ref:`Section 6.8<howto-grids>` of the manual for an explanation of clumped and dispersed grid cell assignments and their relative performance trade-offs.
	       The :ref:`balance_grid<command-balance-grid>` command can be used after the grid is created, to assign child cells to processors in different ways.
	       The "fix balance" command can be used to re-assign them in a load-balanced manner periodically during a running simulation.

--------------

The specified file can be a text file or a gzipped text file (detected
by a .gz suffix).

A grid file contains only a listing of parent cells. Child cells are
inferred from the parent cell definitions.

A grid file has a header and a body. The header appears first. The first
line of the header is always skipped; it typically contains a
description of the file. Then lines are read one at a time. Lines can
have a trailing comment starting with '#' that is ignored. If the line
is blank (only whitespace after comment is deleted), it is skipped. If
the line contains a header keyword, the corresponding value is read from
the line. If it doesn't contain a header keyword, the line begins the
body of the file.

The body of the file contains one or more sections. The first line of a
section has only a keyword. The next line is skipped. The remaining
lines of the section contain values. The number of lines in a section
depends on the section keyword as described below. Zero or more blank
lines can be used between sections. Sections can appear in any order.

The formatting of individual lines in the grid file (indentation,
spacing between words and numbers) is not important except that header
and section keywords must be capitalized as shown and can't have extra
white space between their words.

These are the recognized header keywords (only one for this file).
Header lines can come in any order. The value(s) are read from the
beginning of the line. Thus the keyword *parents* should be in a line
like "1000 parents".

-  *parents* = # of parent cells in file

These are the recognized section keywords for the body of the file (only
one for this file).

-  *Parents*

The *Parents* section consists of N consecutive entries, where N = # of
parents, each of this form:

::

   index parent-ID Nx Ny Nz 

The index is ignored; it is only added to assist in examining the file.
Typically, the indices should run consecutively from 1 to N.

The parent-ID is a string of numbers (one per level) separated by
dashes, e.g. 12-352-65, where level 1 is the coarsest grid overlaying
the simulation domain, level 2 is the refined grid within a level 1
cell, etc.

The first number in the ID string is which level 1 cell (from 1 to N1)
this parent cell descends from, the second number is which level 2 cell
(from 1 to N2) this parent cell descends from, etc. The final number is
which cell this cell is within its own parent.

As an example, consider the parent ID 12-352-65. Assume the simulation
box was partitioned with a 10x10x10 level 1 grid, or 1000 level 1 grid
cells. These are numbered from 1 to 1000, with x varying fastest, then
y, finally z. The parent cell with ID 12-352-65 is inside the 12th of
those level 1 cells. If that cell were sub-divided into 8x6x10 cells,
there would be 480 level 2 cells within the 12th level 1 cell. The
parent cell with ID 12-352-65 is inside the 352nd of those level 2
cells. Likewise it is within the 65th of the level 3 cells inside the
352nd level 2 cell.

The Nx, Ny, Nz values determine how the parent cell is sub-divided into
Nx by Ny by Nz cells at the next level. Each of those cells could be a
child cell or yet another parent cell. Nz must be specified as 1 for 2d
grids.

For example, this entry:

::

   index 12-352-65 2 2 2 

means the parent cell 12-352-65 at level 3 is further sub-divided into
2x2x2 level 4 cells. The IDs of the 8 new cells will be 12-352-65-1,
12-352-65-2, ..., 12-352-65-8.

The lines in the *Parents* section must be ordered such that no parent
cell is listed before its own parent cell appears. A simple way to
insure this is to list the single level 0 cell first, all level 1 parent
cells next, then level 2 parent cells, etc.

The parent cell with ID = 0 is a special case. It can be thought of as
the "root" cell, or the single level 0 cell, which represents the entire
simulation domain. Its specification in the grid file defines the level
1 grid that overlays the simulation domain. Thus the first line of the
*Parents* section should be formatted something like this:

::

   1 0 10 10 20 

which means the level 1 grid has 10x10x20 cells.

**Restrictions:**

This command can only be used after the simulation box is defined by the
:ref:`create_box<command-create-box>` command.

To read gzipped grid files, you must compile SPARTA with the
-DSPARTA_GZIP option - see :ref:`Section 2.2<start-steps-build>`
of the manual for details.

The hierarchical grid used by SPARTA is encoded in a 32-bit or 64-bit
integer ID. The precision is set by the -DSPARTA_BIG or -DSPARTA_SMALL
or -DSPARTA_BIGBIG compiler switch, as described in `Section 2.2 <Section_start.html#start2_2>`__. The number of grid levels that can
be used depends on the resolution of the grid at each level. For a
minimal refinement of 2x2x2, a level uses 4 bits of the integer ID. Thus
a maximum of 7 levels can be used for 32-bit IDs and 15 levels for
64-bit IDs.

**Related commands:**

:ref:`command-create-box`,
:ref:`command-create-grid`

**Default:** none
