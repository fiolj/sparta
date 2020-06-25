:orphan:

.. index:: collide



.. _command-collide:

###############
collide command
###############


**Syntax:**

::

   collide style args keyword value ... 

-  style = *none* or *vss*
-  args = arguments for that style

   ::

        none args = none
        vss args = mix-ID file
          mix-ID = ID of mixture to use for group definitions
          file = filename that lists species with their VSS model parameters
        vss/kk args = mix-ID file
          mix-ID = ID of mixture to use for group definitions
          file = filename that lists species with their VSS model parameters 

-  zero or more keyword/value pairs may be appended
-  keyword = *relax*

   ::

        relax value = constant or variable 

**Examples:**

::

   collide none
   collide vss all ../data/air.vss
   collide vss species all.vss relax variable 

**Description:**

Define what style of particle-particle collisions will be performed by
SPARTA each timestep. If collisions are performed, particles are sorted
into grid cells every timestep and the appropriate collision model is
invoked on a per-grid-cell basis. Collisions alter the velocity of
participating particles as well as their rotational and vibrational
energies. The rotational and vibrational properties of each species are
set in the file read by the :ref:`species<command-species>` command.

The collision style determines how many pairs of particles are
considered for collisions, the criteria for which collisions actually
occurs, and the outcome of individual collision, which alters the
velocities of the two particles. If chemistry is enabled, via the
:ref:`react<command-react>` command, particles involved in collisions may
also change species, or a particle may be deleted, or a new particle
created. The :ref:`collide_modify<command-collide-modify>` command can also
be used to alter aspects of how collisions are performed. For example,
it can be used to turn on/off the tracking of vibrational energy and its
exchange in collisions.

A *mix-ID* argument is specified for each collision style. It must
contain all the species defined for use by the simulation, via the
:ref:`species<command-species>` command. The group definitions in the mixture
assign one or more particle species to each group. These groupings are
used to determine how pairs of particles are chosen to collide with each
other, in the following manner.

Consider a cell with N particles and a mixture with M groups. Based on
its species, each particle is assigned to one of the M groups. Each
unique pair of groups is considered, including each group paired with
itself. For each pair of groups a value *Nattempt* (see equation 11.3 in
[Bird94]_) is calculated which is the number of collisions
to attempt. This is a function of N1 and N2 (the number of particles in
each group), the grid cell volume, and other parameters of the collision
style.

For each collision attempt, a random pair of particles is selected, with
one particle from each group. Whether the collision occurs or not is a
function of the relative velocities of the two particles, their
respectives species, and other parameters of the collision style; see
equation 11.4 in [Bird94]_.

--------------

The *none* style means that no particle-particle collisions will be
performed, i.e. the simulation models free-molecular flow.

--------------

The *vss* style implements the Variable Soft Sphere (VSS) model for
collisions. As discussed below, with appropriate parameter choices, it
can also compute the Variable Hard Sphere (VHS) model and the Hard
Sphere (HS) model. See chapters 2.6 and 2.7 in [Bird94]_
for details.

In DSMC, the variable-soft-sphere (VSS) interaction of Koura and
Matsumoto [Koura92]_ and the variable-hard-sphere (VHS) interaction
of [Bird94]_ are used to approximate molecular interactions.
Both models yield transport properties proportional to a power (omega)
of the gas temperature. This temperature dependence of the transport
properties is similar to the Inverse Power Law model (IPL) for which
Chapman-Enskog theory provides closed form solutions for the transport
properties.

Both VSS and VHS interactions define parameters *diam* = molecular
diameter, which is a function of the molecular speed, and *alpha* =
angular-scattering parameter, which relates the scattering angle to the
impact parameter. Setting *alpha* = 1 produces isotropic (hard sphere)
interactions, which converts the VSS model into a VHS model.

The *file* argument is for a collision data file which contains
definitions of VSS model parameters for some number of species. Example
files are included in the data directory of the SPARTA distribution,
with a "\*.css" suffix. The file can contain species not used by this
simulation; they will simply be ignored. All species currently defined
by the simulation must be present in the file.

The format of the file depends of the setting of the optional *relax*
keyword, as explained below. Comments or blank lines are allowed in the
file. Comment lines start with a "#" character. All other lines must
have the following format with parameters separated by whitespace.

If the *relax* keyword is specified as *constant*, which is the default,
then each line has 4 parameters following the species ID:

::

   species-ID diam omega tref alpha 

The species-ID is a string that will be matched to one of the species
defined by the simulation, via the :ref:`species<command-species>` command.
The meaning of additional properties is as follows:

-  diam = VHS or VSS diameter of particle (distance units)
-  omega = temperature-dependence of viscosity (unitless)
-  tref = reference temperature (temperature units)
-  alpha = angular scattering parameter (unitless)

The methodolgy for deriving VSS/VHS parameters from these properties is
explained in Chapter 3 of [Bird94]_. Parameter values for
the most common gases are given in Appendix A of the same book. These
values are based on the first-order approximation of the Chapman-Enskog
theory. Infinite-order parameters are described in
[Gallis04]_.

In the *constant* case rotational and vibrational relaxation during a
collision is treated in the same constant manner for every collision,
using the rotational and vibrational relaxation numbers from the species
data file, as read by the :ref:`species<command-species>` command.

If the *relax* keyword is specified as *variable*, then each line has 8
parameters following the species ID:

::

   species-ID diam omega tref alpha Zrotinf T* C1 C2 

The first 4 parameters are the same as above. Parameters 5 and 6 affect
rotational relaxation; parameters 7 and 8 affect vibrational relaxation.
In this case the rotational and vibrational relaxation during a
collision is treated as a variable and is computed for each collision.
This calculation is only performed for polyatomic species, using
equations A5 and A6 on pages 413 and 414 in [Bird94]_.
Zrotinf and T\* are parameters in the numerator and denominator of eq
A5. C1 and C2 are in eq A6. The units of these parameters is as follows:

-  Zrotinf (unitless)
-  T\* (temperature units)
-  C1 (temperature units)
-  C2 (temperature^(1/3) units)

Note that a collision data file with the 4 extra relaxation parameters
(per species) can be used when the *relax* keyword is specified as
*constant*. In that case, the extra parameters are simply ignored.

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

**Restrictions:** none

**Related commands:**

:ref:`command-collide-modify`,
:ref:`command-mixture`,
:ref:`command-react`

**Default:**

Style = none is the default (no collisions). If the vss style is specified, then relax = constant is the default.

--------------

.. [Koura92] K. Koura and H. Matsumoto, "Variable soft sphere molecular model for air species," Phys Fluids A, 4, 1083 (1992).


.. [Gallis04] M. A. Gallis, J. R. Torczynski, and D. J. Rader, "Molecular gas dynamics observations of Chapman-Enskog behavior and departures therefrom in nonequilibrium gases," Phys Rev E, 69, 042201 (2004).
