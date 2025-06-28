
.. _commands:

.. _commands-3:

###########
3. Commands
###########

This section describes how a SPARTA input script is formatted and what
commands are used to define a SPARTA simulation.

1 :ref:`SPARTA input script<commands-31-sparta-input-script>`
3.2 :ref:`Parsing rules<commands-parsing-rules>`
3.3 :ref:`Input script structure<commands-input-script-structure>`
3.4 :ref:`Commands listed by category<commands-listed-by-category>`
3.5 :ref:`Commands listed alphabetically<commands-individual>`

.. _commands-31-sparta-input-script:

***********************
3.1 SPARTA input script
***********************

SPARTA executes by reading commands from a input script (text file),
one line at a time.  When the input script ends, SPARTA exits.  Each
command causes SPARTA to take some action.  It may set an internal
variable, read in a file, or run a simulation.  Most commands have
default settings, which means you only need to use the command if you
wish to change the default.

In many cases, the ordering of commands in an input script is not
important.  However the following rules apply:

(1) SPARTA does not read your entire input script and then perform a
simulation with all the settings.  Rather, the input script is read
one line at a time and each command takes effect when it is read.
Thus this sequence of commands:

::

   timestep 0.5 
   run      100 
   run      100

does something different than this sequence:

::

   run      100 
   timestep 0.5 
   run      100

In the first case, the specified timestep (0.5 secs) is used for two
simulations of 100 timesteps each.  In the 2nd case, the default
timestep (1.0 sec is used for the 1st 100 step simulation and a 0.5
fmsec timestep is used for the 2nd one.

(2) Some commands are only valid when they follow other commands.  For
example you cannot define the grid overlaying the simulation box until
the box itself has been defined.  Likewise you cannot read in
triangulated surfaces until a grid has been defined to store them.

Many input script errors are detected by SPARTA and an ERROR or
WARNING message is printed.  :ref:`Section 12<errors>` gives
more information on what errors mean.  The documentation for each
command lists restrictions on how the command can be used.

.. _commands-parsing-rules:

*************
Parsing rules
*************

Each non-blank line in the input script is treated as a command.
SPARTA commands are case sensitive.  Command names are lower-case, as
are specified command arguments.  Upper case letters may be used in
file names or user-chosen ID strings.

Here is how each line in the input script is parsed by SPARTA:

(1) If the last printable character on the line is a "&" character
(with no surrounding quotes), the command is assumed to continue on
the next line.  The next line is concatenated to the previous line by
removing the "&" character and newline.  This allows long commands to
be continued across two or more lines.

.. note::

  that a
  comment after a trailing "&" character will prevent the command from
  continuing on the next line.  Also note that for multi-line commands a
  single leading "#" will comment out the entire command.

(3) The line is searched repeatedly for $ characters, which indicate
variables that are replaced with a text string.  See an exception in
(6).

If the $ is followed by curly brackets, then the variable name is the
text inside the curly brackets.  If no curly brackets follow the $,
then the variable name is the single character immediately following
the $.  Thus $\{myTemp\} and $x refer to variable names "myTemp" and
"x".

How the variable is converted to a text string depends on what style
of variable it is; see the :ref:`variable<variable>` doc page for details.
It can be a variable that stores multiple text strings, and return one
of them.  The returned text string can be multiple "words" (space
separated) which will then be interpreted as multiple arguments in the
input command.  The variable can also store a numeric formula which
will be evaluated and its numeric result returned as a string.

As a special case, if the $ is followed by parenthesis, then the text
inside the parenthesis is treated as an "immediate" variable and
evaluated as an :ref:`equal-style variable<variable>`.  This is a way
to use numeric formulas in an input script without having to assign
them to variable names.  For example, these 3 input script lines:

::

   variable X equal (xlo+xhi)/2+sqrt(v_area)
   region 1 block $X 2 INF INF EDGE EDGE
   variable X delete

can be replaced by

::

   region 1 block $((xlo+xhi)/2+sqrt(v_area)) 2 INF INF EDGE EDGE

so that you do not have to define (or discard) a temporary variable X.

.. note::

  that neither the curly-bracket or immediate form of variables can
  contain nested $ characters for other variables to substitute for.
  Thus you cannot do this:

::

   variable        a equal 2
   variable        b2 equal 4
   print           "B2 = $\{b$a\}"

Nor can you specify this $($x-1.0) for an immediate variable, but
you could use $(v_x-1.0), since the latter is valid syntax for an
:ref:`equal-style variable<variable>`.

See the :ref:`variable<variable>` command for more details of how
strings are assigned to variables and evaluated, and how they can be
used in input script commands.

.. note::

  that words can thus contain letters, digits,
  underscores, or punctuation characters.

(5) The first word is the command name.  All successive words in the
line are arguments.

(6) If you want text with spaces to be treated as a single argument,
it can be enclosed in either single (') or double (") or triple quotes
(""").  A long single argument enclosed in single or double quotes can
span multiple lines if the "&" character is used, as described above.
When the lines are concatenated together by SPARTA (and the "&"
characters and line breaks removed), the combined text will become a
single line.  If you want multiple lines of an argument to retain
their line breaks, the text can be enclosed in triple quotes, in which
case "&" characters are not needed and do not function as line
continuation character.

For example:

print "Volume = $v"
print 'Volume = $v'
print """
System volume = $v
System temperature = $t
"""
variable a string "red green blue &
                   purple orange cyan"
if "$*steps* > 1000" then quit

In each of these cases, the single, double, or triple quotes are
removed and the enclosed text stored internally as a single argument.

See the :ref:`dump modify format<dump-modify>`, :ref:`print<print>`,
:ref:`if<if>`, or :ref:`python<python>` commands for examples.

A "#" or "$" character that is between quotes will not be treated as a
comment indicator in (2) or substituted for as a variable in (3).

.. important::

  If the argument is itself a command that requires a
  quoted argument (e.g. using a :ref:`print<print>` command as part of an
  :ref:`if<if>` or :ref:`run every<run>` command), then single, double, or
  triple quotes can be nested in the usual manner.  See the doc pages
  for those commands for examples.  Only one of level of nesting is
  allowed, but that should be sufficient for most use cases.

.. _commands-input-script-structure:

**********************
Input script structure
**********************

This section describes the structure of a typical SPARTA input script.
The "examples" directory in the SPARTA distribution contains sample
input scripts; the corresponding problems are discussed in :ref:`Section 5<example>`, and animated on the `SPARTA WWW Site <http://sparta.sandia.gov>`__.

A SPARTA input script typically has 4 parts:

   
   0. Initialization
   1. Problem definition
   2. Settings
   3. Run a simulation

The last 2 parts can be repeated as many times as desired.  I.e. run a
simulation, change some settings, run some more, etc.  Each of the 4
parts is now described in more detail.  Remember that almost all the
commands need only be used if a non-default value is desired.

(1) Initialization

Set parameters that need to be defined before the simulation domain,
particles, grid cells, and surfaces are defined.

Relevant commands include :ref:`dimension<dimension>`,
:ref:`units<units>`, and :ref:`seed<seed>`.

(2) Problem definition

These items must be defined before running a SPARTA calculation, and
typically in this order:

   - :ref:`create_box<create-box>` for the simulation box
   - :ref:`create_grid<create-grid>` or :ref:`read_grid<read-grid>` for grid cells
   - :ref:`read_surf<read-surf>` or :ref:`read_isurf<read-isurf>` for surfaces
   - :ref:`species<species>` for particle species properties
   - :ref:`create_particles<create-particles>` for particles

The first two are required.  Surfaces are optional.  Particles are also
optional in the setup stage, since they can be added as the simulation
runs.

The system can also be load-balanced after the grid and/or particles
are defined in the setup stage using the
:ref:`balance_grid<balance-grid>` command.  The grid can also be
adapted before or betwee simulations using the
:ref:`adapt_grid<adapt-grid>` command.

(3) Settings

Once the problem geometry, grid cells, surfaces, and particles are
defined, a variety of settings can be specified, which include
simulation parameters, output options, etc.

Commands that do this include

:ref:`global<global>`
:ref:`timestep<timestep>`
:ref:`collide<collide>` for a collision model
:ref:`react<react>` for a chemisty model
:ref:`fix<fix>` for boundary conditions, time-averaging, load-balancing, etc
:ref:`compute<compute>` for diagnostic computations
:ref:`stats_style<stats-style>` for screen output
:ref:`dump<dump>` for snapshots of particle, grid, and surface info
:ref:`dump image<dump>` for on-the-fly images of the simulation

(4) Run a simulation

A simulation is run using the :ref:`run<run>` command.

.. _commands-listed-by-category:

***************************
Commands listed by category
***************************

This section lists many SPARTA commands, grouped by category.  The
:ref:`next section<commands-individual>` lists all commands alphabetically.

Initialization:

:ref:`dimension<dimension>`, :ref:`package<package>`, :ref:`seed<seed>`,
:ref:`suffix<suffix>`, :ref:`units<units>`

Problem definition:

:ref:`boundary<boundary>`, :ref:`bound_modify<bound-modify>`,
:ref:`create_box<create-box>`, :ref:`create_grid<create-grid>`,
:ref:`create_particles<create-particles>`, :ref:`mixture<mixture>`,
:ref:`read_grid<read-grid>`, :ref:`read_isurf<read-isurf>`,
:ref:`read_particles<read-particles>`, :ref:`read_surf<read-surf>`,
:ref:`read_restart<read-restart>`, :ref:`species<species>`,

Settings:

:ref:`collide<collide>`, :ref:`collide_modify<collide-modify>`,
:ref:`compute<compute>`, :ref:`fix<fix>`, :ref:`global<global>`,
:ref:`react<react>`, :ref:`react_modify<react-modify>`,
:ref:`region<region>`, :ref:`surf_collide<surf-collide>`,
:ref:`surf_modify<surf-modify>`, :ref:`surf_react<surf-react>`,
:ref:`timestep<timestep>`, :ref:`uncompute<uncompute>`,
:ref:`unfix<unfix>`

Output:

:ref:`dump<dump>`, :ref:`dump_image<dump-image>`,
:ref:`dump_modify<dump-modify>`, :ref:`restart<restart>`,
:ref:`stats<stats>`, :ref:`stats_modify<stats-modify>`,
:ref:`stats_style<stats-style>`, :ref:`undump<undump>`,
:ref:`write_grid<write-grid>`, :ref:`write_isurf<write-isurf>`,
:ref:`write_surf<write-surf>`, :ref:`write_restart<write-restart>`

Actions:

:ref:`adapt_grid<adapt-grid>`, :ref:`balance_grid<balance-grid>`,
:ref:`run<run>`, :ref:`scale_particles<scale-particles>`

Miscellaneous:

:ref:`clear<clear>`, :ref:`echo<echo>`, :ref:`if<if>`,
:ref:`include<include>`, :ref:`jump<jump>`, :ref:`label<label>`,
:ref:`log<log>`, :ref:`next<next>`, :ref:`partition<partition>`,
:ref:`print<print>`, :ref:`quit<quit>`, :ref:`shell<shell>`,
:ref:`variable<variable>`

.. _commands-commandsin-individual:

.. _commands-individual:

*******************
Individual commands
*******************

This section lists all SPARTA commands alphabetically, with a separate
listing below of styles within certain commands.  The :ref:`previous section<commands-listed-by-category>` lists many of the same commands, grouped by category.

.. list-table::
   :header-rows: 0

   * - :ref:`adapt_grid<adapt-grid>`
     -  :ref:`balance_grid<balance-grid>`
     -  :ref:`boundary<boundary>`
     -  :ref:`bound_modify<bound-modify>`
     -  :ref:`clear<clear>`
     -  :ref:`collide<collide>`
   * -  :ref:`collide_modify<collide-modify>`
     -  :ref:`compute<compute>`
     -  :ref:`create_box<create-box>`
     -  :ref:`create_grid<create-grid>`
     -  :ref:`create_isurf<create-isurf>`
     -  :ref:`create_particles<create-particles>`
   * -  :ref:`custom<custom>`
     -  :ref:`dimension<dimension>`
     -  :ref:`dump<dump>`
     -  :ref:`dump image<dump-image>`
     -  :ref:`dump_modify<dump-modify>`
     -  :ref:`dump movie<dump-image>`
   * -  :ref:`echo<echo>`
     -  :ref:`fix<fix>`
     -  :ref:`global<global>`
     -  :ref:`group<group>`
     -  :ref:`if<if>`
     -  :ref:`include<include>`
   * -  :ref:`jump<jump>`
     -  :ref:`label<label>`
     -  :ref:`log<log>`
     -  :ref:`mixture<mixture>`
     -  :ref:`move_surf<move-surf>`
     -  :ref:`next<next>`
   * -  :ref:`package<package>`
     -  :ref:`partition<partition>`
     -  :ref:`print<print>`
     -  :ref:`quit<quit>`
     -  :ref:`react<react>`
     -  :ref:`react_modify<react-modify>`
   * -  :ref:`read_grid<read-grid>`
     -  :ref:`read_isurf<read-isurf>`
     -  :ref:`read_particles<read-particles>`
     -  :ref:`read_restart<read-restart>`
     -  :ref:`read_surf<read-surf>`
     -  :ref:`region<region>`
   * -  :ref:`remove_surf<remove-surf>`
     -  :ref:`reset_timestep<reset-timestep>`
     -  :ref:`restart<restart>`
     -  :ref:`run<run>`
     -  :ref:`scale_particles<scale-particles>`
     -  :ref:`seed<seed>`
   * -  :ref:`shell<shell>`
     -  :ref:`species<species>`
     -  :ref:`species_modify<species-modify>`
     -  :ref:`stats<stats>`
     -  :ref:`stats_modify<stats-modify>`
     -  :ref:`stats_style<stats-style>`
   * -  :ref:`suffix<suffix>`
     -  :ref:`surf_collide<surf-collide>`
     -  :ref:`surf_react<surf-react>`
     -  :ref:`surf_modify<surf-modify>`
     -  :ref:`timestep<timestep>`
     -  :ref:`uncompute<uncompute>`
   * -  :ref:`undump<undump>`
     -  :ref:`unfix<unfix>`
     -  :ref:`units<units>`
     -  :ref:`variable<variable>`
     -  :ref:`write_grid<write-grid>`
     -  :ref:`write_isurf<write-isurf>`
   * -  :ref:`write_restart<write-restart>`
     -  :ref:`write_surf<write-surf>`
     - 
     - 
     - 
     -

.. _commands-fix-styles:

**********
Fix styles
**********

See the :ref:`fix<fix>` command for one-line descriptions of each style
or click on the style itself for a full description.  Some of the
styles have accelerated versions, which can be used if SPARTA is built
with the :ref:`appropriate accelerated package<accelerate>`.
This is indicated by additional letters in parenthesis: k = KOKKOS.

.. list-table::
   :header-rows: 0

   * - :ref:`ablate<fix-ablate>`
     -  :ref:`adapt (k)<fix-adapt>`
     -  :ref:`ambipolar (k)<fix-ambipolar>`
     -  :ref:`ave/grid (k)<fix-ave-grid>`
     -  :ref:`ave/histo (k)<fix-ave-histo>`
     -  :ref:`ave/histo/weight (k)<fix-ave-histo>`
   * -  :ref:`ave/surf<fix-ave-surf>`
     -  :ref:`ave/time<fix-ave-time>`
     -  :ref:`balance (k)<fix-balance>`
     -  :ref:`dt/reset (k)<fix-dt-reset>`
     -  :ref:`emit/face (k)<fix-emit-face>`
     -  :ref:`emit/face/file<fix-emit-face-file>`
   * -  :ref:`emit/surf<fix-emit-surf>`
     -  :ref:`field/grid<fix-field-grid>`
     -  :ref:`field/particle<fix-field-particle>`
     -  :ref:`grid/check (k)<fix-grid-check>`
     -  :ref:`halt<fix-halt>`
     -  :ref:`move/surf (k)<fix-move-surf>`
   * -  :ref:`print<fix-print>`
     -  :ref:`surf/temp<fix-surf-temp>`
     -  :ref:`temp/global/rescale<fix-temp-global-rescale>`
     -  :ref:`temp/rescale (k)<fix-temp-rescale>`
     -  :ref:`vibmode (k)<fix-vibmode>`
     -

.. _commands-compute-styles:

**************
Compute styles
**************

See the :ref:`compute<compute>` command for one-line descriptions of
each style or click on the style itself for a full description.  Some
of the styles have accelerated versions, which can be used if SPARTA
is built with the :ref:`appropriate accelerated package<accelerate>`.  This is indicated by additional
letters in parenthesis: k = KOKKOS.

.. list-table::
   :header-rows: 0

   * - :ref:`boundary (k)<compute-boundary>`
     -  :ref:`count (k)<compute-count>`
     -  :ref:`distsurf/grid (k)<compute-distsurf-grid>`
     -  :ref:`dt/grid (k)<compute-dt-grid>`
     -  :ref:`eflux/grid (k)<compute-eflux-grid>`
     -  :ref:`fft/grid (k)<compute-fft-grid>`
   * -  :ref:`grid (k)<compute-grid>`
     -  :ref:`isurf/grid<compute-isurf-grid>`
     -  :ref:`ke/particle (k)<compute-ke-particle>`
     -  :ref:`lambda/grid (k)<compute-lambda-grid>`
     -  :ref:`pflux/grid (k)<compute-pflux-grid>`
     -  :ref:`property/grid (k)<compute-property-grid>`
   * -  :ref:`react/boundary<compute-react-boundary>`
     -  :ref:`react/surf<compute-react-surf>`
     -  :ref:`react/isurf/grid<compute-react-isurf-grid>`
     -  :ref:`reduce<compute-reduce>`
     -  :ref:`sonine/grid (k)<compute-sonine-grid>`
     -  :ref:`surf (k)<compute-surf>`
   * -  :ref:`thermal/grid (k)<compute-thermal-grid>`
     -  :ref:`temp (k)<compute-temp>`
     -  :ref:`tvib/grid<compute-tvib-grid>`
     - 
     - 
     -

.. _commands-collide-styles:

**************
Collide styles
**************

See the :ref:`collide<collide>` command for details of each style.
Some of the styles have accelerated versions, which can be used if
SPARTA is built with the :ref:`appropriate accelerated package<accelerate>`.  This is indicated by additional
letters in parenthesis: k = KOKKOS.

.. list-table::
   :header-rows: 0

   * - :ref:`vss (k)<collide>`

.. _commands-surface-collide-styles:

**********************
Surface collide styles
**********************

See the :ref:`surf_collide<surf-collide>` command for details of each
style.  Some of the styles have accelerated versions, which can be
used if SPARTA is built with the :ref:`appropriate accelerated package<accelerate>`.  This is indicated by additional
letters in parenthesis: k = KOKKOS.

.. list-table::
   :header-rows: 0

   * - :ref:`cll<surf-collide>`
     -  :ref:`diffuse (k)<surf-collide>`
     -  :ref:`impulsive<surf-collide>`
   * -  :ref:`piston (k)<surf-collide>`
     -  :ref:`specular (k)<surf-collide>`
     -  :ref:`td<surf-collide>`
   * -  :ref:`vanish (k)<surf-collide>`
     - 
     -

.. _commands-surface-reaction-styles:

***********************
Surface reaction styles
***********************

See the :ref:`surf_react<surf-react>` command for details of each
style. Some of the styles have accelerated versions, which can be
used if SPARTA is built with the :ref:`appropriate accelerated package<accelerate>`.  This is indicated by additional
letters in parenthesis: k = KOKKOS.

.. list-table::
   :header-rows: 0

   * - :ref:`adsorb<surf-react-adsorb>`
     -  :ref:`global (k)<surf-react>`
   * -  :ref:`prob (k)<surf-react>`
     -

