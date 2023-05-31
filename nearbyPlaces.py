import requests
import googlemaps
from langdetect import detect
from googletrans import Translator
import json
import openai

openai.api_key = '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'
API_KEY = "AIzaSyC5goLM2ann_BQKVN4F6WR-FFJWlc_g8ao"

def ai_translate(sight):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Please translate the following word to an English word:" + sight + ". Please return the English word without any additional explanation.",
        max_tokens=60
    )
    return response.choices[0].text.strip()


gmaps = googlemaps.Client(key=API_KEY)

# cities = {'New York City':[], 'Hualien':[], 'Lukang':[]}

# for c in cities:
def get_sights(c):
    geocode_result = gmaps.geocode(c)
    location = geocode_result[0]['geometry']['location']
    # location_str = f"{location['lat']},{location['lng']}"
    # url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location_str}&radius=5000&type=tourist_attraction&language=en&key={API_KEY}"
    # response = requests.get(url)
    places_result = gmaps.places_nearby(location=location, radius=5000, type='tourist_attraction', language='en')

    # if response.status_code == 200:
    #     places_result = json.loads(response.text)
    # else:
    #     print(f"Request failed with status code {response.status_code}")
    sights = []
    for result in places_result['results'][:3]:
        sight = result["name"]
        translator = Translator()
        src_lang = detect(sight)
        if src_lang != 'en':
            try:
                # sight = translator.translate(sight, src=detect(sight), dest='en').text
                sight = ai_translate(sight)
            except Exception as e:
                print(f"Error translating sight {sight}: {e}")
                continue
        sights.append(sight)
    return sights