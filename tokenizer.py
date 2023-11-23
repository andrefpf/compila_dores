from dataclasses import dataclass

@dataclass
class Token:
    name: str
    lexema: str
    index: int = 0

class Tokenizer:
    def run(self, string):
        yield from string
