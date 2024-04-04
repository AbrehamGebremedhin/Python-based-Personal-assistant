from transformers import AutoTokenizer
from utils.db_calls import DatabaseCalls
from dotenv import load_dotenv
import transformers
import torch
import os


class Respond():
    def __init__(self) -> None:
        load_dotenv('config/config.env')

        # Access  key
        self.model_name = os.getenv('model_name')
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.pipeline = transformers.pipeline(
            'text-generation',
            model=self.model_name,
            tokenizer=self.tokenizer,
            torch_dtype=torch.float32,
            device_map='cpu',
        )
        self.db = DatabaseCalls("dialog_history")

    def generator(self, prompt):
        system_message = os.getenv("system_message")
        inst = f'<SYS> {system_message} <INST> {prompt} <RESP> '

        response = self.pipeline(
            inst,
            max_length=5000,
            pad_token_id=50526,
            repetition_penalty=1.05
        )
        start_marker = "<RESP>"
        index = response[0]['generated_text'].find(start_marker)

        if index != -1:
            result = response[0]['generated_text'][index +
                                                   len(start_marker):].strip()
            self.db.insert_one({"user": prompt, "response": result})
            return result
