
.. _accelerate:

.. _accelerate-accelerati-sparta-performanc:

###############################
Accelerating SPARTA performance
###############################

This section describes various methods for improving SPARTA
performance for different classes of problems running on different
kinds of machines.

Currently the only option is to use the KOKKOS accelerator
packages provided with SPARTA that
contains code optimized for certain kinds of hardware, including
multi-core CPUs, GPUs, and Intel Xeon Phi coprocessors.

.. contents::
   :depth: 1
   :local:

The `Benchmark page <http://sparta.sandia.gov/bench.html>`__ of the SPARTA
web site gives performance results for the various accelerator
packages discussed in Section 5.2, for several of the standard SPARTA
benchmark problems, as a function of problem size and number of
compute nodes, on different hardware platforms.

.. _accelerate-measuring-performanc:

*********************
Measuring performance
*********************

Before trying to make your simulation run faster, you should
understand how it currently performs and where the bottlenecks are.

The best way to do this is run the your system (actual number of
particles) for a modest number of timesteps (say 100 steps) on several
different processor counts, including a single processor if possible.
Do this for an equilibrium version of your system, so that the
100-step timings are representative of a much longer run.  There is
typically no need to run for 1000s of timesteps to get accurate
timings; you can simply extrapolate from short runs.

For the set of runs, look at the timing data printed to the screen and
log file at the end of each SPARTA run.  :ref:`This section<start-commandlin-options>` of the manual has an overview.

Running on one (or a few processors) should give a good estimate of
the serial performance and what portions of the timestep are taking
the most time.  Running the same problem on a few different processor
counts should give an estimate of parallel scalability.  I.e. if the
simulation runs 16x faster on 16 processors, its 100% parallel
efficient; if it runs 8x faster on 16 processors, it's 50% efficient.

The most important data to look at in the timing info is the timing
breakdown and relative percentages.  For example, trying different
options for speeding up the FFTs will have little impact
if they only consume 10% of the run time.  If the collide time is
dominating, you may want to look at the KOKKOS package, as discussed
below.  Comparing how the percentages change as
you increase the processor count gives you a sense of how different
operations within the timestep are scaling.

Another important detail in the timing info are the histograms of
particles counts and neighbor counts.  If these vary widely across
processors, you have a load-imbalance issue.  This often results in
inaccurate relative timing data, because processors have to wait when
communication occurs for other processors to catch up.  Thus the
reported times for "Communication" or "Other" may be higher than they
really are, due to load-imbalance.  If this is an issue, you can
uncomment the MPI_Barrier() lines in src/timer.cpp, and recompile
SPARTA, to obtain synchronized timings.

.. _accelerate-packages-optimized-styles:

******************************
Packages with optimized styles
******************************

Accelerated versions of various :ref:`collide_style<collide>`,
:ref:`fixes<fix>`, :ref:`computes<compute>`, and other commands have
been added to SPARTA via the KOKKOS package, which may run faster than
the standard non-accelerated versions.

All of these commands are in the KOKKOS package provided with SPARTA.
An overview of packages is give in :ref:`Section packages<packages>`.

SPARTA currently has acceleration support for three kinds of hardware,
via the KOKKOS package: Many-core CPUs, NVIDIA GPUs, and Intel Xeon
Phi.

Whether you will see speedup for your hardware may depend on the size
problem you are running and what commands (accelerated and
non-accelerated) are invoked by your input script.  While these doc
pages include performance guidelines, there is no substitute for
trying out the KOKKOS package.

Any accelerated style has the same name as the corresponding standard
style, except that a suffix is appended.  Otherwise, the syntax for
the command that uses the style is identical, their functionality is
the same, and the numerical results it produces should also be the
same, except for precision and round-off effects, and differences in
random numbers.

For example, the KOKKOS package provides an accelerated variant of the
Temperature Compute :ref:`compute temp<compute-temp>`, namely :ref:`compute temp/kk<compute-temp>`

To see what accelerate styles are currently available, see :ref:`Section 3.5<commands-individual>` of the manual.  The doc pages for
individual commands (e.g. :ref:`compute temp<compute-temp>`) also list
any accelerated variants available for that style.

To use an accelerator package in SPARTA, and one or more of the styles
it provides, follow these general steps:

using make:

.. list-table::
   :header-rows: 0

   * - install the accelerator package 
     -  make yes-fft, make yes-kokkos, etc 
   * -  add compile/link flags to Makefile.machine in src/MAKE 
     -  KOKKOS_ARCH=PASCAL60 
   * -  re-build SPARTA 
     -  make kokkos_cuda

or, using CMake from a build directory:

.. list-table::
   :header-rows: 0

   * - install the accelerator package 
     -  cmake -DPKG_FFT=ON -DPKG_KOKKOS=ON, etc 
   * -  add compile/link flags 
     -  cmake -C /path/to/sparta/cmake/presets/kokkos_cuda.cmake -DKokkos_ARCH_PASCAL60=ON 
   * -  re-build SPARTA 
     -  make

Then do the following:

.. list-table::
   :header-rows: 0

   * - prepare and test a regular SPARTA simulation 
     -  lmp_kokkos_cuda -in in.script; mpirun -np 32 lmp_kokkos_cuda -in in.script 
   * -  enable specific accelerator support via '-k on' :ref:`command-line switch<start-running-sparta>`, 
     -  -k on g 1 
   * -  set any needed options for the package via "-pk" :ref:`command-line switch<start-running-sparta>` or :ref:`package<package>` command, 
     -  only if defaults need to be changed, -pk kokkos react/retry yes 
   * -  use accelerated styles in your input via "-sf" :ref:`command-line switch<start-running-sparta>` or :ref:`suffix<suffix>` command 
     -  lmp_kokkos_cuda -in in.script -sf kk

.. note::

  that the first 3 steps can be done as a single command with
  suitable make command invocations. This is discussed in :ref:`Section   4<packages>` of the manual, and its use is illustrated in
  the individual accelerator sections.  Typically these steps only need
  to be done once, to create an executable that uses one or more
  accelerator packages.

The last 4 steps can all be done from the command-line when SPARTA is
launched, without changing your input script, as illustrated in the
individual accelerator sections.  Or you can add
:ref:`package<package>` and :ref:`suffix<suffix>` commands to your input
script.

The `Benchmark page <http://sparta.sandia.gov/bench.html>`__ of the SPARTA
web site gives performance results for the various accelerator
packages for several of the standard SPARTA benchmark problems, as a
function of problem size and number of compute nodes, on different
hardware platforms.

Here is a brief summary of what the KOKKOS package provides.

- Styles with a "kk" suffix are part of the KOKKOS package, and can be run using OpenMP on multicore CPUs, on an NVIDIA GPU, or on an Intel Xeon Phi in "native" mode.  The speed-up depends on a variety of factors, as discussed on the KOKKOS accelerator page.

The KOKKOS accelerator package doc page explains:

what hardware and software the accelerated package requires
how to build SPARTA with the accelerated package
how to run with the accelerated package either via command-line switches or modifying the input script
speed-ups to expect
guidelines for best performance
restrictions

.. _accelerate-kokkos-package:

**************
KOKKOS package
**************

Kokkos is a templated C++ library that provides abstractions to allow
a single implementation of an application kernel (e.g. a collision
style) to run efficiently on different kinds of hardware, such as
GPUs, Intel Xeon Phis, or many-core CPUs. Kokkos maps the C++ kernel
onto different backend languages such as CUDA, OpenMP, or Pthreads.
The Kokkos library also provides data abstractions to adjust (at
compile time) the memory layout of data structures like 2d and 3d
arrays to optimize performance on different hardware. For more
information on Kokkos, see
`Github <https://github.com/kokkos/kokkos>`__. Kokkos is part of
`Trilinos <http://trilinos.sandia.gov/packages/kokkos>`__. The Kokkos
library was written primarily by Carter Edwards, Christian Trott, and
Dan Sunderland (all Sandia).

The SPARTA KOKKOS package contains versions of collide, fix, and
compute styles that use data structures and macros provided by the
Kokkos library, which is included with SPARTA in /lib/kokkos. The
KOKKOS package was developed primarily by Stan Moore (Sandia) with
contributions of various styles by others, including Dan Ibanez
(Sandia), Tim Fuller (Sandia), and Sam Mish (Sandia). For more
information on developing using Kokkos abstractions see the Kokkos
programmers' guide at /lib/kokkos/doc/Kokkos_PG.pdf.

The KOKKOS package currently provides support for 3 modes of execution
(per MPI task). These are Serial (MPI-only for CPUs and Intel Phi),
OpenMP (threading for many-core CPUs and Intel Phi), and CUDA (for
NVIDIA GPUs). You choose the mode at build time to produce an
executable compatible with specific hardware.

.. note::

  Kokkos support within SPARTA must be built with a C++17
  compatible compiler. For a list of compilers that have been tested with
  the Kokkos library, see the Kokkos `README <https://github.com/kokkos/kokkos/blob/master/README.md>`__.

.. _accelerate-building-sparta-kokkos-package:

Building SPARTA with the KOKKOS package with Makefiles:
=======================================================

To build with the KOKKOS package, start with the provided Kokkos
Makefiles in /src/MAKE/. You may need to modify the KOKKOS_ARCH
variable in the Makefile to match your specific hardware. For example:

for Sandy Bridge CPUs, set KOKKOS_ARCH=SNB
for Broadwell CPUs, set KOKKOS_ARCH=BWD
for K80 GPUs, set KOKKOS_ARCH=KEPLER37
for P100 GPUs and Power8 CPUs, set KOKKOS_ARCH=PASCAL60,POWER8

Building SPARTA with the KOKKOS package with CMake:
===================================================

To build with the KOKKOS package, start with the provided preset files
in /cmake/presets/. You may need to set -D Kokkos_ARCH_*TYPE*=ON
to match your specific hardware. For example:

for Sandy Bridge CPUs, set -D Kokkos_ARCH_SNB=ON
for Broadwell CPUs, set -D Kokkos_ARCH_BWD=ON
for K80 GPUs, set -D Kokkos_ARCH_KEPLER37=ON
for P100 GPUs and Power8 CPUs, set -D Kokkos_ARCH_PASCAL60=ON, -D Kokkos_ARCH_POWER8=ON

See the **Advanced Kokkos Options** section below for a listing of all
Kokkos architecture options.

.. _accelerate-compile-cpuonly-(mpi-only,:

Compile for CPU-only (MPI only, no threading):
==============================================

Use a C++17 compatible compiler and set Kokkos architicture variable in as described above.  Then do the
following:

using Makefiles:

::

   cd sparta/src
   make yes-kokkos
   make kokkos_mpi_only

using CMake:

::

   cd build
   cmake -C /path/to/sparta/cmake/presets/kokkos_mpi_only.cmake
   make

.. _accelerate-compile-cpuonly-(mpi-plus:

Compile for CPU-only (MPI plus OpenMP threading):
=================================================

.. note::

  To build with Kokkos support for OpenMP threading, your compiler
  must support the OpenMP interface. You should have one or more
  multi-core CPUs so that multiple threads can be launched by each MPI
  task running on a CPU.

Use a C++17 compatible compiler and set Kokkos architecture variable in
as described above.  Then do the
following:

using Makefiles:

::

   cd sparta/src
   make yes-kokkos
   make kokkos_omp

using CMake:

::

   cd build
   cmake -C /path/to/sparta/cmake/presets/kokkos_omp.cmake
   make

.. _accelerate-compile-intel-knl-xeon:

Compile for Intel KNL Xeon Phi (Intel Compiler, OpenMPI):
=========================================================

Use a C++17 compatible compiler and do the following:

using Makefiles:

::

   cd sparta/src
   make yes-kokkos
   make kokkos_phi

using CMake:

::

   cd build
   cmake -C /path/to/sparta/cmake/presets/kokkos_phi.cmake
   make

.. _accelerate-compile-cpus-gpus-(with:

Compile for CPUs and GPUs (with OpenMPI or MPICH):
==================================================

.. note::

  To build with Kokkos support for NVIDIA GPUs, NVIDIA CUDA
  software version 11.0 or later must be installed on your system.

Use a C++17 compatible compiler and set Kokkos architecture variable in
for both GPU and CPU as described
above.  Then do the following:

using Makefiles:

::

   cd sparta/src
   make yes-kokkos
   make kokkos_cuda

using CMake:

::

   cd build
   cmake -C /path/to/sparta/cmake/presets/kokkos_cuda.cmake
   make

.. _accelerate-running-sparta-kokkos-package:

Running SPARTA with the KOKKOS package:
=======================================

All Kokkos operations occur within the context of an individual MPI
task running on a single node of the machine. The total number of MPI
tasks used by SPARTA (one or multiple per compute node) is set in the
usual manner via the mpirun or mpiexec commands, and is independent of
Kokkos. The mpirun or mpiexec command sets the total number of MPI
tasks used by SPARTA (one or multiple per compute node) and the number
of MPI tasks used per node. E.g. the mpirun command in OpenMPI does
this via its -np and -npernode switches. Ditto for MPICH via -np and
-ppn.

.. _accelerate-running-multicore-cpu:

Running on a multi-core CPU:
============================

Here is a quick overview of how to use the KOKKOS package for CPU
acceleration, assuming one or more 16-core nodes.

::

   mpirun -np 16 spa_kokkos_mpi_only -k on -sf kk -in in.collide        # 1 node, 16 MPI tasks/node, no multi-threading
   mpirun -np 2 -ppn 1 spa_kokkos_omp -k on t 16 -sf kk -in in.collide  # 2 nodes, 1 MPI task/node, 16 threads/task
   mpirun -np 2 spa_kokkos_omp -k on t 8 -sf kk -in in.collide          # 1 node,  2 MPI tasks/node, 8 threads/task
   mpirun -np 32 -ppn 4 spa_kokkos_omp -k on t 4 -sf kk -in in.collide  # 8 nodes, 4 MPI tasks/node, 4 threads/task

To run using the KOKKOS package, use the "-k on", "-sf kk" and "-pk
kokkos" :ref:`command-line switches<start-commandlin-options>` in your
mpirun command.  You must use the "-k on" :ref:`command-line switch<start-commandlin-options>` to enable the KOKKOS package. It
takes additional arguments for hardware settings appropriate to your
system. Those arguments are :ref:`documented here<start-commandlin-options>`. For OpenMP use:

::

   -k on t Nt

.. note::

  that the product of MPI tasks \* OpenMP threads/task should not exceed
  the physical number of cores (on a node), otherwise performance will
  suffer. If hyperthreading is enabled, then the product of MPI tasks \*
  OpenMP threads/task should not exceed the physical number of cores \*
  hardware threads.  The "-k on" switch also issues a "package kokkos"
  command (with no additional arguments) which sets various KOKKOS
  options to default values, as discussed on the :ref:`package<package>`
  command doc page.

The "-sf kk" :ref:`command-line switch<start-commandlin-options>` will
automatically append the "/kk" suffix to styles that support it.  In
this manner no modification to the input script is
needed. Alternatively, one can run with the KOKKOS package by editing
the input script as described below.

.. note::

  When using a single OpenMP thread, the Kokkos Serial backend (i.e. 
  Makefile.kokkos_mpi_only) will give better performance than the OpenMP 
  backend (i.e. Makefile.kokkos_omp) because some of the overhead to make 
  the code thread-safe is removed.

.. note::

  The default for the :ref:`package kokkos<package>` command is to
  use "threaded" communication. However, when running on CPUs, it will
  typically be faster to use "classic" non-threaded communication.  Use
  the "-pk kokkos" :ref:`command-line switch<start-commandlin-options>` to
  change the default :ref:`package kokkos<package>` options. See its doc
  page for details and default settings. Experimenting with its options
  can provide a speed-up for specific calculations. For example:

::

   mpirun -np 16 spa_kokkos_mpi_only -k on -sf kk -pk kokkos comm classic -in in.collide       # non-threaded comm

For OpenMP, the KOKKOS package uses data duplication (i.e. 
thread-private arrays) by default to avoid thread-level write conflicts 
in some compute styles. Data duplication is typically fastest for small 
numbers of threads (i.e. 8 or less) but does increase memory footprint 
and is not scalable to large numbers of threads. An alternative to data 
duplication is to use thread-level atomics, which don't require 
duplication. When using the Kokkos Serial backend or the OpenMP backend 
with a single thread, no duplication or atomics are used. For CUDA, the 
KOKKOS package always uses atomics in these computes when necessary. The 
use of atomics instead of duplication can be forced by compiling with the 
"-DSPARTA_KOKKOS_USE_ATOMICS" compile switch.

.. _accelerate-core-thread-affinity:

Core and Thread Affinity:
=========================

When using multi-threading, it is important for performance to bind
both MPI tasks to physical cores, and threads to physical cores, so
they do not migrate during a simulation.

If you are not certain MPI tasks are being bound (check the defaults
for your MPI installation), binding can be forced with these flags:

::

   OpenMPI 1.8: mpirun -np 2 -bind-to socket -map-by socket ./spa_openmpi ...
   Mvapich2 2.0: mpiexec -np 2 -bind-to socket -map-by socket ./spa_mvapich ...

For binding threads with KOKKOS OpenMP, use thread affinity
environment variables to force binding. With OpenMP 3.1 (gcc 4.7 or
later, intel 12 or later) setting the environment variable
OMP_PROC_BIND=true should be sufficient. In general, for best
performance with OpenMP 4.0 or better set OMP_PROC_BIND=spread and
OMP_PLACES=threads.  For binding threads with the KOKKOS pthreads
option, compile SPARTA the KOKKOS HWLOC=yes option as described below.

.. _accelerate-running-knight's-landing-(knl):

Running on Knight's Landing (KNL) Intel Xeon Phi:
=================================================

Here is a quick overview of how to use the KOKKOS package for the
Intel Knight's Landing (KNL) Xeon Phi:

.. note::

  that with the KOKKOS package you do not need to specify how many KNLs
  there are per node; each KNL is simply treated as running some number
  of MPI tasks.

Examples of mpirun commands that follow these rules are shown below.

::

   Intel KNL node with 64 cores (256 threads/node via 4x hardware threading):
   mpirun -np 64 spa_kokkos_phi -k on t 4 -sf kk -in in.collide      # 1 node, 64 MPI tasks/node, 4 threads/task
   mpirun -np 66 spa_kokkos_phi -k on t 4 -sf kk -in in.collide      # 1 node, 66 MPI tasks/node, 4 threads/task
   mpirun -np 32 spa_kokkos_phi -k on t 8 -sf kk -in in.collide      # 1 node, 32 MPI tasks/node, 8 threads/task
   mpirun -np 512 -ppn 64 spa_kokkos_phi -k on t 4 -sf kk -in in.collide  # 8 nodes, 64 MPI tasks/node, 4 threads/task

The -np setting of the mpirun command sets the number of MPI
tasks/node. The "-k on t Nt" command-line switch sets the number of
threads/task as Nt. The product of these two values should be N, i.e.
or 264.

.. note::

  The default for the :ref:`package kokkos<package>` command is to
  use "threaded" communication. However, when running on KNL, it will
  typically be faster to use "classic" non-threaded communication.  Use
  the "-pk kokkos" :ref:`command-line switch<start-commandlin-options>` to
  change the default :ref:`package kokkos<package>` options. See its doc
  page for details and default settings. Experimenting with its options
  can provide a speed-up for specific calculations. For example:

::

   mpirun -np 64 spa_kokkos_phi -k on t 4 -sf kk -pk kokkos comm classic -in in.collide      # non-threaded comm

.. note::

  MPI tasks and threads should be bound to cores as described
  above for CPUs.

.. note::

  To build with Kokkos support for Intel Xeon Phi coprocessors
  such as Knight's Corner (KNC), your system must be configured to use
  them in "native" mode, not "offload" mode.

.. _accelerate-running-gpus:

Running on GPUs:
================

Use the "-k" :ref:`command-line switch<start-commandlin-options>` to
specify the number of GPUs per node, and the number of threads per MPI
task. Typically the -np setting of the mpirun command should set the
number of MPI tasks/node to be equal to the # of physical GPUs on the
node.  You can assign multiple MPI tasks to the same GPU with the
KOKKOS package, but this is usually only faster if significant
portions of the input script have not been ported to use Kokkos. Using
CUDA MPS is recommended in this scenario. As above for multi-core CPUs
(and no GPU), if N is the number of physical cores/node, then the
number of MPI tasks/node should not exceed N.

::

   -k on g Ng

Here are examples of how to use the KOKKOS package for GPUs, assuming
one or more nodes, each with two GPUs.

::

   mpirun -np 2 spa_kokkos_cuda -k on g 2 -sf kk -in in.collide          # 1 node,   2 MPI tasks/node, 2 GPUs/node
   mpirun -np 32 -ppn 2 spa_kokkos_cuda -k on g 2 -sf kk -in in.collide  # 16 nodes, 2 MPI tasks/node, 2 GPUs/node (32 GPUs total)

.. note::

  Use the "-pk kokkos" :ref:`command-line   switch<start-commandlin-options>` to change the default :ref:`package   kokkos<package>` options. See its doc page for details and default
  settings. For example:

::

   mpirun -np 2 spa_kokkos_cuda -k on g 2 -sf kk -pk kokkos gpu/aware off -in in.collide      # set gpu/aware MPI support off

.. note::

  Using OpenMP threading and CUDA together is currently not
  possible with the SPARTA KOKKOS package.

.. note::

  For good performance of the KOKKOS package on GPUs, you must
  have Kepler generation GPUs (or later). The Kokkos library exploits
  texture cache options not supported by Telsa generation GPUs (or
  older).

.. note::

  When using a GPU, you will achieve the best performance if your
  input script does not use fix or compute styles which are not yet
  Kokkos-enabled. This allows data to stay on the GPU for multiple
  timesteps, without being copied back to the host CPU. Invoking a
  non-Kokkos fix or compute, or performing I/O for :ref:`stats<stats>` or
  :ref:`dump<dump>` output will cause data to be copied back to the CPU
  incurring a performance penalty.

.. _accelerate-run-kokkos-package-by:

Run with the KOKKOS package by editing an input script:
=======================================================

Alternatively the effect of the "-sf" or "-pk" switches can be
duplicated by adding the :ref:`package kokkos<package>` or :ref:`suffix kk<suffix>` commands to your input script.

The discussion above for building SPARTA with the KOKKOS package, the
mpirun/mpiexec command, and setting appropriate thread are the same.

You must still use the "-k on" :ref:`command-line switch<start-commandlin-options>` to enable the KOKKOS package, and
specify its additional arguments for hardware options appropriate to
your system, as documented above.

You can use the :ref:`suffix kk<suffix>` command, or you can explicitly add a
"kk" suffix to individual styles in your input script, e.g.

::

   collide vss/kk air ar.vss

You only need to use the :ref:`package kokkos<package>` command if you
wish to change any of its option defaults, as set by the "-k on"
:ref:`command-line switch<start-commandlin-options>`.

.. _accelerate-speedups-expect:

Speed-ups to expect:
====================

The performance of KOKKOS running in different modes is a function of
your hardware, which KOKKOS-enable styles are used, and the problem
size.

Generally speaking, when running on CPUs only, with a single thread per MPI task, the
performance difference of a KOKKOS style and (un-accelerated) styles
(MPI-only mode) is typically small (less than 20%).

See the `Benchmark page <http://sparta.sandia.gov/bench.html>`__ of the
SPARTA web site for performance of the KOKKOS package on different
hardware.

.. _accelerate-advanced-kokkos-options:

Advanced Kokkos options:
========================

There are other allowed options when building with the KOKKOS package.
A few options are listed here; for a full list of all options,
please refer to the Kokkos documentation.
As above, these options can be set as variables on the command line,
in a Makefile, or in a CMake presets file. For default CMake values,
see cmake -LH | grep -i kokkos.

The CMake option Kokkos_ENABLE_*OPTION* or the makefile setting KOKKOS_DEVICE=*OPTION* sets the 
parallelization method used for Kokkos code (within SPARTA). 
For example, the CMake option Kokkos_ENABLE_SERIAL=ON or the makefile setting KOKKOS_DEVICES=SERIAL
means that no threading will be used.  The CMake option Kokkos_ENABLE_OPENMP=ON or the 
makefile setting KOKKOS_DEVICES=OPENMP means that OpenMP threading will be
used. The CMake option Kokkos_ENABLE_CUDA=ON or the makefile setting
KOKKOS_DEVICES=CUDA means an NVIDIA GPU running CUDA will be used.

As described above, the CMake option Kokkos_ARCH_*TYPE*=ON or the makefile setting KOKKOS_ARCH=*TYPE* enables compiler switches needed when compiling for a specific hardware:

.. list-table::
   :header-rows: 0

   * - **Arch-ID**	
     -  **HOST or GPU** 
     - 	**Description** 
   * -  NATIVE 
     -  HOST 
     -  Local machine 
   * -  AMDAVX 
     -  HOST 
     -  AMD 64-bit x86 CPU (AVX 1) 
   * -  ZEN 
     -  HOST 
     -  AMD Zen class CPU (AVX 2) 
   * -  ZEN2 
     -  HOST 
     -  AMD Zen2 class CPU (AVX 2) 
   * -  ZEN3 
     -  HOST 
     -  AMD Zen3 class CPU (AVX 2) 
   * -  ARMV80 
     -  HOST 
     -  ARMv8.0 Compatible CPU 
   * -  ARMV81 
     -  HOST 
     -  ARMv8.1 Compatible CPU 
   * -  ARMV8_THUNDERX 
     -  HOST 
     -  ARMv8 Cavium ThunderX CPU 
   * -  ARMV8_THUNDERX2 
     -  HOST 
     -  ARMv8 Cavium ThunderX2 CPU 
   * -  A64FX 
     -  HOST 
     -  ARMv8.2 with SVE Support 
   * -  SNB 
     -  HOST 
     -  Intel Sandy/Ivy Bridge CPU (AVX 1) 
   * -  HSW 
     -  HOST 
     -  Intel Haswell CPU (AVX 2) 
   * -  BDW 
     -  HOST 
     -  Intel Broadwell Xeon E-class CPU (AVX 2 + transactional mem) 
   * -  SKL 
     -  HOST 
     -  Intel Skylake Client CPU 
   * -  SKX 
     -  HOST 
     -  Intel Skylake Xeon Server CPU (AVX512) 
   * -  ICL 
     -  HOST 
     -  Intel Ice Lake Client CPU (AVX512) 
   * -  ICX 
     -  HOST 
     -  Intel Ice Lake Xeon Server CPU (AVX512) 
   * -  SPR 
     -  HOST 
     -  Intel Sapphire Rapids Xeon Server CPU (AVX512) 
   * -  KNC 
     -  HOST 
     -  Intel Knights Corner Xeon Phi 
   * -  KNL 
     -  HOST 
     -  Intel Knights Landing Xeon Phi 
   * -  POWER8 
     -  HOST 
     -  IBM POWER8 CPU 
   * -  POWER9 
     -  HOST 
     -  IBM POWER9 CPU 
   * -  RISCV_SG2042 
     -  HOST 
     -  SG2042 (RISC-V) CPU 
   * -  KEPLER30 
     -  GPU 
     -  NVIDIA Kepler generation CC 3.0 GPU 
   * -  KEPLER32 
     -  GPU 
     -  NVIDIA Kepler generation CC 3.2 GPU 
   * -  KEPLER35 
     -  GPU 
     -  NVIDIA Kepler generation CC 3.5 GPU 
   * -  KEPLER37 
     -  GPU 
     -  NVIDIA Kepler generation CC 3.7 GPU 
   * -  MAXWELL50 
     -  GPU 
     -  NVIDIA Maxwell generation CC 5.0 GPU 
   * -  MAXWELL52 
     -  GPU 
     -  NVIDIA Maxwell generation CC 5.2 GPU 
   * -  MAXWELL53 
     -  GPU 
     -  NVIDIA Maxwell generation CC 5.3 GPU 
   * -  PASCAL60 
     -  GPU 
     -  NVIDIA Pascal generation CC 6.0 GPU 
   * -  PASCAL61 
     -  GPU 
     -  NVIDIA Pascal generation CC 6.1 GPU 
   * -  VOLTA70 
     -  GPU 
     -  NVIDIA Volta generation CC 7.0 GPU 
   * -  VOLTA72 
     -  GPU 
     -  NVIDIA Volta generation CC 7.2 GPU 
   * -  TURING75 
     -  GPU 
     -  NVIDIA Turing generation CC 7.5 GPU 
   * -  AMPERE80 
     -  GPU 
     -  NVIDIA Ampere generation CC 8.0 GPU 
   * -  AMPERE86 
     -  GPU 
     -  NVIDIA Ampere generation CC 8.6 GPU 
   * -  ADA89 
     -  GPU 
     -  NVIDIA Ada Lovelace generation CC 8.9 GPU 
   * -  HOPPER90 
     -  GPU 
     -  NVIDIA Hopper generation CC 9.0 GPU 
   * -  AMD_GFX908 
     -  GPU 
     -  AMD GPU MI100 
   * -  AMD_GFX90A 
     -  GPU 
     -  AMD GPU MI200 
   * -  AMD_GFX942 
     -  GPU 
     -  AMD GPU MI300 
   * -  AMD_GFX1030 
     -  GPU 
     -  AMD GPU V620/W6800 
   * -  AMD_GFX1100 
     -  GPU 
     -  AMD GPU RX7900XTX 
   * -  INTEL_GEN GPU SPIR64-based devices, e.g. Intel GPUs, using JIT 
     -  INTEL_DG1 
     -  GPU 
   * -  Intel Iris XeMAX GPU 
     -  INTEL_GEN9 
     -  GPU 
   * -  Intel GPU Gen9 
     -  INTEL_GEN11 
     -  GPU 
   * -  Intel GPU Gen11 
     -  INTEL_GEN12LP 
     -  GPU 
   * -  Intel GPU Gen12LP 
     -  INTEL_XEHP 
     -  GPU 
   * -  Intel GPU Xe-HP 
     -  INTEL_PVC 
     -  GPU 
   * -  Intel GPU Ponte Vecchio 
     - 
     -

The CMake option Kokkos_ENABLE_CUDA_*OPTION* or the makefile setting KOKKOS_CUDA_OPTIONS=*OPTION* are 
additional options for CUDA. For example, the CMake option Kokkos_ENABLE_CUDA_UVM=ON or the makefile setting KOKKOS_CUDA_OPTIONS="enable_lambda,force_uvm" enables the use of CUDA "Unified Virtual Memory" (UVM) in Kokkos. UVM allows to one to use the host CPU memory to supplement the memory used on the GPU (with some performance penalty) and thus enables running larger problems that would otherwise not fit into the RAM on the GPU. Please note, that the SPARTA KOKKOS package must always be compiled with the CMake option Kokkos_ENABLE_CUDA_LAMBDA=ON or the makefile setting KOKKOS_CUDA_OPTIONS=enable_lambda when using GPUs. The CMake configuration will thus always enable it.

The CMake option Kokkos_ENABLE_DEBUG=ON or the makefile setting KOKKOS_DEBUG=yes is useful
when developing a Kokkos-enabled style within SPARTA. This option enables printing of run-time debugging
information that can be useful and also enables runtime bounds
checking on Kokkos data structures, but may slow down performance.

.. _accelerate-restrictio:

Restrictions:
=============

Currently, there are no precision options with the KOKKOS package. All
compilation and computation is performed in double precision.

