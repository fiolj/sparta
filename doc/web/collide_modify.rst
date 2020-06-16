:orphan:

.. index:: collide_modify

.. _command-collide-modify:

######################
collide_modify command
######################

**Syntax:**

::

   collide_modify keyword values ...  

-  one or more keyword/value pairs may be listed
-  keywords = *vremax* or *remain* or *ambipolar* or *nearcp* or
   *rotate* or *vibrate*

   ::

        vremax values = Nevery startflag
          Nevery = zero vremax every this many timesteps
          startflag = yes or no = zero vremax at start of every run
        remain value = yes or no = hold remaining fraction of collisions over to next timestep
        nearcp values = choice Nlimit
          choice = yes or no to turn on/off near collision partners
          Nlimit = max # of attempts made to find a collision partner
        ambipolar value = no or yes
        rotate value = no or smooth
        vibrate value = no or smooth or discrete 

**Examples:**

::

   collide_modify vremax 1000 yes
   collide_modify vremax 0 no remain no
   collide_modify ambipolar yes 

**Description:**

Set parameters that affect how collisions are performed.

The *vremax* keyword affects how often the Vremax parameter, for
collision frequency is re-zeroed during the simulation. This parameter
is stored for each grid cell and each pair of collision groups (groups
are described by the `collide <collide.html>`__ command).

The value of Vremax affects how many events are attempted in each grid
cell for a pair of groups, and thus the overall time spent performing
collisions. Vremax is continuously set to the largest difference in
velocity between a pair of colliding particles. The larger Vremax grows,
the more collisions are attempted for the grid cell on each timestep,
though this does not affect the number of collisions actually performed.
Thus if Vremax grows large, collisions become less efficient, though
still accurate.

For non-equilibrium flows, it is typically desirable to reset Vremax to
zero fairly frequently (e.g. every 1000 steps) so that it does not
become large, due to anomolously fast moving particles. In contrast,
when a system is at equilibrium, it is typically desirable to not reset
Vremax to zero since it will also stay roughly constant.

If *Nevery* is specified as 0, Vremax is not zeroed during a run.
Otherwise Vremax is zeroed on timesteps that are a multiple of *Nevery*.
Additionally, if *startflag* is set to *yes*, Vremax is zeroed at the
start of every run. If it is set to *no*, it is not.

The *remain* keyword affects how the number of attempted collisions for
each grid cell is calculated each timestep. If the value is set to
*yes*, then any fractional collision count (for each grid cell and pair
of grgroups) is carried over to the next timestep. E.g. if the computed
collision count is 7.3, then 7 attempts are made on this timestep, and
0.3 are carried over to the next timestep, to be added to the computed
collision count for that step. If the value is set to *no*, then no
carry-over is made. Instead, in this example, 7 attempts are made and an
8th attempt is made conditionally with a probability of 0.3, using a
random number.

The *nearcp* keyword stands for "near collision partner" and affects how
collision partners are selected. If *no* is specified, which is the
default, then collision partner pairs are selected randomly from all
particles in the grid cell. In this case the *Nlimit* parameter is
ignored, though it must still be specfied.

If *yes* is specified, then up to *Nlimit* collision partners are
considered for each collision. The first partner I is chosen randomly
from all particles in the grid cell. A distance R that particle I moves
in that timestep is calculated, based on its velocity. *Nlimit* possible
collision partners J are examined, starting at a random J. If one of
them is within a distance R of particle I, it is immediately selected as
the collision partner. If none of the *Nlimit* particles are within a
distance R, the closest J particle to I is selected. An exception to
these rules is that a particle J is not considered for a collision if
the I,J pair were the most recent collision partners (in the current
timestep) for each other. The convergence properties of this
near-neighbor algorithm are described in [Gallis11]_.
Note that choosing *Nlimit* judiciously will avoid costly searches when
there are large numbers of particles in some or all grid cells.

If the *ambipolar* keyword is set to *yes*, then collisions within a
grid cell with use the ambipolar approximation. This requires use of the
`fix ambipolar <fix_ambipolar.html>`__ command to define which species
is an electron and which species are ions. There can be many of the
latter. When collisions within a single grid cell are performed, each
ambipolar ion is split into two particles, the ion and an associated
electron. Collisions between the augmented set of particles are
calculated. Ion/electron chemistry can also occur if the
`react <react.html>`__ command has been used to read a file of reactions
that include such reactions. See the `react <react.html>`__ command doc
page. After all collisions in the grid cell have been computed, there is
still a one-to-one correspondence between ambipolar ions and electron,
and each pair is recombined into a single ambipolar particle.

The *rotate* keyword determines how rotational energy is treated in
particle collisions and stored by particles. If the value is set to
*no*, then rotational energy is not tracked; every particle's rotational
energy is 0.0. If the value is set to *smooth*, a particle's rotational
energy is a single continuous value.

The *vibrate* keyword determines how vibrational energy is treated in
particle collisions and stored by particles. If the value is set to
*no*, then vibrational energy is not tracked; every particle's
vibrational energy is 0.0. If the value is set to *smooth*, a particle's
vibrational energy is a single continuous value. If the value is set to
*discrete*, each particle's vibrational energy is set to discrete
values, namely multiples of kT where k = the Boltzmann constant and T is
one or more characteristic vibrational temperatures set for the particle
species.

Note that in the *discrete* case, if any species are defined that have
4,6,8 vibrational degrees of freedom, which correspond to 2,3,4
vibrational modes, then the `species <species.html>`__ command must be
used with its optional *vibfile* keyword to set the vibrational info
(temperature, relaxation number, degeneracy) for those species.

Also note that if any such species are defined (with more than one
vibrational mode, then use of the *discrete* option also requires the
`fix vibmode <fix_vibmode.html>`__ command be used to allocate storage
for the per-particle mode values.

--------------

**Restrictions:** none

**Related commands:**

:ref:`command-collide`

**Default:**

The option defaults are vremax = (0,yes), remain = yes, ambipolar no,
nearcp no, rotate smooth, and vibrate = no.

--------------

.. [Gallis11] M. A. Gallis, J. R. Torczynski, "Effect of Collision-Partner Selection Schemes on the Accuracy and Efficiency of the Direct Simulation Monte Carlo Method," International Journal for Numerical Methods in Fluids, 67(8):1057-1072. DOI:10.1002/fld.2409 (2011).
