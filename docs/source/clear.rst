
:orphan:



.. index:: clear



.. _clear:




.. _clear-command:



#############
clear command
#############




.. _clear-syntax:



*******
Syntax:
*******





::



   clear




.. _clear-examples:



*********
Examples:
*********





::



   (commands for 1st simulation)
   clear
   (commands for 2nd simulation)




.. _clear-descriptio:



************
Description:
************




This command deletes all atoms, restores all settings to their default
values, and frees all memory allocated by SPARTA.  Once a clear
command has been executed, it is almost as if SPARTA were starting
over, with only the exceptions noted below.  This command enables
multiple jobs to be run sequentially from one input script.



These settings are not affected by a clear command: the working
directory (:ref:`shell<shell>` command), log file status
(:ref:`log<log>` command), echo status (:ref:`echo<echo>` command), and
input script variables (:ref:`variable<variable>` command).



.. _clear-restrictio:



*************
Restrictions:
*************




none



.. _clear-related-commands:



*****************
Related commands:
*****************




none



.. _clear-default:



********
Default:
********




none



