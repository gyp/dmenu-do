# Copyright (C) 2012 Peter Gyongyosi
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
import xdg.Menu
import re

class FreeDesktopMenu(object):

    def __init__(self):
        self.root = xdg.Menu.parse()

    def getEntries(self):
        xdg_entries = self.__getDesktopEntries(self.root)
        entries = []
        for entry in xdg_entries:
            entries.append(entry.DesktopEntry.getName())
        return entries

    def __getDesktopEntries(self, menu = None):
        entries = []
        if not menu:
            menu = self.root

        for entry in menu.getEntries():
            if isinstance(entry, xdg.Menu.Menu):
                entries = entries + self.__getDesktopEntries(entry)
            elif isinstance(entry, xdg.Menu.MenuEntry):
                entries.append(entry)
        return entries

    def getExec(self, name):
        xdg_entries = self.__getDesktopEntries(self.root)
        for entry in xdg_entries:
            desktop_entry = entry.DesktopEntry
            if desktop_entry.getName() == name:
                return self.__prepareExecCommand(desktop_entry)

        return None

    def __prepareExecCommand(self, desktop_entry):
        exec_command = desktop_entry.getExec()
        # Remove deprecated field codes, as the spec dictates.
        exec_command = re.sub(r'%[dDnNvm]', '', exec_command)

        # Remove all other field codes which we do not support
        # uU: URL
        # fF: filename
        # c: application name
        # i: icon
        # k: desktop file

        exec_command = re.sub(r'%[uUfFcik]', '', exec_command)
        exec_command = exec_command.strip()

        return exec_command
