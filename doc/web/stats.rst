:orphan:

.. index:: stats

.. _command-stats:

#############
stats command
#############

**Syntax:**

::

   stats N 

-  N = output statistics every N timesteps

**Examples:**

::

   stats 100 

**Description:**

Compute and print statistical info (e.g. particle count, temperature) on
timesteps that are a multiple of N and at the beginning and end of a
simulation run. A value of 0 will only print statistics at the beginning
and end.

The content and format of what is printed is controlled by the
`stats_style <stats_style.html>`__ and
`stats_modify <stats_modify.html>`__ commands.

The timesteps on which statistical output is written can also be
controlled by a `variable <variable.html>`__. See the `stats_modify
every <stats_modify.html>`__ command.

**Restrictions:** none

**Related commands:**

:ref:`command-stats-style`,
:ref:`command-stats-modify`

**Default:**

::

   stats 0 
