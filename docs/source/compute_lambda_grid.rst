
:orphan:

.. index:: compute_lambda_grid

.. _compute-lambda-grid:

.. _compute-lambda-grid-command:

###########################
compute lambda/grid command
###########################

.. _compute-lambda-grid-kk-command:

##############################
compute lambda/grid/kk command
##############################

.. _compute-lambda-grid-syntax:

*******
Syntax:
*******

::

   compute ID lambda/grid nrho temp value1 value2 ...

- ID is documented in :ref:`compute<compute>` command 

- lambda/grid = style name of this compute command

- nrho = compute or fix for number density, prefaced by "c\_" or "f\_"

- temp = NULL or compute or fix column for temperature, prefaced by "c\_" or "f\_"

- value = *lambda* or *tau* or *knall* or *knx* or *kny* or *knz*

::

     *lambda* = calculate mean free path
     *tau* = calculate mean collision time
     *knall* = calculate Knudsen number based on cell size in all dimensions
     *knx* = calculate Knudsen number based on cell size in x dimension
     *kny* = calculate Knudsen number based on cell size in y dimension
     *knz* = calculate Knudsen number based on cell size in z dimension

.. _compute-lambda-grid-examples:

*********
Examples:
*********

::

   compute 1 lambda/grid c_GR\[\*\] NULL lambda tau
   compute 1 lambda/grid f_ave\[\*\] f_ave\[3\] lambda knall

These commands will dump time averages for the mean free path and mean
collision time for each grid cell to a dump file every 1000 steps:

::

   compute 1 grid species nrho temp
   fix 1 ave/grid 10 100 1000 c_1\[\*\]
   compute 2 lambda/grid f_1\[1\] f_1\[2\] lambda tau
   dump 1 grid all 1000 tmp.grid id c_2

.. _compute-lambda-grid-descriptio:

************
Description:
************

If the *lambda* keyword is specified, the mean free path will be
computed. If the *tau* keyword is specified, the mean collision time
between molecular collisions for each grid cell based on the particles
in that cell will be computed. If one or more of the *knall* or *knx*
or *kny* or *knz* keywords are specified, the dimensionless Knudsen
number will be calculated, which is the ratio of the mean free path to
the cell size. For *knall*, the cell size is taken to be the average
of the three grid cell side lengths (or two cell lengths for a 2d
simulation).  For *knx*, *kny*, or *knz*, the cell size is the single
cell side length in the corresponding x,y,z dimension. The Knudsen
number can be useful for estimating the optimal grid cell size when
adapting the grid, e.g.  via the :ref:`adapt_grid<adapt-grid>` or :ref:`fix adapt/grid<fix-adapt-grid>` commands, as well as the optimal time
step size.

Unlike other computes that calculate per grid cell values, this
compute does not take a "group-ID" for a grid cell group as an
argument, nor a particle :ref:`mixture<mixture>` ID as an argument.
This is because it uses the number density and temperature calculated
by other computes or fixes as input, and those computes or fixes use
grid group IDs or mixture IDs as part of their computations.

The results of this compute can be used by different commands in
different ways.  For example, the values can be output by the
:ref:`dump grid<dump>` command.

The formula used to calculate the mean free path (lambda) is given in
:ref:`(Bird94)<Bird94>` as equation 4.77:

.. math:: \lambda = \sum_{p=1}^{s} \frac{n_{p}}{n} \left [ \sum_{q=1}^{s}  \left \{ \pi (d_{\rm ref})^2_{pq} n_{q} \left (\frac{(T_{\rm ref})_{pq}}{T} \right )^{\omega_{pq} - 1/2} \left (1+\frac{m_{p}}{m_{q}} \right )^{1/2} \right \} \right ]^{-1}

.. note::

  In October 2024, the formula to compute the mean free path was updated
  to the equation above, from :ref:`(Bird94)<Bird94>`, equation 4.65:

.. math:: \lambda = \left\{ \sqrt{2}\pi D^{2}_{\rm ref} n \left ({(T_{\rm ref})}/{T} \right )^{\omega - 1/2} \right\} ^{-1}

The new formula is more accurate as it uses the number densities, 
translational temperatures and VSS parameters of each gases in the
mixture, as opposed to using the flow total number density and the
VSS parameters of only one species.
This will make a significant difference for gas mixtures, in particular
for reacting flow problems where the composition of the mixture changes
significantly in time.

The formula used to calculate the mean collision time (tau) is given in
:ref:`(Bird94)<Bird94>` as equation 1.38 combined with 4.75:

.. math:: \tau = \sum_{p=1}^{s} \frac{n_{p}}{n} \left [ \sum_{q=1}^{s}  \left \{ 2(d_{\rm ref})^2_{pq} n_{q} \left (\frac{T}{(T_{\rm ref})_{pq}} \right )^{1 - \omega_{pq}} \left ( \frac{2 \pi k (T_{\rm ref})_{pq}}{m_{r}} \right )^{1/2} \right \} \right ]^{-1}

These are the exact mean free path and mean collision time for a
multi-species mixture, suitable for estimating optimal grid cell sizes
and timestep as explained above.

*dref* and *Tref* and *omega* are collision properties for a pair of
species species in the flow. Specifically, *dref* is the diameter of
molecules of the species pair, *Tref* is the reference temperature,
and *omega* is the viscosity temperature-dependence for the species
pair.

In the formula above, *n* is the number density and *T* is the thermal
temperature of particles in a grid cell.  This compute does not
calculate these quantities itself; instead it uses another compute or
fix to perform the calculation.  This is done by specifying the *nrho*
and *temp* arguments like this:

::

   c_ID = compute with ID that calculates temp as a vector output
   c_ID\[m\] = compute with ID that calculates temp as its Mth column of array output
   c_ID\[\*\] = compute with ID that calculates nrho as an array output
   f_ID\[m\] = fix with ID that calculates a time-averaged temp as a vector output
   f_ID\[m\] = fix with ID that calculates a time-averaged temp as its Mth column of array output
   f_ID\[\*\] = fix with ID that calculates a time-averaged nrho as an array output

The *temp* argument can also be specified as NULL, which drops the
(Tref/T) ratio term from the formula above.  That is also effectively
the case if the reference species defines omega = 1/2.  In that case,
the *temp* argument is ignored, whether it is NULL or not.

.. important::

  A per species number density array calculated by
  either a compute or a fix has to be specified.  The code will
  automatically detect the number of species in the mixture to perform
  the mean free path and mean collision time calculation.  The
  :ref:`compute_grid<compute-grid>` command with mixture "species" has to
  be invoked to ensure that the number density of all the species in the
  mixture is computed.

.. note::

  that if the value of *n* is 0.0 for a grid cell, its
  mean-free-path and mean-collision-time will be set to 1.0e20 (infinite
  length and time).

.. note::

  that this temperature is inferred from
  the translational kinetic energy of the particles, which is only
  appopriate for a mean free path calculation for systems with zero or
  small streaming velocities.  For systems with streaming flow, an
  appropriate temperature can be calculated by the :ref:`compute_thermal_grid.html<howto-computes-generate-values-output>`
  thermal/grid command.  The formulas on its
  doc page show that the the center-of-mass velocity from the particles
  in each grid cell is subtracted from each particle's velocity to yield
  a translational thermal velocity, from which a thermal temperature is
  calculated.

The :ref:`fix ave/grid<fix-ave-grid>` command can calculate the same
values in a time-averaged sense, assuming it uses these same computes
as input.  Using this fix as input to this compute will thus yield
less noisy values, due to the time averaging.

.. note::

  that the compute or fix (via the compute(s) it uses as input) has to
  perform its number density calculation for a subset of
  the particles based on the "mixture" it uses.  See the
  :ref:`mixture<mixture>` command for how a set of species can be
  partitioned into groups.

.. important::

  If the ID of a :ref:`fix ave/grid<fix-ave-grid>`
  command is used as the *nrho* or *temp* argument, it only produces
  output on timesteps that are multiples of its *Nfreq* argument.  Thus
  this compute can only be invoked on those timesteps.  For example, if
  a :ref:`dump grid<dump>` command invokes this compute to write values
  to a dump file, it must do so on timesteps that are multiples of
  *Nfreq*.

.. _compute-lambda-grid-output-info:

************
Output info:
************

If only one output value is specified, this compute outputs a per-grid
vector. Otherwise outputs a per-grid array with two or more columns,
in the order the output values were specified in the input.

.. note::

  that cells inside closed surfaces contain no particles.  These
  could be unsplit or cut cells (if they have zero flow volume).  Both
  of these kinds of cells will compute a zero result for all the
  individual values.  Likewise, split cells store no particles and will
  produce a zero result.  This is because their sub-cells actually
  contain the particles that are geometrically inside the split cell.

The vector or array can be accessed by any command that uses per-grid
values from a compute as input.  See :ref:`Section 4.4<howto-output-sparta-(stats,-dumps,>` for an overview of SPARTA output
options.

The per-grid values for the column of output corresponding to *lambda*
will will be in distance :ref:`units<units>`. The column corresponding
to *tau* will be time distance divided by time :ref:`units<units>`.
Columns of corresponding to *knall* or *knx* or *kny* or *knz* will be
dimensionless.

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

.. _compute-lambda-grid-restrictio:

*************
Restrictions:
*************

To use this compute, a collision style must be defined via the
:ref:`collide<collide>` command, which defines properties for the
mixture *species*.

As explained above, to use this compute with *nrho* or *temp* defined
as input from a :ref:`fix ave/grid<fix-ave-grid>` command, this compute
must only be invoked on timesteps that are multiples of the *Nfreq*
argument used by the fix, since those are the steps when it produces
output.

One or more output values must be specified. The same output value
cannot be repeated more than once. The *knz* value cannot but used in
a two-dimensional simulation.

.. _compute-lambda-grid-related-commands:

*****************
Related commands:
*****************

:ref:`compute grid<compute-grid>`, :ref:`compute thermal/grid<compute-thermal-grid>`, :ref:`fix ave/grid<fix-ave-grid>`, :ref:`dump grid<dump>`

.. _compute-lambda-grid-default:

********
Default:
********

none

.. _Bird94:

**(Bird94)** G. A. Bird, Molecular Gas Dynamics and the Direct
Simulation of Gas Flows, Clarendon Press, Oxford (1994).

