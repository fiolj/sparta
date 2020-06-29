:orphan:

.. index:: surf_react



.. _command-surf-react:

##################
surf_react command
##################


*******
Syntax:
*******

::

   surf_react ID style args 

-  ID = user-assigned name for the surface reaction model
-  style = *global* or *prob*
-  args = arguments for that style

   ::

        global args = pdelete pcreate
          pdelete = probability that surface collision removes the incident particle
          pcreate = probability that surface collision clones the incident particle
        prob args = infile
          infile = file with list of surface chemistry reactions 

*********
Examples:
*********

::

   surf_react global 0.2 0.15
   surf_react prob air.surf 

************
Description:
************

Define a model for surface chemistry reactions to perform when particles
collide with surface elements or the global boundaries of the simulation
box. One or more models can be defined and assigned to different
surfaces or simulation box boundaries via the
:ref:`surf_modify<command-surf-modify>` or
:ref:`bound_modify<command-bound-modify>` commands. See :ref:`Section 6.9<howto-surfaces>` for more details of how SPARTA
defines surfaces as collections of geometric elements, triangles in 3d
and line segments in 2d. Also see the :ref:`react<command-react>` command for
specification of a gas-phase chemistry reaction model.

The ID for a surface reaction model is used to identify it in other
commands. Each surface reaction model ID must be unique. The ID can only
contain alphanumeric characters and underscores.

The surface reaction models for the various styles are described below.
When a a particle collides with a surface element or boundary. the list
of all reactions possible with that species as the reactant is looped
over. A probability for each reaction is calculated, using the formulas
discussed below, and a random number is used to decide which reaction
(if any) takes place. A check is made that the sum of probabilities for
all possible reactions is <= 1.0, which should normally be the case if
reasonable reaction coefficients are defined.

.. important:: A surface reaction model can not be specified for surfaces whose surface collision style does not support reactions.  Currently this is only the *vanish* collision style. See the :ref:`surf_collide<command-surf-collide>` doc page for details.

--------------

The *global* style is a simple model that can be used to test whether
surface reactions are occurring as expected. There is no list of
reactions for different species; all species are treated the same. This
style thus defines two universal reactions, the first for particle
deletion, the second for particle creation.

The *global* style takes two parameters, *pdelete* and *pcreate*. The
first is the probability that a "deletion" reaction takes place when a
collision occurs. If it does, the particle is deleted. The second is the
probablity that a "creation" reaction occurs, which clones the particle,
so that one particle becomes two. The two particles leave the surface
according to whatever surface collision model is defined by the
:ref:`surf_collide<command-surf-collide>` command, and is assigned to that
surface/boundary by the :ref:`surf_modify collide<command-surf-modify>`
command.

The sum of *pdelete* and *pcreate* must be <= 1.0.

Note that if you simply wish to delete all particles which hit the
surface, you can use the :ref:`surf_collide vanish<command-surf-collide>`
command, which is simpler.

--------------

For the *prob* style, a file is specified which contains a list of
surface chemical reactions, with their associated parameters. The
reactions are read into SPARTA and stored in a list. Each time a
simulation is run via the :ref:`run<command-run>` command, the list is
scanned. Only reactions for which all the reactants and all the products
are currently defined as species-IDs will be active for the simulation.
Thus the file can contain more reactions than are used in a particular
simulation. See the :ref:`species<command-species>` command for how species
IDs are defined. This style thus defines N reactions, where N is the
number of reactions listed in the specified file.

As explained below each reaction has a specified probability between 0.0
and 1.0. That probability is used to choose which reaction (if any) is
performed.

The format of the input surface reaction file is as follows. Comments or
blank lines are allowed in the file. Comment lines start with a "#"
character. All other entries must come in 2-line pairs with values
separated by whitespace in the following format

::

   R1 --> P1 + P2
   type style C1 C2 ... 

The first line is a text-based description of a single reaction. R1 is a
single reactant for the particle that collides with the
surface/boundary, listed as a :ref:`species<command-species>` IDs. P1 and P2
are one or two products, also listed as :ref:`species<command-species>` IDs.
The number of reactants is always 1. The number of allowed products
depends on the reaction type, as discussed below. Individual reactants
and products must be separated by whitespace and a "+" sign. The
left-hand and right-hand sides of the equation must be separated by
whitespace and "-->".

The *type* of each reaction is a single character (upper or lower case)
with the following meaning. The type determines how many reactants and
products can be specified in the first line.

::

   D = dissociation = 1 reactant and 2 products
   E = exchange = 1 reactant and 1 product
   R = recombination = 1 reactant and 1 product named NULL 

A dissociation reaction means that R1 dissociates into P1 and P2 when it
collides with the surface/boundary. There is no restriction on the
species involved in the reaction.

An exchange reaction is a collision where R1 becomes a new product P1.
There is no restriction on the species involved in the reaction.

A recombination reaction is a collision where R1 is absorbed by the
surface, so that the particle disappears. There are no products which is
indicated in the file by listing a single product as NULL. There is no
restriction on the species involved in the reaction.

The *style* of each reaction is a single character (upper or lower case)
with the following meaning:

-  S = Surface

The style determines how many reaction coefficients are listed as C1,
C2, etc, and how they are interpreted by SPARTA.

For S = Surface style, there is a single coefficient:

-  C1 = probability that the reaction occurs (0.0 to 1.0)

--------------

If the ambipolar approximation is being used, via the :ref:`command-fix-ambipolar`, then reactions which involve
either ambipolar ions or the ambipolar electron have more restricitve
rules about the ordering of reactants and products, than those described
in the preceeding section for the *prob* style.

The first is an "exchange" reaction which converts an ambipolar ion into
a neutral species. Internally this removes the ambipolar electron
associated with the ion. In the file of reactions this is done by having
the reactant be an ambipolar ion, and the product not be an ambipolar
ion.

The second is a "dissociation" reaction where a neutral species is
ionized by colliding with the surface/boundary, creating an ambipolar
ion and ambipolar electron. In the file of reactions this is done by
having the reactant not be an ambipolar ion, the first product be an
ambipolar ion, and the second product be an ambipolar electron. The two
products must be specified in this order.

--------------

**Output info:**

All the surface reaction models calculate a global vector of values. The
values can be used by the :ref:`stats_style<command-stats-style>` command and
by :ref:`variables<command-variable>` that define formulas. The latter means
they can be used by any command that uses a variable as input, e.g. "the
:ref:`fix ave/time<command-fix-ave-time>` command. See :ref:`Section 4.4<howto-output>` for an overview of SPARTA output
options.

The *global* and *prob* styles each compute a vector of length 2 +
2*nlist. For the *global* style, nlist = 2, for "delete" and "create"
reactions. For the *prob* style, nlist is the number of reactions listed
in the file is read as input.

The first element of the vector is the count of particles that performed
surface reactions for surface elements assigned to this reaction model
during the current timestep. The second element is the cummulative count
of particles that have performed reactions since the beginning of the
current run. The next nlist elements are the count of each individual
reaction that occurred during the current timestep. The final nlist
elements are the cummulative count of each individual reaction since the
beginning of the current run.

--------------

*************
Restrictions:
*************
 none

*****************
Related commands:
*****************

:ref:`command-react`
:ref:`command-surf-modify`
:ref:`command-bound-modify`

********
Default:
********
 none
