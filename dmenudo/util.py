# Copyright (C) 2012 Eyal Erez
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; if not,
# write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import logging as log
import os
import subprocess

def home(path):
  return path.replace('~', os.environ['HOME'])

def execute(command):
  '''Execute command'''
  log.debug('EXECUTE %s' % command)
  os.popen(command + '&')

def is_executable(path):
  '''Is this path an executable file'''
  return os.path.isfile(path) and os.access(path, os.X_OK)

def is_directory(path):
  '''Is this path a directory'''
  return os.path.isdir(path)

def calculate(expression):
  '''Return the results for a numeric expression'''
  # code based on http://lybniz2.sourceforge.net/safeeval.html
  import math
  safe_calls = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees',
                'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log',
                'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
  # use the list to filter the local namespace
  safe_dict = dict([ (k, math.__dict__.get(k, None)) for k in safe_calls ])
  #add any needed builtins back in.
  safe_dict['abs'] = abs
  try:
      return eval(expression, {"__builtins__":None}, safe_dict)
  except:
      return "invalid syntax!"
