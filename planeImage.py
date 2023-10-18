import flickrapi
import os

flickr_key = os.environ.get('FLICKR_KEY')
flickr_secret = os.environ.get('FLICKR_SECRET')

def get_image_link(search_query):
    flickr = flickrapi.FlickrAPI(flickr_key, flickr_secret, format='parsed-json')

    flickr.authenticate_via_browser(perms='read')
    photos = flickr.photos.search(per_page='1', text={search_query})
    photo_id = photos['photos']['photo'][0]['id']

    return f'https://www.flickr.com/photo.gne?id={photo_id}'