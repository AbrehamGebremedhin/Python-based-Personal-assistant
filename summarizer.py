from transformers import pipeline
import os
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def get_file(input):
    doc = nlp(input)
    tokens = ["summarize", "about"]
    result = []

    for token in tokens:
        # Find the index of the token
        token_index = next(
            (i for i, t in enumerate(doc) if t.text == token), -1)

        if token_index != -1 and token_index < len(doc) - 1:
            # Extract all strings after the token
            result += [token.text for token in doc[token_index + 1:]]

    file_name = ' '.join(result)

    directory = "files"
    extensions = [".pdf", ".docx", ".txt"]

    found_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            name = os.path.basename(file)
            filename = name.upper()
            file_name = str(file_name)
            file_name = file_name.upper()
            if any(file.endswith(ext) for ext in extensions):
                if (filename.__contains__(file_name)):
                    with open(f"{directory}/{name}", 'r') as f:
                        data = f.read()
                    doc = nlp(data)
                    return (doc)
                else:
                    return None


def summarize(filename):
    document = str(get_file(input=filename))

    if document is not None:
        summary = summarizer(document, max_length=258,
                             min_length=100, do_sample=False)

        return (summary[0]['summary_text'])

    else:
        return "Sorry, I have run into a problem while processing the file."
