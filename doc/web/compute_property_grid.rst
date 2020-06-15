:orphan:

.. _command-compute-property-grid:

#############################
compute property/grid command
#############################

**Syntax:**

::

   compute ID property/grid group-ID input1 input2 ... 

-  ID is documented in `compute <compute.html>`__ command
-  property/grid = style name of this compute command
-  group-ID = group ID for which grid cells to perform calculation on
-  input = one or more grid attributes

   ::

        possible attributes = id, proc, xlo, ylo, zlo, xhi, yhi, zhi, xc, yc, zc 

   ::

        id = integer form of grid cell ID
        proc = processor that owns grid cell
        xlo,ylo,zlo = coords of lower left corner of grid cell
        xhi,yhi,zhi = coords of lower left corner of grid cell
        xc,yc,zc = coords of center of grid cell
        vol = flow volume of grid cell (area in 2d) 

**Examples:**

::

   compute 1 property/grid all id xc yc zc 

**Description:**

Define a computation that simply stores grid attributes for each grid
cell in a grid cell group. This is useful so that the values can be used
by other `output commands <Section_howto.html#howto_4>`__ that take
computes as inputs. See for example, the `compute
reduce <compute_reduce.html>`__, `fix ave/grid <fix_ave_atom.html>`__,
and `dump grid <dump.html>`__ commands.

Only grid cells in the grid group specified by *group-ID* are included
in the calculation. See the `group grid <group.html>`__ command for info
on how grid cells can be assigned to grid groups.

The values are stored in a per-grid vector or array as discussed below.

*Id* is the grid cell ID. In SPARTA each grid cell is assigned a unique
ID which represents its location, in a topological sense, within the
hierarchical grid. This ID is stored as an integer such as 5774983, but
can also be decoded into a string such as 33-4-6, which makes it easier
to understand the grid hierarchy. In this case it means the grid cell is
at the 3rd level of the hierarchy. Its grandparent cell was 33 at the
1st level, its parent was cell 4 (at level 2) within cell 33, and the
cell itself is cell 6 (at level 3) within cell 4 within cell 33. If you
specify *id*, the ID is printed directly as an integer. The ID in string
format can be accessed by the `dump grid <dump.html>`__ command and its
*idstr* argument.

*Proc* is the ID of the processor which currently owns the grid cell.

The *xlo*, *ylo*, *zlo* attributes are the coordinates of the lower-left
corner of the grid cell in the appropriate distance
`units <units.html>`__. The *xhi*, *yhi*, *zhi* are the coordinates of
the upper-right corner of the grid cell. The *xc*, *yc*, *zc* attributes
are the coordinates of the center point of the grid cell. The *zlo*,
*zhi*, *zc* attributes cannot be used for a 2d simulation.

The *vol* attribute is the flow volume of the grid cell (or area in 2d).
Flow volume is the portion of the grid cell that is accessible to
particles, i.e. outside any closed surface that may intersect the cell.

--------------

**Output info:**

This compute calculates a per-grid vector or per-grid array depending on
the number of input values. If a single input is specified, a per-grid
vector is produced. If two or more inputs are specified, a per-grid
array is produced where the number of columns = the number of inputs.

This compute performs calculations for all flavors of child grid cells
in the simulation, which includes unsplit, cut, split, and sub cells.
See `Section 6.8 <Section_howto.html#howto_8>`__ of the manual gives
details of how SPARTA defines child, unsplit, split, and sub cells. The
*id* and *xlo,ylo,zlo* and *xhi,yhi,zhi* values for a split cell and its
sub cells are all the same. The *vol* of a cut cell is the portion of
the cell in the flow. The *vol* of a split cell is the same as if it
were unsplit. The *vol* of each sub cell within a split cell is its
portion of the flow volume.

Grid cells not in the specified *group-ID* will output zeroes for all
their values.

The vector or array can be accessed by any command that uses per-atom
values from a compute as input. See `Section
4.4 <Section_howto.html#howto_4>`__ for an overview of SPARTA output
options.

The vector or array values will be in whatever `units <units.html>`__
the corresponding attribute is in, e.g. distance units for xlo or xc.

**Restrictions:** none

**Related commands:**

:ref:`dump grid <command-dump>`
:ref:`command-compute-reduce`
:ref:`command-fix-ave-grid`

**Default:** none
