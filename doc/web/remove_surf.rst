:orphan:

.. index:: remove_surf

.. _command-remove-surf:

###################
remove_surf command
###################

**Syntax:**

::

   remove_surf surfID 

-  surfID = group ID for which surface elements to remove

**Examples:**

::

   remove_surf topsurf 

**Description:**

Remove a group of surface elements that have previously been read-in via
the `read_surf <read_surf.html>`__ command. The `group
surf <group.html>`__ or `read_surf <read_surf.html>`__ can be used to
assign each surface element to one or more groups. This command removes
all surface elements in the specified *surfID* group.

Note that the remaining surface elements must still constitute a
"watertight" surface or an error will be generated. The definition of
watertight is explained in the Restrictions section of the
`read_surf <read_surf.html>`__ doc page.

After surface elements have been deleted, any surface points that are no
longer part of a surface element are also deleted. The remaining surface
points and elements are renumbered to create compressed, contiguous
lists. The new list of surface elements can be output via the
`write_surf <write_surf.html>`__ command.

**Restrictions:** none

**Related commands:**

:ref:`command-read-surf`

**Default:** none
