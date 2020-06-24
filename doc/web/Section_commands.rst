




.. _commands:

########
Commands
########



This section describes how a SPARTA input script is formatted and what
commands are used to define a SPARTA simulation.

.. contents::
   :depth: 2

--------------



.. _commands-sparta-input:

*******************
SPARTA input script
*******************



SPARTA executes by reading commands from a input script (text file), one
line at a time. When the input script ends, SPARTA exits. Each command
causes SPARTA to take some action. It may set an internal variable, read
in a file, or run a simulation. Most commands have default settings,
which means you only need to use the command if you wish to change the
default.

In many cases, the ordering of commands in an input script is not
important. However the following rules apply:

(1) SPARTA does not read your entire input script and then perform a
simulation with all the settings. Rather, the input script is read one
line at a time and each command takes effect when it is read. Thus this
sequence of commands:

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
simulations of 100 timesteps each. In the 2nd case, the default timestep
(1.0 sec is used for the 1st 100 step simulation and a 0.5 fmsec
timestep is used for the 2nd one.

(2) Some commands are only valid when they follow other commands. For
example you cannot define the grid overlaying the simulation box until
the box itself has been defined. Likewise you cannot read in
triangulated surfaces until a grid has been defined to store them.

Many input script errors are detected by SPARTA and an ERROR or WARNING
message is printed. Section :ref:`errors` gives more
information on what errors mean. The documentation for each command
lists restrictions on how the command can be used.

--------------





.. _commands-parsing-rules:

*************
Parsing rules
*************



Each non-blank line in the input script is treated as a command. SPARTA
commands are case sensitive. Command names are lower-case, as are
specified command arguments. Upper case letters may be used in file
names or user-chosen ID strings.

Here is how each line in the input script is parsed by SPARTA:

(1) If the last printable character on the line is a "&" character (with
no surrounding quotes), the command is assumed to continue on the next
line. The next line is concatenated to the previous line by removing the
"&" character and newline. This allows long commands to be continued
across two or more lines.

(2) All characters from the first "#" character onward are treated as
comment and discarded. See an exception in (6). Note that a comment
after a trailing "&" character will prevent the command from continuing
on the next line. Also note that for multi-line commands a single
leading "#" will comment out the entire command.

(3) The line is searched repeatedly for $ characters, which indicate
variables that are replaced with a text string. See an exception in (6).

If the $ is followed by curly brackets, then the variable name is the
text inside the curly brackets. If no curly brackets follow the $, then
the variable name is the single character immediately following the $.
Thus ${myTemp} and $x refer to variable names "myTemp" and "x".

How the variable is converted to a text string depends on what style of
variable it is; see the :ref:`variable<command-variable>` doc page for details. It
can be a variable that stores multiple text strings, and return one of
them. The returned text string can be multiple "words" (space separated)
which will then be interpreted as multiple arguments in the input
command. The variable can also store a numeric formula which will be
evaluated and its numeric result returned as a string.

As a special case, if the $ is followed by parenthesis, then the text
inside the parenthesis is treated as an "immediate" variable and
evaluated as an :ref:`equal-style variable<command-variable>`. This is a way
to use numeric formulas in an input script without having to assign them
to variable names. For example, these 3 input script lines:

::

   variable X equal (xlo+xhi)/2+sqrt(v_area)
   region 1 block $X 2 INF INF EDGE EDGE
   variable X delete 

can be replaced by

::

   region 1 block $((xlo+xhi)/2+sqrt(v_area)) 2 INF INF EDGE EDGE 

so that you do not have to define (or discard) a temporary variable X.

Note that neither the curly-bracket or immediate form of variables can
contain nested $ characters for other variables to substitute for. Thus
you cannot do this:

::

   variable        a equal 2
   variable        b2 equal 4
   print           "B2 = ${b$a}" 

Nor can you specify this $($x-1.0) for an immediate variable, but you
could use $(v_x-1.0), since the latter is valid syntax for an
`equal-style variable <command-variable>`.

See the `command-variable` for more details of how
strings are assigned to variables and evaluated, and how they can be
used in input script commands.

(4) The line is broken into "words" separated by whitespace (tabs,
spaces). Note that words can thus contain letters, digits, underscores,
or punctuation characters.

(5) The first word is the command name. All successive words in the line
are arguments.

(6) If you want text with spaces to be treated as a single argument, it
can be enclosed in either double or single quotes. A long single
argument enclosed in quotes can even span multiple lines if the "&"
character is used, as described above. E.g.

::

   print "Volume = $v"
   print 'Volume = $v'
   variable a string "red green blue &
                      purple orange cyan"
   if "$steps > 1000" then quit 

The quotes are removed when the single argument is stored internally.

See the :ref:`dump modify format<command-dump-modify>` or
:ref:`command-print`, or :ref:`command-if` for examples. A "#"
or "$" character that is between quotes will not be treated as a comment
indicator in (2) or substituted for as a variable in (3).

.. important:: If the argument is itself a command that requires a quoted argument (e.g. using a :ref:`command-print` command as part of an :ref:`command-if` or :ref:`run every<command-run>` command), then the double and single quotes can be nested in the usual manner. See the doc pages for those commands for examples. Only one of level of nesting is allowed, but that should be sufficient for most use cases.



.. _commands-input-script:

**********************
Input script structure
**********************



This section describes the structure of a typical SPARTA input script.
The "examples" directory in the SPARTA distribution contains sample
input scripts; the corresponding problems are discussed in Section :ref:`example`, and animated on the `SPARTA WWW Site <http://sparta.sandia.gov>`__.

A SPARTA input script typically has 4 parts:

#. Initialization
#. Problem definition
#. Settings
#. Run a simulation

The last 2 parts can be repeated as many times as desired. I.e. run a
simulation, change some settings, run some more, etc. Each of the 4
parts is now described in more detail. Remember that almost all the
commands need only be used if a non-default value is desired.

1. Initialization
   Set parameters that need to be defined before the simulation domain,
   particles, grid cells, and surfaces are defined.

   Relevant commands include :ref:`command-dimension`
   :ref:`command-units`, and :ref:`command-seed`.

2. Problem definition

   These items must be defined before running a SPARTA calculation, and
   typically in this order:

   -  :ref:`create_box<command-create-box>` for the simulation box 
   -  :ref:`create_grid<command-create-grid>` or :ref:`read_grid<command-read-grid>` for grid cells
   -  :ref:`read_surf<command-read-surf>` or :ref:`read_isurf<command-read-isurf>` for surfaces
   -  :ref:`species<command-species>` for particle species properties
   -  :ref:`create_particles<command-create-particles>` for particles

   The first two are required. Surfaces are optional. Particles are also
   optional in the setup stage, since they can be added as the simulation
   runs.

   The system can also be load-balanced after the grid and/or particles are
   defined in the setup stage using the :ref:`command-balance-grid`. The grid can also be adapted before or betwee simulations using the :ref:`command-adapt-grid`.

3. Settings

   Once the problem geometry, grid cells, surfaces, and particles are
   defined, a variety of settings can be specified, which include
   simulation parameters, output options, etc.

   Commands that do this include

   :ref:`global<command-global>`,  :ref:`timestep<command-timestep>`,
   :ref:`collide<command-collide>` for a collision model, :ref:`react<command-react>` for a chemisty model, :ref:`fix<command-fix>` for boundary conditions,
   time-averaging, load-balancing, etc. :ref:`compute<command-compute>` for
   diagnostic computations :ref:`stats_style<command-stats-style>` for screen
   output :ref:`dump<command-dump>` for snapshots of particle, grid, and surface
   info :ref:`dump image<command-dump>` for on-the-fly images of the simulation

4. Run a simulation

  A simulation is run using the :ref:`command-run`.





.. _commands-category:

***************************
Commands listed by category
***************************



This section lists many SPARTA commands, grouped by category. The :ref:`next section<commands-individual>` lists all commands alphabetically.

Initialization:
   :ref:`dimension<command-dimension>`, :ref:`package<command-package>`,
   :ref:`seed<command-seed>`, :ref:`suffix<command-suffix>`, :ref:`units<command-units>`

Problem definition:
   :ref:`boundary<command-boundary>`, :ref:`bound_modify<command-bound-modify>`,
   :ref:`create_box<command-create-box>`, :ref:`create_grid<command-create-grid>`,
   :ref:`create_particles<command-create-particles>`,
   :ref:`mixture<command-mixture>`, :ref:`read_grid<command-read-grid>`,
   :ref:`read_isurf<command-read-isurf>`,
   :ref:`read_particles<command-read-particles>`,
   :ref:`read_surf<command-read-surf>`, :ref:`read_restart<command-read-restart>`,
   :ref:`species<command-species>`

Settings:
   :ref:`collide<command-collide>`, :ref:`collide_modify<command-collide-modify>`,
   :ref:`compute<command-compute>`, :ref:`fix<command-fix>`,
   :ref:`global<command-global>`, :ref:`react<command-react>`,
   :ref:`react_modify<command-react-modify>`, :ref:`region<command-region>`,
   :ref:`surf_collide<command-surf-collide>`,
   :ref:`surf_modify<command-surf-modify>`, :ref:`surf_react<command-surf-react>`,
   :ref:`timestep<command-timestep>`, :ref:`uncompute<command-uncompute>`,
   :ref:`unfix<command-unfix>`

Output:
   :ref:`dump<command-dump>`, :ref:`dump_image<command-dump-image>`,
   :ref:`dump_modify<command-dump-modify>`, :ref:`restart<command-restart>`,
   :ref:`stats<command-stats>`, :ref:`stats_modify<command-stats-modify>`,
   :ref:`stats_style<command-stats-style>`, :ref:`undump<command-undump>`,
   :ref:`write_grid<command-write-grid>`, :ref:`write_isurf<command-write-isurf>`,
   :ref:`write_surf<command-write-surf>`, :ref:`write_restart<command-write-restart>`

Actions:
   :ref:`adapt_grid<command-adapt-grid>`, :ref:`balance_grid<command-balance-grid>`,
   :ref:`run<command-run>`, :ref:`scale_particles<command-scale-particles>`
   
Miscellaneous:
   :ref:`clear<command-clear>`, :ref:`echo<command-echo>`, :ref:`if<command-if>`,
   :ref:`include<command-include>`, :ref:`jump<command-jump>`,
   :ref:`label<command-label>`, :ref:`log<command-log>`, :ref:`next<command-next>`,
   :ref:`partition<command-partition>`, :ref:`print<command-print>`,
   :ref:`quit<command-quit>`, :ref:`shell<command-shell>`,
   :ref:`variable<command-variable>`








.. _commands-individual:

*******************
Individual commands
*******************



This section lists all SPARTA commands alphabetically, with a separate listing below of styles within certain commands. The :ref:`previous section<commands-category>` lists many of the same commands, grouped by category.

.. list-table::
   :header-rows: 0

   * -  :ref:`adapt_grid<command-adapt-grid>`         
     -  :ref:`balance_grid<command-balance-grid>` 
     -  :ref:`boundary<command-boundary>`               
     -  :ref:`bound_modify<command-bound-modify>`   
     -  :ref:`clear<command-clear>`                       
     -  :ref:`collide<command-collide>`               
   * -  :ref:`collide_modify<command-collide-modify>` 
     -  :ref:`compute<command-compute>`           
     -  :ref:`create_box<command-create-box>`           
     -  :ref:`create_grid<command-create-grid>`     
     -  :ref:`create_particles<command-create-particles>` 
     -  :ref:`dimension<command-dimension>`           
   * -  :ref:`dump<command-dump>`                     
     -  :ref:`dump image<command-dump-image>`     
     -  :ref:`dump_modify<command-dump-modify>`         
     -  :ref:`dump movie<command-dump-image>`       
     -  :ref:`echo<command-echo>`                         
     -  :ref:`fix<command-fix>`                       
   * -  :ref:`global<command-global>`                 
     -  :ref:`group<command-group>`               
     -  :ref:`if<command-if>`                           
     -  :ref:`include<command-include>`             
     -  :ref:`jump<command-jump>`                         
     -  :ref:`label<command-label>`                   
   * -  :ref:`log<command-log>`                       
     -  :ref:`mixture<command-mixture>`           
     -  :ref:`move_surf<command-move-surf>`             
     -  :ref:`next<command-next>`                   
     -  :ref:`package<command-package>`                   
     -  :ref:`partition<command-partition>`           
   * -  :ref:`print<command-print>`                   
     -  :ref:`quit<command-quit>`                 
     -  :ref:`react<command-react>`                     
     -  :ref:`react_modify<command-react-modify>`   
     -  :ref:`read_grid<command-read-grid>`               
     -  :ref:`read_isurf<command-read-isurf>`         
   * -  :ref:`read_particles<command-read-particles>` 
     -  :ref:`read_restart<command-read-restart>` 
     -  :ref:`read_surf<command-read-surf>`             
     -  :ref:`region<command-region>`               
     -  :ref:`remove_surf<command-remove-surf>`           
     -  :ref:`reset_timestep<command-reset-timestep>` 
   * -  :ref:`restart<command-restart>`               
     -  :ref:`run<command-run>`                   
     -  :ref:`scale_particles<command-scale-particles>` 
     -  :ref:`seed<command-seed>`                   
     -  :ref:`shell<command-shell>`                       
     -  :ref:`species<command-species>`               
   * -  :ref:`stats<command-stats>`                   
     -  :ref:`stats_modify<command-stats-modify>` 
     -  :ref:`stats_style<command-stats-style>`         
     -  :ref:`suffix<command-suffix>`               
     -  :ref:`surf_collide<command-surf-collide>`         
     -  :ref:`surf_react<command-surf-react>`         
   * -  :ref:`surf_modify<command-surf-modify>`       
     -  :ref:`timestep<command-timestep>`         
     -  :ref:`uncompute<command-uncompute>`             
     -  :ref:`undump<command-undump>`               
     -  :ref:`unfix<command-unfix>`                       
     -  :ref:`units<command-units>`                   
   * -  :ref:`variable<command-variable>`             
     -  :ref:`write_grid<command-write-grid>`     
     -  :ref:`write_isurf<command-write-isurf>`         
     -  :ref:`write_restart<command-write-restart>` 
     -  :ref:`write_surf<command-write-surf>`             
     -



.. _commands-fix-styles:


Fix styles
==========



See the :ref:`command-fix` for one-line descriptions of each
style or click on the style itself for a full description. Some of the
styles have accelerated versions, which can be used if SPARTA is built
with the :ref:`appropriate accelerated package<accelerate>`.
This is indicated by additional letters in parenthesis: k = KOKKOS.

.. list-table:: 
   :header-rows: 0

   * - :ref:`ablate<command-fix-ablate>`
     - :ref:`adapt (k)<command-fix-adapt>`
     - :ref:`ambipolar<command-fix-ambipolar>`
     - :ref:`ave/grid (k)<command-fix-ave-grid>`
     - :ref:`ave/histo (k)<command-fix-ave-histo>`
     - :ref:`ave/histo/weight (k)<command-fix-ave-histo>`
   * - :ref:`ave/surf<command-fix-ave-surf>`
     - :ref:`ave/time<command-fix-ave-time>`
     - :ref:`balance (k)<command-fix-balance>`
     - :ref:`emit/face (k)<command-fix-emit-face>`
     - :ref:`emit/face/file<command-fix-emit-face-file>`
     - :ref:`emit/surf<command-fix-emit-surf>`
   * - :ref:`grid/check (k)<command-fix-grid-check>`
     - :ref:`move/surf (k)<command-fix-move-surf>`
     - :ref:`print<command-print>`
     - :ref:`vibmode<command-fix-vibmode>`
     -
     -



.. _commands-compute-styles:


Compute styles
==============



See the :ref:`command-compute` for one-line descriptions of
each style or click on the style itself for a full description. Some of
the styles have accelerated versions, which can be used if SPARTA is
built with the :ref:`appropriate accelerated package<accelerate>`. This is indicated by additional letters in parenthesis: k = KOKKOS.

.. list-table:: 
   :header-rows: 0
   
   * - :ref:`boundary (k)<command-compute-boundary>` 
     - :ref:`count (k)<command-compute-count>` 
     - :ref:`distsurf/grid<command-compute-distsurf-grid>` 
     - :ref:`eflux/grid (k)<command-compute-eflux-grid>` 
     - :ref:`fft/grid<command-compute-fft-grid>` 
     - :ref:`grid (k)<command-compute-grid>`
   * - :ref:`isurf/grid<command-compute-isurf-grid>`
     - :ref:`ke/particle (k)<command-compute-ke-particle>` 
     - :ref:`lambda/grid (k)<command-compute-lambda-grid>` 
     - :ref:`pflux/grid (k)<command-compute-pflux-grid>` 
     - :ref:`property/grid<command-compute-property-grid>` 
     - :ref:`react/boundary<command-compute-react-boundary>` 
   * - :ref:`react/surf<command-compute-react-surf>` 
     - :ref:`react/isurf/grid<command-compute-react-isurf-grid>` 
     - :ref:`reduce<command-compute-reduce>` 
     - :ref:`sonine/grid (k)<command-compute-sonine-grid>` 
     - :ref:`surf (k)<command-compute-surf>` 
     - :ref:`thermal/grid (k)<command-compute-thermal-grid>` 
   * - :ref:`temp (k)<command-compute-temp>` 
     - :ref:`tvib/grid<command-compute-tvib-grid>` 
     - 
     - 
     -
     -



.. _commands-collide-styles:


Collide styles
==============



See the :ref:`command-collide` for details of each style.
Some of the styles have accelerated versions, which can be used if
SPARTA is built with the :ref:`appropriate accelerated package<accelerate>`. This is indicated by additional letters in parenthesis: k = KOKKOS.

.. list-table:: 
   :header-rows: 0
   
   * - :ref:`vss (k)<command-collide>`



.. _commands-surface-collide:


Surface collide styles
======================



See the :ref:`command-surf-collide` for details of each style. Some of the
styles have accelerated versions, which can be used if SPARTA is built
with the :ref:`appropriate accelerated package<accelerate>`.  This
is indicated by additional letters in parenthesis: k = KOKKOS.


.. list-table:: 
   :header-rows: 0
   
   * - :ref:`cll<command-surf-collide>`
     - :ref:`diffuse (k)<command-surf-collide>`
     - :ref:`impulsive<command-surf-collide>`
   * - :ref:`piston (k)<command-surf-collide>`
     - :ref:`specular (k)<command-surf-collide>`
     - :ref:`td<command-surf-collide>`
   * - :ref:`vanish (k)<command-surf-collide>`
     -
     -



.. _commands-surface-reaction:


Surface reaction styles
=======================



See the :ref:`command-surf-react` for details of each
style.

.. list-table:: 
   :header-rows: 0
   
   * - :ref:`global<command-global>`
     - :ref:`prob<command-surf-react>`


