
:orphan:

.. index:: fix_adapt

.. _fix-adapt:

.. _fix-adapt-command:

#################
fix adapt command
#################

.. _fix-adapt-kk-command:

####################
fix adapt/kk command
####################

.. _fix-adapt-syntax:

*******
Syntax:
*******

::

   fix ID adapt Nfreq args ...

   - ID is documented in :ref:`fix<fix>` command
   - adapt = style name of this fix command
   - Nfreq = perform grid adaptation every this many steps
   - args = all remaining args are identical to those defined for the :ref:`adapt_grid<adapt-grid>` command

.. _fix-adapt-examples:

*********
Examples:
*********

::

   fix 1 adapt 1000 all refine particle 10 50
   fix 1 adapt 1000 all coarsen particle 10 50
   fix 1 adapt 500 subset refine coarsen particle 10 50
   fix 1 adapt 10000 all refine surf 0.15 iterate 1 dir 1 0 0 
   fix 10 adapt 1000 all refine coarsen value c_1\[1\] 5.0 10.0 iterate 2

.. _fix-adapt-descriptio:

************
Description:
************

This command performs on-the-fly adapatation of grid cells as a
simulation runs, either by refinement or coarsening or both.  Grid
adaptation can also be performed before or between simulations by
using the :ref:`adapt_grid<adapt-grid>` command.

Refinement means splitting one child cell into multiple new child
cells; the original child cell becomes a parent cell.  Coarsening
means combining all the child cells of a parent cell, so that the
child cells are deleted and the parent cell becomes a single new child
cell.  See :ref:`Section howto 4.8<howto-68-details-grid-geometry>` for a
description of the hierarchical grid used by SPARTA and a defintion of
child and parent cells.

Grid adaptation can be useful for adjusting the grid cell sizes to the
current particle density distribution, or mean-free-path of particles,
or to other simulation attributes such as the presence of surface
elements.  A well-adapted grid can improve accuracy of the simulation
and/or reduce a simulation's computational cost.

Adaptation is performed by this command once every *Nfreq* timesteps.

All of the command arguments which appear after *Nfreq*, which
determine how adapation is done for both refinement and coarsening,
are exactly the same as for the :ref:`adapt_grid<adapt-grid>` command.

This includes a group-ID parameter which can be used to limit
adaptation to a subset of current grid cells.  See the
:ref:`adapt_grid<adapt-grid>` command doc page for details.

The one exception is that the *iterate* keyword cannot be used with
the fix adapt command.  Only a single iteration of the action1 and
action2 parameters (described on the :ref:`adapt_grid<adapt-grid>` doc
page) can be performed each time grid adaptation is performed.

.. note::

  that if you want the grid partitioning (and their particles) to
  be rebalanced across processors after grid adaptation, you can use the
  :ref:`fix_balance<fix-balance>` command.  If you set the *Nfreq*
  setting for this command and the :ref:`fix_balance<fix-balance>`
  command to the same value, then both operations will occur on the same
  timesteps.  However, the fix balance command needs to appear in the
  input script after the fix adapt command, if you want balancing to
  occur after adaptation (whether the Nfreq values are the same or not).

.. _fix-adapt-restart,-output-info:

*********************
Restart, output info:
*********************

No information about this fix is written to :ref:`binary restart files<restart>`.

This fix computes a global scalar which is a flag for whether any grid
cells were adapted on the last timestep it was invoked.  The value of
the flag is 1 if any cells were refined or coarsened, else it is 0.

This fix also computes a global vector of length 2.  The first value
is the number of cells which were refined.  The second is the number
which were coarsened.  Both on the last timestep the fix was invoked.

Styles with a *kk* suffix are functionally the same as the
corresponding style without the suffix.  They have been optimized to
run faster, depending on your available hardware, as discussed in the
:ref:`Accelerating SPARTA<accelerate>` section of the manual.
The accelerated styles take the same arguments and should produce the
same results, except for different random number, round-off and
precision issues.

These accelerated styles are part of the KOKKOS package. They are only
enabled if SPARTA was built with that package.  See the :ref:`Making SPARTA<start-making-sparta-optional-packages>` section for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the :ref:`-suffix command-line switch<start-commandlin-options>` when you invoke SPARTA, or you can
use the :ref:`suffix<suffix>` command in your input script.

See the :ref:`Accelerating SPARTA<accelerate>` section of the
manual for more instructions on how to use the accelerated styles
effectively.

.. _fix-adapt-restrictio:

*************
Restrictions:
*************

Currently, if there are custom attributes defined for grid cells, grid
adaptation does not set new values for new grid cells created when
either refinement or coarsening takes place.  The new cells will have
zero values for their attributes.  This is because there is no simple
way to determine how new attribute values should be computed.  This
may be changed in the future.

.. _fix-adapt-related-commands:

*****************
Related commands:
*****************

:ref:`adapt_grid<adapt-grid>`, :ref:`fix balance<fix-balance>`

.. _fix-adapt-default:

********
Default:
********

none

