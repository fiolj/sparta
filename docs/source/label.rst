
:orphan:

.. index:: label

.. _label:

.. _label-command:

#############
label command
#############

.. _label-syntax:

*******
Syntax:
*******

::

   label ID

   - ID = string used as label name

.. _label-examples:

*********
Examples:
*********

::

   label xyz
   label loop

.. _label-descriptio:

************
Description:
************

Label this line of the input script with the chosen ID.  Unless a jump
command was used previously, this does nothing.  But if a
:ref:`jump<jump>` command was used with a label argument to begin
invoking this script file, then all command lines in the script prior
to this line will be ignored.  I.e. execution of the script will begin
at this line.  This is useful for looping over a section of the input
script as discussed in the :ref:`jump<jump>` command.

.. _label-restrictio:

*************
Restrictions:
*************

none

.. _label-related-commands:

*****************
Related commands:
*****************

none

.. _label-default:

********
Default:
********

none

