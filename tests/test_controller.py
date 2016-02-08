
import unittest
from unittest.mock import MagicMock
from ..controller import FlashlightController
from ..views.console_view import ConsoleView
from struct import *

TL_STRUCT = '>ch'
TLV_STRUCT = '>chBBB'


class TestControllerFunctions(unittest.TestCase):

    def setUp(self):
        view = ConsoleView()
        view.draw = MagicMock()
        self.controller = FlashlightController(view)
        self.dec = self.controller._decompose_tlv

    def test_decompose_empty_tlv(self):
        """empty command"""
        self.assertEqual(self.dec(""), {})

    def test_decompose_correct(self):
        """correct structures"""
        command = pack(TL_STRUCT,
            b"\x12", 0)
        self.assertEqual(self.dec(command), {b"\x12": None})

        command = pack(TL_STRUCT,
            b"\x13", 0)
        self.assertEqual(self.dec(command), {b"\x13": None})

        command = pack(TLV_STRUCT,
            b'\x20', 3, 255, 16, 17)
        self.assertEqual(self.dec(command), {b"\x20": [255, 16, 17]})

        command = pack(TLV_STRUCT+TL_STRUCT[1:]+TL_STRUCT[1:],
            b"\x20", 3, 15, 16, 17,
            b"\x13", 0,
            b"\x12", 0)
        self.assertEqual(self.dec(command),
            {b"\x20": [15, 16, 17], b"\x13": None, b"\x12": None})

    def test_decompose_wrong_length(self):
        """wrong length specified in tlv"""
        command = pack(TLV_STRUCT,
            b'\x20', 0, 255, 16, 17)
        self.assertEqual(self.dec(command), {})

        command = pack(TLV_STRUCT,
            b'\x20', 4, 255, 16, 17)
        self.assertEqual(self.dec(command), {})

        command = pack(TLV_STRUCT,
            b'\x12', 4, 255, 16, 17)
        self.assertEqual(self.dec(command), {})

    def test_decompose_broken(self):
        """wrong data"""
        command = pack(TLV_STRUCT,
            b"\xc0", 0, 2, 3, 5)
        self.assertEqual(self.dec(command), {})

    def test_decompose_mashed(self):
        """mashed data"""
        command = pack(TL_STRUCT + TLV_STRUCT[1:],
            b"\x12", 1,
            b"\x20", 3, 15, 16, 17)
        self.assertEqual(self.dec(command), {b"\x20": [15, 16, 17]})

        command = pack(TLV_STRUCT + TL_STRUCT[1:],
            b"\x20", 3, 15, 16, 17,
            b"\x12", 1)
        self.assertEqual(self.dec(command), {b"\x20": [15, 16, 17]})

if __name__ == '__main__':
    unittest.main()
