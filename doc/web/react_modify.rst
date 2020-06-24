:orphan:

.. index:: react_modify



.. _command-react-modify:

####################
react_modify command
####################


**Syntax:**

::

   react_modify keyword values ...  

-  one or more keyword/value pairs may be listed
-  keywords = *recomb* or *rboost*

   ::

        recomb value = yes or no = enable or disable defined recombination reactions
        rboost value = rfactor
          rfactor = boost probability of recombination reactions by this factor 

**Examples:**

::

   react_modify recomb no
   react_modify rboost 100.0 

**Description:**

Set parameters that affect how reactions are performed.

The *recomb* keyword turns on or off recombination reactions. It is only
relevant if recombination reactions were defined in the reaction file
read in by the :ref:`react<command-react>` command. If the setting is *no*
then they will be disabled even if they were listed in the reaction
file. This is useful to turn recombination reactions off, to see if they
affect simulation results.

The *rboost* keyword is a setting for recombination reactions. It is
ignored if no recombination reactions exist, or the *recomb* keyword is
set to *no*. The *rboost* setting does not affect the overalll
statistical results of recombination reactions, but tries to improve
their computational efficiency. Recombination reactions typically occur
with very low probability, which means the code spends time testing for
reactions that rarely occur. If the *rfactor* is set to N > 1, then
recombination reactions are skipped N-1 out of N times, when one or more
such reactions is defined for a pair of colliding particles. A random
number us used to select on that probability. To compensate, when a
recombination reaction is actually tested for occurrence, its rate is
boosted by a factor of N, making it N times more likely to occur.

The smallest value *rboost* can be set to is 1.0, which effectively
applies no boost factor.

.. important:: Setting *rboost* too large could meant the probability of a recombination reaction becomes > 1.0, when it is does occur. SPARTA does not check for this, so you should estimate the largest boost factor that is safe to use for your model.

--------------

**Restrictions:** none

**Related commands:**

:ref:`command-react`

**Default:**

The option defaults are recomb = yes and rboost = 1000.0.
