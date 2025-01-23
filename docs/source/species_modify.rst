
:orphan:

.. index:: species_modify

.. _species-modify:

.. _species-modify-command:

######################
species_modify command
######################

.. _species-modify-syntax:

*******
Syntax:
*******

::

   species_modify ID property value ...

- ID, property, value can be repeated one or more times

- ID = species ID

- property = *mu*

::

     mu = magnetic moment

- value = value of property for that species

::

     value for *mu* (magnetic moment units)

.. _species-modify-examples:

*********
Examples:
*********

::

   species_modify Fe mu 2.0 Cr mu 3.0

.. _species-modify-descriptio:

************
Description:
************

Set additional properties of one or more species used in a simulation.
This can be used as many times as desired for different species and
properties.  Currently it only supports setting of a single optional
property (the magnetic moment) which is not included in the species
files read in by the :ref:`species<species>` command.

Each *ID* is a character string used to identify a species, such as N
or O2 or NO or D or Fe-.  See the :ref:`species<species>` command for
how species are added to a simulation model by reading their
properties from a species file.

The only property currently recognized is *mu* or the scalar magnetic
moment of each particle of the species.  The *value* for the *mu*
property should be specified in the units described on the
:ref:`units<units>` doc page.

.. _species-modify-restrictio:

*************
Restrictions:
*************

none

.. _species-modify-related-commands:

*****************
Related commands:
*****************

none

.. _species-modify-default:

********
Default:
********

No magnetic moments are defined for any species (all 0.0).

