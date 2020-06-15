:orphan:

.. _command-read-restart:

####################
read_restart command
####################

**Syntax:**

::

   read_restart file keyword args ... 

-  file = name of binary restart file to read in
-  zero or one keyword/args pair may be listed

::

   keywords = gridcut or balance
     gridcut arg = cutoff
       cutoff = acquire ghost cells up to this far away (distance units)
     balance args = same as for balance_grid command 

**Examples:**

::

   read_restart save.10000
   read_restart restart.*
   read_restart flow.*.%
   read_restart save.10000 gridcut -1.0
   read_restart save.10000 balance rcb cell 

**Description:**

Read in a previously saved simulation from a restart file. This allows
continuation of a previous run on the same or different number of
processors. Information about what is stored in a restart file is given
below. Basically this operation will re-create the simulation box with
all its particles, the hierarchical grid used to track particles, and
surface elements embedded in the grid, all with their attributes at the
point in time the information was written to the restart file by a
previous simluation.

Although restart files are saved in binary format to allow exact
regeneration of information, the random numbers used in the continued
run will not be identical to those used if the run had been continued.
Hence the new run will not be identical to the continued original run,
but should be statistically similar.

IMPORTANT NOTE: Because restart files are binary, they may not be
portable to other machines. SPARTA will print an error message if it
cannot read a restart file for this reason.

If a restarted run is performed on the same number of processors as the
original run, then the assignment of grid cells (and their particles) to
processors will be the same as in the original simulation. If the
processor count changes, then the assignment will necessarily be
different. In particular, even if the original assignment was "clumped",
meaning each processor's cells were geometrically compact, the new
assignment will not be clumped; it will be "dispersed". See `Section
6.8 <Section_howto.html#howto_8>`__ of the manual for an explanation of
clumped and dispersed grid cell assignments and their relative
performance trade-offs.

Note that the restart file contains the setting for the `global
gridcut <global.html>`__ command. If it is >= 0.0 and the assignment of
grid cells to processors is "dispersed" (as described in the preceeding
paragraph), and there are surface elements defined in the restart file,
an error will be triggered. This is because the read_restart command
needs to mark all the grid cells as inside vs outside the defined
surface and cannot do this without ghost cell information. As explained
on the doc page for the `global gridcut <global.html>`__ command, ghost
cells cannot be setup with gridcut >= 0.0 and "dispersed" grid cells.

The solution is to use one of the two keywords listed above, either
*gridcut* or *balance*. The former allows you to reset the grid cutoff
to -1.0 so that ghost cells can be setup. Note however that this means
each processor will own a copy of all grid cells (at least until you
change it later), which may be undesirable or even impossible for large
problems if it requires too much memory. The other solution is to use
the *balance* keyword to trigger a re-balance of the grid cells to
processors as soon as the read_restart command reads them in. The
arguments for the *balance* keyword are identical to those for the
`balance_grid <balance_grid.html>`__ command. If you choose a balancing
style that results in a "clumped" assignment, then ghost cells will be
setup successfully.

--------------

Similar to how restart files are written (see the
`write_restart <write_restart.html>`__ and `restart <restart.html>`__
commands), the restart filename can contain two wild-card characters. If
a "*" appears in the filename, the directory is searched for all
filenames that match the pattern where "*" is replaced with a timestep
value. The file with the largest timestep value is read in. Thus, this
effectively means, read the latest restart file. It's useful if you want
your script to continue a run from where it left off. See the
`run <run.html>`__ command and its "upto" option for how to specify the
run command so it doesn't need to be changed either.

If a "%" character appears in the restart filename, SPARTA expects a set
of multiple files to exist. The `restart <restart.html>`__ and
`write_restart <write_restart.html>`__ commands explain how such sets
are created. Read_restart will first read a filename where "%" is
replaced by "base". This file tells SPARTA how many processors created
the set and how many files are in it. Read_restart then reads the
additional files. For example, if the restart file was specified as
save.% when it was written, then read_restart reads the files save.base,
save.0, save.1, ... save.P-1, where P is the number of processors that
created the restart file.

Note that P could be the total number of processors in the previous
simulation, or some subset of those processors, if the *fileper* or
*nfile* options were used when the restart file was written; see the
`restart <restart.html>`__ and `write_restart <write_restart.html>`__
commands for details. The processors in the current SPARTA simulation
share the work of reading these files; each reads a roughly equal subset
of the files. The number of processors which created the set can be
different than the number of processors in the current SPARTA
simulation. This can be a fast mode of input on parallel machines that
support parallel I/O.

--------------

A restart file stores only the following information about a simulation,
as specified by the associated commands:

-  `units <units.html>`__
-  `dimension <dimension.html>`__
-  `simulation box size <create_box.html>`__ and `boundary
   conditions <boundary.html>`__
-  `global settings <global.html>`__
-  particles with their individual attributes and custom attributes
   defined by fixes
-  `particle species info <species.html>`__
-  `mixtures <mixture.html>`__
-  geometry of the hierarchical grid that overlays the simulation domain
   as `created <create_grid.html>`__ or `read from a
   file <read_grid.html>`__
-  geometry of all defined `surface elements <read_surf.html>`__
-  `group definitions <group.html>`__ for grid cells and surface
   elements
-  current timestep number

No other information is stored in the restart file. Specifically,
information about these simulation entities and their associated
commands is NOT stored:

-  `random number seed <seed,html>`__
-  `computes <compute.html>`__
-  `fixes <fix.html>`__
-  `collision model <collide.html>`__
-  `chemistry (reaction) model <react.html>`__
-  `surface collision models <surf_collide.html>`__
-  `surface reaction models <surf_react.html>`__
-  assignment of surfaces/boundaries to surface models
-  `variables <variable.html>`__
-  `regions <region.html>`__
-  output options for `stats <stats_style.html>`__,
   `dump <dump.html>`__, `restart <restart.html>`__ files
-  `timestep size <timestep.html>`__

This means any information specified in the original input script by
these commands needs to be re-specified in the restart input script,
assuming the continued simulation needs the information.

Also note that many commands can be used after a restart file is read,
to override a setting that was stored in the restart file. For example,
the `global <global.html>`__ command can be used to reset the values of
its specified keywords.

In particular, take note of the following issues:

The status of time-averaging fixes, such as `fix
ave/time <fix_ave_time.html>`__, `fix ave/grid <fix_ave_grid.html>`__,
`fix ave/surf <fix_ave_surf.html>`__, does not carry over into the
restarted run. E.g. if the *ave running* option is used with those
commands in the original script and again specified in the restart
script, the running averaged quantities do not persist into the new run.

The `surf_modify <surf_modify.html>`__ command must be used in the
restart script to assign surface collision models, specified by the
`surf_collide <surf_collide.html>`__ command, to all `global
boundaries <boundary.html>`__ of type "s", and to any surfaces contained
in the restart file, as read in by the `read_surf <read_surf.html>`__
command.

If a collision model is specified in the restart script, and the
`collide_modify vremax or remain <collide_modify.html>`__ command is
used to enable Vremax and fractional collision count to persist for many
timesteps, no information about these quantities persists from the
original simulation to the restarted simulation. The initial run in the
restart script will re-initialize these data structures.

If a fix is used which defines custom attributes of particles, the
vectors or arrays for these attributes are stored in the restart file.
See the `fix ambipolar <fix_ambipolar>`__ command as an example; it
creates a custom vector called "ionambi" and a custom array called
"velambi". However, the restart script must specify the same fix before
the first `run <run.html>`__ command it uses, so that the same custom
attributes are re-created, otherwise the custom attribute info from the
restart file will be deleted.

--------------

**Restrictions:** none

**Related commands:**

:ref:`command-read-grid`,
:ref:`command-read-surf`,
:ref:`command-write-restart`,
:ref:`command-restart`

**Default:** none
