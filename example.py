import json
import openai
import os
from ratelimit import limits, sleep_and_retry
import concurrent.futures
import googlemaps
from langdetect import detect

openai.api_key = ''
gmap_api_key = ""

example = {"name": "Taipei",
           "country": "Taiwan",
           "overview": "Taipei, the capital city of Taiwan, is a popular tourist destination known for its modern architecture, vibrant culture, delicious food, and lively nightlife. Top attractions include Taipei 101, National Palace Museum, and night markets like Shilin and Raohe. The city also has a convenient metro system making it fun for work and play. Its nightlife is accessible, but leaves something to be desired - a sense of adventure and a pinch of danger",
           "day1name": "Day 1: Arrival and Exploration",
           "day1": "After arriving in Taipei and checking into my hotel, I decided to explore the city. I started by visiting the National Palace Museum, which is home to some of the world's most extensive collections of Chinese art and artifacts. I guess I am not that into Chinese art because I nearly fell asleep by noon. If not for the loud noise from the city streets, I would have drooled all over my tour pamphlet. Afterward, I walked around the bustling Ximending district, which is famous for its trendy shops and street food. I stopped at a local restaurant called Ay-Chung Flour-Rice Noodle, where I tried their famous bowl of oyster vermicelli, which was absolutely delicious. For dinner, I went to Din Tai Fung, a world-renowned restaurant chain famous for its xiao long bao (soup dumplings). The dumplings were just okay, nothing special.",
           "day2name": "Day 2: Adventure and Scenery",
           "day2": "On my second day, I wanted to get out of the city and explore some of the surrounding nature. I took the MRT to Beitou, which is famous for its hot springs and scenic views. I hiked up to the top of Yangming Mountain, which is known for its breathtaking views of the city and the ocean. Afterward, I visited the Beitou Hot Springs Museum. The old style left me feeling a bit uneasy and I quickly rushed away. For lunch, I stopped at a local restaurant called Rong's Pork Liver Soup, where I tried their signature dish, a bowl of savory pork liver soup with rice. It was my first time trying liver and I wasn't really a fan, but I could see that it was well seasoned. In the evening, I went to Taipei 101, one of the most iconic landmarks in the city, and enjoyed the stunning views of the city lights.",
           "day3name": "Day 3: Culture and Cuisine",
           "day3": "On my last day in Taipei, I decided to explore some of the city's cultural and historical sites. I started by visiting the Longshan Temple, one of the oldest and most famous temples in Taiwan. The temple was beautiful, and I was impressed by the intricate carvings and decorations. Afterward, I visited the Taipei Confucius Temple, which is a tranquil oasis in the middle of the bustling city. For lunch, I went to a local restaurant called Kao Chi, which is famous for its traditional Taiwanese dishes. I ordered their famous braised pork rice and some stir-fried vegetables, which were both delicious. In the evening, I went to a local night market called Raohe Night Market, where I tried some of the city's most famous street foods, including pepper buns, grilled squid, and shaved ice.",
           "summary": "Overall, my trip to Taipei was a fun one. Some of the locations were too crowded, but I enjoyed all ot the nature, culture, and tasty food. Next time I would probably stay for longer and skip some of the cultural exhibitions. They were fun to see once, but I don't think I'd be interested in seeing them again.",
           "restaurant1name": "Din Tai Fung",
           "restaurant1": "Din Tai Fung is a world-famous restaurant chain that originated in Taipei and is known for its delicious xiao long bao (soup dumplings). The restaurant has multiple locations throughout the city, but the original location on Xinyi Road is the most popular. To be honest, I am not sure why it is so popular. The food is fresh to order, but I feel like the dumplings aren't all that different from the local street vendors. In addition to the dumplings, Din Tai Fung also serves a variety of other Taiwanese and Chinese dishes, such as fried rice, noodles, and steamed buns.",
           "restaurant2name": "Addiction Aquatic Development",
           "restaurant2": "Addiction Aquatic Development is a unique seafood market and restaurant in Taipei. The market features a wide selection of fresh seafood, including fish, crab, shrimp, and more. Visitors can choose their seafood and have it prepared to their liking at one of the many restaurants located inside the market. There are also several sushi and sashimi counters where you can watch the chefs prepare your meal right in front of you. The atmosphere is lively and bustling, and the seafood is some of the freshest you'll find in the city.",
           "restaurant3name": "Raw",
           "restaurant3": "Raw is a Michelin-starred restaurant in Taipei that offers a unique and innovative dining experience. The restaurant is known for its use of fresh and seasonal ingredients, and its menu changes frequently to reflect the best ingredients available. Dishes are beautifully presented and incorporate a variety of flavors and textures. The tasting menu is a great way to experience the full range of what Raw has to offer, and the wine pairings are expertly chosen to complement each dish. The atmosphere is elegant and refined, making it a perfect choice for a special occasion or a romantic evening out.",
           "hotel1name": "Shangri-La's Far Eastern Plaza Hotel",
           "hotel1": "This hotel live up to its namesake! As soon as you enter, the marble art and oriental smell make you feel like you've been transported to some secret paradise. The rooms were clean, spacious, and comfortable with enormous desks that make you feel like you're Donald Trump the TV star. I would definitely recommend this hotel to anyone visiting Taipei.",
           "hotel2name": "W Taipei",
           "hotel2": "The W Taipei is a a modern and stylish design. That being said the staff leave a lot to be desired. They seem to be too busy for you even when the lobby is completely empty. Of course I think a certain level of person can be in to that. If you are too cool to talk to plebs this is your dream hotel. In the summer you can look down on people from the rooftop pool as you showoff your perfectly chiseled pecs and laugh. The hotel also has a great location, with easy access to many restaurants, shops, and sights.",
           "hotel3name": "Kimpton Taipei",
           "hotel3": "The Kimpton Taipei is where all the stylish youth stay. Bring your dog or your mistress, either way you'll be treated like royalty. The staff always remeber your name and your favorite happy hour cocktail.",
           "sight1name": "Visit Taipei 101",
           "sight1": "Taipei 101 is an iconic skyscraper in Taipei that is a must-visit attraction for anyone traveling to the city. The tower stands at 508 meters tall and was the tallest building in the world until 2010. Visitors can take a ride up to the observation deck on the 89th floor for panoramic views of the city. On a clear day, you can see all the way to the mountains in the distance. The observation deck also has a souvenir shop, a restaurant, and an outdoor viewing area for even more stunning views. For those who are feeling adventurous, you can take a ride up to the 91st floor and experience the outdoor wind damper, which is the largest in the world.",
           "sight2name": "Explore the night markets",
           "sight2": "One of the most popular things to do in Taipei is to explore the citys many night markets. These bustling markets offer a wide variety of street food, shopping, and entertainment. Yet at the end of the day they really don't lead much of a lasting impact. Once you have seen one night markey, you've pretty much seen them all. The vendors and games are so similar. It's something to do for young kids or families, but not all that exciting the umpteenth time you visit. Ine of the most famous night markets is the Shilin Night Market, which is home to hundreds of food vendors selling everything from stinky tofu to grilled squid. The market also has a wide selection of clothing, accessories, and souvenirs. Another popular night market is the Raohe Street Night Market, which has a more traditional feel with its historic architecture and narrow alleyways.",
           "sight3name": "Take a day trip to Jiufen",
           "sight3": "Jiufen is a charming mountain town located just a short drive from Taipei. The town was the inspiration for the movie 'Spirited Away' and is known for its traditional architecture, scenic views, and delicious street food. The narrow streets are lined with tea houses, souvenir shops, and food stalls selling local favorites like taro balls, shaved ice, and mochi. Visitors can also climb the many staircases and hills to reach panoramic viewpoints overlooking the town and the coastline. Jiufen is a great way to escape the hustle and bustle of Taipei for a day and experience a more peaceful and traditional side of Taiwan."}

save_path = "CityTexts"
gmaps = googlemaps.Client(key=gmap_api_key)


@sleep_and_retry
@limits(calls=3, period=60)
def call_chat(city_name, params):
    geocode_result = gmaps.geocode(c)
    location = geocode_result[0]['geometry']['location']
    restaurants = get_places(city_name, location, "restaurant")
    hotels = get_places(city_name, location, "lodging")
    sights = get_places(city_name, location, "tourist_attraction")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "This is an example json:" +
                json.dumps(params)},
            {"role": "user", "content": "Please write a similar json for " + city_name +
             ", with the following restaurants: " + f"restaurant1: {restaurants[0]}, restaurant2: {restaurants[1]}, restaurant3: {restaurants[2]}" +
             ", with the following hotels: " + f"hotel1: {hotels[0]}, hotel2: {hotels[1]}, hotel3: {hotels[2]}" +
             ", with the following sights: " + f"sight1: {sights[0]}, sight2: {sights[1]}, sight3: {sights[2]}"}
        ]
    )

    result = json.loads(response['choices'][0]['message']['content'])
    if result.keys() < example.keys():
        raise Exception('Missing content exception:' + '|'.join(result.keys()))
    return result


def get_content(country):
    result = {}
    result.update(call_chat(country, example))
    return result


def ai_translate(sight):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Please translate the following word to an English word:" + sight +
        ". Please return the English word without any additional explanation.",
        max_tokens=60
    )
    return response.choices[0].text.strip()


def get_places(c, location, type):
    places_result = gmaps.places_nearby(
        location=location, radius=5000, type=type, language='en')
    eng_results = []
    for result in places_result['results'][:5]:
        sight = result["name"]
        src_lang = detect(sight)
        if src_lang != 'en':
            try:
                sight = ai_translate(sight)
            except Exception as e:
                print(f"Error translating sight {sight}: {e}")
                continue
        eng_results.append(sight)
    return eng_results


cities = ['New York City, NY, USA', 'Hualien, Taiwan']
for c in cities:
    filename = os.path.join(save_path, f"{c}.json")
    try:
        content = get_content(c)
        with open(filename, 'w') as w:
            json.dump(content, w)
            print(f'Completed {c}')
    except Exception as e:
        print('Problem for ' f"{c}")
        print(e)

# def make_city(c):
#     split = c[1].split(',')
#     city = split[1].replace('"', '')
#     country = split[4].replace('"', '')
#     state = split[-4].replace('"', '')
#     file_name = f'/Users/computer/Desktop/travel/content/generated/{country}/{city}.vars'
#     if os.path.exists(file_name):
#         return
    # try:
    #     content = get_content(city + " " + state + " " + country)
    #     with open(file_name, 'w') as w:
    #         json.dump(content, w)
    #         print(f'Completed {city} {state} {country}')
    # except Exception as e:
    #     print('Problem for ' + city + ',' + country)
    #     print(e)

# cities = []
# with open('/Users/computer/Desktop/travel/content/worldcities_no_dups.csv', 'r') as f:
#     for line in f:
#         pop = int(line.split(',')[-2].replace('"', ''))
#         cities.append((pop, line))
# cities.sort(key=lambda tup: tup[0], reverse=True)

# tourist_cities = set()
# with open('/Users/computer/Desktop/travel/content/tourists.csv', 'r') as f:
#     for line in f:
#         split = line.split(',')
#         if len(split) != 2:
#             print('Long line:' + line)
#             continue
#         tourist_cities.add(split[0].lower())

# cities = [city for city in cities if city[1].split(',')[1].replace('"', '').lower() in tourist_cities]

# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#     for c in cities:
#         split = c[1].split(',')
#         city = split[1].replace('"', '').lower()
#         country = split[4].replace('"', '').lower()
#         state = split[-4].replace('"', '').lower()
#         file_name = f'/Users/computer/Desktop/travel/content/generated/{country}/{city}.vars'
#         if os.path.exists(file_name):
#             continue
#         executor.submit(make_city, c)
