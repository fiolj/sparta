
:orphan:

.. index:: fix_ave_surf

.. _fix-ave-surf:

.. _fix-ave-surf-command:

####################
fix ave/surf command
####################

.. _fix-ave-surf-syntax:

*******
Syntax:
*******

::

   fix ID ave/surf group-ID Nevery Nrepeat Nfreq value1 value2 ... keyword args ...

- ID is documented in :ref:`fix<fix>` command 

- ave/surf = style name of this fix command

- group-ID = group ID for which surface elements to perform calculation on

- Nevery = use input values every this many timesteps

- Nrepeat = # of times to use input values for calculating averages

- Nfreq = calculate averages every this many timesteps zero or more input values can be listed

- value = c_ID, c_ID\[N\], f_ID, f_ID\[N\], v_name, s_name, s_name\[N\]

::

     c_ID = per-surf vector calculated by a compute with ID
     c_ID\[N\] = Nth column of per-surf array calculated by a compute with ID, N can include wildcard (see below)
     f_ID = per-surf vector calculated by a fix with ID
     f_ID\[N\] = Nth column of per-surf array calculated by a fix with ID, N can include wildcard (see below)
     v_name = per-surf vector calculated by a surf-style variable with name
     s_name = custom per-surf vector with name
     s_name\[N\] = Nth column of per-surf custom array with name, N can include wildcard (see below)

-  zero or more keyword/arg pairs may be appended

::

   keyword = *ave*
     *ave* args = one or running
       one = output a new average value every Nfreq steps
       running = accumulate average continuously

.. _fix-ave-surf-examples:

*********
Examples:
*********

::

   fix 1 ave/surf all 1 100 100 c_surf ave running
   fix 1 ave/surf leftcircle 10 20 1000 c_mine\[2\]
   fix 1 ave/surf leftcircle 10 20 1000 c_mine\[\*\]
   fix 1 ave/surf all 5 20 100 v_myEng

These commands will dump time averages for each species and each
surface element to a dump file every 1000 steps:

::

   compute 1 surf all species n press shx shy shz
   fix 1 ave/surf all 10 100 1000 c_1\[\*\]
   dump 1 surf all 1000 tmp.surf id f_1\[\*\]

.. _fix-ave-surf-descriptio:

************
Description:
************

Use one or more per-surf vectors as inputs every few timesteps, and
average them surface element by surface element by over longer
timescales, applying appropriate normalization factors. The resulting
per-surf averages can be used by other output commands such as the
:ref:`dump surf<dump>` command.  Only surface elements in the surface
group specified by *group-ID* are included in the averaging.  See the
:ref:`group surf<group>` command for info on how surface elements can
be assigned to surface groups.

Each input value can be the result of a :ref:`compute<compute>` or
:ref:`fix<fix>` or :ref:`surf-style variable<variable>` or a custom
per-surf attribute..  The compute or fix must produce a per-surf
vector or array, not a global or per-particle or per-grid quantity.
If you wish to time-average global quantities from a compute or fix
then see the :ref:`fix ave/time<fix-ave-time>` command.  To
time-average per-grid quantities, see the :ref:`fix ave/grid<fix-ave-surf>` command.

Each per-surf value of each input vector is averaged independently.

:ref:`Computes<compute>` that produce per-surf vectors or arrays are
those which have the word *surf* in their style name.  See the doc
pages for individual :ref:`fixes<fix>` to determine which ones produce
per-surf vectors or arrays.

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
had been listed one by one.  E.g. these 2 fix ave/surf commands are
equivalent, since the :ref:`compute surf<compute-grid>` command creates
a per-surf array with 4 columns:

::

   compute mySurf all all n fx fy fz
   fix 1 ave/surf all 10 20 1000 c_mySurf\[\*\]
   fix 1 ave/surf all 10 20 1000 c_mySurf\[1\] c_mySurf\[2\] &
                                 c_mySurf\[3\] c_mySurf\[4\]

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
appended, the compute must calculate a per-surf vector.  If
*c_ID\[N\]* is used, the compute must calculate a per-surf array with
M columns and N must be in the range from 1-M, which will use the Nth
column of the M-column per-surf array.  See the discussion above for
how N can be specified with a wildcard asterisk to effectively specify
multiple values.

Users can also write code for their own compute styles and :ref:`add them to SPARTA<modify>`.

If a value begins with "f\_", a fix ID must follow which has been
previously defined in the input script.  If no bracketed term is
appended, the fix must calculates a per-surf vector.  If *f_ID\[N\]*
is used, the fix must calculate a per-surf array with M columns and N
must be in the range from 1-M, which will use the Nth column of the
M-column per-surf array.  See the discussion above for how N can be
specified with a wildcard asterisk to effectively specify multiple
values.

.. note::

  that some fixes only produce their values on certain timesteps,
  which must be compatible with *Nevery*, else an error will result.
  Users can also write code for their own fix styles and :ref:`add them to   SPARTA<modify>`.

.. note::

  that surf-style variables define a formula which
  can reference :ref:`stats_style<stats-style>` keywords, or they can
  invoke other computes, fixes, or variables when they are evaluated, so
  this is a very general means of specifying quantities to time average.

If a value begins with "s\_", the name of a custom per-surf vector or
array must follow.  Custom attributes can store either a single or
multiple values per surface element.  See :ref:`Section 6.17<howto-custom-perparticl-pergrid,-persurf>` for more discussion of custom
attributes and command that define them.  For example, the
:ref:`read_surf<read-surf>`, :ref:`fix surf/temp<fix-surf-temp>`, and
:ref:`surf_react adsorb<surf-react-adsorb>` commands can define
per-surf attributes.

If *s_name* is used as a value, the custom attribute must be a vector.
If *s_name\[N\]* is used, the custom attribute must be an array, and N
must be in the range from 1-M for an M-column array.  See the
discussion above for how N can be specified with a wildcard asterisk
to effectively specify multiple values.

.. note::

  that no normalization is
  performed on a value produced by a surf-style variable.

If the compute or fix is summing over particles to calculate a
per-surf quantity (e.g. pressure or energy flux), this takes the form
of a numerator divided by a denominator.  For example, see the
formulas discussed on the :ref:`compute surf<compute-surf>` doc page,
where the denominator is 1 (for keyword n), area times dt (timestep)
for the other quantities (press, shx, ke, etc).  When this command
averages over a series of timesteps, the numerator and denominator are
summed separately.  This means the numerator/denominator division only
takes place when this fix produces output, every Nfreq timesteps.

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

.. _fix-ave-surf-restart,-output:

*********************
Restart, output info:
*********************

No information about this fix is written to :ref:`binary restart files<restart>`.

This fix produces a per-surf vector or array which can be accessed by
various output commands.  A vector is produced if only a single
quantity is averaged by this fix.  If two or more quantities are
averaged, then an array of values is produced, where the number of
columns is the number of quantities averaged.  The per-surf values can
only be accessed on timesteps that are multiples of *Nfreq* since that
is when averaging is performed.

Surface elements not in the specified *group-ID* will output zeroes
for all their values.

.. _fix-ave-surf-restrictio:

*************
Restrictions:
*************

If one of the specified values is a compute which tallies information
about particle/surface element collisions, then all the values must be
for compute(s) which do this.  I.e. you cannot mix tallying computes
with other kinds of values in the same fix ave/surf command.

Examples of computes which tally particle/surface element collision
info are :ref:`compute surf<compute-surf>` and :ref:`compute react/surf<compute-react-surf>`.

.. _fix-ave-surf-related-commands:

*****************
Related commands:
*****************

:ref:`compute<compute>`, :ref:`fix ave/time<fix-ave-time>`

.. _fix-ave-surf-default:

********
Default:
********

The option defaults are ave = one.

