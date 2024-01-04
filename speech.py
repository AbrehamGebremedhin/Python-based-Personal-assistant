from pydub import AudioSegment
from pydub.playback import play
from TTS.api import TTS
import soundfile as sf
import speech_recognition as sr
import torch
import subprocess


class Speech():
    def __init__(self) -> None:
        # initialize recognizer
        self.recognizer = sr.Recognizer()
        # Get device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Init TTS with the target model name
        self.tts = TTS(
            "tts_models/en/ljspeech/tacotron2-DDC_ph").to(self.device)

    def speak(self, input):
        file_path = 'output.wav'

        self.tts.tts_to_file(
            text=input, file_path=file_path, speaker_wav=['models/one.wav', 'models/two.wav', 'models/three.wav', 'models/four.wav', 'models/five.wav', 'models/six.wav', 'models/seven.wav', 'models/eight.wav', 'models/nine.wav', 'models/ten.wav'], split_sentences=True)

        # Play the synthesized speech using playsound
        sound = AudioSegment.from_wav(file_path)
        play(sound)

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # recognizer.dynamic_energy_threshold = True
            self.recognizer.energy_threshold = 400
            audio = self.recognizer.listen(source)
            try:
                print("Recognizing...")
                return self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                return None
