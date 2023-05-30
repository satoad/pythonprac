from unittest import main, TestCase
from unittest.mock import MagicMock
from moodclient.mymud import Game
import sys
from io import StringIO

class Test_Client(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.socket = MagicMock()
        cls.res = []
        cls.socket.send = lambda x: cls.res.append(x)
        cls.cmd = Game(cls.socket)


    def test_1_addmon(self):
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        Test_Client.cmd.onecmd("addmon dragon")
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), "Invalid arguments\n")

    def test_2_addmon(self):
        Test_Client.cmd.onecmd('addmon dragon hp 999 coords 6 9 hello "Who goes there?"\n')
        self.assertEqual(Test_Client.res[-1].decode(), 'addmon dragon hp 999 coords 6 9 hello "Who goes there?"\n')

    def test_1_attack(self):
        Test_Client.cmd.onecmd("attack dragon")
        self.assertEqual(Test_Client.res[-1].decode(), 'attack dragon sword\n')

    def test_2_attack(self):
        Test_Client.cmd.onecmd("attack dragon with spear")
        self.assertEqual(Test_Client.res[-1].decode(), 'attack dragon spear\n')
