from dataclasses import dataclass
from collections.abc import Generator

@dataclass
class Token:
    name: str
    lexema: str
    index: int = 0

class Tokenizer:
    def run(self, string: str) -> Generator[Token]:
        for i in string:
            yield Token("char", i)