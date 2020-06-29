:orphan:

.. index:: compute



.. _command-compute:

###############
compute command
###############


*******
Syntax:
*******

::

   compute ID style args 

-  ID = user-assigned name for the computation
-  style = one of a list of possible style names (see below)
-  args = arguments used by a particular style

*********
Examples:
*********

::

   compute 1 ke/particle 
   compute myGrid all n mass u usq temp 

************
Description:
************

Define a computation that will be performed on a collection of particles
or grid cells or surface elements. Quantities calculated by a compute
are instantaneous values, meaning they are calculated from information
about the current timestep. Examples include calculation of the system
temperature or counting collisions of particles with surface elements.
Code for new computes can be added to SPARTA; see :ref:`Section 10<modify>` of the manual for details.

Note that defining a compute does not perform a computation. Instead
computes are invoked by other SPARTA commands as needed, e.g. to
generate statistics or dump file output. See :ref:`Section 4.4<howto-output>` for a summary of various SPARTA
output options, many of which involve computes.

The ID for a compute is used to identify the compute in other commands.
Each compute ID must be unique. The ID can only contain alphanumeric
characters and underscores. You can specify multiple computees of the
same style so long as they have different IDs. A compute can be deleted
with the :ref:`uncompute<command-uncompute>` command, after which its ID can
be re-used.

--------------

Each compute style has its own doc page which describes its arguments
and what it does. Here is an alphabetic list of compute styles available
in SPARTA:

-  :ref:`boundary<command-compute-boundary>` - various quantities on each
   global boundary
-  :ref:`count<command-compute-count>` - particle counts for species and
   mixtures and mixture groups
-  :ref:`distsurf/grid<command-compute-distsurf-grid>` - distance from grid
   cells to surface
-  :ref:`eflux/grid<command-compute-eflux-grid>` - energy flux density per
   grid cell
-  :ref:`fft/grid<command-compute-fft-grid>` - FFTs across grid cells
-  :ref:`grid<command-compute-grid>` - various per grid cell quantities
-  :ref:`isurf/grid<command-compute-isurf-grid>` - various implicit surface
   element quantities
-  :ref:`ke/particle<command-compute-ke-particle>` - temperature per particle
-  :ref:`lambda/grid<command-compute-lambda-grid>` - mean-free path per grid
   cell
-  :ref:`pflux/grid<command-compute-pflux-grid>` - momentum flux density per
   grid cell
-  :ref:`property/grid<command-compute-property-grid>` - per grid cell
   properties
-  :ref:`react/boundary<command-compute-react-boundary>` - reaction stats on
   global boundary
-  :ref:`react/surf<command-compute-react-surf>` = reaction stats for
   explicit surfs
-  :ref:`react/isurf/grid<command-compute-react-isurf-grid>` - reactions
   stats for implicit surfs
-  :ref:`reduce<command-compute-reduce>` - reduce vectors to scalars
-  :ref:`sonine/grid<command-compute-sonine-grid>` - Sonine moments per grid
   cell
-  :ref:`surf<command-compute-surf>` - various explicit surface element
   quantities
-  :ref:`thermal/grid<command-compute-thermal-grid>` - thermal temperature
   per grid cell
-  :ref:`temp<command-compute-temp>` - temperature of particles
-  :ref:`tvib/grid<command-compute-tvib-grid>` - vibrational temperature per
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

Note that commands and :ref:`variables<command-variable>` which use compute
quantities typically do not allow for all kinds, e.g. a command may
require a vector of values, not a scalar. This means there is no
ambiguity about referring to a compute quantity as f_ID even if it
produces, for example, both a scalar and vector. The doc pages for
various commands explain the details.

--------------

The values generated by a compute can be used in several ways:

-  Global values can be output via the
   :ref:`stats_style<command-stats-style>` command. Or the values can be
   referenced in a :ref:`variable equal<command-variable>` or :ref:`variable    atom<command-variable>` command.
-  Per-particle values can be output via the :ref:`dump    particle<command-dump>` command. Or the values can be referenced in a
   :ref:`particle-style variable<command-variable>`.
-  Per-grid values can be output via the :ref:`dump grid<command-dump>`
   command. They can be time-averaged via the :ref:`fix    ave/grid<command-fix-ave-grid>` command.
-  Per-surf values can be output via the :ref:`dump surf<command-dump>`
   command. They can be time-averaged via the :ref:`fix    ave/surf<command-fix-ave-surf>` command.

--------------

*************
Restrictions:
*************
 none

*****************
Related commands:
*****************

:ref:`command-uncompute`

********
Default:
********
 none
