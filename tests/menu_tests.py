import unittest
from unittest import TestCase
from unittest.mock import patch, call
import Main
from planeModel import FlightInfo

class TestFlickrAPI(TestCase):
    """This test makes a fake input of 9 at the main menu, which should loop the program."""
    @patch('builtins.input', side_effect=['9', '6'])
    def test_no_input_main_menu(self, mock_input):
        self.assertEqual(Main.Main(), 'That was an invalid input. Please try again from the given options.')
        with self.assertRaises(SystemExit):
            Main.Main()

    """This test inputs a 4 into the bookmark menu, which should be rejected, not cause an error, and go back to the bookmark menu."""
    @patch('builtins.input', side_effect=['4'])
    def test_no_input_bookmark_menu(self, mock_input):
        with self.assertRaises(SystemExit):
            Main.handle_bookmark_menu(Main.create_bookmark_menu(), 'search', 'test_desc', 'test_url')


if __name__ == '__main__':
    unittest.main()
