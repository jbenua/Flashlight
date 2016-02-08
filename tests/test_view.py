
import unittest
from ..views.console_view import ConsoleView
from unittest.mock import MagicMock


class TestViewFunctions(unittest.TestCase):

    def setUp(self):
        self.flashlight = ConsoleView()
        self.flashlight.draw = MagicMock()

    def test_flashlight(self):
        self.flashlight.ON()
        self.assertEqual(self.flashlight.isOn,  True)

        self.flashlight.OFF()
        self.assertEqual(self.flashlight.isOn,  False)

        self.flashlight.COLOR((120, 145, 30))
        self.assertEqual(self.flashlight.color, (120, 145, 30))

        self.flashlight.COLOR((-140, 205, 130))
        self.assertEqual(self.flashlight.color, (120, 145, 30))

        self.flashlight.COLOR((140, -205, 130))
        self.assertEqual(self.flashlight.color, (120, 145, 30))

        self.flashlight.COLOR((140, 205, -130))
        self.assertEqual(self.flashlight.color, (120, 145, 30))

        self.flashlight.COLOR((260, 201, 110))
        self.assertEqual(self.flashlight.color, (120, 145, 30))

        self.flashlight.COLOR((201, 260, -110))
        self.assertEqual(self.flashlight.color, (120, 145, 30))

        self.flashlight.COLOR((201, 110, 260))
        self.assertEqual(self.flashlight.color, (120, 145, 30))

        self.flashlight.ON()
        self.assertEqual(self.flashlight.isOn, True)

        self.flashlight.COLOR((120, 145, 30))
        self.assertEqual(self.flashlight.color, (120, 145, 30))

        self.flashlight.COLOR((-140, 205, 130))
        self.assertEqual(self.flashlight.color, (120, 145, 30))

        self.flashlight.COLOR((140, -205, 130))
        self.assertEqual(self.flashlight.color, (120, 145, 30))

        self.flashlight.COLOR((140, 205, -130))
        self.assertEqual(self.flashlight.color, (120, 145, 30))

        self.flashlight.COLOR((260, 201, 110))
        self.assertEqual(self.flashlight.color, (120, 145, 30))

        self.flashlight.COLOR((201, 260, -110))
        self.assertEqual(self.flashlight.color, (120, 145, 30))

        self.flashlight.COLOR((201, 110, 260))
        self.assertEqual(self.flashlight.color, (120, 145, 30))

if __name__ == '__main__':
    unittest.main()
