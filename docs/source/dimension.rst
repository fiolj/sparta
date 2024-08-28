
:orphan:



.. index:: dimension



.. _dimension:




.. _dimension-command:



#################
dimension command
#################




.. _dimension-syntax:



*******
Syntax:
*******





::



   dimension N




N = 2 or 3




.. _dimension-examples:



*********
Examples:
*********





::



   dimension 2
   dimension 3




.. _dimension-descriptio:



************
Description:
************




Set the dimensionality of the simulation.  By default SPARTA runs 3d
simulations, but 2d simulations can also be run.



2d axi-symmetric models can be run by setting the dimension to 2, and
defining the lower boundary in the y-dimension to axi-symmetric via
the :ref:`boundary<boundary>` command.



.. _dimension-restrictio:



*************
Restrictions:
*************




This command must be used before the simulation box is defined by a
:ref:`create_box<create-box>` command.



.. _dimension-related-commands:



*****************
Related commands:
*****************




none



.. _dimension-default:



********
Default:
********





::



   dimension 3




