
:orphan:



.. index:: stats



.. _stats:




.. _stats-command:



#############
stats command
#############




.. _stats-syntax:



*******
Syntax:
*******





::



   stats N




N = output statistics every N timesteps




.. _stats-examples:



*********
Examples:
*********





::



   stats 100




.. _stats-descriptio:



************
Description:
************




Compute and print statistical info (e.g. particle count, temperature)
on timesteps that are a multiple of N and at the beginning and end of
a simulation run.  A value of 0 will only print statistics at the
beginning and end.



The content and format of what is printed is controlled by the
:ref:`stats_style<stats-style>` and :ref:`stats_modify<stats-modify>`
commands.



The timesteps on which statistical output is written can also be
controlled by a :ref:`variable<variable>`.  See the :ref:`stats_modify every<stats-modify>` command.



.. _stats-restrictio:



*************
Restrictions:
*************




none



.. _stats-related-commands:



*****************
Related commands:
*****************




:ref:`stats_style<stats-style>`, :ref:`stats_modify<stats-modify>`



.. _stats-default:



********
Default:
********





::



   stats 0




