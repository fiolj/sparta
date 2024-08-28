
:orphan:

.. index:: fix_vibmode

.. _fix-vibmode:

.. _fix-vibmode-command:

###################
fix vibmode command
###################

.. _fix-vibmode-syntax:

*******
Syntax:
*******

::

   fix ID vibmode

ID is documented in :ref:`fix<fix>` command
vibmode = style name of this fix command

.. _fix-vibmode-examples:

*********
Examples:
*********

::

   fix 1 vibmode

.. _fix-vibmode-descriptio:

************
Description:
************

Enable multiple vibrational energy levels, defined on a per-species
basis, to be used in a simulation.  This fix is meant to be used with
the :ref:`collide_modify vibrate discrete<collide-modify>` setting
which means that the vibrational energy of each (non-monoatomic)
particle is discretized across one or more energy modes, each with its
own characteristic vibrational temperature.  This fix allocates
per-particle storage for the mode indices and also has code to
populate the multiple levels appropriately when particles are created.
Collisions between pairs of particles will then transfer energy
between the different modes of the two particles.

An overview of how to run simulations with multiple vibrational energy
modes is given in the :ref:`Section 4.12<howto-multiple-vibrationa-energy-levels>`.
This includes use of the :ref:`species<species>` command with its
*vibfile* option, and the use of the :ref:`collide_modify vibrate discrete<collide-modify>` command.  The section also lists all the
commands that can be used in an input script to invoke various options
associated with the vibrational energy modes.  All of them depend on
this fix vibmode command being defined.

Internally, this fix defines a custom particle attribute named
"vibmode".  It is an integer array with N values per particle.  N is
the maximum number of energy modes for any species defined in the
simulation.  The number of energy modes is half the vibrational
degrees of freedom defined for each species.  See the "species"
command for how the degrees of freedom and associated vibrational
temperatures and other properties are defined for each mode for each
species.

Each of the N values is an integer count for the

.. _fix-vibmode-restart,-output-info:

*********************
Restart, output info:
*********************

No information about this fix is written to :ref:`binary restart files<restart>`.

However, the values of the custom particle attribute defined by this
fix are written to the restart file.  Namely the integer values stored
in "vibmode" for each particle.  As explained on the
:ref:`read_restart<read-restart>` doc page these values can be
re-assigned to particles when a restart file is read, if a new fix
vibmode command is specified in the restart script before the first
:ref:`run<run>` command is used.

No global or per-particle or per-grid quantities are stored by this
fix for access by various output commands.

However, the custom particle attributes defined by this fix can be
accessed by the :ref:`dump particle<dump>` command, as p_vibmode.  That
means those per-particle values can be written to particle dump files.

.. _fix-vibmode-restrictio:

*************
Restrictions:
*************

This fix is required if "collide_modify vibrate discrete" is used and
there is one or more species defined which haave multiple vibrational
energy modes (2 or more).  In this scenario, if it is not defined, an
error will occur when a "create_particles" or :ref:`run<run>` command
is issued.  Conversely, if no species has multiple vibrational modes,
this fix cannot be used.

Defining this fix after particles have been created will not populate
the vibrational energy modes of particles that already exist.  An
exception is if the :ref:`read_restart<read-restart>` command is used
to read in particles from a previous simulation where this fix was
used.  In that case, defining this fix after reading the restart file
will enable the particles to keep their previous vibrational energy
mode values.

.. _fix-vibmode-related-commands:

*****************
Related commands:
*****************

:ref:`collide_modify vibrate discrete<collide-modify>`

.. _fix-vibmode-default:

********
Default:
********

none

