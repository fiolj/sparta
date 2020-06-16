:orphan:

.. index:: dimension

.. _command-dimension:

#################
dimension command
#################

**Syntax:**

::

   dimension N 

-  N = 2 or 3

**Examples:**

::

   dimension 2
   dimension 3 

**Description:**

Set the dimensionality of the simulation. By default SPARTA runs 3d
simulations, but 2d simulations can also be run.

2d axi-symmetric models can be run by setting the dimension to 2, and
defining the lower boundary in the y-dimension to axi-symmetric via the
`boundary <boundary.html>`__ command.

**Restrictions:**

This command must be used before the simulation box is defined by a
`create_box <create_box.html>`__ command.

**Related commands:** none

**Default:**

::

   dimension 3 
