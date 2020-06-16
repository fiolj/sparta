:orphan:

.. index:: compute

.. _command-compute:

###############
compute command
###############

**Syntax:**

::

   compute ID style args 

-  ID = user-assigned name for the computation
-  style = one of a list of possible style names (see below)
-  args = arguments used by a particular style

**Examples:**

::

   compute 1 ke/particle 
   compute myGrid all n mass u usq temp 

**Description:**

Define a computation that will be performed on a collection of particles
or grid cells or surface elements. Quantities calculated by a compute
are instantaneous values, meaning they are calculated from information
about the current timestep. Examples include calculation of the system
temperature or counting collisions of particles with surface elements.
Code for new computes can be added to SPARTA; see `Section
10 <Section_modify.html>`__ of the manual for details.

Note that defining a compute does not perform a computation. Instead
computes are invoked by other SPARTA commands as needed, e.g. to
generate statistics or dump file output. See `Section
4.4 <Section_howto.html#howto_4>`__ for a summary of various SPARTA
output options, many of which involve computes.

The ID for a compute is used to identify the compute in other commands.
Each compute ID must be unique. The ID can only contain alphanumeric
characters and underscores. You can specify multiple computees of the
same style so long as they have different IDs. A compute can be deleted
with the `uncompute <uncompute.html>`__ command, after which its ID can
be re-used.

--------------

Each compute style has its own doc page which describes its arguments
and what it does. Here is an alphabetic list of compute styles available
in SPARTA:

-  `boundary <compute_boundary.html>`__ - various quantities on each
   global boundary
-  `count <compute_count.html>`__ - particle counts for species and
   mixtures and mixture groups
-  `distsurf/grid <compute_distsurf_grid.html>`__ - distance from grid
   cells to surface
-  `eflux/grid <compute_eflux_grid.html>`__ - energy flux density per
   grid cell
-  `fft/grid <compute_fft_grid.html>`__ - FFTs across grid cells
-  `grid <compute_grid.html>`__ - various per grid cell quantities
-  `isurf/grid <compute_isurf_grid.html>`__ - various implicit surface
   element quantities
-  `ke/particle <compute_ke_particle.html>`__ - temperature per particle
-  `lambda/grid <compute_lambda_grid.html>`__ - mean-free path per grid
   cell
-  `pflux/grid <compute_pflux_grid.html>`__ - momentum flux density per
   grid cell
-  `property/grid <compute_property_grid.html>`__ - per grid cell
   properties
-  `react/boundary <compute_react_boundary.html>`__ - reaction stats on
   global boundary
-  `react/surf <compute_react_surf.html>`__ = reaction stats for
   explicit surfs
-  `react/isurf/grid <compute_react_isurf_grid.html>`__ - reactions
   stats for implicit surfs
-  `reduce <compute_reduce.html>`__ - reduce vectors to scalars
-  `sonine/grid <compute_sonine_grid.html>`__ - Sonine moments per grid
   cell
-  `surf <compute_surf.html>`__ - various explicit surface element
   quantities
-  `thermal/grid <compute_thermal_grid.html>`__ - thermal temperature
   per grid cell
-  `temp <compute_temp.html>`__ - temperature of particles
-  `tvib/grid <compute_tvib_grid.html>`__ - vibrational temperature per
   grid cell

There are also additional accelerated compute styles included in the
SPARTA distribution for faster performance on specific hardware. The
list of these with links to the individual styles are given in the pair
section of `this page <Section_commands.html#cmd_5>`__.

--------------

Computes calculate one of four styles of quantities: global,
per-particle, per-grid, or per-surf. A global quantity is one or more
system-wide values, e.g. the temperature of the system. A per-particle
quantity is one or more values per particle, e.g. the kinetic energy of
each particle. A per-grid quantity is one or more values per grid cell.
A per-surf quantity is one or more values per surface element.

Global, per-particle, per-grid, and per-surf quantities each come in two
forms: a single scalar value or a vector of values. Additionaly, global
quantities can also be a 2d array of values. The doc page for each
compute describes the style and kind of values it produces, e.g. a
per-particle vector. Some computes can produce more than one form of a
single style, e.g. a global scalar and a global vector.

When a compute quantity is accessed, as in many of the output commands
discussed below, it can be referenced via the following bracket
notation, where ID is the ID of the compute:

.. container::

   ========== ==========================================
   c_ID       entire scalar, vector, or array
   c_ID[I]    one element of vector, one column of array
   c_ID[I][J] one element of array
   ========== ==========================================

In other words, using one bracket reduces the dimension of the quantity
once (vector -> scalar, array -> vector). Using two brackets reduces the
dimension twice (array -> scalar). Thus a command that uses scalar
compute values as input can also process elements of a vector or array.

Note that commands and `variables <variable.html>`__ which use compute
quantities typically do not allow for all kinds, e.g. a command may
require a vector of values, not a scalar. This means there is no
ambiguity about referring to a compute quantity as f_ID even if it
produces, for example, both a scalar and vector. The doc pages for
various commands explain the details.

--------------

The values generated by a compute can be used in several ways:

-  Global values can be output via the
   `stats_style <stats_style.html>`__ command. Or the values can be
   referenced in a `variable equal <variable.html>`__ or `variable
   atom <variable.html>`__ command.
-  Per-particle values can be output via the `dump
   particle <dump.html>`__ command. Or the values can be referenced in a
   `particle-style variable <variable.html>`__.
-  Per-grid values can be output via the `dump grid <dump.html>`__
   command. They can be time-averaged via the `fix
   ave/grid <fix_ave_grid.html>`__ command.
-  Per-surf values can be output via the `dump surf <dump.html>`__
   command. They can be time-averaged via the `fix
   ave/surf <fix_ave_surf.html>`__ command.

--------------

**Restrictions:** none

**Related commands:**

:ref:`command-uncompute`

**Default:** none
