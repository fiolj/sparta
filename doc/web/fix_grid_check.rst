:orphan:

.. index:: fix grid/check
.. index:: fix grid/check/kk





.. _command-fix-grid-check:

######################
fix grid/check command
######################






.. _command-fix-grid-check-fix-gridcheckkk:

#########################
fix grid/check/kk command
#########################



*******
Syntax:
*******

::

   fix ID grid/check N outflag keyword arg ... 

-  ID is documented in :ref:`fix<command-fix>` command
-  grid/check = style name of this fix command
-  N = check every N timesteps
-  outflag = *error* or *warn* or *silent*
-  zero or more keyword/args pairs may be appended
-  keyword = *outside*

   ::

        outside arg = yes or no 

*********
Examples:
*********

::

   fix 1 grid/check 100 error 

************
Description:
************

Check if particles are inside the grid cell they are supposed to be,
based on their current coordinates. This is useful as a debugging check
to insure that no particles have been assigned to the incorrect grid
cell during the particle move stage of the SPARTA timestepping
algorithm.

The check is performed once every *N* timesteps. Particles not inside
the correct grid cell are counted and the value of the count can be
monitored (see below). A value of 0 is "correct", meaning that no
particle was found outside its assigned grid cell.

If the *outside* keyword is set to *yes*, then a check for particles
inside implicit surfaces is also performed. If a particle is in a grid
cell with implicit surface elements and the particles is "inside" the
surfaces (which have possibly ablated), then the error count is
incremented.

If the outflag setting is *error*, SPARTA will print an error and stop
if it finds a particle in an incorrect grid cell or inside the implicit
surface elements. For *warn*, it will print a warning message and
continue. For *silent*, it will print no message, but the count of such
occurrences can be monitored as described below, e.g. by outputting the
value with the :ref:`stats<command-stats>` command.

--------------

**Restart, output info:**

No information about this fix is written to :ref:`binary restart files<command-restart>`.

This fix computes a global scalar which can be accessed by various
output commands. The scalar is the count of how many particles were not
in the correct grid cell. The count is cummulative over all the
timesteps the check was performed since the start of the run. It is
initialized to zero each time a run is performed.

--------------

Styles with a *kk* suffix are functionally the same as the corresponding
style without the suffix. They have been optimized to run faster,
depending on your available hardware, as discussed in the :ref:`Accelerating SPARTA<accelerate>` section of the manual. The
accelerated styles take the same arguments and should produce the same
results, except for different random number, round-off and precision
issues.

These accelerated styles are part of the KOKKOS package. They are only
enabled if SPARTA was built with that package. See the :ref:`Making SPARTA<start-making-sparta>` section for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the :ref:`-suffix command-line switch<start-command-line-options>` when you invoke SPARTA, or you
can use the :ref:`suffix<command-suffix>` command in your input script.

See the :ref:`Accelerating SPARTA<accelerate>` section of the
manual for more instructions on how to use the accelerated styles
effectively.

--------------

*************
Restrictions:
*************
 none

*****************
Related commands:
***************** none

********
Default:
********


The option default is outside = no.
