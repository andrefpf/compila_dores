from automata import FiniteAutomata
from grammar import Grammar, Production, EPSILON
from parser_ll1 import Parser


productions = [
    Production("EXPRESSION", ["OR"]),
    Production("OR", ["AND", "OR1"]),
    Production("OR1", ["|", "AND", "OR1"]),
    Production("OR1", [EPSILON]),

    Production("AND", ["UNITY", "AND1"]),
    Production("AND1", ["UNITY", "AND1"]),
    Production("AND1", [EPSILON]),

    Production("UNITY", ["GROUP", "UNITY1"]),
    Production("UNITY1", ["*"]),
    Production("UNITY1", ["+"]),
    Production("UNITY1", [EPSILON]),

    Production("GROUP", ["(", "EXPRESSION", ")"]),
    Production("GROUP", ["SYMBOL"]),
]

for i in "qwertyuiopasdfghjklçzxcvbnm QWERTYUIOPASDFGHJKLÇZXCVBNM 0123456789":
# for i in "a":
    productions.append(Production("SYMBOL", [i]))

regex_grammar = Grammar(productions)
syn = Parser(regex_grammar)

# for i in regex_grammar.first.items():
#     print(i)
# print()

# for i in regex_grammar.follow.items():
#     print(i)
# print()

# for a, b in syn.table.items():
#     print(a, "\t", b)
# print()

tokens = list("a|a(bc)")
syn.analyze(tokens)