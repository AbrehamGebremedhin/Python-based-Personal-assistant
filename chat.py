from transformers import AutoTokenizer, AutoModelForCausalLM
from db_calls import DatabaseCalls
import transformers
import torch


class Respond():
    def __init__(self) -> None:

        self.model_name = "ericzzz/falcon-rw-1b-instruct-openorca"

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
        system_message = 'You are a personal virtual assistant. Your name is Saba. Your job is to provide help abreham. Give short answers.'
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
