
:orphan:



.. index:: balance_grid



.. _balance-grid:




.. _balance-grid-command:



####################
balance_grid command
####################




.. _balance-grid-syntax:



*******
Syntax:
*******





::



   balance_grid style args ...




- style = *none* or *stride* or *clump* or *block* or *random* or *proc* or *rcb* 




::



   *none* args = none
   *stride* args = *xyz* or *xzy* or *yxz* or *yzx* or *zxy* or *zyx*
   *clump* args = *xyz* or *xzy* or *yxz* or *yzx* or *zxy* or *zyx*
   *block* args = Px Py Pz
   Px,Py,Pz = # of processors in each dimension
   *random* args = none 
   *proc* args = none
   *rcb* args = weight
   weight = *cell* or *part* or *time*




- zero or more keyword/value(s) pairs may be appended



- keyword = *axes* or *flip*




::



   *axes* value = dims
   dims = string with any of "x", "y", or "z" characters in it
   *flip* value = yes or no








.. _balance-grid-examples:



*********
Examples:
*********





::



   balance_grid block \* \* \*
   balance_grid block \* 4 \*
   balance_grid clump yxz
   balance_grid random
   balance_grid rcb part
   balance_grid rcb part axes xz




.. _balance-grid-descriptio:



************
Description:
************




This command adjusts the assignment of grid cells and their particles
to processors, to attempt to balance the computational cost (load)
evenly across processors.  The load balancing is "static" in the sense
that this command performs the balancing once, before or between
simulations. The assignments will remain static during the
subsequent run.  To perform "dynamic" balancing, see the :ref:`fix balance<fix-balance>` command, which can adjust the assignemt of
grid cells to processors on-the-fly during a run.



After grid cells have been assigned, they are migrated to new owning
processors, along with any particles they own or other per-cell
attributes stored by fixes.  The internal data structures within
SPARTA for grid cells and particles are re-initialized with the new
decomposition.



This command can be used immediately after the grid is created, via
the :ref:`create_grid<create-grid>` or :ref:`read_restart<read-restart>`
commands.  In the former case balance_grid can be used to partition
the grid in a more desirable manner than the default creation options
allow for.  In the latter case, balance grid can be used to change the
somewhat random assignment of grid cells to processors that will be
made if the restart file is read by a different number of processors
than it was written by.



This command can also be used once particles have been created, or a
simulation has come to equilibrium with a spatially varying density
distribution of particles, so that the computational load is more
evenly balanced across processors.



The details of how child cells are assigned to processors by the
various options of this command are described below.  The cells
assigned to each processor will either be "clumped" or "dispersed".



The *clump* and *block* and *rcb* styles will produce clumped
assignments of child cells to each processor.  This means each
processor's cells will be geometrically compact.  The *stride* and
*random* and *proc* styles will produce dispersed assignments of
child cells to each processor.



.. important::

  See :ref:`Section 6.8<howto-details-grid-geometry-sparta>` of the
  manual for an explanation of clumped and dispersed grid cell
  assignments and their relative performance trade-offs.





The *none* style will not change the assignment of grid cells to
processors.  However it will update the internal data structures
within SPARTA that store ghost cell information on each processor for
cells owned by other processors.  This is useful if the :ref:`global gridcut<global>` command was used after grid cells were already
defined.  That command erases ghost cell information stored by
processors, which then needs to be re-generated before a simulation is
run.  Using the balance_grid none command will re-generate the ghost
cell information.



The *stride*, *clump*, and *block* styles can only be used if the grid
is "uniform".  The grid in SPARTA is hierarchical with one or more
levels, as defined by the :ref:`create_grid<create-grid>` or
:ref:`read_grid<read-grid>` commlands.  If the parent cell of every
grid cell is at the same level of the hierarchy, then for purposes of
this command the grid is uniform, meaning the collection of grid cells
effectively form a uniform fine grid overlaying the entire simulation
domain.



The meaning of the *stride*, *clump*, and *block* styles is exactly
the same as when they are used as keywords with the
:ref:`create_grid<create-grid>` command.  See its doc page for details.



.. note::

  that in this case every
  processor will typically not be assigned the exact same number of
  cells.


.. note::

  that in this
  case every processor will typically not be assigned exactly the same
  number of cells.


The *rcb* style uses a recursive coordinate bisectioning (RCB)
algorithm to assign spatially-compact clumps of grid cells to
processors.  Each grid cell has a "weight" in this algorithm so that
each processor is assigned an equal total weight of grid cells, as
nearly as possible.



If the *weight* argument is specified as *cell*, then the weight for
each grid cell is 1.0, so that each processor will end up with an
equal number of grid cells.



If the *weight* argument is specified as *part*, then the weight for
each grid cell is the number of particles it currently owns, so that
each processor will end up with an equal number of particles.



If the *weight* argument is specified as *time*, then timers are used
to estimate the cost of each grid cell.  The cost from the timers is
given on a per processor basis, and then assigned to grid cells by
weighting by the relative number of particles in the grid cells. If no
timing data has yet been collected at the point in a script where this
command is issued, a *cell* style weight will be used instead of
*time*.  A small warmup run (for example 100 timesteps) can be used
before the balance command so that timer data is available. The timers
used for balancing tally time from the move, sort, collide, and modify
portions of each timestep.



.. important::

  The :ref:`adapt_grid<adapt-grid>` command zeros out
  timing data, so the weight *time* option is not available immediatly
  after this command.


.. important::

  The coarsening option in :ref:`fix_adapt<fix-adapt>` may
  shift cells to different processors, which makes the accumulated
  timing data for the weight *time* option less accurate when load
  balancing is performed immediately after this command.


.. note::

  that
  less colors than processors were used, so the disjoint yellow cells
  actually belong to three different processors).  This is an example of
  a clumped distribution where each processor's assigned cells can be
  compactly bounded by a rectangle.  Click for a larger version of the
  image.


.. image:: JPG/partition_small.jpg
           :target: JPG/partition.jpg






The optional keywords *axes* and *flip* only apply to the *rcb*
style.  Otherwise they are ignored.



The *axes* keyword allows limiting the partitioning created by the RCB
algorithm to a subset of dimensions.  The default is to allow cuts in
all dimension, e.g. x,y,z for 3d simulations.  The dims value is a
string with 1, 2, or 3 characters.  The characters must be one of "x",
"y", or "z".  They can be in any order and must be unique.  For
example, in 3d, a dims = xz would only partition the 3d grid only in
the x and z dimensions.



The *flip* keyword is useful for debugging.  If it is set to *yes*
then each time an RCB partitioning is done, the coordinates of grid
cells will (internally only) undergo a sign flip to insure that the
new owner of each grid cell is a different processor than the previous
owner, at least when more than a few processors are used.  This will
insure all particle and grid data moves to new processors, fully
exercising the rebalancing code.






.. _balance-grid-restrictio:



*************
Restrictions:
*************




This command can only be used after the grid has been created by the
:ref:`create_grid<create-grid>`, :ref:`read_grid<read-grid>`, or
:ref:`read_restart<read-restart>` commands.



This command also initializes various options in SPARTA before
performing the balancing.  This is so that grid cells are ready to
migrate to new processors.  Thus if an error is flagged, e.g. that a
simulation box boundary condition is not yet assigned, that operation
needs to be performed in the input script before balancing can be
performed.



.. _balance-grid-related-commands:



*****************
Related commands:
*****************




:ref:`fix balance<fix-balance>`



.. _balance-grid-default:



********
Default:
********




The default settings for the optional keywords are axes = xyz, flip =
no.



