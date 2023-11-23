from grammar import EPSILON, END_MARKER, Grammar, Production
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

        start_symbol = deepcopy(self.grammar.start_symbol())
        node = start_symbol

        tokens = [i for i in tokens]
        tokens.append(END_MARKER)
        stack.append(END_MARKER)
        stack.append(start_symbol)

        while len(stack) > 1:
            # print(stack)

            token = tokens[index]
            node = stack.pop()

            if node == EPSILON:
                continue

            if isinstance(node, SemanticRule):
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

            production = self.table[node, token]
            # deepcoping here creates different objects for
            # the same symbol, so it is possible to deal with
            # productions like A -> A + B
            to_stack = [deepcopy(i) for i in production.target]
            avaliable_params = [i for i in to_stack if not callable(i)]

            for i, val in enumerate(to_stack):
                if callable(val):
                    rule = SemanticRule(
                        val,
                        node,
                        *avaliable_params,
                    )
                    to_stack[i] = rule
            
            # Stacks are FIFO, so we put it in reverse
            stack.extend(reversed(to_stack))

        # print(stack)
        if stack.pop() != END_MARKER:
            print("Oh no")
        
        return start_symbol

    def create_table(self):
        table = LL1Table()

        for production in self.grammar.productions:
            target_symbols = production.get_target_symbols()
            nullable = EPSILON in target_symbols

            if nullable:
                for symbol in self.grammar.follow[production.origin]:
                    table[production.origin, symbol] = production
            else:
                start_symbol = target_symbols[0]
                for symbol in self.grammar.first[start_symbol]:
                    if symbol == EPSILON:
                        continue
                    table[production.origin, symbol] = production

        self.table = table
