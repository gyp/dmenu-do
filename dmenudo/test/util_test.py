
from dmenudo.util import *

from unittest import TestCase


class UtilTest(TestCase):

  def test_home(self):
    self.assertNotEquals('~/', home('~/'))
    self.assertEquals('/bin', home('/bin'))

  def test_execute(self):
    execute('ls')

  def test_is_executable(self):
    self.assertTrue(is_executable('/bin/sh'))
    self.assertFalse(is_executable('/etc/hosts'))
    self.assertFalse(is_executable('/doesnt_exist'))

  def test_is_directory(self):
    self.assertTrue(is_directory('/bin'))
    self.assertFalse(is_directory('/etc/hosts'))
    self.assertFalse(is_directory('/doesnt_exist'))

  def test_calculate(self):
    self.assertEqual(str(calculate("2+2")), "4")
    self.assertEqual(str(calculate("10/4")), "2")
    self.assertEqual(str(calculate("10.0/4")), "2.5")
    self.assertEqual(str(calculate("log10(100)")), "2.0")
    self.assertEqual(str(calculate("foobar((/234")), "invalid syntax!")
