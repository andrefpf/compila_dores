from grammar import Epsilon, Grammar, Production, EndMarker


class LL1Table(dict):
    pass


class Syntactic:
    def __init__(self, grammar: Grammar):
        self.set_grammar(grammar)

    def set_grammar(self, grammar: Grammar):
        self.grammar = grammar
        self.create_table()
    
    def analyze(self, tokens):
        tokens = [i for i in tokens]
        tokens.append(EndMarker())

        index = 0
        stack = []
        stack.append(EndMarker())
        stack.append(self.grammar.start_symbol())
        node = stack[-1]

        while len(stack) > 1:
            symbol = tokens[index]
            print(stack, symbol)
            node = stack.pop()

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
            
            if Epsilon() in production.target:
                continue

            stack.extend(reversed(production.target))

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

# cfg = Grammar([
#     Production("S", ["B"]),
#     Production("B", ["0M", "B'"]),
#     Production("B", ["1M", "B'"]),
#     Production("B", ["0"]),
#     Production("B", ["1"]),
#     Production("B'", ["0m", "B"]),
#     Production("B'", ["1m", "B"]),
#     Production("B'", ["0"]),
#     Production("B'", ["1"]),
# ])

syn = Syntactic(cfg)
# for a, b in syn.table.items():
#     print(f"{a} \t {b}")
# print()

tokens = list("a+a*a+a")
syn.analyze(tokens)