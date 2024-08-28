
:orphan:

.. index:: quit

.. _quit:

.. _quit-command:

############
quit command
############

.. _quit-syntax:

*******
Syntax:
*******

::

   quit

.. _quit-examples:

*********
Examples:
*********

::

   quit
   if "$n > 10000" then quit

.. _quit-descriptio:

************
Description:
************

This command causes SPARTA to exit, after shutting down all
output cleanly.

It can be used as a debug statement in an input script, to terminate
the script at some intermediate point.

It can also be used as an invoked command inside the
"then" or "else" portion of an :ref:`if<if>` command.

.. _quit-restrictio:

*************
Restrictions:
*************

none

.. _quit-related-commands:

*****************
Related commands:
*****************

:ref:`if<if>`

.. _quit-default:

********
Default:
********

none

