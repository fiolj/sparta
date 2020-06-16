:orphan:

.. index:: move_surf

.. _command-move-surf:

#################
move_surf command
#################

**Syntax:**

::

   move_surf groupID style args ... keyword value ... 

-  group-ID = group ID for which surface elements to move
-  style = *file* or *trans* or *rotate*

   ::

        file args = filename entry
        trans args = Dx Dy Dz
          Dx,Dy,Dz = displacement applied to all surface points (distance units)
        rotate args = theta Rx Ry Rz Ox Oy Oz 
          theta = rotate surface points by this angle in counter-clockwise direction (degrees)
          Rx,Ry,Rz = rotate around vector starting at origin pointing in this direction
          Ox,Oy,Oz = origin to rotate around (distance units) 

-  zero or more keyword/value pairs may be appended
-  keyword = *connect*

   ::

        connect arg = yes or no 

**Examples:**

::

   move_surf all trans 1 0 0
   move_surf partial rotate 360 0 0 1 5 5 0 connect yes
   move_surf object2 rotate 360 0 0 1 5 5 0 

**Description:**

This command performs a one-time movement of all the surface elements in the specified group via the specified style. See the :ref:`group surf <command-group>` command for info on how surface elements can be assigned to surface groups.

This command can be invoked as many times as desired, before or between simulation runs. Surface points can also be moved on-the-fly during a simulation by using the :ref:`command-fix-move-surf`.

Moving surfaces between simulations can be useful if you want to perform a series of runs from one input script, where some attribute of the surface elements change, e.g. the separation between two spheres.

.. important:: The *file* style is not yet implemented.
	       It will allow new positions of points to be listed in a file.

In 2d, surface elements are line segments with 2 vertices each. In 3d,
surface elements are triangles with 3 vertices each. If a line segment
or triangle belongs to the specified group, all of its vertices are
moved. This effectively moves the entire surface element.

.. important:: Unless a vertex is on the simulation box boundary, it will be part of two surface elements (in 2d) or multiple surface elements (in 3d).
	       If you choose a surface groupID which does not include all the elements in a gridded object, then you cannot move them without breaking apart the object in a "watertight" sense (so that particles could erroneously move inside the object).
	       To prevent this use the optional *connect* keyword with its *yes* setting. This will insure that multiple copies of the same vertex in other elements (not in the surface group) will also be moved. This is a way to morph the shape of a gridded object, e.g. make a sphere more oblate, by moving only a portion of its elements.

The *trans* style shifts or displaces each vertex by the vector (Dx,Dy,Dz).

The *rotate* style rotates the coordinates of all vertices by an angle *theta* in a counter-clockwise direction, around the vector starting at (Ox,Oy,Oz) and pointing in the direction *Rx,Ry,Rz*. Any desired rotation can be represented by an appropriate choice of (Ox,Oy,Oz), *theta*, and (Rx,Ry,Rz).

After the surface has been moved, then all particles in grid cells that meet either of these criteria are deleted:

- the grid cell is now inside a surface
- the grid cell overlaps with a surface element that moved

This is to prevent particles from ending up inside surface objects.

Note that in this context, "overlaps" means that any part of the surface element touches any part of the grid cell, including its surface. Also note that if a surface element object (e.g. a sphere) moved a long distance then grid cells that were inside the object in its old position and thus contained no particles, will still have no particles immediately after the move. This will effectively leave a "void" in the flow until particles re-fill the grid cells that are now outside the object.

**Restrictions:**

An error will be generated if any surface element vertex is moved
outside the simulation box.

**Related commands:**

:ref:`command-read-surf`,
:ref:`command-fix-move-surf`
:ref:`command-remove-surf`

**Default:**

The option default is connect = no.
