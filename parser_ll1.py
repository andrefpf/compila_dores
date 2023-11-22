from grammar import Epsilon, Grammar, Production, EndMarker
from functools import partial
from copy import deepcopy


class LL1Table(dict):
    pass

class SemanticRule(partial):
    def __repr__(self) -> str:
        return "SemanticRule"

class Parser:
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

            token = tokens[index]
            node = stack.pop()

            if callable(node):
                node()
                continue

            if (node == token):
                index += 1
                continue

            if node in self.grammar.terminal:
                print(f'Bla bla "{token}"')
                break

            if (node, token) not in self.table:
                print(f'Error. Unexpected pair "{node, token}"')
                break

            # deepcoping here creates different objects for
            # the same symbol, so it is possible to deal with
            # productions like A -> A + B
            production = self.table[node, token]
            to_stack = [deepcopy(i) for i in production.target]

            if callable(production.after_run):
                function = SemanticRule(
                    production.after_run,
                    node,
                    *to_stack,
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
