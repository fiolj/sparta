# -*- coding: utf-8 -*-
"""
    pygments.lexers.sparta
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for SPARTA scripts.

    :copyright: Copyright 2020- by J. Fiol.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, words, bygroups
from pygments.token import Comment, Keyword, String, Name, Text

__all__ = ['SpartaLexer']


class SpartaLexer(RegexLexer):
  """Lexer for SPARTA input file."""
  name = 'Sparta'
  aliases = ['sparta']
  filenames = ['*.in', 'in.*']
  mimetypes = ['text/x-ini', 'text/inf']

  tokens = {
      'root': [
          (r'\s+', Text),       # If spaces, do not highlight
          (r'#.*$', Comment),   # If starts with "#" is a comment
          (words((  # All SPARTA commands at the beginning as builtins
              'adapt_grid', 'balance_grid', 'bound_modify', 'boundary', 'clear',
              'collide_modify', 'collide', 'compute', 'create_box',
              'create_grid', 'dimension', 'dump', 'dump_modify', 'echo', 'fix',
              'global', 'group', 'if', 'include', 'jump', 'label', 'log',
              'mixture', 'move_surf', 'next', 'package', 'partition', 'print',
              'quit', 'react_modify', 'react', 'read_grid', 'read_isurf',
              'read_particles', 'read_restart', 'read_surf',
              'region', 'remove_surf', 'reset_timestep',
              'restart', 'run', 'scale_particles', 'seed', 'shell',
              'species', 'stats_modify', 'stats_style', 'stats', 'suffix',
              'surf_collide', 'surf_modify', 'surf_react', 'timestep',
              'uncompute', 'undump', 'unfix', 'units', 'variable',
              'write_grid', 'write_isurf', 'write_restart', 'write_surf'),
              prefix=r'^', suffix=r'\b'), Name.Builtin),
          (words((
              'surf', 'grid', 'particle', 'ave/', 'distsurf/', 'eflux/',
              'property/', 'react/', 'thermal/', 'emit/', 'face'),
              prefix=r'\b', suffix=r'\b'), Keyword),

          (r'"(""|[^"])*"', String.Double),

          # ('([rR]|[uUbB][rR]|[rR][uUbB])(")',  # Between '"' are strings
          #  bygroups(String.Affix, String.Double), 'dqs'),

          # (r'((?:Sub)?Section)(\s+)("\w+")',
          #  bygroups(String.Escape, Text, String.Escape)),
          # (r'(End(|Sub)Section)', String.Escape),

          # (r'(^\w+)(\s+)([^\n#]+)',
          #  bygroups(Name.Builtin, Text, Text)),
          # (r'(^\w+)(\s*)',
          #  bygroups(Name.Builtin, Text)),
      ],
  }
