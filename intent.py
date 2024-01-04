from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

model_name = 'cartesinus/xlm-r-base-amazon-massive-intent'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
classifier = TextClassificationPipeline(model=model, tokenizer=tokenizer)


def classify_intent(input):
    res = classifier(input)
    return res[0]['label']
