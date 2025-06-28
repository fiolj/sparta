
:orphan:

.. index:: compute_react_boundary

.. _compute-react-boundary:

.. _compute-react-boundary-command:

##############################
compute react/boundary command
##############################

.. _compute-react-boundary-syntax:

*******
Syntax:
*******

::

   compute ID react/boundary reaction-ID value1 value2 ...

- ID is documented in :ref:`compute<compute>` command 

- react/boundary = style name of this compute command

- reaction-ID = surface reaction ID which defines surface reactions

- zero or more values can be appended

- value = *r:s1/s2/s3 ...* or *p:s1/s2/s3 ...*

::

     r: or p: = list of reactant species or product species
     s1,s2,s3 = one or more species IDs, separated by "/" character

.. _compute-react-boundary-examples:

*********
Examples:
*********

::

   surf_react air prob air.surf
   compute 1 react/boundary air
   compute 2 react/boundary air r:N/O/N2/O2 p:N/O/NO

These commands will time average the reaction tallies for each face
and output the results as part of statistical output:

::

   compute 2 react/boundary air r:N/O/N2/O2 p:N/O/NO

::

   fix 1 ave/time all 10 100 1000 c_2\[\*\]
   stats_style step np f_1\[1\]\[\*\] f_1\[2\]\[\*\] f_1\[3\]\[\*\] f_1\[4\]\[\*\]

.. _compute-react-boundary-descriptio:

************
Description:
************

Define a computation that tallies counts of reactions for each
boundary (i.e. face) of the simulation box, based on the particles
that collide with the boundary.  Only faces assigned to the surface
reaction model specified by *reaction-ID* are included in the
tallying.

.. note::

  that when a particle collides with a face, it can bounce off
  (possibly as a different species), be captured by the surface
  (vanish), or a 2nd particle can also be emitted.

The doc page for the :ref:`surf_react<surf-react>` command explains the
different reactions that can occur for each specified style.

If no values are specified each reaction specified by the
:ref:`surf_react<surf-react>` style is tallied individually for each
boundary.

.. note::

  that these rules mean
  that a single reaction may be tallied multiple times depending on
  which values it matches.

The results of this compute can be used by different commands in
different ways.  The values for a single timestep can be output by the
:ref:`stats_style<stats-style>` command.  The values over many sampling
timesteps can be averaged by the :ref:`fix ave/time<fix-ave-time>`
command.

.. _compute-react-boundary-output-info:

************
Output info:
************

This compute calculates a global array, with the number of columns
either equal to the number of reactions defined by the
:ref:`surf_react<surf-react>` style (if no values are specified) or equal to
M = the # of values specified.  The number of rows is 4 for a 2d
simulation for the 4 faces (xlo, xhi, ylo, yhi), and it is 6 for a 3d
simulation (xlo, xhi, ylo, yhi, zlo, zhi).

The array can be accessed by any command that uses global array values
from a compute as input.  See :ref:`Section 6.4<howto-64-output-sparta-(stats,>`
for an overview of SPARTA output options.

The array values are counts of the number of reactions that occurred
on each face.

.. _compute-react-boundary-restrictio:

*************
Restrictions:
*************

none

.. _compute-react-boundary-related-commands:

*****************
Related commands:
*****************

:ref:`fix ave/time<fix-ave-time>`, :ref:`compute react/surf<compute-react-surf>`

.. _compute-react-boundary-default:

********
Default:
********

none

