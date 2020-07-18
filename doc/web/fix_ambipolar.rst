:orphan:

.. index:: fix ambipolar



.. _command-fix-ambipolar:

#####################
fix ambipolar command
#####################


*******
Syntax:
*******

::

   fix ID ambipolar especies ion1 ion2 ... 

-  ID is documented in :ref:`fix<command-fix>` command
-  ambipolar = style name of this fix command
-  especies = species ID for ambipolar electrons
-  ion1,ion2,... = species IDs for one or more ambipolar ions

*********
Examples:
*********

::

   fix 1 ambipolar e N+ O+ NO+ 

************
Description:
************

Enable the ambipolar approximation to be used in a simulation. The
ambipolar approximation is a computationally efficient way to model
low-density plasmas which contain positively-charged ions and
negatively-charged electrons. In this model, electrons are not free
particles which move independently. This would require a simulation with
a very small timestep due to electon's small mass and high speed (1000x
that of an ion or neutral particle).

Instead each ambipolar electron is assumed to stay "close" to its parent
ion, so that the plasma gas appears macroscopically neutral. Each pair
of particles thus moves together through the simulation domain, as if
they were a single particle, which is how they are stored within SPARTA.
This means a normal timestep can be used.

An overview of how to run simulations with the ambipolar approximation
is given in the :ref:`Section 6.11<howto-ambipolar>`. This
includes gas-phase collisions and chemistry as well as surface chemistry
when particles collide with surface elements or the global boundary of
the simulation box. The section also lists all the commands that can be
used in an input script to invoke various options associated with the
ambipolar approximation. All of them depend on this fix ambipolar
command being defined.

This command defines *especies* which is the species ID associated with
the ambipolar electrons. It also specifies one or more species IDs as
*ion1*, *ion2*, etc for ambipolar ions. SPARTA checks that the especies
has a negative charge (as read in by the :ref:`species<command-species>`
command), and the ions have positive charges. An error is flagged if
that is not the case.

Internally, this fix defines two custom particle attributes. The first
is named "ionambi" and is an integer vector (one integer per particle).
It stores a value of 1 for ambipolar ions, or 0 otherwise. The second is
named "velambi" and is a floating-point arrays (3 values per particle).
It stores the velocity of the ambipolar electron associated with the
ambipolar ion, or zeroes otherwise.

--------------

*********************
Restart, output info:
*********************

No information about this fix is written to :ref:`binary restart files<command-restart>`.

However, the values of the two custom particle attributes defined by
this fix are written to the restart file. Namely the integer value
"ionambi" and floating-point velocity values "velambi" for each
particle. As explained on the :ref:`read_restart<command-read-restart>` doc
page these values can be re-assigned to particles when a restart file is
read, if a new fix ambipolar command is specified in the restart script
before the first :ref:`run<command-run>` command is used.

No global or per-particle or per-grid quantities are stored by this fix
for access by various output commands.

However, the two custom particle attributes defined by this fix can be
accessed by the :ref:`dump particle<command-dump>` command, as p_ionambi and
p_velambi. That means those per-particle values can be written to
particle dump files.

*************
Restrictions:
*************
 none

*****************
Related commands:
*****************

:ref:`collide_modify ambipolar yes<command-collide-modify>`

********
Default:
********
 none
