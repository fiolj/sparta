
:orphan:

.. index:: remove_surf

.. _remove-surf:

.. _remove-surf-command:

###################
remove_surf command
###################

.. _remove-surf-syntax:

*******
Syntax:
*******

::

   remove_surf surfID

surfID = group ID for which surface elements to remove

.. _remove-surf-examples:

*********
Examples:
*********

::

   remove_surf topsurf

.. _remove-surf-descriptio:

************
Description:
************

Remove a group of surface elements that have previously been read-in
via the :ref:`read_surf<read-surf>` command.  The :ref:`group surf<group>` or :ref:`read_surf<read-surf>` can be used to assign
each surface element to one or more groups.  This command removes all
surface elements in the specified *surfID* group.

.. note::

  that the remaining surface elements must still constitute a
  "watertight" surface or an error will be generated.  The definition of
  watertight is explained in the Restrictions section of the
  :ref:`read_surf<read-surf>` doc page.

After surface elements have been deleted the IDs of the remaining
surface points and elements are renumbered so that the remaining N
elements have IDs from 1 to N.  The new list of surface elements can
be output via the :ref:`write_surf<write-surf>` or :ref:`dump surf<dump>` commands.

.. _remove-surf-restrictio:

*************
Restrictions:
*************

none

.. _remove-surf-related-commands:

*****************
Related commands:
*****************

:ref:`read_surf<read-surf>`

.. _remove-surf-default:

********
Default:
********

none

