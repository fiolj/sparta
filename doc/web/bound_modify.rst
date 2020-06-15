:orphan:

.. _command-bound-modify:

####################
bound_modify command
####################

**Syntax:**

::

   bound_modify wall1 wall2 ... keyword value ... 

-  wall1,wall2,... = *xlo* or *xhi* or *ylo* or *yhi* or *zlo* or *zhi*
-  one or more keyword/value pairs may be listed

   ::

      keywords = collide or react
        collide value = sc-ID
          sc-ID = ID of a surface collision model
        react value = sr-ID
          sr-ID = ID of a surface reaction model or none 

**Examples:**

::

   bound_modify yhi collide 1 react 2
   bound_modify zlo zhi collide hotwall 

**Description:**

Set parameters for one or more of the boundaries of the global
simulation box. Any of the 6 faces can be selected via the list of
*wall* settings.

The *collide* keyword can only be used when the boundary is of type "s",
for surface, as set by the `boundary <boundary.html>`__ command. This
keyword assigns a surface collision model to the boundary, as defined by
the `surf_collide <surf_collide.html>`__ command. The ID of the surface
collision model is specified as *sc-ID*, which is the ID used in the
`surf_collide <surf_collide.html>`__ command.

The effect of this keyword is that particle collisions with the
specified boundaries will be computed by the specified surface collision
model.

The *react* keyword can only be used when the boundary is of type "s",
for surface, as set by the `boundary <boundary.html>`__ command. This
keyword assigns a surface reaction model to the boundary, as defined by
the `surf_react <surf_react.html>`__ command. The ID of the surface
reaction model is specified as *sr-ID*, which is the ID used in the
`surf_react <surf_react.html>`__ command. If an sr-ID of *none* is used
then surface reactions are turned off.

The effect of this keyword is that particle collisions with the
specified boundaries will induce reactions which are computed by the
specified surface reaction model.

**Restrictions:**

For 2d simulations, the *zlo* and *zhi* boundaries cannot be modified by
this command, since they are always periodic.

All boundaries of type "s" must be assigned to a surface collision model
via the *collide* keyword before a simlulation can be performed. Using a
surface reaction model is optional.

**Related commands:**

:ref:`command-boundary`
:ref:`command-surf-modify`

**Default:**

The default for boundary reactions is none.
