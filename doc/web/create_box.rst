:orphan:

.. _command-create-box:

##################
create_box command
##################

**Syntax:**

::

   create_box xlo xhi ylo yhi zlo zhi 

::

   xlo,xhi = box bounds in the x dimension (distance units)
   ylo,yhi = box bounds in the y dimension (distance units)
   zlo,zhi = box bounds in the z dimension (distance units) 

**Examples:**

::

   create_box 0 1 0 1 0 1
   create_box 0 1 0 1 -0.5 0.5
   create_box 0 10.0 0 5.0 -4.0 0.0 

**Description:**

Set the size of the simulation box.

For a 2d simulation, as specifed by the `dimension <dimension.html>`__
command, *zlo* < 0.0 and *zhi* > 0.0 is required. This means the z
dimensions straddle 0.0. Typical values are -0.5 and 0.5, but this is
not required. See `Section 6.1 <Section_howto.html#howto_1>`__ of the
manual for more information about 2d simulations.

For 2d axisymmetric simulations, as set by the
`dimension <dimension.html>`__ and `boundary <boundary.html>`__
commands, the ylo setting must be 0.0. See `Section
6.2 <Section_howto.html#howto_2>`__ of the manual for more information
about axisymmetric simulations.

**Restrictions:** none

**Related commands:** none

**Default:** none
