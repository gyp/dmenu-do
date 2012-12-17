
from util import patch_config_parser

from dmenudo.freedesktop_menu import FreeDesktopMenu


from mock import patch
from unittest import TestCase

class FreeDesktopMenuTest(TestCase):
    """
    NOTE: this is not a real unit test rather a functional/learning test. The class itself
    depends heavily on the underlying XDG classes to work as they should and that the
    user has various given things installed. Yeah, that sucks.
    """
    def setUp(self):
        self.menu = FreeDesktopMenu()
        self.entries = self.menu.getEntries()

    def test_getentries_returns_a_list_of_strings(self):
        for entry in self.entries:
            self.assertIsInstance(entry, unicode)

    def test_getentries_list_is_not_empty(self):
        self.assertGreater(len(self.entries), 0)

    def test_getentries_lists_toplevel_elements(self):
        self.assertTrue(u'Mines' in self.entries)

    def test_getentries_lists_elements_in_application_menu(self):
        self.assertTrue(u'GIMP Image Editor' in self.entries)

    def test_getexec_returns_executable_for_name(self):
        self.assertEqual('gimp-2.6', self.menu.getExec(u'GIMP Image Editor'))
