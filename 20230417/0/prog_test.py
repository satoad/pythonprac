import unittest
import prog
import client

class Testing(unittest.TestCase):
    def test_1(self):
        self.assertEqual(prog.sqroots("1 3 2"), (-2.0, -1.0))

    def test_2(self):
        self.assertEqual(prog.sqroots("1 4 4"), (-2, -2))
        
    def test_3(self):
        self.assertEqual(prog.sqroots("1 2 1"), (-1, -1))

    def test_exception(self):
        with self.assertRaises(AttributeError):
            prog.sqroots("5 2 3")

class TestServer(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.proc = multiprocessing.Process(target=server.serve)
        cls.proc.start()
        time.sleep(2) 

    def setUp(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.connect(("localhost", 1337))
        self.s = _socket

    def test_server1(self):
        self.assertEqual(client.sqrootnet("1 2 1", self.s), "-1.00\n")

    def test_server2(self):
        self.assertEqual(client.sqrootnet("1 2 0", self.s), "-2.00 0.00\n")

    def test_server3(self):
        self.assertEqual(client.sqrootnet("1 2 3", self.s), "\n")

    def test_server4(self):
        self.assertEqual(sqroots.sqrootnet("1 2", self.s), "\n")

    def test_server5(self):
        self.assertEqual(sqroots.sqrootnet("0 2 3", self.s), "\n")

    def tearDown(self):
        self.s.close()
    
    @classmethod
    def tearDownClass(cls):
        cls.socket.close()
        cls.proc.terminate()
