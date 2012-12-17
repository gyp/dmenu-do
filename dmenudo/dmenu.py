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

import os
from subprocess import Popen, PIPE
import logging as log

from util import execute, home, is_directory, is_executable, calculate

class DMenu(object):

  def __init__(self, config, history, freedesktop_menu):
    self._current = None
    self._config = config
    self._history = history
    self._freedesktop_menu = freedesktop_menu

  def run(self, command=''):
    '''Run the dmenu command recursively'''
    items = []
    # user entered something
    if command:
      new_items = self._handle_command(command)
      if not new_items:
          # this means that the command was actually a final that we started, nothing else to do
          return
      items += new_items
    else:
      # default initial listing
      items = self._history.keys() + \
              self._config.folders + \
              list(self._config.session.keys()) + \
              sorted(self._config.executables) + \
              self._freedesktop_menu.getEntries()
    # Open the dmenu command
    proc = Popen(self._config.dmenu, shell=False, stdout=PIPE, stdin=PIPE)
    # Run dmenu with the items defined above
    for item in items:
      proc.stdin.write(item)
      proc.stdin.write('\n')
    command = proc.communicate()[0]
    # If we got something back, run dmenu again
    if command:
      self.run(command.strip())

  def _handle_command(self, command):
    if not self._current:
      # try to process the command as a toplevel stuff
      if self._try_as_toplevel_command(command):
          return None

      # try it as a calculate expression
      calculate_result = self._try_as_calculate(command)
      if calculate_result:
          return calculate_result

    # fall back to handling as a file / directory
    return self._open_file_or_directory(command)

  def _try_as_toplevel_command(self, command):
      if command in self._history:
        log.debug('HISTORY: %s' % command)
        # This is a history command, so run it.
        self._history.execute(command)
        return True
      if command in self._config.session.keys():
        log.debug('SESSION: %s' % command)
        # This is a session command, so run it.
        execute(self._config.session[command])
        return True

      freedesktop_exec = self._freedesktop_menu.getExec(command)
      if freedesktop_exec:
        log.debug('FREEDESKTOP MENU: %s' % command)
        # no need to add it to the history, we'll find it anyway
        execute(freedesktop_exec)
        return True

      if command in self._config.executables:
        log.debug('EXECUTABLE: %s' % command)
        self._history.add_executable(command)
        # This is an executable, so run it.
        execute(command)
        return True

  def _try_as_calculate(self, command):
      if command[0] == '=':
        log.debug('CALCULATION: %s' % command)
        result = calculate(command[1:])
        return ['%s' % result]

  def _open_file_or_directory(self, filename):
    # Otherwise, we must be walking a path, so join our current path
    if self._current:
        path = os.path.join(self._current, home(filename))
    else:
        path = home(filename)

    if is_directory(path):
      log.debug('DIRECTORY: %s' % filename)
      # Update current path
      self._current = path
      # This is a directory, so we are going to list all child files and folders.
      items = ['..'] + os.listdir(path)
      return items
    elif is_executable(filename):
      # This is a full path executable, so run it.
      log.debug('EXECUTABLE: %s' % filename)
      execute(filename, path)
      return
    else:
      # This is just a file, use mailcap and try to find the right program to run it.
      log.debug('FILE: %s' % path)
      self._history.add_file(filename, path)
      execute('edit "%s"' % path)
      return
