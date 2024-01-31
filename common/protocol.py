from typing import Optional, List, Dict, Any, Union, Literal
from pydantic import BaseModel, Field

class ChatCompletionInput(BaseModel):
    model: str = "gpt-4"
    messages: list
    temperature: float = 1.0
    top_p: float = 1.0
    n: int = 1
    stream: bool = False
    stop: Optional[Union[str, list]] = ""
    max_tokens: int = 2048
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    user: str = ""
    
class ChatMessageHistory:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

def process_messages(messages, history):
    for message in messages:
        role = message["role"]
        content = message["content"]
        history.add_message(role, content)
        

class Model:
    def __init__(self, name):
        self.name = name

gpt35turbo = "gpt-3.5-turbo"
gpt35turbo16k = "gpt-3.5-turbo-16k"
gpt4 = "gpt-4"

model_names = [gpt35turbo, gpt35turbo16k, gpt4]
models = {name: Model(name=name) for name in model_names}

class ModelUtils:
    convert = models
