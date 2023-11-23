from tokenizer import Tokenizer, Token
import regex
from collections.abc import Generator

class CCLangTokenizer(Tokenizer):
    all_expressions = dict(
        identifier = r"[a-zA-Z]([a-zA-Z]|[0-9])*",
        number = r"[0-9]+",
        _ = r" ",
    )

    def run(self, string: str) -> Generator[Token]:
        all_machines = {
            name : regex.compiles(exp) 
            for name, exp in self.all_expressions.items()
        }

        index = 0
        while index < len(string):
            token_name = ""
            best_match = ""
            substring = string[index:]

            for name, machine in all_machines.items():
                current_match = machine.match(substring)
                if len(current_match) > len(best_match):
                    token_name = name
                    best_match = current_match
            index += len(best_match)

            if token_name == "_":
                continue

            if not best_match:
                print("DEU MERDA GRANDE")
                break

            yield Token(token_name, lexema=best_match)
