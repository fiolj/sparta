:orphan:

.. index:: surf_modify



.. _command-surf-modify:

###################
surf_modify command
###################


*******
Syntax:
*******

::

   surf_modify group-ID keyword args ... 

group-ID = ID of the surface group to operate on

-  one or more keyword/arg pairs may be listed
-  keyword = *collide* or (react)

   collide arg = sc-ID
     sc-ID = ID of a surface collision model
   react arg = sr-ID
     sr-ID = ID of a surface reaction model or none 

*********
Examples:
*********

::

   surf_modify sphere collide 1
   surf_modify all collide sphere react sphere 

************
Description:
************

Set parameters for a group of surface elements in the specified group-ID. Surface elements are read in by the :ref:`read_surf<command-read-surf>` command. They can be assigned to groups by that command or via the :ref:`group<command-group>` command.

The *collide* keyword
  is used to assign a surface collision model.  Surface collision models are defined by the :ref:`surf_collide<command-surf-collide>` command, which assigns each a surface collision ID, specified here as *sc-ID*.

  The effect of this keyword is that particle collisions with surface elements in group-ID will be computed by the surface collision model with *sc-ID*.

The *react* keyword
  is used to assign a surface reaction model. Surface reaction models are defined by the :ref:`surf_react<command-surf-react>` command, which assigns each a surface reaction ID, specified here as *sr-ID* or the word "none". The latter means no reaction model.

The effect of this keyword
  is that particle collisions with surface elements in group-ID will induce reactions which are computed by the surface reaction model with *sr-ID*. If "none" is used, no surface reactions occur.

.. note::  If the same surface element is assigned to multiple groups, using this command multiple times may override the effect of a previous command that assigned a different collision or reaction model to a particular surface element.

*************
Restrictions:
*************


All surface elements must be assigned to a surface collision model via
the *collide* keyword before a simlulation can be performed. Using a
surface reaction model is optional.

This command cannot be used before surfaces exist.

*****************
Related commands:
*****************

:ref:`command-read-surf`,
:ref:`command-bound-modify`

********
Default:
********

The default for surface reactions is none.
