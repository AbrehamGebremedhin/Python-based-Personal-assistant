import requests
import os
import spacy
from utils.utils import named_entity
from dotenv import load_dotenv


class API():
    def __init__(self):
        # Load variables from the .env file
        load_dotenv('config/config.env')
        # Load the spaCy model
        self.nlp = spacy.load("en_core_web_sm")

    def get_movie(self, title):
        doc = self.nlp(title)
        tokens = ["movie", "series", "anime"]
        result = []

        for token in tokens:
            # Find the index of the token
            token_index = next(
                (i for i, t in enumerate(doc) if t.text == token), -1)

            if token_index != -1 and token_index < len(doc) - 1:
                # Extract all strings after the token
                result += [token.text for token in doc[token_index + 1:]]

        movie_title = ' '.join(result)

        movie_key = os.getenv('movie_api_key')
        url = f"http://www.omdbapi.com/?apikey={movie_key}&t={movie_title}"

        response = requests.request("GET", url)

        if response.status_code == 200:
            data = response.json()

            if data['Response'] == 'False':
                return ("Error: Movie not found")
            if data['Type'] == 'series':
                return (str(f"{data['Title']} is {data['Type']} about {data['Plot']} Each episode is {data['Runtime']}utes long. It has {data['totalSeasons']} seasons. It is rated {data['Rated']}."))
            else:
                return (str(f"{data['Title']} is {data['Type']} about {data['Plot']} It is {data['Runtime']}utes long. It is rated {data['Rated']}."))

        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    def get_weather(self, input):
        """Get weather information using OpenWeatherMap's API"""
        location_key = os.getenv('location_api_key')
        url = f'https://ipinfo.io/json?token={location_key}'
        response = requests.get(url)
        data = response.json()
        tokens = ['in']
        doc = self.nlp(input)
        location = ''

        for token in tokens:
            result = []
            # Find the index of the token
            token_index = next(
                (i for i, t in enumerate(doc) if t.text == token), -1)

            if token_index != -1 and token_index < len(doc) - 1:
                # Extract all strings after the token
                result += [token.text for token in doc[token_index + 1:]]

                location = ' '.join(result)

            else:
                location = data['city']

        weather_key = os.getenv('weather_api_key')
        url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={weather_key}"

        response = requests.request("GET", url)

        if response.status_code == 200:
            data = response.json()

            humidity = ''
            cloudy = ''
            rain_probablity = ''

            if data['data']['values']['humidity'] < 30:
                humidity = 'low humidity'
            elif data['data']['values']['humidity'] <= 60:
                humidity = 'moderate humidity'
            else:
                humidity = 'high humidity'

            if data['data']['values']['cloudCover'] == 0:
                cloudy = "Clear Sky"
            elif 1 >= data['data']['values']['cloudCover'] <= 30:
                cloudy = "Mostly Clear"
            elif 31 >= data['data']['values']['cloudCover'] <= 70:
                cloudy = "Partly Cloudy"
            elif 71 >= data['data']['values']['cloudCover'] <= 91:
                cloudy = "Mostly Cloudy"
            else:
                cloudy = "Overcast"

            if 0 >= data['data']['values']['precipitationProbability'] <= 30:
                rain_probablity = "relatively small chance"
            elif 31 >= data['data']['values']['precipitationProbability'] <= 60:
                rain_probablity = "moderate chance"
            else:
                rain_probablity = "high chance"

            return (f"The weather in {location} is {cloudy}. The temperature is {data['data']['values']['temperature']} degree celsius feels like {data['data']['values']['temperatureApparent']} and has {humidity}. There is a {rain_probablity} of rain.")

        else:
            print(f"Error: {response.status_code}")
            print(response.text)
