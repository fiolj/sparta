
:orphan:



.. index:: compute_react_isurf_grid



.. _compute-react-isurf-grid:




.. _compute-react-isurf-grid-command:



################################
compute react/isurf/grid command
################################




.. _compute-react-isurf-grid-syntax:



*******
Syntax:
*******





::



   compute ID react/isurf/grid group-ID reaction-ID value1 value2 ...




- ID is documented in :ref:`compute<compute>` command 



- react/isurf/grid = style name of this compute command



- group-ID = group ID for which grid cells to perform calculation on



- reaction-ID = ID of surface reaction model which defines surface reactions



- zero or more values can be appended



- value = *r:s1/s2/s3 ...* or *p:s1/s2/s3 ...*




::



   r: or p: = list of reactant species or product species
   s1,s2,s3 = one or more species IDs, separated by "/" character








.. _compute-react-isurf-grid-examples:



*********
Examples:
*********





::



   surf_react air prob air.surf
   compute 1 react/isurf/grid all air
   compute 2 react/isurf/grid all air r:N/O/N2/O2 p:N/O/NO




These commands will dump time averages for each grid cell to a dump
file every 1000 steps:




::



   compute 2 react/isurf/grid all air r:N/O/N2/O2 p:N/O/NO
   fix 1 ave/grid all 10 100 1000 c_2\[\*\]
   dump 1 grid all 1000 tmp.surgrid id f_1\[\*\]




.. _compute-react-isurf-grid-descriptio:



************
Description:
************




Define a computation that tallies counts of reactions for each grid
cell containing implicit surface elements, based on the particles that
collide with those elements.  Only grid cells in the grid group
specified by *group-ID* are included in the tallying.  See the :ref:`group grid<group>` command for info on how grid cells can be assigned to
grid groups.  Likewise only grid cells with surface elements assigned
to the surface reaction model specified by *reaction-ID* are included
in the tallying.  This assignment is done via the
:ref:`surf_modify<surf-modify>` command.



Implicit surface elements are triangles for 3d simulations and line
segments for 2d simulations.  Unlike explicit surface elements, each
triangle or line segment is wholly contained within a single grid
cell.  See the :ref:`read_isurf<read-isurf>` command for details.



This command can only be used for simulations with implicit surface
elements.  See the similar :ref:`compute react/surf<compute-react-surf>` command for use with simulations
with explicit surface elements.



.. note::

  that when a particle collides with a surface element, it can
  bounce off (possibly as a different species), be captured by the
  surface (vanish), or a 2nd particle can also be emitted.


The doc page for the :ref:`surf_react<surf-react>` command explains the
different reactions that can occur for each specified style.



If no values are specified each reaction specified by the
:ref:`surf_react<surf-react>` style is tallied individually for each
grid cell.



.. note::

  that these rules mean
  that a single reaction may be tallied multiple times depending on
  which values it matches.


The results of this compute can be used by different commands in
different ways.  The values for a single timestep can be output by the
:ref:`dump grid<dump>` command.



The values over many sampling timesteps can be averaged by the :ref:`fix ave/grid<fix-ave-grid>` command.






.. _compute-react-isurf-grid-output:



************
Output info:
************




This compute calculates a per-grid array, with the number of columns
either equal to the number of reactions defined by the
:ref:`surf_react<surf-react>` style (if no values are specified) or equal to
M = the # of values specified.



Grid cells not in the specified *group-ID* or whose implicit surfaces
are not assigned to the specified *reaction-ID* will output zeroes for
all their values.



The array can be accessed by any command that uses per-grid values
from a compute as input.  See :ref:`Section 6.4<howto-output-sparta-(stats,-dumps,>`
for an overview of SPARTA output options.



The per-grid array values are counts of the number of reactions that
occurred on surface elements in that grid cell.






.. _compute-react-isurf-grid-restrictio:



*************
Restrictions:
*************




none



.. _compute-react-isurf-grid-related:



*****************
Related commands:
*****************




:ref:`fix ave/grid<fix-ave-grid>`, :ref:`dump grid<dump>`, :ref:`compute react/surf<compute-react-surf>`



.. _compute-react-isurf-grid-default:



********
Default:
********




none



