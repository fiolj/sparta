# ----------------------------------------------------------------------
#   SPARTA - Stochastic PArallel Rarefied-gas Time-accurate Analyzer
#   http://sparta.sandia.gov
#   Steve Plimpton, sjplimp@sandia.gov, Michael Gallis, magalli@sandia.gov
#   Sandia National Laboratories
#
#   Copyright (2012) Sandia Corporation.  Under the terms of Contract
#   DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains
#   certain rights in this software.  This software is distributed under
#   the GNU General Public License.
#
#   See the README file in the top-level SPARTA directory.
# -------------------------------------------------------------------------

# Python wrapper on SPARTA library via ctypes
# Version for python 3

import sys
import traceback
import types
from ctypes import *

from collections.abc import Iterable   # drop `.abc` with Python 2.7 or lower


def ensurebytes(data):
  """Returns bytes from strings.
  It works for a single string and for a list/tuple of them """
  if isinstance(data, bytes):
    return data
  if isinstance(data, str):
    return data.encode('utf-8')
  if isinstance(data, Iterable):
    return [ensurebytes(x) for x in data]
  return data


class sparta:
  def __init__(self, name="", cmdargs=None):

    # load libsparta.so by default
    # if name = "g++", load libsparta_g++.so

    try:
      if not name: self.lib = CDLL("libsparta.so", RTLD_GLOBAL)
      else: self.lib = CDLL(f"libsparta_{name}.so", RTLD_GLOBAL)
    except BaseException:
      type, value, tb = sys.exc_info()
      traceback.print_exception(type, value, tb)
      raise OSError("Could not load SPARTA dynamic library")

    # create an instance of SPARTA
    # don't know how to pass an MPI communicator from PyPar
    # no_mpi call lets SPARTA use MPI_COMM_WORLD
    # cargs = array of C strings from args

    if cmdargs:
      cmdargs.insert(0, b"sparta.py")
      cmdargs = ensurebytes(cmdargs)
      narg = len(cmdargs)
      cargs = (c_char_p * narg)(*cmdargs)
      self.spa = c_void_p()
      self.lib.sparta_open_no_mpi(narg, cargs, byref(self.spa))
    else:
      self.spa = c_void_p()
      self.lib.sparta_open_no_mpi(0, None, byref(self.spa))
      # could use just this if SPARTA lib interface supported it
      # self.spa = self.lib.sparta_open_no_mpi(0,None)

  def __del__(self):
    if self.spa: self.lib.sparta_close(self.spa)

  def close(self):
    self.lib.sparta_close(self.spa)
    self.spa = None

  def file(self, filename):
    self.lib.sparta_file(self.spa, ensurebytes(filename))

  def command(self, cmd):
    self.lib.sparta_command(self.spa, ensurebytes(cmd))

  def extract_global(self, name, type):
    if type == 0:
      self.lib.sparta_extract_global.restype = POINTER(c_int)
    elif type == 1:
      self.lib.sparta_extract_global.restype = POINTER(c_double)
    else: return None
    ptr = self.lib.sparta_extract_global(self.spa, ensurebytes(name))
    return ptr[0]

  def extract_compute(self, id, style, type):
    Id = ensurebytes(id)
    if type == 0:
      if style > 0: return None
      self.lib.sparta_extract_compute.restype = POINTER(c_double)
      ptr = self.lib.sparta_extract_compute(self.spa, Id, style, type)
      return ptr[0]
    if type == 1:
      self.lib.sparta_extract_compute.restype = POINTER(c_double)
      ptr = self.lib.sparta_extract_compute(self.spa, Id, style, type)
      return ptr
    if type == 2:
      self.lib.sparta_extract_compute.restype = POINTER(POINTER(c_double))
      ptr = self.lib.sparta_extract_compute(self.spa, Id, style, type)
      return ptr
    return None

  # free memory for 1 double or 1 vector of doubles via sparta_free()
  # for vector, must copy nlocal returned values to local c_double vector
  # memory was allocated by library interface function

  def extract_variable(self, name, type):
    nname = ensurebytes(name)
    if type == 0:
      self.lib.sparta_extract_variable.restype = POINTER(c_double)
      ptr = self.lib.sparta_extract_variable(self.spa, nname)
      result = ptr[0]
      self.lib.sparta_free(ptr)
      return result
    if type == 1:
      self.lib.sparta_extract_global.restype = POINTER(c_int)
      nlocalptr = self.lib.sparta_extract_global(self.spa, b"nplocal")
      nlocal = nlocalptr[0]
      result = (c_double * nlocal)()
      self.lib.sparta_extract_variable.restype = POINTER(c_double)
      ptr = self.lib.sparta_extract_variable(self.spa, nname)
      for i in range(nlocal): result[i] = ptr[i]
      self.lib.sparta_free(ptr)
      return result
    return None
