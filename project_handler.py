from speech import Speech
import speech_recognition as sr
import subprocess


class Handle_Project():
    def __init__(self, input, model) -> None:
        # initialize recognizer
        self.recognizer = sr.Recognizer()

        self.speech = model

        self.input("What is the project title, sir?")

    def input(self, prompt):
        self.speech.speak(prompt)

        while True:
            command = self.speech.listen()

            if command:
                title = command
                # self.input("What language do you want to use?")
                # language = command
                # self.input("Do you to want to initialize git for you?")
                # init_git = command
                line = "D: && cd Projects"
                subprocess.Popen(command, shell=True)
                line = f"mkdir trial"
                subprocess.Popen(command, shell=True)
