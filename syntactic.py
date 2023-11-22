from grammar import Epsilon, Grammar, Production, EndMarker
from functools import partial
from copy import deepcopy


class LL1Table(dict):
    pass


class Syntactic:
    def __init__(self, grammar: Grammar):
        self.set_grammar(grammar)

    def set_grammar(self, grammar: Grammar):
        self.grammar = grammar
        self.create_table()
    
    def analyze(self, tokens):
        index = 0
        stack = []
        node = self.grammar.start_symbol()

        tokens = [i for i in tokens]
        tokens.append(EndMarker())
        stack.append(EndMarker())
        stack.append(self.grammar.start_symbol())

        while len(stack) > 1:
            print(stack)

            symbol = tokens[index]
            node = stack.pop()

            if callable(node):
                node()
                continue

            if (node == symbol):
                index += 1
                continue

            if node in self.grammar.terminal:
                print(f'Bla bla "{symbol}"')
                break

            if (node, symbol) not in self.table:
                print(f'Error. Unexpected pair "{node, symbol}"')
                break

            production = self.table[node, symbol]
            to_stack = [deepcopy(i) for i in reversed(production.target)]

            if callable(production.before_run):
                function = partial(
                    production.before_run,
                    production.origin,
                    *production.target
                )
                stack.append(function)

            if Epsilon() in production.target:
                continue

            stack.extend(to_stack)

        print(stack)
        if stack.pop() != EndMarker():
            print("Oh no")

    def create_table(self):
        table = LL1Table()

        for production in self.grammar.productions:
            nullable = Epsilon() in production.target

            if nullable:
                for symbol in self.grammar.follow[production.origin]:
                    table[production.origin, symbol] = production
            else:
                start_symbol = production.target[0]
                for symbol in self.grammar.first[start_symbol]:
                    if symbol == Epsilon():
                        continue
                    table[production.origin, symbol] = production

        self.table = table


cfg = Grammar([
    Production("E", ["T", "E'"]),
    Production("E'", ["+", "T", "E'"]),
    Production("E'", [Epsilon()]),
    Production("T", ["F", "T'"]),
    Production("T'", ["*", "F", "T'"]),
    Production("T'", [Epsilon()]),
    Production("F", ["(", "E", ")"]),
    Production("F", ["a"]),
])

cfg = Grammar([
    Production("S", ["B"]),
    Production("B", ["0M", "B'"]),
    Production("B", ["1M", "B'"]),
    Production("B", ["0"]),
    Production("B", ["1"]),
    Production("B'", ["0m", "B"]),
    Production("B'", ["1m", "B"]),
    Production("B'", ["0"]),
    Production("B'", ["1"]),
])

syn = Syntactic(cfg)
# for a, b in syn.table.items():
#     print(f"{a} \t {b}")
# print()

# tokens = list("a+a*a+a")
tokens = ['0M','1m','1M','0']
syn.analyze(tokens)