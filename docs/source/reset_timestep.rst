
:orphan:

.. index:: reset_timestep

.. _reset-timestep:

.. _reset-timestep-command:

######################
reset_timestep command
######################

.. _reset-timestep-syntax:

*******
Syntax:
*******

::

   reset_timestep N

N = timestep number

.. _reset-timestep-examples:

*********
Examples:
*********

::

   reset_timestep 0
   reset_timestep 4000000

.. _reset-timestep-descriptio:

************
Description:
************

Set the timestep counter to the specified value.  This command
normally comes after the timestep has been set by reading a restart
file via the :ref:`read_restart<read-restart>` command, or a previous
simulation advanced the timestep.

The :ref:`create_box<create-box>` command sets the timestep to 0; the
:ref:`read_restart<read-restart>` command sets the timestep to the
value it had when the restart file was written.

.. _reset-timestep-restrictio:

*************
Restrictions:
*************

none

This command cannot be used when any fixes are defined that keep track
of elapsed time to perform certain kinds of time-dependent operations.
Examples are the :ref:`fix ave/time<fix-ave-time>`, :ref:`fix ave/grid<fix-ave-grid>`, and :ref:`fix ave/surf<fix-ave-surf>`
commands.  Thus these fixes should be specified after the timestep has
been reset.

Resetting the timestep clears flags for :ref:`computes<compute>` that
may have calculated some quantity from a previous run.  This means
these quantity cannot be accessed by a variable in between runs until
a new run is performed.  See the :ref:`variable<variable>` command for
more details.

.. _reset-timestep-related-commands:

*****************
Related commands:
*****************

none

.. _reset-timestep-default:

********
Default:
********

none

