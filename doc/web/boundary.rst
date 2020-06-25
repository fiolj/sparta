:orphan:

.. index:: boundary



.. _command-boundary:

################
boundary command
################


**Syntax:**

::

   boundary x y z 

-  x,y,z = *o* or *p* or *r* or *a* or *s*, one or two letters

   ::

        o is outflow
        p is periodic
        r is specular reflection
        a is axi-symmetric
        s is treat boundary as a surface 

**Examples:**

::

   boundary o p p
   boundary os o o
   boundary r p rs 

**Description:**

Set the style of boundaries for the global simulation box in each of the
x, y, z dimensions. A single letter assigns the same style to both the
lower and upper face of the box in that dimension. Two letters assigns
the first style to the lower face and the second style to the upper
face. The size of the simulation box is set by the
:ref:`create_box<command-create-box>` command.

The boundary style determines how particles exiting the box are handled.

Style *o* means an outflow boundary, so that particles freely exit the
simulation.

Style *p* means the box is periodic, so that particles exit one end of
the box and re-enter the other end. The *p* style must be applied to
both faces of a dimension.

Style *r* means a specularly reflecting boundary. Particles that cross
this boundary have their velocity reversed so as to re-enter the box.
The new velocity is used to advect the particle for the reminder of the
timestep following the collision.

Style *a* means an axi-symmetric boundary, which can only be used for
the lower y-dimension boundary in a 2d simulation. The simulation box
must also have a value of 0.0 for *ylo*; see the
:ref:`create_box<command-create-box>` command. This effectively means that
the x-axis is the axis of symmetry. The upper y-dimension boundary
cannot be periodic.

Style *s* means the boundary is treated as a surface which allows the
particle-surface interaction to be treated in a variety of ways via the
options provided by the :ref:`surf_collide<command-surf-collide>` command.
This is effectively the same as when a particle collides with a
triangulated surface read in and setup by the
:ref:`read_surf<command-read-surf>` command.

For style *s*, the boundary face must also be assigned to a surface
collision model defined by the :ref:`surf_collide<command-surf-collide>`
command. The assignment of the boundary to the model is done via the
:ref:`bound_modify<command-bound-modify>` command.

**Restrictions:**

This command must be used before the grid is defined, e.g. by a
:ref:`create_grid<command-create-grid>` command.

For 2d simulations, the z dimension must be periodic.

**Related commands:**

:ref:`command-bound-modify`
:ref:`command-surf-collide`

**Default:**

::

   boundary p p p 
