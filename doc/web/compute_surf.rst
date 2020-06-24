:orphan:

.. index::  compute surf
.. index::  compute surf/kk





.. _command-compute-surf:

#####################
 compute surf command
#####################






.. _command-compute-surf-compute-surfkk:

########################
 compute surf/kk command
########################



**Syntax:**

::

   compute ID surf group-ID mix-ID value1 value2 ... 

-  ID is documented in :ref:`compute<command-compute>` command
-  surf = style name of this compute command
-  group-ID = group ID for which surface elements to perform calculation
   on
-  mix-ID = mixture ID for particles to perform calculation on
-  one or more values can be appended
-  value = *n* or *nwt* or *mflux* or *fx* or *fy* or *fz* or *press* or
   *px* or *py* or *pz* or *shx* or *shy* or *shz* or *ke*

   ::

        n = count of particles hitting surface element
        nwt = weighted count of particles hitting surface element
        mflux = flux of mass on surface element
        fx,fy,fz = components of force on surface element
        press = magnitude of normal pressure on surface element
        px,py,pz = components of normal pressure on surface element
        shx,shy,shz = components of shear stress on surface element
        ke = flux of particle kinetic energy on surface element
        erot = flux of particle rotational energy on surface element
        evib = flux of particle vibrational energy on surface element
        etot = flux of particle total energy on surface element 

**Examples:**

::

   compute 1 surf all all n press eng
   compute mine surf sphere species press shx shy shz 

These commands will dump time averages for each species and each surface
element to a dump file every 1000 steps:

::

   compute 1 surf all species n press shx shy shz
   fix 1 ave/surf all 10 100 1000 c_1[*]
   dump 1 surf all 1000 tmp.surf id f_1[*] 

These commands will time-average the force on each surface element then
sum them across element to compute drag (fx) and lift (fy) on the body:

::

   compute 1 surf all all fx fy
   fix 1 ave/surf all 10 100 1000 c_1[*]
   compute 2 reduce sum f_1[1] f_1[2]
   stats 1000
   stats_style step cpu np c_2[1] c_2[2] 

**Description:**

Define a computation that calculates one or more values for each
explicit surface element in a surface element group, based on the
particles that collide with that element. The values are summed for each
group of species in the specified mixture. See the
:ref:`mixture<command-mixture>` command for how a set of species can be
partitioned into groups. Only surface elements in the surface group
specified by *group-ID* are included in the calculations. See the :ref:`group surf<command-group>` command for info on how surface elements can be
assigned to surface groups.

Explicit surface elements are triangles for 3d simulations and line
segments for 2d simulations. Unlike implicit surface elements, each
explicit triangle or line segment may span multiple grid cells. See the
:ref:`read_surf<command-read-surf>` command for details.

This command can only be used for simulations with explicit surface
elements. See the similar :ref:`compute isurf/grid<command-compute-isurf-grid>` command for use with simulations
with implicit surface elements.

Note that when a particle collides with a surface element, it can bounce
off (possibly as a different species), be captured by the surface
(vanish), or a 2nd particle can also be emitted. The formulas below
account for all the possible outcomes. For example, the kinetic energy
flux *ke* onto a suface element for a single collision includes a
positive contribution from the incoming particle and negative
contributions from 0, 1, or 2 outgoing particles. The exception is the
*n* and *nwt* values which simply tally counts of particles colliding
with the surface element.

If the surface element is transparent, the particle will pass through
the surface unaltered. The flux of particle count, mass, or energy to
the surface can still be tallied by this compute. See details on
transparent surface elements below.

Also note that all values for a collision are tallied based on the
species group of the incident particle. Quantities associated with
outgoing particles are part of the same tally, even if they are in
different species groups.

The results of this compute can be used by different commands in
different ways. The values for a single timestep can be output by the
:ref:`dump surf<command-dump>` command.

The values over many sampling timesteps can be averaged by the :ref:`fix ave/surf<command-fix-ave-surf>` command. It does its averaging as if the
particles striking the surface element at each sampling timestep were
combined together into one large set to compute the formulas below. The
answer is then divided by the number of sampling timesteps if it is not
otherwise normalized by the number of particles. Note that in general
this is a different normalization than taking the values produced by the
formulas below for a single timestep, summing them over the sampling
timesteps, and then dividing by the number of sampling steps. However
for the current values listed below, the two normalization methods are
the same.

.. note:: If particle weighting is enabled via the :ref:`global weight<command-global>` command, then all of the values below are scaled by the weight assigned to the grid cell in which the particle collision with the surface element occurs. The only exception is the the *n* value, which is NOT scaled by the weight; it is a simple count of particle collisions with the surface element.

--------------

The *n* value counts the number of particles in the group striking the
surface element.

The *nwt* value counts the number of particles in the group striking the
surface element and weights the count by the weight assigned to the grid
cell in which the particle collision with the surface element occurs.
The *nwt* quantity will only be different than *n* if particle weighting
is enabled via the :ref:`global weight<command-global>` command.

The *mflux* value calculates the mass flux imparted to the surface
element by particles in the group. This is computed as

::

   Mflux = Sum_i (mass_i) / (A * dt / fnum) 

where the sum is over all contributing particle masses, normalized by A
= the area of the surface element, dt = the timestep, and fnum = the
real/simulated particle ratio set by the :ref:`global fnum<command-global>`
command.

The *fx*, *fy*, *fz* values calculate the components of force extered on
the surface element by particles in the group, with respect to the x, y,
z coordinate axes. These are computed as

::

   p_delta = mass * (V_post - V_pre)
   Px = - Sum_i (p_delta_x) / (dt / fnum)
   Py = - Sum_i (p_delta_y) / (dt / fnum)
   Pz = - Sum_i (p_delta_z) / (dt / fnum) 

where p_delta is the change in momentum of a particle, whose velocity
changes from V_pre to V_post when colliding with the surface element.
The force exerted on the surface element is the sum over all
contributing p_delta, normalized by dt and fnum as defined before.

The *press* value calculates the pressure *P* exerted on the surface
element in the normal direction by particles in the group, such that
outward pressure is positive. This is computed as

::

   p_delta = mass * (V_post - V_pre)
   P = Sum_i (p_delta_i dot N) / (A * dt / fnum) 

where p_delta, V_pre, V_post, dt, fnum are defined as before. The
pressure exerted on the surface element is the sum over all contributing
p_delta dotted into the outward normal N of the surface element, also
normalized by A = the area of the surface element.

The *px*, *py*, *pz* values calculate the normal pressure Px, Py, Pz
extered on the surface element in the direction of its normal by
particles in the group, with respect to the x, y, z coordinate axes.
These are computed as

::

   p_delta = mass * (V_post - V_pre)
   p_delta_n = (p_delta dot N) N
   Px = - Sum_i (p_delta_n_x) / (A * dt / fnum)
   Py = - Sum_i (p_delta_n_y) / (A * dt / fnum)
   Pz = - Sum_i (p_delta_n_z) / (A * dt / fnum) 

where p_delta, V_pre, V_post, N, A, and dt are defined as before.
P_delta_n is the normal component of the change in momentum vector
p_delta of a particle. P_delta_n_x (and y,z) are its x, y, z components.

The *shx*, *shy*, *shz* values calculate the shear pressure Sx, Sy, Sz
extered on the surface element in the tangential direction to its normal
by particles in the group, with respect to the x, y, z coordinate axes.
These are computed as

::

   p_delta = mass * (V_post - V_pre)
   p_delta_t = p_delta - (p_delta dot N) N
   Sx = - Sum_i (p_delta_t_x) / (A * dt / fnum)
   Sy = - Sum_i (p_delta_t_y) / (A * dt / fnum)
   Sz = - Sum_i (p_delta_t_z) / (A * dt / fnum) 

where p_delta, V_pre, V_post, N, A, and dt are defined as before.
P_delta_t is the tangential component of the change in momentum vector
p_delta of a particle. P_delta_t_x (and y,z) are its x, y, z components.

The *ke* value calculates the kinetic energy flux *Eflux* imparted to
the surface element by particles in the group, such that energy lost by
a particle is a positive flux. This is computed as

::

   e_delta = 1/2 mass (V_post^2 - V_pre^2)
   Eflux = - Sum_i (e_delta) / (A * dt / fnum) 

where e_delta is the kinetic energy change in a particle, whose velocity
changes from V_pre to V_post when colliding with the surface element.
The energy flux imparted to the surface element is the sum over all
contributing e_delta, normalized by A = the area of the surface element
and dt = the timestep and fnum = the real/simulated particle ratio set
by the :ref:`global fnum<command-global>` command.

The *erot* value calculates the rotational energy flux *Eflux* imparted
to the surface element by particles in the group, such that energy lost
by a particle is a positive flux. This is computed as

::

   e_delta = Erot_post - Erot_pre
   Eflux = - Sum_i (e_delta) / (A * dt / fnum) 

where e_delta is the rotational energy change in a particle, whose
internal rotational energy changes from Erot_pre to Erot_post when
colliding with the surface element. The flux equation is the same as for
the *ke* value.

The *evib* value calculates the vibrational energy flux *Eflux* imparted
to the surface element by particles in the group, such that energy lost
by a particle is a positive flux. This is computed as

::

   e_delta = Evib_post - Evib_pre
   Eflux = - Sum_i (e_delta) / (A * dt / fnum) 

where e_delta is the vibrational energy change in a particle, whose
internal vibrational energy changes from Evib_pre to Evib_post when
colliding with the surface element. The flux equation is the same as for
the *ke* value.

The *etot* value calculates the total energy flux imparted to the
surface element by particles in the group, such that energy lost by a
particle is a positive flux. This is simply the sum of kinetic,
rotational, and vibrational energies. Thus the total energy flux is the
sum of what is computed by the *ke*, *erot*, and *evib* values.

--------------

**Transparent surface elements:**

This compute will tally information on particles that pass through
transparent surface elements. The :ref:`Section 6.15<howto-transparent-surface>` doc page provides an overview of
transparent surfaces and how to create them.

The *n* and *nwt* value are calculated the same for transparent
surfaces. I.e. they are the count and weighted count of particles
passing through the surface.

The *mflux*, *ke*, *erot*. *evib*, and *etot* values are fluxes. For
transparent surfaces, they are calculated for the incident particle as
if they had struck the surface. The outgoing particle is ignored. This
means the tally quantity is the flux of particles onto the outward face
of the surface. No tallying is done for particles hitting the inward
face of the surface. See :ref:`Section 6.15<howto-transparent-surface>`
for how to do tallying in both directions.

All the other values are calculated as described above. This means they
will be zero, since the incident particle and outgoing particle have the
same mass and velocity.

--------------

**Output info:**

This compute calculates a per-surf array, with the number of columns
equal to the number of values times the number of groups. The ordering
of columns is first by values, then by groups. I.e. if the *n* and *u*
values were specified as keywords, then the first two columns would be
*n* and *u* for the first group, the 3rd and 4th columns would be *n*
and *u* for the second group, etc.

Surface elements not in the specified *group-ID* will output zeroes for
all their values.

The array can be accessed by any command that uses per-surf values from
a compute as input. See :ref:`Section 6.4<howto-output>` for
an overview of SPARTA output options.

The per-surf array values will be in the :ref:`units<command-units>`
appropriate to the individual values as described above. *N* is
unitless. *Press*, *px*, *py*, *pz*, *shx*, *shy*, *shz* are in in
pressure units. *Ke*, *erot*, *evib*, and *etot* are in energy/area-time
units for 3d simulations and energy/length-time units for 2d
simulations.

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

:ref:`command-fix-ave-surf`,
:ref:`dump surf<command-dump>`,
:ref:`command-compute-isurf-grid`

**Default:** none
