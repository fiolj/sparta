
:orphan:



.. index:: log



.. _log:




.. _log-command:



###########
log command
###########




.. _log-syntax:



*******
Syntax:
*******





::



   log file keyword




file = name of new logfile




keyword = *append* if output should be appended to logfile (optional)




.. _log-examples:



*********
Examples:
*********





::



   log log.equil
   log log.equil append




.. _log-descriptio:



************
Description:
************




This command closes the current SPARTA log file, opens a new file with
the specified name, and begins logging information to it.  If the
specified file name is *none*, then no new log file is opened.  If the
optional keyword *append* is specified, then output will be appended
to an existing log file, instead of overwriting it.



If multiple processor partitions are being used, the file name should
be a variable, so that different processors do not attempt to write to
the same log file.



The file "log.sparta" is the default log file for a SPARTA run.  The
name of the initial log file can also be set by the command-line
switch -log.  See :ref:`Section 2.6<start-running-sparta>` for
details.



.. _log-restrictio:



*************
Restrictions:
*************




none



.. _log-related-commands:



*****************
Related commands:
*****************




none



.. _log-default:



********
Default:
********




The default SPARTA log file is named log.sparta



