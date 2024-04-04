from youtubesearchpython import VideosSearch
import spacy
import webbrowser


class Browse():
    # Load the spaCy model
    nlp = spacy.load("en_core_web_sm")

    def __init__(self) -> None:
        pass

    def search(self, query):
        doc = self.nlp(query)
        tokens = ["browse"]
        result = []

        for token in tokens:
            # Find the index of the token
            token_index = next(
                (i for i, t in enumerate(doc) if t.text == token), -1)

            if token_index != -1 and token_index < len(doc) - 1:
                # Extract all strings after the token
                result += [token.text for token in doc[token_index + 1:]]

        search = f"https://search.brave.com/search?q={result}&source=desktop"

        webbrowser.open(search)

    def open_youtube(self, query):
        # Perform the YouTube search
        videos_search = VideosSearch(query, limit=1)

        # Get the URL of the top result
        results = videos_search.result()
        if len(results['result']) > 0:
            top_result = results['result'][0]
            video_url = top_result['link']

            # Open the URL in the default web browser
            webbrowser.open(video_url)
