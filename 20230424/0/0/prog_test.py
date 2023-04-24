import unittest
import prog
import client

class Testing(unittest.TestCase):
    def test_1(self):
        self.assertEqual(prog.sqroots("a a a ab a"), ("5 words entered"))
