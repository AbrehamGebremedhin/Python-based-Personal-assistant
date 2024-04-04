from gliner import GLiNER


def named_entity(text: str, labels: list):
    model = GLiNER.from_pretrained("urchade/gliner_multi")

    entities = model.predict_entities(text, labels)

    return (entities)
