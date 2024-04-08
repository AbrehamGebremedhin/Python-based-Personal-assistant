from utils.intent import classify_intent
from utils.speech import Speech
from handlers.api_calls import API
from handlers.browser_handler import Browse
from utils.db_calls import DatabaseCalls
from handlers.chat import Respond
from handlers.system_handle import handle_speaker
import speech_recognition as sr
import datetime
import sys

# initialize recognizer
recognizer = sr.Recognizer()

# initialize API, Speech, Browse class
speech = Speech()
browse = Browse()
respond = Respond()
api = API(respond)
db = DatabaseCalls("intent")


def process_command(command):
    label = classify_intent(input=command)

    if label == 'general_greet':
        db.insert_one({"input": command, "intent": "greeting"})
        speech.speak(respond.generator(command))
    elif label == 'datetime_query':
        db.insert_one({"input": command, "intent": "datetime_query"})
        current_time = str(datetime.datetime.now().strftime("%H:%M"))
        speech.speak(f"The current time is {current_time}")
    elif label == 'weather_query':
        db.insert_one({"input": command, "intent": "weather_query"})
        speech.speak(api.get_weather(input=command))
    elif label == 'play_music':
        db.insert_one({"input": command, "intent": "play_music"})
        speech.speak("Playing music on youtube")
        browse.open_youtube(command)
    elif "browse" in command or "search" in command:
        db.insert_one({"input": command, "intent": "search_browser"})
        speech.speak("Searching on brave")
        browse.search(command)
    elif "movie" in command or "series" in command or "anime" in command:
        db.insert_one(
            {"input": command, "intent": "entertainment_query"})
        speech.speak(api.get_movie(title=command))
    elif "message" in command:
        db.insert_one(
            {"input": command, "intent": "send_telegram_message"})
        from utils.message import prepare_message
        prepare_message(speech, text=command)
    elif label == "audio_volume_mute":
        db.insert_one(
            {"input": command, "intent": "mute_speaker"})
        handle_speaker()
    elif label == "audio_volume_up":
        db.insert_one(
            {"input": command, "intent": "unmute_speaker"})
        handle_speaker()
    elif "bye" in command:
        db.insert_one({"input": command, "intent": "terminate"})
        sys.exit(speech.speak(respond.generator(command)))
    else:
        db.insert_one({"input": command, "intent": "general_query"})
        speech.speak(respond.generator(command))


def main():
    speech.speak(
        "Hello, I am Saba. Your Personal Assistant, How may I help you?")

    while True:
        command = speech.listen()

        if command:
            print("You said:", command)
            process_command(command)


main()
