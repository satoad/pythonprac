from unittest import main, TestCase
from moodserver.__main__ import serve
import moodclient
import socket
import time
from asyncio import run
import cowsay
import multiprocessing




class Test_Server(TestCase):
    def send_recv(s, data):
        s.send(data.encode())
        return s.recv(1024).decode()

    @classmethod
    def setUpClass(cls):
        cls.proc = multiprocessing.Process(target=serve)
        cls.proc.start()

        time.sleep(2)

    def setUp(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.connect(("localhost", 1337))
        self.s = _socket

    
    def test_1(self):
        self.s.send("cat".encode())
        buff = Test_Server.send_recv(self.s, 'addmon dragon hp 999 coords 6 9 hello "Who goes there?"\n')
        self.assertEqual(buff, 'You are not logged in.\n')

    def test_2(self):
        self.s.send("cat\n".encode())
        buff = Test_Server.send_recv(self.s, "up\n")
        self.assertEqual(buff, 'You are not logged in.\n')
        buff = Test_Server.send_recv(self.s, "right\n")
        self.assertEqual(buff, 'You are not logged in.\n')
    
    def test_3(self):
        self.s.send("milk\n".encode())
        Test_Server.send_recv(self.s, "addmon default hello hi coords 0 0 hp 15\n")
        buff = Test_Server.send_recv(self.s, "attack default 10\n")
        self.assertEqual(buff, 'You are not logged in.\n')



    def tearDown(self):
        self.s.close()

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
