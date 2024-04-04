from handlers.telegram_handle import handler
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

telegram = handler()


def prepare_message(speech, text):
    doc = nlp(text)
    tokens = ["to"]
    result = []

    for token in tokens:
        # Find the index of the token
        token_index = next(
            (i for i, t in enumerate(doc) if t.text == token), -1)

        if token_index != -1 and token_index < len(doc) - 1:
            # Extract all strings after the token
            result += [token.text for token in doc[token_index + 1:]]

    username = ''.join(result)

    speech.speak("what is the message you want to send?")

    while True:
        message = speech.listen()

        if message:
            speech.speak(telegram.send_message(name=username, message=message))
            break
