
:orphan:

.. index:: compute_dt_grid

.. _compute-dt-grid:

.. _compute-dt-grid-command:

#######################
compute dt/grid command
#######################

.. _compute-dt-grid-kk-command:

##########################
compute dt/grid/kk command
##########################

.. _compute-dt-grid-syntax:

*******
Syntax:
*******

::

   compute ID dt/grid group-ID tfraction cfraction tau temperature usq vsq wsq

- ID is documented in :ref:`compute<compute>` command 

- dt/grid = style name of this compute command

- group-ID = group ID for which grid cells to perform calculation on

- tfraction = fraction of grid cell transit time used to calculate timestep

- cfraction = fraction of grid cell mean collision time used to calculate timestep

- tau = compute or fix column for mean collision time, prefaced by "c\_" or "f\_"

- temperature = compute or fix column for temperature, prefaced by "c\_" or "f\_"

- usq = compute or fix column for x component of velocity squared, prefaced by "c\_" or "f\_"

- vsq = compute or fix column for y component of velocity squared, prefaced by "c\_" or "f\_"

- wsq = compute or fix column for z component of velocity squared, prefaced by "c\_" or "f\_"

.. _compute-dt-grid-examples:

*********
Examples:
*********

::

   compute 1 grid all mymixture nrho temp usq vsq wsq
   fix 1 ave/grid all 10 50 500 c_1\[\*\]
   compute mct lambda/grid f_1\[1\] f_1\[2\] tau
   compute tstep dt/grid all 0.25 0.1 c_mct f_1\[2\] f_1\[3\] f_1\[4\] f_1\[5\]

.. _compute-dt-grid-descriptio:

************
Description:
************

Calculate a current timestep for each grid cell in a grid cell group,
based on the properties of particles currently in the cell and the
grid cell size.  The per-grid cell timesteps can be output in a
per-grid dump file for post analyses.  Or they can be used as input to
the :ref:`fix dt/reset<fix-dt-reset>` command to adjust the global
timestep for a variable timestep simulation.  See this
:ref:`section<howto-618-variable-timestep-simulation>` of the manual for more
information on variable timestep simulations.

Only grid cells in the grid group specified by *group-ID* are included
in the calculations.  See the :ref:`group grid<group>` command for info
on how grid cells can be assigned to grid groups.

The *tfraction* and *cfraction* arguments are both values from 0.0 to
1.0 which are applied to the transit term and collision term in the
example formula for a candidate cell timestep below.

.. math:: \Delta t_{\mathrm{cell}} = \min{\left( \mathrm{cfraction} \times \mathrm{mean\_collision\_time}, \mathrm{tfraction}\times \Delta x /\mathrm{max\_most\_probable\_speed} \right)}

In practice, multiple transit-based timestep candidates are
constructed based on the cell dimensions in each coordinate direction
and the associated average particle velocity components in addition to
the maximum most probable speed.  The selected cell timestep is the
minumum of all candidate timesteps. The collision and transit
fractions simply provide a user-defined safety margin for the
collision time and transit time estimates. In :ref:`(Bird2013)<Bird2013>`,
Bird recomnmends setting the collision fraction to 0.2, which is
likely a good starting point for the selection of both of these
fractions.

The remaining 5 arguments specify either computes which calculate various per
grid cell quantities or fixes which time average those
per grid cell quantities.  The 5 quantities are per grid cell mean
collision time (tau), temperature, and the xyz components of the
velocity squared for particles in the grid cell. A mean collision time can be
calculated with the :ref:`compute lambda/grid<compute-lambda-grid>` command using the
tau option. The :ref:`compute grid<compute-grid>` command can calculate the other 4 quantities.
The :ref:`compute thermal/grid<compute-thermal-grid>` command can also
compute a per grid cell temperature.

This is done by specifying the tau, temperature, usq, vsq, wsq
arguments like this:

   - c_ID = compute with ID that calculates a per grid cell quantity as a vector output
   - c_ID\[m\] = compute with ID that calculates a quantity as its Mth column of array output
   - f_ID\[m\] = fix with ID that calculates a time-averaged quantity as a vector output
   - f_ID\[m\] = fix with ID that calculates a time-averaged quantity as its Mth column of array output

See the Example section above for an example of how these arguments
can be specified.

.. important::

  If the IDs of one or more :ref:`fix   ave/grid<fix-ave-grid>` commands is used for these 5 arguments,
  they only produce output on timesteps that are multiples of their
  *Nfreq* argument.  Thus this compute can only be invoked on those
  timesteps.

.. _compute-dt-grid-output-info:

************
Output info:
************

This compute calculates a per-grid vector.

.. note::

  that cells inside closed surfaces contain no particles.  These
  could be unsplit or cut cells (if they have zero flow volume).  Both
  of these kinds of cells will compute a zero result for the cell timestep.
  Likewise, split cells store no particles and will produce a zero result.
  This is because their sub-cells actually contain the particles that are
  geometrically inside the split cell.  Additionally, any cell that is able
  to store particles but does not have any particles when this compute is
  invoked produces a zero result.  Finally, a zero result is produced if any
  cell data to be used in the timestep calculation is
  zero (including temperature, speed, and mean collision time).

The vector can be accessed by any command that uses per-grid values
from a compute as input.  See :ref:`Section 4.4<howto-64-output-sparta-(stats,>`
for an overview of SPARTA output options.

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

.. _compute-dt-grid-restrictio:

*************
Restrictions:
*************

As explained above, to use this compute with *nrho* or *temp* defined
as input from a :ref:`fix ave/grid<fix-ave-grid>` command, this compute
must only be invoked on timesteps that are multiples of the *Nfreq*
argument used by the fix, since those are the steps when it produces
output.

.. _compute-dt-grid-related-commands:

*****************
Related commands:
*****************

:ref:`fix dt/reset<fix-dt-reset>`, :ref:`compute grid<compute-grid>`,
:ref:`compute thermal/grid<compute-thermal-grid>`, :ref:`compute lambda/grid<compute-lambda-grid>`,
:ref:`fix ave/grid<fix-ave-grid>`

.. _compute-dt-grid-default:

********
Default:
********

none

.. _Bird2013:

**(Bird2013)** G. A. Bird, The DSMC method, CreateSpace Independent Publishing Platform, 2013.

