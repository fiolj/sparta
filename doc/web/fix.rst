:orphan:

.. index:: fix



.. _command-fix:

###########
fix command
###########


*******
Syntax:
*******

::

   fix ID style args 

-  ID = user-assigned name for the fix
-  style = one of a long list of possible style names (see below)
-  args = arguments used by a particular style

*********
Examples:
*********

::

   fix 1 grid/check 100 warn
   fix 1 ave/time all 100 5 1000 c_myTemp c_thermo_temp file temp.profile 

************
Description:
************

Set a fix that will be applied to the system. In SPARTA, a "fix" is an
operation that is applied to the system during timestepping. Examples
include adding particles via inlet boundary conditions or computing
diagnostics. Code for new fixes can be added to SPARTA; see :ref:`Section 10<modify>` of the manual for details.

Fixes perform their operations at different stages of the timestep. If 2
or more fixes operate at the same stage of the timestep, they are
invoked in the order they were specified in the input script.

The ID for a fix is used to identify the fix in other commands. Each fix
ID must be unique; see an exception below. The ID can only contain
alphanumeric characters and underscores. You can specify multiple fixes
of the same style so long as they have different IDs. A fix can be
deleted with the :ref:`unfix<command-unfix>` command, after which its ID can
be re-used.

.. important:: The :ref:`unfix<command-unfix>` command is the only way to turn off a fix; simply specifying a new fix with the same style and a different ID will not turn off the first one.

	       If you specify a new fix with the same ID and style as an existing fix, the old fix is deleted and the new one is created (presumably with new settings). This is the same as if an "unfix" command were first performed on the old fix, except that the new fix is kept in the same order relative to the existing fixes as the old one originally was.

Some fixes store an internal "state" which is written to binary restart
files via the :ref:`restart<command-restart>` or
:ref:`write_restart<command-write-restart>` commands. This allows the fix to
continue on with its calculations in a restarted simulation. See the
:ref:`read_restart<command-read-restart>` command for info on how to
re-specify a fix in an input script that reads a restart file. See the
doc pages for individual fixes for info on which ones can be restarted.

--------------

Each fix style has its own doc page which describes its arguments and
what it does, as listed below. Here is an alphabetic list of fix styles
available in SPARTA:

-  :ref:`adapt<command-fix-adapt>` - on-the-fly grid adaptation
-  :ref:`adapt/kk<command-fix-adapt>` - Kokkos version of fix adapt
-  :ref:`ambipolar<command-fix-ambipolar>` - ambipolar approximation for
   ionized plasmas
-  :ref:`ave/grid<command-fix-ave-grid>` - compute per grid cell
   time-averaged quantities
-  :ref:`ave/grid/kk<command-fix-ave-grid>` - Kokkos version of fix ave/grid
-  :ref:`ave/histo<command-fix-ave-histo>` - compute/output time averaged
   histograms
-  :ref:`ave/histo/weight<command-fix-ave-histo>` - compute/output weighted
   histograms
-  :ref:`ave/surf<command-fix-ave-surf>` - compute per surface element
   time-averaged quantities
-  :ref:`ave/time<command-fix-ave-time>` - compute/output global
   time-averaged quantities
-  :ref:`balance<command-fix-balance>` - perform dynamic load-balancing
-  :ref:`balance/kk<command-fix-balance>` - Kokkos version of fix balance
-  :ref:`emit/face<command-fix-emit-face>` - emit particles at global
   boundaries
-  :ref:`emit/face/kk<command-fix-emit-face>` - Kokkos version of fix
   emit/face
-  :ref:`emit/face/file<command-fix-emit-face-file>` - emit particles at
   global boundaries using a distribution defined in a file
-  :ref:`emit/surf<command-fix-emit-surf>` - emit particles at surfaces
-  :ref:`grid/check<command-fix-grid-check>` - check if particles are in the
   correct grid cell
-  :ref:`grid/check/kk<command-fix-grid-check>` - Kokkos version of fix
   grid/check
-  :ref:`move/surf<command-fix-move-surf>` - move surfaces dynamically during
   a simulation
-  :ref:`move/surf/kk<command-fix-move-surf>` - Kokkos version of fix
   move/surf
-  :ref:`print<command-fix-print>` - print text and variables during a
   simulation
-  :ref:`vibmode<command-fix-vibmode>` - discrete vibrational energy modes

There are also additional accelerated compute styles included in the
SPARTA distribution for faster performance on specific hardware. The
list of these with links to the individual styles are given in the pair
section of `this page <Section_commands.html#cmd_5>`__.

--------------

In addition to the operation they perform, some fixes also produce one
of four styles of quantities: global, per-particle, per-grid, or
per-surf. These can be used by other commands or output as described
below. A global quantity is one or more system-wide values, e.g. the
temperature of the system. A per-particle quantity is one or more values
per particle, e.g. the kinetic energy of each particle. A per-grid
quantity is one or more values per grid cell. A per-surf quantity is one
or more values per surface element.

Global, per-particle, per-grid, and per-surf quantities each come in two
forms: a single scalar value or a vector of values. Additionaly, global
quantities can also be a 2d array of values. The doc page for each fix
describes the style and kind of values it produces, e.g. a per-particle
vector. Some fixes can produce more than one form of a single style,
e.g. a global scalar and a global vector.

When a fix quantity is accessed, as in many of the output commands
discussed below, it can be referenced via the following bracket
notation, where ID is the ID of the fix:

.. container::

   ========== ==========================================
   f_ID       entire scalar, vector, or array
   f_ID[I]    one element of vector, one column of array
   f_ID[I][J] one element of array
   ========== ==========================================

In other words, using one bracket reduces the dimension of the quantity
once (vector -> scalar, array -> vector). Using two brackets reduces the
dimension twice (array -> scalar). Thus a command that uses scalar fix
values as input can also process elements of a vector or array.

Note that commands and :ref:`variables<command-variable>` which use fix
quantities typically do not allow for all kinds, e.g. a command may
require a vector of values, not a scalar. This means there is no
ambiguity about referring to a fix quantity as f_ID even if it produces,
for example, both a scalar and vector. The doc pages for various
commands explain the details.

--------------

Any values generated by a fix can be used in several ways:

-  Global values can be output via the
   :ref:`stats_style<command-stats-style>` command. Or the values can be
   referenced in a :ref:`variable equal<command-variable>` or :ref:`variable    atom<command-variable>` command.
-  Per-particle values can be output via the :ref:`dump    particle<command-dump>` command. Or the per-particle values can be
   referenced in an :ref:`particle-style variable<command-variable>`.
-  Per-grid values can be output via the :ref:`dump grid<command-dump>`
   command. Or the per-grid values can be referenced in a :ref:`grid-style    variable<command-variable>`.

--------------

*************
Restrictions:
*************
 none

*****************
Related commands:
*****************

:ref:`command-unfix`

********
Default:
********
 none
