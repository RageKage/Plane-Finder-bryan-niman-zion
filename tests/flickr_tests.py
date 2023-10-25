import unittest
from unittest import TestCase
from unittest.mock import patch, call

import planeImage
from planeImage import *
import Main

class TestFlickrAPI(TestCase):
    """This test will replace the flickr API key with a dud, which should cause an Exception within the flickrapi module"""
    @patch('planeImage.flickr_key', 'No_key')
    def test_no_flickr_key(self):
        error_message = 'The Flickr API is currently unavailable.'
        with self.assertRaises(flickrapi.exceptions.FlickrError):
            get_image_link('B733')

    """This test inputs a search query that provides no images to manipulate, which should raise an IndexError."""
    def test_no_search_results(self):
        with self.assertRaises(IndexError):
            get_image_link('dfjhkvfsfjsvhsdsgkjh')





if __name__ == '__main__':
    unittest.main()