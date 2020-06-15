:orphan:

.. _command-quit:

############
quit command
############

**Syntax:**

::

   quit 

**Examples:**

::

   quit
   if "$n > 10000" then quit 

**Description:**

This command causes SPARTA to exit, after shutting down all output
cleanly.

It can be used as a debug statement in an input script, to terminate the
script at some intermediate point.

It can also be used as an invoked command inside the "then" or "else"
portion of an `if <if.html>`__ command.

**Restrictions:** none

**Related commands:**

:ref:`command-if`

**Default:** none
