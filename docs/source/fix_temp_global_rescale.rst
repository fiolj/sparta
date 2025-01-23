
:orphan:

.. index:: fix_temp_global_rescale

.. _fix-temp-global-rescale:

.. _fix-temp-global-rescale-command:

###############################
fix temp/global/rescale command
###############################

.. _fix-temp-global-rescale-syntax:

*******
Syntax:
*******

::

   fix ID temp/global/rescale N Tstart Tstop fraction

   - ID is documented in :ref:`fix<fix>` command
   - temp/global/rescale = style name of this fix command
   - N = thermostat every N timesteps
   - Tstart,Tstop = desired temperature at start/end of run (temperature units)
   - fraction = rescale to target temperature by this fraction

.. _fix-temp-global-rescale-examples:

*********
Examples:
*********

::

   fix 1 temp/global/rescale 100 300.0 300.0 0.5
   fix 5 temp/global/rescale 10 300.0 10.0 1.0

.. _fix-temp-global-rescale-descriptio:

************
Description:
************

Reset the temperature of all the particles in the entire simulation by
explicitly rescaling their velocities.  This is a simple
thermostatting operation to keep the temperature of the gas near the
desired target temperature.  This can be useful if an external driving
force is adding energy to the system.  Or if you wish the heat or cool
the temperature of the system over time.

The rescaling is applied to only the translational degrees of freedom
for the particles.  Their rotational or vibrational degrees of freedom
are not altered.

Rescaling is performed every N timesteps. The target temperature is a
ramped value between the Tstart and Tstop temperatures at the
beginning and end of the run.

From the current global temperature and the current target
temperature, a velocity scale factor is calculated.  The amount of
rescaling that is applied is adjusted by the *fraction* parameter
which is a value from 0.0 to 1.0.  difference between the actual and
desired temperature.  If *fraction* = 1.0, the temperature is reset to
exactly the desired value.  If *fraction* = 0.5, the temperature is
reset to a value halfway between the current global and target
temperatures.

The rescaling factor is applied to each of the components of the
translational velocity for every particle in the simulation.

.. note::

  that this fix performs thermostatting using the same formula for
  temperature as calculated by the :ref:`compute temp<compute-temp>`
  command.  It does not currently subtract out a net streaming velocity
  to measure a thermal temperature since it assumes the net center of
  mass velocity for the entire system is zero.  An option for this may
  be added in the future.  See the :ref:`fix   temp/rescale<fix-temp-rescale>` doc page for a command that
  thermostats the thermal temperature on a per-grid-cell basis.

.. _fix-temp-global-rescale-restart,:

*********************
Restart, output info:
*********************

No information about this fix is written to :ref:`binary restart files<restart>`.

This fix produces no output.

This fix can ramp its target temperature over multiple runs, using the
start and stop keywords of the run command. See the run command for
details of how to do this.

.. _fix-temp-global-rescale-restrictio:

*************
Restrictions:
*************

none

.. _fix-temp-global-rescale-related:

*****************
Related commands:
*****************

:ref:`fix temp/rescale<fix-temp-rescale>`

.. _fix-temp-global-rescale-default:

********
Default:
********

none

