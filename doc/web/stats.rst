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
:ref:`stats_style<command-stats-style>` and
:ref:`stats_modify<command-stats-modify>` commands.

The timesteps on which statistical output is written can also be
controlled by a :ref:`variable<command-variable>`. See the :ref:`stats_modify every<command-stats-modify>` command.

**Restrictions:** none

**Related commands:**

:ref:`command-stats-style`,
:ref:`command-stats-modify`

**Default:**

::

   stats 0 
