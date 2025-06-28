
:orphan:

.. index:: compute_ke_particle

.. _compute-ke-particle:

.. _compute-ke-particle-command:

###########################
compute ke/particle command
###########################

.. _compute-ke-particle-kk-command:

##############################
compute ke/particle/kk command
##############################

.. _compute-ke-particle-syntax:

*******
Syntax:
*******

::

   compute ID ke/particle

   - ID is documented in :ref:`compute<compute>` command
   - ke/particle = style name of this compute command

.. _compute-ke-particle-examples:

*********
Examples:
*********

::

   compute 1 ke/particle

.. _compute-ke-particle-descriptio:

************
Description:
************

Define a computation that calculates the per-atom translational
kinetic energy for each particle.

The results of this compute can be used by different commands in
different ways.  The values for a single timestep can be output by the
:ref:`dump particle<dump>` command.

The kinetic energy is

::

   Vsq = Vx\*Vx + Vy\*Vy + Vz\*Vz
   KE = 1/2 m Vsq

where m is the mass and (Vx,Vy,Vz) are the velocity components of the
particle.

.. _compute-ke-particle-output-info:

************
Output info:
************

This compute calculates a per-particle vector, which can be accessed
by any command that uses per-particle values from a compute as input.

The vector can be accessed by any command that uses per-particle
values from a compute as input.  See :ref:`Section 4.4<howto-64-output-sparta-(stats,>` for an overview of SPARTA output
options.

The per-particle vector values will be in energy :ref:`units<units>`.

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

.. _compute-ke-particle-restrictio:

*************
Restrictions:
*************

none

.. _compute-ke-particle-related-commands:

*****************
Related commands:
*****************

:ref:`dump particle<dump>`

.. _compute-ke-particle-default:

********
Default:
********

none

