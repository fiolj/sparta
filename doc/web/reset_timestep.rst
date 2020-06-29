:orphan:

.. index:: reset_timestep



.. _command-reset-timestep:

######################
reset_timestep command
######################


*******
Syntax:
*******

::

   reset_timestep N 

-  N = timestep number

*********
Examples:
*********

::

   reset_timestep 0
   reset_timestep 4000000 

************
Description:
************

Set the timestep counter to the specified value. This command normally
comes after the timestep has been set by reading a restart file via the
:ref:`read_restart<command-read-restart>` command, or a previous simulation
advanced the timestep.

The :ref:`create_box<command-create-box>` command sets the timestep to 0; the
:ref:`read_restart<command-read-restart>` command sets the timestep to the
value it had when the restart file was written.

*************
Restrictions:
*************
 none

This command cannot be used when any fixes are defined that keep track
of elapsed time to perform certain kinds of time-dependent operations.
Examples are the :ref:`fix ave/time<command-fix-ave-time>`, :ref:`fix ave/grid<command-fix-ave-grid>`, and :ref:`fix ave/surf<command-fix-ave-surf>` commands. Thus these fixes should be
specified after the timestep has been reset.

Resetting the timestep clears flags for :ref:`computes<command-compute>` that
may have calculated some quantity from a previous run. This means these
quantity cannot be accessed by a variable in between runs until a new
run is performed. See the :ref:`variable<command-variable>` command for more
details.

*****************
Related commands:
***************** none

********
Default:
********
 none
