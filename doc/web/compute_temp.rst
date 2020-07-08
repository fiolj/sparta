:orphan:

.. index:: compute temp
.. index:: compute temp/kk





.. _command-compute-temp:

####################
compute temp command
####################






.. _command-compute-temp-compute-tempkk:

#######################
compute temp/kk command
#######################



*******
Syntax:
*******

::

   compute ID temp 

-  ID is documented in :ref:`compute<command-compute>` command
-  temp = style name of this compute command

*********
Examples:
*********

::

   compute 1 temp
   compute myTemp temp 

************
Description:
************

Define a computation that calculates the temperature of all particles.

The temperature is calculated by the formula KE = dim/2 N kB T, where KE
= total kinetic energy of the particles (sum of 1/2 m v^2), dim =
dimensionality of the simulation, N = number of particles, kB =
Boltzmann constant, and T = temperature.

Note that this definition of temperature does not subtract out a net
streaming velocity for particles, so it is not a thermal temperature
when the particles have a non-zero streaming velocity. See the :ref:`compute thermal/grid<command-compute-thermal-grid>` command for calculation of
thermal temperatures on a per grid cell basis.

--------------

**Output info:**

This compute calculates a global scalar (the temperature). This value
can be used by any command that uses global scalar values from a compute
as input. See :ref:`Section 6.4<howto-output>` for an
overview of SPARTA output options.

The scalar value will be in temperature :ref:`units<command-units>`.

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
*****************

none

********
Default:
********
 none
