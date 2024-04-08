import requests
import os
import spacy
from utils.utils import named_entity
from dotenv import load_dotenv
from handlers.chat import Respond


class API():
    def __init__(self, respond: Respond):
        # Load variables from the .env file
        load_dotenv('config/config.env')
        # Load the spaCy model
        self.nlp = spacy.load("en_core_web_sm")
        self.respond = respond

    def get_movie(self, title):
        entities = named_entity(title, ['movie title'])
        for entity in entities:
            if entity['label'] == 'movie title':
                movie_title = entity['text']
            else:
                return ("Error occured while trying to get the title, please tell me again")

        movie_key = os.getenv('movie_api_key')
        url = f"http://www.omdbapi.com/?apikey={movie_key}&t={movie_title}"

        response = requests.request("GET", url)

        if response.status_code == 200:
            data = response.json()

            if data['Response'] == 'False':
                return (f"Error could not find the movie {title}")
            else:
                return (self.respond.generator(f"summarize this information {data}in a paragraph format"))

        else:
            return (response.text)

    def get_weather(self, input):
        """Get weather information using OpenWeatherMap's API"""
        location_key = os.getenv('location_api_key')
        url = f'https://ipinfo.io/json?token={location_key}'
        response = requests.get(url)
        data = response.json()
        entities = named_entity(input, ['place'])
        location = data['city']
        for entity in entities:
            if entity['label'] == 'place':
                location = entity['text']
            else:
                break
        print(location)
        weather_key = os.getenv('weather_api_key')
        url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={weather_key}"

        response = requests.request("GET", url)

        if response.status_code == 200:
            data = response.json()

            return (self.respond.generator(
                f"summarized information from {data} into an explained weather paragraph"))

        else:
            return (response.text)
