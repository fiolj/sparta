:orphan:

.. index:: compute tvib/grid



.. _command-compute-tvib-grid:

#########################
compute tvib/grid command
#########################


*******
Syntax:
*******

::

   compute ID tvib/grid group-ID mix-ID keyword ... 

-  ID is documented in :ref:`compute<command-compute>` command
-  tvib/grid = style name of this compute command
-  group-ID = group ID for which grid cells to perform calculation on
-  mix-ID = mixture ID to perform calculation on
-  zero or more keywords can follow

   ::

        possible keywords = mode
        mode = output one temperature per vibrational mode 

*********
Examples:
*********

::

   compute 1 tvib/grid all species
   compute 1 tvib/grid subset all
   compute 1 tvib/grid all species mode 

************
Description:
************

Define a computation that calculates the vibrational temperature for
each grid cell in a grid cell group, based on the particles in the cell.
How the vibrational temperature is computed is explained below. The
temperature is calculated separately for each group of species in the
specified mixture, as described in the Output section below. See the
mixture command for how a set of species can be partitioned into groups.

Only grid cells in the grid group specified by *group-ID* are included
in the calculations. See the :ref:`group grid<command-group>` command for
info on how grid cells can be assigned to grid groups.

The results of this compute can be used by different commands in
different ways. The values for a single timestep can be output by the
:ref:`dump grid<command-dump>` command.

The values over many sampling timesteps can be averaged by the :ref:`fix ave/grid<command-fix-ave-grid>` command. It does its averaging as if the
particles in the cell at each sampling timestep were combined together
into one large set to compute the formulas below. Note that this is a
different normalization than taking the values produced by the formulas
below for a single timestep, summing them over the sampling timesteps,
and then dividing by the number of sampling steps.

If the *mode* keyword is specified, then temperatures for each
vibrational mode of each polyatomic species are calculated and output as
explained below. To use this option, the :ref:`collide_modify vibrate discrete<command-collide-modify>` option must be set, and the "fix
vibmode" command must be used to store info about individual vibrational
modes with each particle.

--------------

The vibrational temperature in a grid cell for a group of particles
comprised of different species and (optionally) different vibrational
modes is defined as a weighted average as follows:

::

   T_group = (T1*N1 + T2*N2 + ...) / (N1 + N2 + ...) 

What is summed over in the numerator and denominator depends on several
settings.

If the :ref:`collide_modify vibrate<command-collide-modify>` setting is *no*,
then no vibrational energy is assigned to particles. All the output
temperatures will be 0.0.

If the :ref:`collide_modify vibrate<command-collide-modify>` setting is
*smooth*, then the sums in the numerator and denominator are over the
different species in the group. T1, T2, ... are the vibrational
temperatures of each species. N1, N2, ... are the counts of particles of
each species.

The vibrational temperature Tsp for particles of a single species is
defined as follows:

::

   Ibar = Sum_i (e_vib_i) / (N kB Theta)
   Tsp = Theta / ln(1 + 1/Ibar)) 

where e_vib is the continuous (smooth) vibrational energy of a single
particle I, N is the total # of particles of that species, and *kB* is
the Boltzmann factor. Theta is the characteristic vibrational
temperature for the species, as defined in the file read by the
:ref:`species<command-species>` command.

If the :ref:`collide_modify vibrate<command-collide-modify>` setting is
*discrete*, but no species has a vibrational DOF setting that implies
multiple vibrational modes (vibdof = 4,6,8), then the calulation of
vibrational temeperatures is the same as for :ref:`collide_modify vibrate smooth<command-collide-modify>`. See the :ref:`species<command-species>`
command and its description of the per-species "vibdof" setting in the
species file.

If the :ref:`collide_modify vibrate<command-collide-modify>` setting is
*discrete*, and one or more species have vibrational DOF settings that
imply multiple vibrational modes (vibdof = 4,6,8), as defined by the
:ref:`species<command-species>` command, then the sums in the numerator and
denominator are over the different species in the group and the modes
for each species. For example if species CO2 has vibdof=6, then it has 3
modes. Three terms in the numerator and demoninator are included when
CO2 is a species in the group.

The vibrational temperature Tsp_m for particles of a single species and
single mode M is defined as follows:

::

   Ibar_m = Sum_i (level_im) / (N)
   Tsp_m = Theta_m / ln(1 + 1/Ibar_m)) 

where level_im is the integer level for mode M of a single particle I,
and N is the total # of particles of that species. Theta_m is the
characteristic vibrational temperature for the species and its mode M,
as defined in the vibfile read by the :ref:`species<command-species>`
command.

Finally, if the *mode* keyword is used, then the output of this compute
is not Ngroup vibrational temperatures, but rather Ngroup*Nmode
vibrational temperatures, where Nmode is the maximum # of vibrational
modes associated with any species in the system (not just in the
mixture). Thus the sums in the numerator and denominator are over the
different species in the group but for only a single modes of each of
those species. If the species does not define that mode, then its
contribution is zero. For example if species CO2 has vibdof=6, then it
has 3 modes. For the group it is in, it will contribute to 3 output
temperature values, one for mode 1, another for mode 2, another for mode
3.

The vibrational temperature Tsp_m for particles of a single species and
single mode M is calculated the same as explained above.

--------------

**Output info:**

This compute calculates a per-grid array. If the *mode* keyword is not
specified, the number of columns is equal to the number of groups in the
specified mixture. If is is specified, the number of columns is equal to
the number of groups in the specified mixture times the maximum number
of vibrational modes defined for any species in the system (not just in
the mixture). The ordering of the columns is as follows: T11, T12, T13,
T21, T22, T23, T31, ... TN1, TN2, TN3. Where the first index is the
group from 1 to N, and the second index is the vibrational mode (1 to 3
in this example).

This compute performs calculations for all flavors of child grid cells
in the simulation, which includes unsplit, cut, split, and sub cells.
See :ref:`Section 4.8<howto-grids>` of the manual gives
details of how SPARTA defines child, unsplit, split, and sub cells. Note
that cells inside closed surfaces contain no particles. These could be
unsplit or cut cells (if they have zero flow volume). Both of these
kinds of cells will compute a zero result for all their values.
Likewise, split cells store no particles and will produce a zero result.
This is because their sub-cells actually contain the particles that are
geometrically inside the split cell.

Grid cells not in the specified *group-ID* will output zeroes for all
their values.

The array can be accessed by any command that uses per-grid values from
a compute as input. See :ref:`Section 4.4<howto-output>` for
an overview of SPARTA output options.

The per-grid array values will be in temperature :ref:`units<command-units>`.

*************
Restrictions:
*************
 none

*****************
Related commands:
*****************

:ref:`command-compute-grid`

********
Default:
********
 none
