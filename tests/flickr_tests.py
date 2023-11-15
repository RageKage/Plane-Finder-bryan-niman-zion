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

    """This test removes the Flickr API secret, which should cause an Exception and ask for authorization in a browser."""
    @patch('planeImage.flickr_secret', 'No_secret')
    def test_no_flickr_secret(self):
        error_message = 'The Flickr API is currently unavailable.'
        with self.assertRaises(flickrapi.exceptions.FlickrError):
            get_image_link('B733')

    """This test inputs a search query that provides no images to manipulate, which should raise an IndexError."""
    def test_no_search_results(self):
        with self.assertRaises(IndexError):
            get_image_link('dfjhkvfsfjsvhsdsgkjh')

    """This test checks what happens if an API connection isn't possible because of internet connection issues. The expectation is an error message
    telling the user to fix their internet connection. This test requires you to turn your wifi off manually to function properly."""
    def test_no_internet(self):
        error_message = 'Error: No internet connection. Please fix your connection before using the Flickr API again.'
        self.assertEqual(error_message, get_image_link('B773'))





if __name__ == '__main__':
    unittest.main()