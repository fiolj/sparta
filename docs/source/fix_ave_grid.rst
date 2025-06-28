
:orphan:

.. index:: fix_ave_grid

.. _fix-ave-grid:

.. _fix-ave-grid-command:

####################
fix ave/grid command
####################

.. _fix-ave-grid-kk-command:

#######################
fix ave/grid/kk command
#######################

.. _fix-ave-grid-syntax:

*******
Syntax:
*******

::

   fix ID ave/grid group-ID Nevery Nrepeat Nfreq value1 value2 ... keyword args ...

- ID is documented in :ref:`fix<fix>` command 

- ave/grid = style name of this fix command

- group-ID = group ID for which grid cells to perform calculation on

- Nevery = use input values every this many timesteps

- Nrepeat = # of times to use input values for calculating averages

- Nfreq = calculate averages every this many timesteps zero or more input values can be listed

- value = c_ID, c_ID\[N\], f_ID, f_ID\[N\], v_name, g_name, g_name\[N\]

::

     c_ID = per-grid vector calculated by a compute with ID
     c_ID\[N\] = Nth column of per-grid array calculated by a compute with ID, N can include wildcard (see below)
     f_ID = per-grid vector calculated by a fix with ID
     f_ID\[N\] = Nth column of per-grid array calculated by a fix with ID, N can include wildcard (see below)
     v_name = per-grid vector calculated by a grid-style variable with name
     g_name = custom per-grid vector with name
     g_name\[N\] = Nth column of per-grid custom array with name, N can include wildcard (see below)

- zero or more keyword/arg pairs may be appended

::

   keyword = *ave*
     *ave* args = one or running
       one = output a new average value every Nfreq steps
       running = accumulate average continuously

.. _fix-ave-grid-examples:

*********
Examples:
*********

::

   fix 1 ave/grid all 10 20 1000 c_mine
   fix 1 ave/grid all 1 100 100 c_2\[1\] ave running
   fix 1 ave/grid all 1 100 100 c_2\[\*\] ave running
   fix 1 ave/grid section1 5 20 100 v_myEng

These commands will dump averages for each species and each grid cell
to a file every 1000 steps:

::

   compute 1 grid species n u v w usq vsq wsq
   fix 1 ave/grid 10 100 1000 c_1\[\*\]
   dump 1 grid all 1000 tmp.grid id f_1\[\*\]

.. _fix-ave-grid-descriptio:

************
Description:
************

Use one or more per-grid vectors as inputs every few timesteps, and
average by grid cell over longer timescales, applying appropriate
normalization factors.  The resulting per grid cell averages can be
used by other output commands such as the :ref:`dump grid<dump>`
command.  Only grid cells in the grid group specified by *group-ID*
are included in the averaging.  See the :ref:`group grid<group>`
command for info on how grid cells can be assigned to grid
groups.

Each input value can be the result of a :ref:`compute<compute>` or
:ref:`fix<fix>` or :ref:`grid-style variable<variable>`.  The compute or
fix must produce a per-grid vector or array, not a global or
per-particle or per-surf quantity.  If you wish to time-average global
quantities from a compute, fix, or variable, then see the :ref:`fix ave/time<fix-ave-time>` command.  To time-average per-surf
quantities, see the :ref:`fix ave/surf<fix-ave-surf>` command.

Each per-grid value of each input vector is averaged independently.

:ref:`Computes<compute>` that produce per-grid vectors or arrays are
those which have the word *grid* in their style name.  See the doc
pages for individual :ref:`fixes<fix>` to determine which ones produce
per-grid vectors or arrays.

.. note::

  that for values from a compute or fix or custom attribute, the
  bracketed index can be specified using a wildcard asterisk with the
  index to effectively specify multiple values.  This takes the form "\*"
  or "\*n" or "n\*" or "m\*n".  If N = the size of the vector (for *mode* =
  scalar) or the number of columns in the array (for *mode* = vector),
  then an asterisk with no numeric values means all indices from 1 to N.
  A leading asterisk means all indices from 1 to n (inclusive).  A
  trailing asterisk means all indices from n to N (inclusive).  A middle
  asterisk means all indices from m to n (inclusive).

Using a wildcard is the same as if the individual columns of the array
had been listed one by one.  E.g. these 2 fix ave/grid commands are
equivalent, since the :ref:`compute grid<compute-grid>` command creates
a per-grid array with 3 columns:

::

   compute myGrid all all u v w
   fix 1 ave/grid all 10 20 1000 c_myGrid\[\*\]
   fix 1 ave/grid all 10 20 1000 c_myGrid\[1\] c_myGrid\[2\] c_myGrid\[3\]

The *Nevery*, *Nrepeat*, and *Nfreq* arguments specify on what
timesteps the input values will be used in order to contribute to the
average.  The final averaged quantities are generated on timesteps
that are a multiple of *Nfreq*.  The average is over *Nrepeat*
quantities, computed in the preceding portion of the simulation every
*Nevery* timesteps.  *Nfreq* must be a multiple of *Nevery* and
*Nevery* must be non-zero even if *Nrepeat* is 1.  Also, the timesteps
contributing to the average value cannot overlap, i.e. Nfreq >
(Nrepeat-1)\*Nevery is required.

For example, if Nevery=2, Nrepeat=6, and Nfreq=100, then values on
timesteps 90,92,94,96,98,100 will be used to compute the final average
on timestep 100.  Similarly for timesteps 190,192,194,196,198,200 on
timestep 200, etc.

If a value begins with "c\_", a compute ID must follow which has been
previously defined in the input script.  If no bracketed term is
appended, the compute must calculate a per-grid vector.  If
*c_ID\[N\]* is used, the compute must calculate a per-grud array with
M columns and N must be in the range from 1-M, which will use the Nth
column of the M-column per-grid array.  See the discussion above for
how N can be specified with a wildcard asterisk to effectively specify
multiple values.

Users can also write code for their own compute styles and :ref:`add them to SPARTA<modify>`.

If a value begins with "f\_", a fix ID must follow which has been
previously defined in the input script.  If no bracketed term is
appended, the fix must calculates a per-grid vector.  If *f_ID\[N\]*
is used, the fix must calculate a per-grid array with M columns and N
must be in the range from 1-M, which will use the Nth column of the
M-column per-grid array.  See the discussion above for how N can be
specified with a wildcard asterisk to effectively specify multiple
values.

.. note::

  that some fixes only produce their values on certain timesteps,
  which must be compatible with *Nevery*, else an error will result.
  Users can also write code for their own fix styles and :ref:`add them to   SPARTA<modify>`.

.. note::

  that grid-style variables define a formula which
  can reference :ref:`stats_style<stats-style>` keywords, or they can
  invoke other computes, fixes, or variables when they are evaluated, so
  this is a very general means of specifying quantities to time average.

If a value begins with "g\_", the name of a custom per-grid vector or
array must follow.  Custom attributes can store either a single or
multiple values per grid cell.  See :ref:`Section 6.17<howto-617-custom-perparticl-pergrid,>` for more discussion of custom
attributes and command that define them.  For example, the
:ref:`read_grid<read-grid>` and :ref:`surf_react implicit<surf-react-implicit>` commands can define per-grid
attributes.  (The surf/react implicit command has not yet been
released in public SPARTA).

If *g_name* is used as a value, the custom attribute must be a vector.
If *g_name\[N\]* is used, the custom attribute must be an array, and N
must be in the range from 1-M for an M-column array.  See the
discussion above for how N can be specified with a wildcard asterisk
to effectively specify multiple values.

.. note::

  that no normalization is
  performed on a value produced by a grid-style variable.

If the compute or fix is summing over particles in a grid cell to
calculate a per-grid quantity (e.g. energy or temperature), this takes
the form of a numerator divided by a denominator.  For example, see
the formulas discussed on the :ref:`compute grid<compute-grid>` doc
page, where the denominator is 1 (for keyword n), or the number of
particles (ke, mass, temp), or the sum of particle masses (u, usq,
etc).  When this command averages over a series of timesteps, the
numerator and denominator are summed separately.  This means the
numerator/denominator division only takes place when this fix produces
output, every Nfreq timesteps.

For example, say the Nfreq output is over 2 timesteps, and the value
produced by :ref:`compute grid mass<compute-grid>` is being averaged.
Say a grid cell has 10 particles on the 1st timestep with a numerator
value of 10.0, and 100 particles on the 2nd timestep with a numerator
value of 50.0.  The output of this fix will be (10+50) / (10+100) =
0.54, not ((10/10) + (50/100)) / 2 = 0.75.

Additional optional keywords also affect the operation of this fix.

The *ave* keyword determines what happens to the accumulation of
statistics every *Nfreq* timesteps.

If the *ave* setting is *one*, then the values produced on timesteps
that are multiples of Nfreq are independent of each other.
Normalization as described above is performed, and all tallies are
zeroed before accumulating over the next *Nfreq* steps.

If the *ave* setting is *running*, then tallies are never zeroed.
Thus the output at any *Nfreq* timestep is normalized over all
previously accumulated samples since the fix was defined.  The tallies
can only be zeroed by deleting the fix via the unfix command, or by
re-defining the fix, or by re-specifying it.

.. _fix-ave-grid-restart,-output:

*********************
Restart, output info:
*********************

No information about this fix is written to :ref:`binary restart files<restart>`.

This fix produces a per-grid vector or array which can be accessed by
various output commands.  A vector is produced if only a single
quantity is averaged by this fix.  If two or more quantities are
averaged, then an array of values is produced, where the number of
columns is the number of quantities averaged.  The per-grid values can
only be accessed on timesteps that are multiples of *Nfreq* since that
is when averaging is performed.

This fix performs averaging for all child grid cells in the
simulation, which includes unsplit, split, and sub cells.  :ref:`Section How-to<howto-68-details-grid-geometry>` of the manual gives details of how
SPARTA defines child, unsplit, split, and sub cells.

Grid cells not in the specified *group-ID* will output zeroes for all
their values.

Styles with a *kk* suffix are functionally the same as the
corresponding style without the suffix.  They have been optimized to
run faster, depending on your available hardware, as discussed in the
:ref:`Accelerating SPARTA<accelerate>` section of the manual.
The accelerated styles take the same arguments and should produce the
same results, except for different random number, round-off and
precision issues.

These accelerated styles are part of the KOKKOS package. They are only
enabled if SPARTA was built with that package.  See the :ref:`Making SPARTA<start-making-sparta-optional-packages>` section for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the :ref:`-suffix command-line switch<start-commandlin-options>` when you invoke SPARTA, or you can
use the :ref:`suffix<suffix>` command in your input script.

See the :ref:`Accelerating SPARTA<accelerate>` section of the
manual for more instructions on how to use the accelerated styles
effectively.

.. _fix-ave-grid-restrictio:

*************
Restrictions:
*************

If one of the specified values is a compute which tallies information
on collisions between particles and implicit surface element within
each grid cell, then all the values must be for compute(s) which do
this.  I.e. you cannot mix computes which operate on implicit surfaces
with other kinds of per-grid values in the same fix ave/grid command.

Examples of computes which tally particle/implicit surface element
collision info within each grid cell are :ref:`compute isurf/grid<compute-isurf-grid>` and :ref:`compute react/isurf/grid<compute-react-isurf-grid>`.

If performing on-the-fly grid adaptation every N timesteps, using the
:ref:`fix adapt<fix-adapt>` command, this fix cannot time-average
across time windows > N steps, since the grid may change.  This means
*Nfreq* cannot be > N, and keyword *ave* = *running* is not allowed.

.. _fix-ave-grid-related-commands:

*****************
Related commands:
*****************

:ref:`compute<compute>`, :ref:`fix ave/time<fix-ave-time>`

.. _fix-ave-grid-default:

********
Default:
********

The option defaults are ave = one.

