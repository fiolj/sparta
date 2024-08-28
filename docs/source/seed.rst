
:orphan:



.. index:: seed



.. _seed:




.. _seed-command:



############
seed command
############




.. _seed-syntax:



*******
Syntax:
*******





::



   seed Nvalue




Nvalue = seed for a random number generator (positive integer)




.. _seed-examples:



*********
Examples:
*********





::



   seed 5838959




.. _seed-descriptio:



************
Description:
************




This command sets the random number seed for a master random number
generator.  This generator is used by SPARTA to initialize auxiliary
random number generators, which in turn are used for all operations in
the code requiring random numbers.  This means you can effectively run
a statistically-independent simulation by simply changing this single
seed.



The various random number generators used in SPARTA are portable,
which means they produce the same random number streams on any
machine.



This command is required to perform a SPARTA simulation.



.. _seed-restrictio:



*************
Restrictions:
*************




none



.. _seed-related-commands:



*****************
Related commands:
*****************




none



.. _seed-default:



********
Default:
********




none



