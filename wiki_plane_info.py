from bs4 import BeautifulSoup
import requests

class PlaneInfo:
    
    def make_wikipedia_request(model_name):
        """This function makes a request to the wikipedia api and returns the response as a json object."""
        try: 
            url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={model_name}&prop=extracts&exintro=True"
            response = requests.get(url)
            response.raise_for_status()  # Check for errors
            return response.json()
        except Exception as err:
            print(err)

    def extract_page_info(data):
        """This function extracts the page info from the json object and returns the page info."""
        pages_dict = data['query']['pages'] 
        first_page_key = list(pages_dict.keys())[0] # Get the first key in the dictionary 
        extract = pages_dict[first_page_key].get('extract', 'No extract available')
        return extract 

    def clean_extract_text(extract):
        """This function cleans the extract text and returns the clean text."""
        soup = BeautifulSoup(extract, 'html.parser') # Parse the HTML as a string
        readable_text = soup.get_text()
        clean_text = ' '.join(readable_text.split())  # Remove extra whitespace
        return clean_text

    
    def get_plane_info(self, model_name):
        """This is an encapsulated function that gets the plane info and returns the clean text."""
        response_data = self.make_wikipedia_request(model_name)
        page_info = self.extract_page_info(response_data)
        clean_text = self.clean_extract_text(page_info)
        return clean_text
    


    

