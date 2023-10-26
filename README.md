PLANE FINDER

By: Niman, Zion, and Bryan

The Plane Finder App makes use of 3 different APIs to bring results to the user, the Flickr API, the Wikipedia API, and AirLabs API.





## Setup

### Create and Activate Virtual Environment

python3 -m venv env
source env/bin/activate


### Install Required Packages
install -r requirements.txt


### Flickr Account Setup
- create a flickr account

### Environment Variables
Add these keys to your environment variables with their api keys:
1. AVIATIONS_API_KEY
2. AIRLABS_API_KEY
3. FLICKR_KEY
4. FLICKR_SECRET

### API sites
1. https://aviationstack.com/documentation
2. https://airlabs.co/
3. https://www.flickr.com/services/api/



The user enters the desired airframe (model/type of plane) and the python file converts the string into an ICAO number, 
which then uses a call to the AirLabs API to get a count of the number of planes with that ICAO number currently aloft. 
The app also makes use of a call to the Flickr API to return a photo of an example of that airframe, 
as well as a call to the Wikipedia API to return a blurb about the airframe.  
A database is populated with rows of airframes as well as their manufacturer, such as "Airbus" by "Boeing" etc upon loading. 
This can take some time, so the app first prompts the user with a warning that it make take awhile. 
The app also uses bookmarking/cacheing of the searches that have been made, and populates it upon loading, so the user can refer back to them.

After populating, the user is presented with the text-based UI with features selected by number:
    '1', 'DB Plane Search', search_bookmarked_plane)
    '2', 'API Plane Search', search_aircraft_in_api)
    '3', 'Display Bookmarked Planes', display_bookmarked_planes)
    '4', 'Delete Plane in DB', delete_bookmarked_plane)
    '5', 'Generate Test Data', create_sample_planes)
    '6', 'Exit Program', exit)

Then after each time a user enters a different airframe search, a new menu is displayed:
    '1', 'Bookmark this plane', add_plane_to_bookmarks)
    '2', 'Go back to main menu', go_back)

Error messages will be displayed for invalid entries by the user in the UI.

Thank you!
