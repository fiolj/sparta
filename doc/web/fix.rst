:orphan:

.. index:: fix

.. _command-fix:

###########
fix command
###########

**Syntax:**

::

   fix ID style args 

-  ID = user-assigned name for the fix
-  style = one of a long list of possible style names (see below)
-  args = arguments used by a particular style

**Examples:**

::

   fix 1 grid/check 100 warn
   fix 1 ave/time all 100 5 1000 c_myTemp c_thermo_temp file temp.profile 

**Description:**

Set a fix that will be applied to the system. In SPARTA, a "fix" is an
operation that is applied to the system during timestepping. Examples
include adding particles via inlet boundary conditions or computing
diagnostics. Code for new fixes can be added to SPARTA; see `Section
10 <Section_modify.html>`__ of the manual for details.

Fixes perform their operations at different stages of the timestep. If 2
or more fixes operate at the same stage of the timestep, they are
invoked in the order they were specified in the input script.

The ID for a fix is used to identify the fix in other commands. Each fix
ID must be unique; see an exception below. The ID can only contain
alphanumeric characters and underscores. You can specify multiple fixes
of the same style so long as they have different IDs. A fix can be
deleted with the `unfix <unfix.html>`__ command, after which its ID can
be re-used.

IMPORTANT NOTE: The `unfix <unfix.html>`__ command is the only way to
turn off a fix; simply specifying a new fix with the same style and a
different ID will not turn off the first one.

If you specify a new fix with the same ID and style as an existing fix,
the old fix is deleted and the new one is created (presumably with new
settings). This is the same as if an "unfix" command were first
performed on the old fix, except that the new fix is kept in the same
order relative to the existing fixes as the old one originally was.

Some fixes store an internal "state" which is written to binary restart
files via the `restart <restart.html>`__ or
`write_restart <write_restart.html>`__ commands. This allows the fix to
continue on with its calculations in a restarted simulation. See the
`read_restart <read_restart.html>`__ command for info on how to
re-specify a fix in an input script that reads a restart file. See the
doc pages for individual fixes for info on which ones can be restarted.

--------------

Each fix style has its own doc page which describes its arguments and
what it does, as listed below. Here is an alphabetic list of fix styles
available in SPARTA:

-  `adapt <fix_adapt.html>`__ - on-the-fly grid adaptation
-  `adapt/kk <fix_adapt.html>`__ - Kokkos version of fix adapt
-  `ambipolar <fix_ambipolar.html>`__ - ambipolar approximation for
   ionized plasmas
-  `ave/grid <fix_ave_grid.html>`__ - compute per grid cell
   time-averaged quantities
-  `ave/grid/kk <fix_ave_grid.html>`__ - Kokkos version of fix ave/grid
-  `ave/histo <fix_ave_histo.html>`__ - compute/output time averaged
   histograms
-  `ave/histo/weight <fix_ave_histo.html>`__ - compute/output weighted
   histograms
-  `ave/surf <fix_ave_surf.html>`__ - compute per surface element
   time-averaged quantities
-  `ave/time <fix_ave_time.html>`__ - compute/output global
   time-averaged quantities
-  `balance <fix_balance.html>`__ - perform dynamic load-balancing
-  `balance/kk <fix_balance.html>`__ - Kokkos version of fix balance
-  `emit/face <fix_emit_face.html>`__ - emit particles at global
   boundaries
-  `emit/face/kk <fix_emit_face.html>`__ - Kokkos version of fix
   emit/face
-  `emit/face/file <fix_emit_face_file.html>`__ - emit particles at
   global boundaries using a distribution defined in a file
-  `emit/surf <fix_emit_surf.html>`__ - emit particles at surfaces
-  `grid/check <fix_grid_check.html>`__ - check if particles are in the
   correct grid cell
-  `grid/check/kk <fix_grid_check.html>`__ - Kokkos version of fix
   grid/check
-  `move/surf <fix_move_surf.html>`__ - move surfaces dynamically during
   a simulation
-  `move/surf/kk <fix_move_surf.html>`__ - Kokkos version of fix
   move/surf
-  `print <fix_print.html>`__ - print text and variables during a
   simulation
-  `vibmode <fix_vibmode.html>`__ - discrete vibrational energy modes

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

Note that commands and `variables <variable.html>`__ which use fix
quantities typically do not allow for all kinds, e.g. a command may
require a vector of values, not a scalar. This means there is no
ambiguity about referring to a fix quantity as f_ID even if it produces,
for example, both a scalar and vector. The doc pages for various
commands explain the details.

--------------

Any values generated by a fix can be used in several ways:

-  Global values can be output via the
   `stats_style <stats_style.html>`__ command. Or the values can be
   referenced in a `variable equal <variable.html>`__ or `variable
   atom <variable.html>`__ command.
-  Per-particle values can be output via the `dump
   particle <dump.html>`__ command. Or the per-particle values can be
   referenced in an `particle-style variable <variable.html>`__.
-  Per-grid values can be output via the `dump grid <dump.html>`__
   command. Or the per-grid values can be referenced in a `grid-style
   variable <variable.html>`__.

--------------

**Restrictions:** none

**Related commands:**

:ref:`command-unfix`

**Default:** none
