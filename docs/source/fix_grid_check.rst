
:orphan:



.. index:: fix_grid_check



.. _fix-grid-check:




.. _fix-grid-check-command:



######################
fix grid/check command
######################




.. _fix-grid-check-kk-command:



#########################
fix grid/check/kk command
#########################




.. _fix-grid-check-syntax:



*******
Syntax:
*******





::



   fix ID grid/check N outflag keyword arg ...




- ID is documented in :ref:`fix<fix>` command 



- grid/check = style name of this fix command



- N = check every N timesteps



- outflag = *error* or *warn* or *silent*



- zero or more keyword/args pairs may be appended



- keyword = *outside*




::



   outside arg = *yes* or *no*








.. _fix-grid-check-examples:



*********
Examples:
*********





::



   fix 1 grid/check 100 error




.. _fix-grid-check-descriptio:



************
Description:
************




Check if particles are inside the grid cell they are supposed to be,
based on their current coordinates.  This is useful as a debugging
check to insure that no particles have been assigned to the incorrect
grid cell during the particle move stage of the SPARTA timestepping
algorithm.



The check is performed once every *N* timesteps.  Particles not inside
the correct grid cell are counted and the value of the count can be
monitored (see below).  A value of 0 is "correct", meaning that no
particle was found outside its assigned grid cell.



If the *outside* keyword is set to *yes*, then a check for particles
inside explicit or implicit surfaces is also performed.  If a particle
is in a grid cell with surface elements and the particle is "inside"
the surfaces, then the error count is incremented.



If the outflag setting is *error*, SPARTA will print an error and stop
if it finds a particle in an incorrect grid cell or inside the surface
elements.  For *warn*, it will print a warning message and continue.
For *silent*, it will print no message, but the count of such
occurrences can be monitored as described below, e.g. by outputting
the value with the :ref:`stats<stats>` command.



.. important::

  Use of *outside yes* can be expensive if the check is
  performed frequently (e.g. every step).





.. _fix-grid-check-restart,-output:



*********************
Restart, output info:
*********************




No information about this fix is written to :ref:`binary restart files<restart>`.



This fix computes a global scalar which can be accessed by various
output commands.  The scalar is the count of how many particles were
not in the correct grid cell.  The count is cummulative over all the
timesteps the check was performed since the start of the run.  It is
initialized to zero each time a run is performed.






Styles with a *kk* suffix are functionally the same as the
corresponding style without the suffix.  They have been optimized to
run faster, depending on your available hardware, as discussed in the
:ref:`Accelerating SPARTA<accelerate>` section of the manual.
The accelerated styles take the same arguments and should produce the
same results, except for different random number, round-off and
precision issues.



These accelerated styles are part of the KOKKOS package. They are only
enabled if SPARTA was built with that package.  See the :ref:`Making SPARTA<start-making-sparta-optional-packages>` section for more info.



You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the :ref:`-suffix command-line switch<start-running-sparta>` when you invoke SPARTA, or you can
use the :ref:`suffix<suffix>` command in your input script.



See the :ref:`Accelerating SPARTA<accelerate>` section of the
manual for more instructions on how to use the accelerated styles
effectively.






.. _fix-grid-check-restrictio:



*************
Restrictions:
*************




none



.. _fix-grid-check-related-commands:



*****************
Related commands:
*****************




none



.. _fix-grid-check-default:



********
Default:
********




The option default is outside = no.



