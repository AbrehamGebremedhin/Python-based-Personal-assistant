from transformers import AutoTokenizer
from dotenv import load_dotenv
from transformers import pipeline
import torch
import os


class Respond():
    def __init__(self) -> None:
        load_dotenv('config/config.env')

        # Access  key
        self.model_name = os.getenv('model_name')
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.pipe = pipeline(
            "text-generation",
            model=self.model_name,
            torch_dtype=torch.float32,
            device_map="cpu"
        )

    def generator(self, prompt):
        inst = [
            {
                "role": "system",
                "content": os.getenv("system_message"),
            },
            {
                "role": "system",
                "content": "What is your name",
            },
            {
                "role": "user",
                "content": "My name is abreham."
            },
            {
                "role": "system",
                "content": "what kind of movies do you enjoy?",
            },
            {
                "role": "user",
                "content": "I enjoy watching action, drama, period, medival, war, historical, documentary and violent movies."
            },
            {
                "role": "user",
                "content": prompt
            },
        ]

        prompt = self.pipe.tokenizer.apply_chat_template(
            inst, tokenize=False, add_generation_prompt=True)
        outputs = self.pipe(prompt, max_new_tokens=2500, do_sample=True,
                            temperature=0.5, top_k=20, top_p=0.9)

        start_marker = "<|assistant|>"
        index = outputs[0]['generated_text'].find(start_marker)

        if index != -1:
            result = outputs[0]['generated_text'][index +
                                                  len(start_marker):].strip()
            return result
