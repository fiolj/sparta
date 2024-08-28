
:orphan:

.. index:: fix_move_surf

.. _fix-move-surf:

.. _fix-move-surf-command:

#####################
fix move/surf command
#####################

.. _fix-move-surf-kk-command:

########################
fix move/surf/kk command
########################

.. _fix-move-surf-syntax:

*******
Syntax:
*******

::

   fix ID move/surf groupID Nevery Nlarge args ...

ID is documented in :ref:`fix<fix>` command
move/surf = style name of this fix command
group-ID = group ID for which surface elements to move
Nevery = move surfaces incrementally every this many steps
Nlarge = move surfaces the entire distance after this many timesteps
args = all remaining args are identical to those defined for the :ref:`move_surf<move-surf>` command starting with its "style" argument

.. _fix-move-surf-examples:

*********
Examples:
*********

::

   fix 1 move/surf all 100 1000 trans 1 0 0
   fix 1 move/surf partial 100 10000 rotate 360 0 0 1 5 5 0 connect yes
   fix 1 move/surf object2 100 50000 rotate 360 0 0 1 5 5 0

.. _fix-move-surf-descriptio:

************
Description:
************

This command performs on-the-fly movement of all the surface elements
in the specfied group via one of several styles.  See the :ref:`group surf<group>` command for info on how surface elements can be
assigned to surface groups.  Surface element moves can also be
performed before or between simulations by using the
:ref:`move_surf<move-surf>` command.

Moving surfaces during a simulation run can be useful if you want to
to track transient changes in a flow while some attribute of the
surface elements change, e.g. the separation between two spheres.

All of the command arguments which appear after *Nlarge*, which
determine how surface elements move, are exactly the same as for the
:ref:`move_surf<move-surf>` command, starting with its *style*
argument.  This includes optional keywords it defines.  See its doc
page for details.

*Nevery* specifies how often surface elements are moved incrementally
along the path towards their final position.  The current timestep
must be a multiple of *Nevery*.

*Nlarge* must be a multiple of *Nevery* and specifies how long it will
take the surface elements to move to their final position.

Thus if *Nlarge* = 100\**Nevery*, each surface elements will move 1/100 of
its total distance every *Nevery* steps.

The same rules that the :ref:`move_surf<move-surf>` command follows for
particle deletion after surface elements move, are followed by this
command as well.  The criteria are applied after every incremental
move.  This is to prevent particles from ending up inside surface
objects.

Likewise, the *connect* option of the :ref:`move_surf<move-surf>`
command should be used in the same manner by this command if you
need to insure that moving only some elements of an object
do not result in a non-watertight surface grid.

.. _fix-move-surf-restart,-output:

*********************
Restart, output info:
*********************

No information about this fix is written to :ref:`binary restart files<restart>`.  No global or per-particle or per-grid quantities
are stored by this fix for access by various output commands.

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

.. _fix-move-surf-restrictio:

*************
Restrictions:
*************

An error will be generated if any surface element vertex is moved
outside the simulation box.

.. _fix-move-surf-related-commands:

*****************
Related commands:
*****************

:ref:`read_surf<read-surf>`, :ref:`move_surf<move-surf>`,
:ref:`remove_surf<remove-surf>`

.. _fix-move-surf-default:

********
Default:
********

none

