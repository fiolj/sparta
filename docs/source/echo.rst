
:orphan:

.. index:: echo

.. _echo:

.. _echo-command:

############
echo command
############

.. _echo-syntax:

*******
Syntax:
*******

::

   echo style

style = *none* or *screen* or *log* or *both*

.. _echo-examples:

*********
Examples:
*********

::

   echo both
   echo log

.. _echo-descriptio:

************
Description:
************

This command determines whether SPARTA echoes each input script
command to the screen and/or log file as it is read and processed.  If
an input script has errors, it can be useful to look at echoed output
to see the last command processed.

The :ref:`command-line switch<start-commandlin-options>` -echo can be used
in place of this command.

.. _echo-restrictio:

*************
Restrictions:
*************

none

.. _echo-related-commands:

*****************
Related commands:
*****************

none

.. _echo-default:

********
Default:
********

::

   echo log

