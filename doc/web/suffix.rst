:orphan:

.. _command-suffix:

##############
suffix command
##############

**Syntax:**

::

   suffix style args 

-  style = *off* or *on* or *kk*

**Examples:**

::

   suffix off
   suffix on
   suffix kk 

**Description:**

This command allows you to use variants of various styles if they exist.
In that respect it operates the same as the `-suffix command-line
switch <Section_start.html#start_6>`__. It also has options to turn off
or back on any suffix setting made via the command line.

The specified style *kk* refers to the optional KOKKOS package that
SPARTA can be built with, as described in `this section of the
manual <Section_start.html#start_3>`__. The KOKKOS package is a
collection of styles optimized to run using the Kokkos library on
various kinds of hardware, including GPUs via CUDA and many-core chips
via OpenMP multi-threading.

As an example, the KOKKOS package provides a `compute_style
temp <compute_temp.html>`__ variant, with style name temp/kk. A variant
style can be specified explicitly in your input script, e.g. compute
temp/kk. If the suffix command is used with the appropriate style, you
do not need to modify your input script. The specified suffix (kk) is
automatically appended whenever your input script command creates a new
`fix <fix.html>`__, `compute <compute.html>`__, etc. If the variant
version does not exist, the standard version is created.

If the specified style is *off*, then any previously specified suffix is
temporarily disabled, whether it was specified by a command-line switch
or a previous suffix command. If the specified style is *on*, a disabled
suffix is turned back on. The use of these 2 commands lets your input
script use a standard SPARTA style (i.e. a non-accelerated variant),
which can be useful for testing or benchmarking purposes. Of course this
is also possible by not using any suffix commands, and explicitly
appending or not appending the suffix to the relevant commands in your
input script.

**Restrictions:** none

**Related commands:**

:ref:`Command-line switch -suffix <start-command-line-options>`

**Default:** none
