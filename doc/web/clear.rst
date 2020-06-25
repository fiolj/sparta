:orphan:

.. index:: clear



.. _command-clear:

#############
clear command
#############


**Syntax:**

::

   clear 

**Examples:**

::

   (commands for 1st simulation)
   clear
   (commands for 2nd simulation) 

**Description:**

This command deletes all atoms, restores all settings to their default
values, and frees all memory allocated by SPARTA. Once a clear command
has been executed, it is almost as if SPARTA were starting over, with
only the exceptions noted below. This command enables multiple jobs to
be run sequentially from one input script.

These settings are not affected by a clear command: the working
directory (:ref:`shell<command-shell>` command), log file status
(:ref:`log<command-log>` command), echo status (:ref:`echo<command-echo>`
command), and input script variables (:ref:`variable<command-variable>`
command).

**Restrictions:** none

**Related commands:** none

**Default:** none
