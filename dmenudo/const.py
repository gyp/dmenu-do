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

from util import home

## File used to read configuration
CONFIG_FILE  = home('~/.dmenu-do.conf')
SEC_SESSION  = 'Session'
SEC_LOGGING  = 'Logging'
SEC_HISTORY  = 'History'
SEC_BROWSE   = 'Browse'
SEC_COMMANDS = 'Commands'
OPT_FILE     = 'file'
OPT_LEVEL    = 'level'
OPT_DIRS     = 'dirs'
OPT_DMENU    = 'dmenu'
OPT_EXEC     = 'executables'
OPT_EXECUTABLE_DIRS = 'executable_dirs'
