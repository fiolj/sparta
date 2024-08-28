

.. _packages:

########
Packages
########

This section gives an overview of the optional packages that extend
SPARTA functionality with instructions on how to build SPARTA with
each of them.  Packages are groups of files that enable a specific set
of features.  For example, the KOKKOS package provides styles that
can run on different hardware such as GPUs.  You can see the list of all
packages and "make" commands to manage them by typing "make package"
from within the src directory of the SPARTA distribution or
"cmake -DSPARTA_LIST_PKGS" from within a build directory.  :ref:`Section 2.3<start-making-sparta-optional-packages>` gives general info on how to install
and un-install packages as part of the SPARTA build process.

Packages may require some
additional code compiled located in the lib folder, or may require
an external library to be downloaded, compiled, installed, and SPARTA
configured to know about its location and additional compiler flags.

Following the next two tables is a sub-section for each package.  It
lists authors (if applicable) and summarizes the package contents.  It
has specific instructions on how to install the package, including (if
necessary) downloading or building any extra library it requires. It
also gives links to documentation, example scripts, and
pictures/movies (if available) that illustrate use of the package.

.. note::

  To see the complete list of commands a package adds to SPARTA,
  just look at the files in its src directory, e.g. "ls src/KOKKOS".
  Files with names that start with fix, compute, etc correspond to
  commands with the same style names.

In these two tables, the "Example" column is a sub-directory in the
examples directory of the distribution which has an input script that
uses the package.  E.g. "fft" refers to the examples/fft
directory; The "Library" column indicates whether an extra library is needed to build
and use the package:

dash = no library
sys = system library: you likely have it on your machine
int = internal library: provided with SPARTA, but you may need to build it
ext = external library: you will need to download and install it on your machine

.. _packages-sparta:

**SPARTA packages**

.. list-table::
   :header-rows: 0

   * - Package
     -  Description
     -  Doc page
     -  Example
     -  Library
   * - :ref:`FFT<packages-fft-package>`
     -  fast Fourier transforms
     -  :ref:`compute_style compute/fft/grid<compute-fft-grid>`
     -  fft
     -  int or ext
   * - :ref:`KOKKOS<packages-kokkos-package>`
     -  Kokkos-enabled styles
     -  :ref:`Section 5.3<accelerate-kokkos-package>`
     -  `Benchmarks <http://sparta.sandia.gov/bench.html>`__
     -  -

.. _packages-fft-package:

***********
FFT package
***********

.. _packages-contents:

Contents:
=========

Apply Fast Fourier Transforms (FFTs) to simulation data. The FFT library is
specified in the Makefile.machine using the FFT_INC, FFT_PATH, and FFT_LIB
variables. Supported external FFT libraries that can be specified include FFTW3
and MKL. If no FFT library is specified in the Makefile, SPARTA will use the
internal KISS FFT library that is included with SPARTA.

Similarly an external FFT library can be specified for the KOKKOS package.
Options are CUFFT, HIPFFT, FFTW3, and MKL. If no FFT library is specified in
the Makefile, SPARTA will use the internal Kokkos version of the KISS FFT
library that is included with SPARTA.

See the see discussion in doc/Section_start.html#2_2 (step 6).

.. _packages-install-uninstall-make:

Install or un-install with make:
================================

::

   make yes-fft
   make machine

::

   make no-fft
   make machine

.. _packages-install-uninstall-cmake:

Install or un-install with CMake:
=================================

::

   cd build
   cmake -C /path/to/sparta/cmake/presets/machine.cmake -DPKG_FFT=ON /path/to/sparta/cmake
   make

::

   cmake -C /path/to/sparta/cmake/presets/machine.cmake -DPKG_FFT=OFF /path/to/sparta/cmake
   make

.. _packages-supporting-info:

Supporting info:
================

:ref:`compute fft/grid<compute-fft-grid>`
examples/fft

.. _packages-kokkos-package:

**************
KOKKOS package
**************

Contents:
=========

Styles adapted to compile using the Kokkos library which can convert
them to OpenMP or CUDA code so that they run efficiently on multicore
CPUs, KNLs, or GPUs.  All the styles have a "kk" as a suffix in their
style name.  :ref:`Section 5.3<accelerate-kokkos-package>` gives details
of what hardware and software is required on your system, and how to
build and use this package.  Its styles can be invoked at run time via
the "-sf kk" or "-suffix kk" :ref:`command-line switches<start-running-sparta>`.

You must have a C++17 compatible compiler to use this package.

.. _packages-authors:

Authors:
========

The KOKKOS package was created primarily by Stan Moore (Sandia),
with contributions from other folks as well.
It uses the open-source `Kokkos library <https://github.com/kokkos>`__
which was developed by Carter Edwards, Christian Trott, and others at
Sandia, and which is included in the SPARTA distribution in
lib/kokkos.

.. _packages-install-uninstall:

Install or un-install:
======================

For the KOKKOS package, you have 3 choices when building.  You can
build with either CPU or KNL or GPU support.  Each choice requires
additional settings in your Makefile.machine or machine.cmake file 
for the KOKKOS_DEVICES and KOKKOS_ARCH settings. See the 
src/MAKE/OPTIONS/Makefile.kokkos\* or cmake/presets/\*kokkos\*.cmake
files for examples. For CMake, it's best to start by copying
cmake/presets/kokkos_cuda.cmake to cmake/presets/machine.cmake.

.. _packages-multicore-cpus-openmp:

For multicore CPUs using OpenMP:
================================

Using Makefiles:

::

   KOKKOS_DEVICES = OpenMP
   KOKKOS_ARCH = HSW           # HSW = Haswell, SNB = SandyBridge, BDW = Broadwell, etc

Using CMake:

-DKokkos_ENABLE_OPENMP=ON
-DKokkos_ARCH_HSW=ON

.. _packages-intel-knls-openmp:

For Intel KNLs using OpenMP:
============================

Using Makefiles:

::

   KOKKOS_DEVICES = OpenMP
   KOKKOS_ARCH = KNL

Using CMake:

::

   -DKokkos_ENABLE_OPENMP=ON
   -DKokkos_ARCH_KNL=ON

.. _packages-nvidia-gpus-cuda:

For NVIDIA GPUs using CUDA:
===========================

::

   KOKKOS_DEVICES = Cuda
   KOKKOS_ARCH = PASCAL60,POWER8     # P100 hosted by an IBM Power8, etc
   KOKKOS_ARCH = KEPLER37,POWER8     # K80 hosted by an IBM Power8, etc

Using CMake:

::

   -DKokkos_ENABLE_CUDA=ON
   -DKokkos_ARCH_PASCAL60=ON -DKokkos_ARCH_POWER8=ON

For make with GPUs, the following 2 lines define a nvcc wrapper compiler, which will use
nvcc for compiling CUDA files or use a C++ compiler for non-Kokkos, non-CUDA
files.

::

   KOKKOS_ABSOLUTE_PATH = $(shell cd $(KOKKOS_PATH); pwd)
   export OMPI_CXX = $(KOKKOS_ABSOLUTE_PATH)/bin/nvcc_wrapper
   CC =		mpicxx

For CMake, copy cmake/presets/kokkos_cuda.cmake so OMPI_CXX and CC are set
properly.

.. note::

  that you cannot build one executable to run on multiple hardware
  targets (CPU or KNL or GPU).  You need to build SPARTA once for each
  hardware target, to produce a separate executable.

Using make:

::

   make yes-kokkos
   make machine

::

   make no-kokkos
   make machine

Using CMake:

::

   cmake -C /path/to/sparta/cmake/presets/machine.cmake /path/to/sparta/cmake
   make

::

   cmake -C /path/to/sparta/cmake/presets/machine.cmake -DPKG_KOKKOS=OFF /path/to/sparta/cmake
   make

Supporting info:
================

src/KOKKOS: filenames -> commands
src/KOKKOS/README
lib/kokkos/README
the :ref:`Accelerating SPARTA<accelerate-kokkos-package>` section
:ref:`Section 5.3<accelerate-kokkos-package>`
:ref:`Section 2.6 -k on ...<start-running-sparta>`
:ref:`Section 2.6 -sf kk<start-running-sparta>`
:ref:`Section 2.6 -pk kokkos<start-running-sparta>`
:ref:`package kokkos<package>`
`Benchmarks page <http://sparta.sandia.gov/bench.html>`__ of web site

