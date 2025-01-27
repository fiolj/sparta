
:orphan:

.. index:: surf_modify

.. _surf-modify:

.. _surf-modify-command:

###################
surf_modify command
###################

.. _surf-modify-syntax:

*******
Syntax:
*******

::

   surf_modify group-ID keyword args ...

- group-ID = ID of the surface group to operate on

- one or more keyword/arg pairs may be listed 

- keyword = *collide* or (react)

::

     *collide* arg = sc-ID
       sc-ID = ID of a surface collision model
     *react* arg = sr-ID
       sr-ID = ID of a surface reaction model or *none*

.. _surf-modify-examples:

*********
Examples:
*********

::

   surf_modify sphere collide 1
   surf_modify all collide sphere react sphere

.. _surf-modify-descriptio:

************
Description:
************

Set parameters for a group of surface elements in the specified
group-ID.  Surface elements are read in by the
:ref:`read_surf<read-surf>` command.  They can be assigned to groups by
that command or via the :ref:`group<group>` command.

The *collide* keyword is used to assign a surface collision model.
Surface collision models are defined by the
:ref:`surf_collide<surf-collide>` command, which assigns each a surface
collision ID, specified here as *sc-ID*.

The effect of this keyword is that particle collisions with surface
elements in group-ID will be computed by the surface collision model
with *sc-ID*.

The *react* keyword is used to assign a surface reaction model.
Surface reaction models are defined by the
:ref:`surf_react<surf-react>` command, which assigns each a surface
reaction ID, specified here as *sr-ID* or the word "none".  The latter
means no reaction model.

The effect of this keyword is that particle collisions with surface
elements in group-ID will induce reactions which are computed by the
surface reaction model with *sr-ID*.  If "none" is used, no surface
reactions occur.

.. note::

  that if the same surface element is assigned to multiple groups,
  using this command multiple times may override the effect of a
  previous command that assigned a different collision or reaction model
  to a particular surface element.

.. _surf-modify-restrictio:

*************
Restrictions:
*************

All surface elements must be assigned to a surface collision model via
the *collide* keyword before a simlulation can be performed.  Using a
surface reaction model is optional.

This command cannot be used before surfaces exist.

.. _surf-modify-related-commands:

*****************
Related commands:
*****************

:ref:`read_surf<read-surf>`, :ref:`bound_modify<bound-modify>`

.. _surf-modify-default:

********
Default:
********

The default for surface reactions is none.

