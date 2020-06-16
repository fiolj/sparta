:orphan:

.. index:: write_restart

.. _command-write-restart:

#####################
write_restart command
#####################

**Syntax:**

::

   write_restart file keyword value ... 

-  file = name of file to write restart information to
-  zero or more keyword/value pairs may be appended
-  keyword = *fileper* or *nfile*

   ::

        fileper arg = Np
          Np = write one file for every this many processors
        nfile arg = Nf
          Nf = write this many files, one from each of Nf processors 

**Examples:**

::

   write_restart restart.equil
   write_restart restart.equil.mpiio
   write_restart flow.%.* nfile 10 

**Description:**

Write a binary restart file with the current state of the simulation.

During a long simulation, the `restart <restart.html>`__ command can be
used to output restart files periodically. The write_restart command is
useful at the end of a run or between two runs, whenever you wish to
write out a single current restart file.

Similar to `dump <dump.html>`__ files, the restart filename can contain
two wild-card characters. If a "*" appears in the filename, it is
replaced with the current timestep value. If a "%" character appears in
the filename, then one file is written by each processor and the "%"
character is replaced with the processor ID from 0 to P-1. An additional
file with the "%" replaced by "base" is also written, which contains
global information. For example, the files written for filename
restart.% would be restart.base, restart.0, restart.1, ... restart.P-1.
This creates smaller files and can be a fast mode of output and
subsequent input on parallel machines that support parallel I/O. The
optional *fileper* and *nfile* keywords discussed below can alter the
number of files written.

Restart files can be read by a `read_restart <read_restart.html>`__
command to restart a simulation from a particular state. Because the
file is binary, it may not be readable on another machine.

IMPORTANT NOTE: Although the purpose of restart files is to enable
restarting a simulation from where it left off, not all information
about a simulation is stored in the file. For example, the list of fixes
that were specified during the initial run is not stored, which means
the new input script must specify any fixes you want to use. See the
`read_restart <read_restart.html>`__ command for details about what is
stored in a restart file.

--------------

The optional *nfile* or *fileper* keywords can be used in conjunction
with the "%" wildcard character in the specified restart file name. As
explained above, the "%" character causes the restart file to be written
in pieces, one piece for each of P processors. By default P = the number
of processors the simulation is running on. The *nfile* or *fileper*
keyword can be used to set P to a smaller value, which can be more
efficient when running on a large number of processors.

The *nfile* keyword sets P to the specified Nf value. For example, if Nf
= 4, and the simulation is running on 100 processors, 4 files will be
written, by processors 0,25,50,75. Each will collect information from
itself and the next 24 processors and write it to a restart file.

For the *fileper* keyword, the specified value of Np means write one
file for every Np processors. For example, if Np = 4, every 4th
processor (0,4,8,12,etc) will collect information from itself and the
next 3 processors and write it to a restart file.

--------------

**Restrictions:** none

**Related commands:**

:ref:`command-restart`
:ref:`command-read-restart`

**Default:** none
