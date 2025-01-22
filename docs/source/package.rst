
:orphan:

.. index:: package

.. _package:

.. _package-command:

###############
package command
###############

.. _package-syntax:

*******
Syntax:
*******

::

   package style args

- style = *kokkos* 

- args = arguments specific to the style

::

   *kokkos* args = keyword value ...
   zero or more keyword/value pairs may be appended
   keywords = *comm* or *react/extra* or *react/retry* or *gpu/aware*
   *comm* value = *threaded* or *serial*
   threaded = perform pack/unpack using KOKKOS (e.g. on GPU or using OpenMP) (default for GPUs)
   serial = perform communication pack/unpack in non-KOKKOS mode (default for CPUs)
   *react/extra* = *factor*
   factor = increase memory used for collisions by this factor (default)
   *react/retry* = *yes* or *no*
   yes = retry collision algorithm until successful
   no = do not retry collision algorithm (default)
   *gpu/aware* = *yes* or *no*
   yes = use GPU-aware MPI (default)
   no = do not use GPU-aware MPI

.. _package-examples:

*********
Examples:
*********

::

   package kokkos comm serial
   package kokkos comm threaded react/retry yes
   package kokkos gpu/aware no

.. _package-descriptio:

************
Description:
************

This command invokes package-specific settings for the KOKKOS
accelerator package available in SPARTA.

If this command is specified in an input script, it must be near the
top of the script, before the simulation box has been created.  This
is because it specifies settings that the accelerator package used in
its initialization, before a simulation is defined.

This command can also be specified from the command-line when
launching SPARTA, using the "-pk" :ref:`command-line switch<start-commandlin-options>`.  The syntax is exactly the same as
when used in an input script.

.. note::

  that the KOKKOS accelerator package requires the package command
  to be specified, if the package is to be used in a simulation (SPARTA
  can be built with the accelerator package without using it in a
  particular simulation).  However, a default version of the command is
  typically invoked by other accelerator settings. For example, the
  KOKKOS package requires a "-k on" :ref:`command-line   switch<start-commandlin-options>` respectively, which invokes a
  "package kokkos" command with default settings.

.. note::

  A package command for a particular style can be invoked multiple
  times when a simulation is setup, e.g. by the "-k on", "-sf", and
  "-pk" :ref:`command-line switches<start-commandlin-options>`, and by using
  this command in an input script.  Each time it is used all of the
  style options are set, either to default values or to specified
  settings.  I.e. settings from previous invocations do not persist
  across multiple invocations.

See the the :ref:`Accelerating SPARTA<accelerate-kokkos-package>`
section of the manual for more details about using the various
accelerator packages for speeding up SPARTA simulations.

The *kokkos* style invokes settings associated with the use of the
KOKKOS package.

All of the settings are optional keyword/value pairs.  Each has a
default value as listed below.

Chemical reactions (gas or surface) can increase the number of
particles in the simulation, which requires extra memory storage. It
is not possible to resize Kokkos data structures during the reaction
routines, so two workarounds are provided. The default is to use the
*react/extra* keyword, which ensures there is extra memory allocated
to store new particles. For example, if *react/extra* is set to 1.1,
then the memory is over-allocated by 10%. If this space is still not
sufficient to hold new particles, the code will error out and the
simulation must be restarted using a larger value for *react/extra*.
Alternatively, if the *react/retry* option is set to *yes*, backup
copies of the Kokkos data structures are created. If space is exceeded
during reactions, the Kokkos data structures are restored from backup,
their size is increased, and the collide or move routine is started
over from the beginning. This guarantees that reactions will
eventually succeed without producing an error, but increases memory by
a factor of 2 and also has overhead from making a backup copy of the
data. If the *react/retry* option is set to *yes*, the
*react/extra* keyword will be ignored. If reactions are not defined,
both of these options will be ignored.

The *comm* keyword determines whether the host or device performs the
packing and unpacking of data when communicating per-atom data between
processors. The value options are *threaded* or *serial*.

The optimal choice for this keyword depends on the hardware used.
When running on CPUs or Xeon Phi, the *serial* option is typically
fastest. When using GPUs, the *threaded* value will typically be
optimal. In this case data can stay on the GPU for many timesteps
without being fully moved between the host and GPU.

The *gpu/aware* keyword chooses whether GPU-aware MPI will be used. When 
this keyword is set to *on*, buffers in GPU memory are passed directly 
through MPI send/receive calls. This can reduce overhead of first 
copying the data to the host CPU. However GPU-aware MPI is not supported on 
all systems, which can lead to segmentation faults and would require 
using a value of *off*.

.. _package-restrictio:

*************
Restrictions:
*************

This command cannot be used after the simulation box is defined by a
:ref:`create_box<create-box>` command.

The kk style of this command can only be invoked if SPARTA was built
with the KOKKOS package.  See the :ref:`Making SPARTA<start-making-sparta-optional-packages>` section for more info.

.. _package-related-commands:

*****************
Related commands:
*****************

:ref:`suffix<suffix>`, "-pk" :ref:`command-line setting<start-commandlin-options>`

.. _package-default:

********
Default:
********

For the KOKKOS package, the option defaults are react/extra = 1.1,
react/retry = no, and gpu/aware yes. For CPUs: comm = serial, and for
GPUs: comm = threaded.  These settings are made automatically by the
required "-k on" :ref:`command-line switch<start-commandlin-options>`. You
can change them by using the package kokkos command in your input script
or via the "-pk kokkos" :ref:`command-line switch<start-commandlin-options>`.

