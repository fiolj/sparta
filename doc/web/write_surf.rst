:orphan:

.. index:: write_surf

.. _command-write-surf:

##################
write_surf command
##################

**Syntax:**

::

   write_surf file 

-  file = name of file to write surface element info to
-  zero or more keyword/args pairs may be appended
-  keyword = *points* or *fileper* or *nfile*

   ::

        points arg = yes or no to include a Points section in the file
        fileper arg = Np
          Np = write one file for every this many processors
        nfile arg = Nf
          Nf = write this many files, one from each of Nf processors 

**Examples:**

::

   write_surf data.surf
   write_surf data.surf points no
   write_surf data.surf.% nfile 50 

**Description:**

Write a surface file in text format describing the currently defined
surface elements, whether they be explicit or implicit surfaces. See the
`read_surf <read_surf.html>`__ and `read_isurf <read_isurf.html>`__
commands for a definition of surface elements and how they are defined
and used be SPARTA. The surface file can be used for later input to a
new simulation or for post-processing and visualization.

Note that if surface objects were clipped when read in by the
`read_surf <read_surf.html>`__ command then some surface elements may
have been deleted and new ones created. Likewise for the points that
define the end points or corner points of surface element lines (2d) or
triangles (3d). Similarly, if surface elements have been removed by the
`remove_surf <remove_surf.html>`__ command, then points may have also
been deleted. In either case, surface points and elements are renumbered
by these operations to create compressed, contiguous lists. These lists
are what is output by this command.

The file is written as a text file in the same format as the
`read_surf <read_surf.html>`__ command reads in. Note that a Points
section is optional. If the *points* keyword is specified with a value
of *yes*, then a Points section is included in the file. If the value is
*no*, then point coordinates are included with individual lines or
triangles.

Similar to `dump <dump.html>`__ files, the surface filename can contain
two wild-card characters. If a "*" appears in the filename, it is
replaced with the current timestep value. If a "%" character appears in
the filename, then one file is written by each processor and the "%"
character is replaced with the processor ID from 0 to P-1. An additional
file with the "%" replaced by "base" is also written, which contains
global information, i.e. just the header information for the number of
points and lines or triangles, as described on the
`read_surf <read_surf.html>`__ doc page.

For example, the files written for filename data.% would be data.base,
data.0, data.1, ..., data.P-1. This creates smaller files and can be a
fast mode of output and subsequent input on parallel machines that
support parallel I/O. The optional *fileper* and *nfile* keywords
discussed below can alter the number of files written.

Note that implicit surfaces read in by the
`read_isurf <read_isurf.html>`__ command can be written out by the
write_surf command, e.g. for visualization purposes. But they cannot be
read back in to SPARTA via the `read_isurf <read_isurf.html>`__ command,
because write_surf creates files in an explicit surface format. See the
`Howto 6.13 <Section_howto.html#howto_13>`__ section of the manual for a
discussion of explicit and implicit surfaces for an explantion of
explicit versus implicit surfaces as well as distributed versus
non-distributed storage. You cannot mix explicit and implicit surfaces
in the same simulation.

--------------

The optional *nfile* or *fileper* keywords can be used in conjunction
with the "%" wildcard character in the specified surface file name. As
explained above, the "%" character causes the surface file to be written
in pieces, one piece for each of P processors. By default P = the number
of processors the simulation is running on. The *nfile* or *fileper*
keyword can be used to set P to a smaller value, which can be more
efficient when running on a large number of processors.

The *nfile* keyword sets P to the specified Nf value. For example, if Nf
= 4, and the simulation is running on 100 processors, 4 files will be
written, by processors 0,25,50,75. Each will collect information from
itself and the next 24 processors and write it to a surface file.

For the *fileper* keyword, the specified value of Np means write one
file for every Np processors. For example, if Np = 4, every 4th
processor (0,4,8,12,etc) will collect information from itself and the
next 3 processors and write it to a surface file.

--------------

**Restrictions:** none

**Related commands:**

:ref:`command-read-surf`
:ref:`command-read-isurf`

**Default:**

The default is points = yes.
