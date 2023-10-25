import unittest
from unittest import TestCase
from unittest.mock import patch, call
import Main

class TestFlickrAPI(TestCase):
    """This test makes a fake input of 9 at the main menu, which should close the program."""
    @patch('builtins.input', side_effect=['9'])
    def test_no_input_main_menu(self, mock_input):
        with self.assertRaises(SystemExit):
            Main.Main()


if __name__ == '__main__':
    unittest.main()
