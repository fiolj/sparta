
:orphan:



.. index:: fix_dt_reset



.. _fix-dt-reset:




.. _fix-dt-reset-command:



####################
fix dt/reset command
####################




.. _fix-dt-reset-syntax:



*******
Syntax:
*******





::



   fix ID dt/reset Nfreq step weight resetflag




- ID is documented in :ref:`fix<fix>` command 



- dt/reset = style name of this fix command



- Nfreq = perform timestep calculation every this many steps



- step = compute or fix column for per-grid cell timestep, prefaced by "c\_" or "f\_"



- weight = weight (0.0 to 1.0) applied to average per-cell timestep when calculating global timestep



- resetflag = 1 to overwrite global timestep with new timestep, 0 to just calculate new timestep







.. _fix-dt-reset-examples:



*********
Examples:
*********





::



   compute 1 grid all mymixture nrho temp usq vsq wsq
   fix 1 ave/grid all 10 50 500 c_1\[\*\]
   compute lambda lambda/grid f_1\[1\] f_1\[2\] Ar
   compute tstep dt/grid all 0.25 0.1 c_lambda f_1\[2\] f_1\[3\] f_1\[4\] f_1\[5\]





::



   fix 2 dt/reset 500 c_tstep 0.1 1




.. _fix-dt-reset-descriptio:



************
Description:
************




Calculate a new global timestep for the simulation based on per grid
cell timesteps calculated by a compute or fix.  The new global
timestep can be output by the :ref:`stats_style<stats-style>` command.
Or it can be used to overwrite the current global timestep for a
variable time simulation.  See this
:ref:`section<howto-custom-perparticl-pergrid,-persurf>` of the manual for more
information on variable timestep simulations.



The *Nfreq* argument specifies how often the global timestep is calculated.



The *step* argument specifies a compute which calculates a per grid
cell timestep.  Or it specifies a fix which time averages a per grid
cell timestep.  Currently the only compute that calculates a per grid
cell timestep is :ref:`compute dt/grid<compute-dt-grid>`.  The :ref:`fix ave/grid<fix-ave-grid>` command could perform a time average of
the compute.



This is done by specifying the *step* argument like this:



c_ID = compute with ID that calculates a per grid cell timestep as a vector output
c_ID\[m\] = compute with ID that calculates a timestep as its Mth column of array output
f_ID\[m\] = fix with ID that calculates a time-averaged timestep as a vector output
f_ID\[m\] = fix with ID that calculates a time-averaged timestep as its Mth column of array output




.. important::

  If the ID of a :ref:`fix ave/grid<fix-ave-grid>`
  command is used as the *step* argument, it only produces output on
  timesteps that are multiples of its *Nfreq* argument.  Thus this fix
  can only be invoked on those timesteps.


.. note::

  that some of the per-cell timesteps may be zero for a number of reasons.  First,
  the data used to calculate the timestep, such as maximum most probable speed and mean
  free path, may be sufficiently close to zero.  Also, some cells may not contain particles,
  either due to their type or to local flow conditions.  For example, split cells
  (in which sub cells store the particles) and cells interior to surface objects do not
  store particles.  See :ref:`Section 6.8<howto-details-grid-geometry-sparta>` of the manual for
  details of how SPARTA defines child, unsplit, split, and sub cells.


From the per-cell timesteps, 3 values are extracted by this fix.  They
are the minimum positive timestep (DTmin) for all cells, the maximum positive timestep
(DTmax) for all cells, and the average positive timestep (DTave) over all
cells.  Cells with a timestep value of zero are not included in the mininum,
maximum, and average timestep calculations.



A new global timestep is than calculated by this formula, using
the specified *weight* argument:




::



   DTnew = (1-weight)\*DTmin + weight\*DTave




If the *resetflag* argument is specified as 1, then the global
timestep for the simulation, initially specified by the
:ref:`timestep<timestep>` command, is overwritten with the new DTnew
value.  If *resetflag* is 0, then the global timestep is not changed.






.. _fix-dt-reset-restart,-output:



*********************
Restart, output info:
*********************




No information about this fix is written to :ref:`binary restart files<restart>`.



This fix computes a global scalar which is the new global timestep
(DTnew above) after the most recent timestep re-calculation.  This
value is accessible to other commands whether or not the global
timestep is overwritten with the new value.



It also computes a global vector of length 3 with these values:



= DTmin
= DTmax
= DTave




.. _fix-dt-reset-related-commands:



*****************
Related commands:
*****************




:ref:`compute dt/grid<compute-dt-grid>`



.. _fix-dt-reset-default:



********
Default:
********




none



