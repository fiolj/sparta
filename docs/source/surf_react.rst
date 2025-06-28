
:orphan:

.. index:: surf_react

.. _surf-react:

.. _surf-react-command:

##################
surf_react command
##################

**"surf_react adsorb"_surf_react_adsorb.html** command

.. _surf-react-syntax:

*******
Syntax:
*******

::

   surf_react ID style args

- ID = user-assigned name for the surface reaction model 

- style = *global* or *prob* or *adsorb* or *global/kk* or *prob/kk*

- args = arguments for that style

::

     *global* or *global/kk* args = pdelete pcreate
       pdelete = probability that surface collision removes the incident particle
       pcreate = probability that surface collision clones the incident particle
     *prob* or *prob/kk* args = infile
       infile = file with list of surface chemistry reactions 
     *adsorb* args = model infile(s) n=Nsync type temp n_sites adsp1 adsp2 ...
       model = *gs* or *ps* or *gs/ps*
         gs = gas-surface reactions
         ps = pure-surface reactions
         gs/ps = both gas-surface and pure-surface reactions
       infile(s) = file(s) with list of surface chemistry reactions
                   one file for model gs or ps
                   two files for model gs/ps, gs first, ps second
       Nsync = perform PS reactions and sync across processors every this many timesteps
       type = *face* or *surf*
         face = domain boundary treated as a surface
         surf = surface elements = triangles in 3d, lines in 2d 
       temp = temperature of the surface
       n_sites = # of available adsorption sites per unit area (3D) or length (2D)
       adsp1,adsp2,... = list of species that can adsorb on surface

.. _surf-react-examples:

*********
Examples:
*********

::

   surf_react 1 global 0.2 0.15
   surf_react 1 prob air.surf  
   surf_react 1 adsorb gs gs_react.surf nsync 10 surf 1000 6.022e18 O CO
   surf_react 1 adsorb gs/ps gs_react.surf ps_react.surf nsync 1 face 300 3e9 O

.. _surf-react-descriptio:

************
Description:
************

Define a model for surface chemistry reactions occurring when
particles collide with surface elements or the global boundaries of
the simulation box.  The *asorb* model also has an option to encode
chemical reactions that can occur on the surface itself.

One or more models can be defined and assigned to different surfaces
or simulation box boundaries via the :ref:`surf_modify<surf-modify>` or
:ref:`bound_modify<bound-modify>` commands.  See :ref:`Section 6.9<howto-69-details-surfaces-sparta>` for more details of how SPARTA defines
surfaces as collections of geometric elements, triangles in 3d and
line segments in 2d.  Also see the :ref:`react<react>` command for
specification of a gas-phase chemistry reaction model.

The ID for a surface reaction model is used to identify it in other
commands.  Each surface reaction model ID must be unique.  The ID can
only contain alphanumeric characters and underscores.

The surface reaction models for the different styles are described
below.  When a a particle collides with a surface element or boundary,
the list of all reactions possible with that species as a reactant is
looped over.  A probability for each reaction is calculated, using the
formulas discussed below, and a random number is used to decide which
reaction (if any) takes place.  A check is made that the sum of
probabilities for all possible reactions is <= 1.0, which should
normally be the case if reasonable reaction coefficients are defined.

.. important::

  A surface reaction model cannot be specified for
  surfaces whose surface collision style does not support reactions.
  Currently this is only the *vanish* collision style.  See the
  :ref:`surf_collide<surf-collide>` doc page for details.

The *global* style is a simple model that can be used to test whether
surface reactions are occurring as expected.  There is no list of
reactions for different species; all species are treated the same.
This style thus defines two universal reactions, the first for
particle deletion, the second for particle creation.

The *global* style takes two parameters, *pdelete* and *pcreate*. The
first is the probability that a "deletion" reaction takes place when a
collision occurs.  If it does, the particle is deleted.  The second is
the probablity that a "creation" reaction occurs, which clones the
particle, so that one particle becomes two.  The two particles leave
the surface according to whatever surface collision model is defined
by the :ref:`surf_collide<surf-collide>` command, and is assigned to
that surface/boundary by the :ref:`surf_modify collide<surf-modify>`
command.

The sum of *pdelete* and *pcreate* must be <= 1.0.

.. note::

  that if you simply wish to delete all particles which hit the
  surface, you can use the :ref:`surf_collide vanish<surf-collide>`
  command, which is simpler.

For the *prob* style, a file is specified which contains a list of
surface chemical reactions, with their associated parameters.  The
reactions are read into SPARTA and stored in a list.  Each time a
simulation is run via the :ref:`run<run>` command, the list is scanned.
Only reactions for which all the reactants and all the products are
currently defined as species-IDs will be active for the simulation.
Thus the file can contain more reactions than are used in a particular
simulation.  See the :ref:`species<species>` command for how species
IDs are defined.  This style thus defines N reactions, where
N is the number of reactions listed in the specified file.

As explained below each reaction has a specified probability between
0.0 and 1.0.  That probability is used to choose which reaction (if
any) is performed.

The format of the input surface reaction file is as follows.  Comments
or blank lines are allowed in the file.  Comment lines start with a
"#" character.  All other entries must come in 2-line pairs with
values separated by whitespace in the following format

::

   R1 --> P1 + P2
   type style C1 C2 ...

The first line is a text-based description of a single reaction.  R1
is a single reactant for the particle that collides with the
surface/boundary, listed as a :ref:`species<species>` IDs.  P1 and P2
are one or two products, also listed as :ref:`species<species>` IDs.
The number of reactants is always 1.  The number of allowed products
depends on the reaction type, as discussed below.  Individual
reactants and products must be separated by whitespace and a "+" sign.
The left-hand and right-hand sides of the equation must be separated
by whitespace and "-->".

The *type* of each reaction is a single character (upper or lower
case) with the following meaning.  The type determines how many
reactants and products can be specified in the first line.

::

   D = dissociation = 1 reactant and 2 products
   E = exchange = 1 reactant and 1 product
   R = recombination = 1 reactant and 1 product named NULL

A dissociation reaction means that R1 dissociates into P1 and P2 when
it collides with the surface/boundary.  There is no restriction on the
species involved in the reaction.

An exchange reaction is a collision where R1 becomes a new product P1.
There is no restriction on the species involved in the reaction.

A recombination reaction is a collision where R1 is absorbed by the
surface, so that the particle disappears.  There are no products which
is indicated in the file by listing a single product as NULL.
There is no restriction on the species involved in the reaction.

The *style* of each reaction is a single character (upper or lower
case) with the following meaning:

   - S = Surface

The style determines how many reaction coefficients are listed as C1,
C2, etc, and how they are interpreted by SPARTA.

For S = Surface style, there are two coefficients. The first is
required and the second is optional and will be set to 0.0 if not
specified:

   - C1 = probability that the reaction occurs (0.0 to 1.0)
   - C2 = catalytic chemical energy of reaction (optional, positive for exothermic)

For the *adsorb* style, gas particles can adsorb on the surface.
Adsorbed particles can then undergo reactions with other adsorbed
particles as well as with new gas-phase particles that strike the
surface.  Each surface element stores its "state" for the counts of
different particle species currently adsorbed on the element, which
alters the probablity for future reactions to take place.

A detailed description of the *adsorb* style and the list of reactions
it supports is given on a separate
:ref:`surf_react_adsorb<surf-react-adsorb>` doc page.

If the ambipolar approximation is being used, via the 
:ref:`fix ambipolar<fix-ambipolar>` command, then reactions which involve
either ambipolar ions or the ambipolar electron have more restricitve
rules about the ordering of reactants and products, than those
described in the preceeding section for the *prob* style.

The first is an "exchange" reaction which converts an ambipolar ion
into a neutral species.  Internally this removes the ambipolar
electron associated with the ion.  In the file of reactions this is
done by having the reactant be an ambipolar ion, and the product not
be an ambipolar ion.

The second is a "dissociation" reaction where a neutral species is
ionized by colliding with the surface/boundary, creating an ambipolar
ion and ambipolar electron.  In the file of reactions this is done by
having the reactant not be an ambipolar ion, the first product be an
ambipolar ion, and the second product be an ambipolar electron.  The
two products must be specified in this order.

.. _surf-react-output-info:

************
Output info:
************

All the surface reaction models calculate a global vector of values.
The values can be used by the :ref:`stats_style<stats-style>` command
and by :ref:`variables<variable>` that define formulas.  The latter
means they can be used by any command that uses a variable as input,
e.g. "the :ref:`fix ave/time<fix-ave-time>` command.  See :ref:`Section 4.4<howto-64-output-sparta-(stats,>` for an overview of SPARTA output
options.

The *global*, *prob*, and *adsorb* styles each compute a vector of
length 2 + 2\*nlist.  For the *global* style, nlist = 2, for "delete"
and "create" reactions.  For the *prob* style, nlist is the number of
reactions listed in the file is read as input.  For the *adsorb*
style, nlist is the sum of both the gas-surface and pure-surface
reactions listed in the file(s) read as input.

The first element of the vector is the count of particles that
performed surface reactions for surface elements assigned to this
reaction model during the current timestep.  The second element is the
cummulative count of particles that have performed reactions since the
beginning of the current run.  The next nlist elements are the count
of each individual reaction that occurred during the current timestep.
The final nlist elements are the cummulative count of each individual
reaction since the beginning of the current run.

Styles with a *kk* suffix are functionally the same as the
corresponding style without the suffix.  They have been optimized to
run faster, depending on your available hardware, as discussed in the
:ref:`Accelerating SPARTA<accelerate>` section of the manual.
The accelerated styles take the same arguments and should produce the
same results, except for different random number, round-off and
precision issues.

These accelerated styles are part of the KOKKOS package. They are only
enabled if SPARTA was built with that package.  See the :ref:`Making SPARTA<start-making-sparta-optional-packages>` section for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the :ref:`-suffix command-line switch<start-commandlin-options>` when you invoke SPARTA, or you can
use the :ref:`suffix<suffix>` command in your input script.

See the :ref:`Accelerating SPARTA<accelerate>` section of the
manual for more instructions on how to use the accelerated styles
effectively.

.. _surf-react-restrictio:

*************
Restrictions:
*************

If specified with a *kk* suffix, this command can be used no more than
twice in the same input script (active at the same time).

.. _surf-react-related-commands:

*****************
Related commands:
*****************

:ref:`react<react>`, :ref:`surf_modify<surf-modify>`,
:ref:`bound_modify<bound-modify>`,
:ref:`surf_react_adsorb<surf-react-adsorb>`

.. _surf-react-default:

********
Default:
********

none

