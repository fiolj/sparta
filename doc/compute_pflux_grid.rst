:orphan:

.. index:: compute pflux/grid
.. index:: compute pflux/grid/kk

.. _command-compute-pflux-grid:

##########################
compute pflux/grid command
##########################

.. _command-compute-pflux-grid-compute-pfluxgridkk:

#############################
compute pflux/grid/kk command
#############################


*******
Syntax:
*******

::

   compute ID pflux/grid group-ID mix-ID value1 value2 ... 

-  ``ID`` is documented in :ref:`compute<command-compute>` command
-  ``pflux/grid`` = style name of this compute command
-  ``group-ID`` = group ID for which grid cells to perform calculation on
-  ``mix-ID`` = mixture ID to perform calculation on
-  one or more values can be appended

   ``values`` = *momxx* or *momyy* or *momzz* or *momxy* or *momyz* or
   *momxz*

   - ``momxx,momyy,momzz`` = diagonal components of momentum flux density tensor
   - ``momxy,momyz,momxz`` = off-diagonal components of momentum flux density tensor 

*********
Examples:
*********

::

   compute 1 pflux/grid all species momxx momyy momzz
   compute 1 pflux/grid subset species momxx momxy 

These commands will dump 10 time averaged momentum flux densities for
each species and each grid cell to a dump file every 1000 steps:

::

   compute 1 pflux/grid all species momxx momyy momzz
   fix 1 ave/grid 10 100 1000 c_1[*]
   dump 1 grid all 1000 tmp.grid id f_1[*] 

************
Description:
************

Define a computation that calculates components of the momemtum flux
density tensor for each grid cell in a grid cell group. This is
equivalent to the kinetic energy density tensor, and is based on the
thermal velocity of the particles in each grid cell. The values are
tallied separately for each group of species in the specified mixture,
as described in the Output section below. See the mixture command for
how a set of species can be partitioned into groups.

Only grid cells in the grid group specified by *group-ID* are included
in the calculations. See the :ref:`group grid<command-group>` command for
info on how grid cells can be assigned to grid groups.

The values listed above rely on first computing and subtracting the
center-of-mass (COM) velocity for all particles in the group and grid
cell from each particle to yield a thermal velocity. This thermal
velocity is used to compute the components of the momentum flux density
tensor, as described below. This is in contrast to some of the values
tallied by the :ref:`compute grid temp<command-compute-grid>` command which
simply uses the full velocity of each particle to compute a momentum or
kinetic energy density. For non-streaming simulations, the two results
should be similar, but for streaming flows, they will be different.

The results of this compute can be used by different commands in
different ways. The values for a single timestep can be output by the
:ref:`dump grid<command-dump>` command.

The values over many sampling timesteps can be averaged by the :ref:`fix ave/grid<command-fix-ave-grid>` command. It does its averaging as if the
particles in the cell at each sampling timestep were combined together
into one large set of particles to compute the formulas below.

Note that the center-of-mass (COM) velocity that is subtracted from each
particle to yield a thermal velocity for each particle, as described
below, is also computed over one large set of particles (across all
timesteps), in contrast to using a COM velocity computed only for
particles in the current timestep, which is what the :ref:`compute sonine/grid<command-compute-sonine-grid>` command does.

Note that this is a different form of averaging than taking the values
produced by the formulas below for a single timestep, summing those
values over the sampling timesteps, and then dividing by the number of
sampling steps.

--------------

Calculation of the momentum flux density is done by first calculating the
center-of-mass (COM) velocity of particles for each group within a grid
cell. This is done as follows:

::

   COMx = Sum_i (mass_i Vx_i) / Sum_i (mass_i)
   COMy = Sum_i (mass_i Vy_i) / Sum_i (mass_i)
   COMz = Sum_i (mass_i Vz_i) / Sum_i (mass_i)
   Cx = Vx - COMx
   Cy = Vy - COMy
   Cz = Vz - COMz 

The COM velocity is (COMx,COMy,COMz). The thermal velocity of each
particle is (Cx,Cy,Cz), i.e. its velocity minus the COM velocity of
particles in its group and cell.

The *momxx*, *momyy*, *momzz* values compute the diagonal components of
the momentum flux density tensor due to particles in the group as
follows:

::

   momxx = fnum/volume Sum_i (mass_i Cx^2)
   momyy = fnum/volume Sum_i (mass_i Cy^2)
   momzz = fnum/volume Sum_i (mass_i Cz^2) 

The *momxy*, *momyz*, *momxz* values compute the off-diagonal components
of the momentum flux density tensor due to particles in the group as
follows:

::

   momxy = fnum/volume Sum_i (mass_i Cx Cy)
   momyz = fnum/volume Sum_i (mass_i Cy Cz)
   momxz = fnum/volume Sum_i (mass_i Cx Cz) 

Note that if particle weighting is enabled via the :ref:`global weight<command-global>` command, then the volume used in the formula is
divided by the weight assigned to the grid cell.

--------------

************
Output info:
************

This compute calculates a per-grid array, with the number of columns
equal to the number of values times the number of groups. The ordering
of columns is first by values, then by groups. I.e. if *momxx* and
*momxy* values were specified as keywords, then the first two columns
would be *momxx* and *momxy* for the first group, the 3rd and 4th
columns would be *momxx* and *momxy* for the second group, etc.

This compute performs calculations for all flavors of child grid cells
in the simulation, which includes unsplit, cut, split, and sub cells.
See :ref:`Section 6.8<howto-grids>` of the manual gives
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
a compute as input. See :ref:`Section 6.4<howto-output>` for
an overview of SPARTA output options.

The per-grid array values will be in the :ref:`units<command-units>` of
momentum flux density = energy density = energy/volume units.

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

:ref:`command-compute-grid`,
:ref:`command-compute-thermal-grid`,
:ref:`command-compute-eflux-grid`,
:ref:`command-fix-ave-grid`,
:ref:`dump grid<command-dump>`

********
Default:
********
 none
