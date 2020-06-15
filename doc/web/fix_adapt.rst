:orphan:

.. _command-fix-adapt:

#################
fix adapt command
#################

####################
fix adapt/kk command
####################

**Syntax:**

::

   fix ID adapt Nfreq args ... 

-  ID is documented in `fix <fix.html>`__ command
-  adapt = style name of this fix command
-  Nfreq = perform grid adaptation every this many steps
-  args = all remaining args are identical to those defined for the
   `adapt_grid <adapt_grid.html>`__ command

**Examples:**

::

   fix 1 adapt 1000 all refine particle 10 50
   fix 1 adapt 1000 all coarsen particle 10 50
   fix 1 adapt 500 subset refine coarsen particle 10 50
   fix 1 adapt 10000 all refine surf 0.15 iterate 1 dir 1 0 0 
   fix 10 adapt 1000 all refine coarsen value c_11 5.0 10.0 iterate 2 

**Description:**

This command performs on-the-fly adapatation of grid cells as a
simulation runs, either by refinement or coarsening or both. Grid
adaptation can also be performed before or between simulations by using
the `adapt_grid <adapt_grid.html>`__ command.

Refinement means splitting one child cell into multiple new child cells;
the original child cell becomes a parent cell. Coarsening means
combining all the child cells of a parent cell, so that the child cells
are deleted and the parent cell becomes a single new child cell. See
`Section howto 4.8 <Section_howto.html#howto_8>`__ for a description of
the hierarchical grid used by SPARTA and a defintion of child and parent
cells.

Grid adaptation can be useful for adjusting the grid cell sizes to the
current particle density distribution, or mean-free-path of particles,
or to other simulation attributes such as the presence of surface
elements. A well-adapted grid can improve accuracy of the simulation
and/or reduce a simulation's computational cost.

Adaptation is performed by this command once every *Nfreq* timesteps.

All of the command arguments which appear after *Nfreq*, which determine
how adapation is done for both refinement and coarsening, are exactly
the same as for the `adapt_grid <adapt_grid.html>`__ command.

This includes a group-ID parameter which can be used to limit adaptation
to a subset of current grid cells. See the
`adapt_grid <adapt_grid.html>`__ command doc page for details.

The one exception is that the *iterate* keyword cannot be used with the
fix adapt command. Only a single iteration of the action1 and action2
parameters (described on the `adapt_grid <adapt_grid.html>`__ doc page)
can be performed each time grid adaptation is performed.

--------------

**Restart, output info:**

No information about this fix is written to `binary restart
files <restart.html>`__.

This fix computes a global scalar which is a flag for whether any grid
cells were adapted on the last timestep it was invoked. The value of the
flag is 1 if any cells were refined or coarsened, else it is 0.

--------------

Styles with a *kk* suffix are functionally the same as the corresponding
style without the suffix. They have been optimized to run faster,
depending on your available hardware, as discussed in the `Accelerating
SPARTA <Section_accelerate.html>`__ section of the manual. The
accelerated styles take the same arguments and should produce the same
results, except for different random number, round-off and precision
issues.

These accelerated styles are part of the KOKKOS package. They are only
enabled if SPARTA was built with that package. See the `Making
SPARTA <Section_start.html#start_3>`__ section for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the `-suffix command-line
switch <Section_start.html#start_6>`__ when you invoke SPARTA, or you
can use the `suffix <suffix.html>`__ command in your input script.

See the `Accelerating SPARTA <Section_accelerate.html>`__ section of the
manual for more instructions on how to use the accelerated styles
effectively.

--------------

**Restrictions:** none

**Related commands:**

:ref:`command-adapt-grid`,
:ref:`command-balance-grid`

**Default:** none
