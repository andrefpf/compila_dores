from automata import FiniteAutomata
from grammar import Grammar, Production, Epsilon
from parser_ll1 import Parser


productions = [
    Production("OR", ["AND", "OR1"]),
    Production("OR1", ["|", "OR"]),
    Production("OR1", [Epsilon()]),

    Production("AND", ["GROUP", "AND1"]),
    Production("AND1", ["AND"]),
    Production("AND1", [Epsilon()]),

    Production("GROUP", ["(", "S", ")"]),
    Production("GROUP", ["[", "S", "]"]),
    Production("GROUP", ["SYMBOL", "GROUP1"]),
    Production("GROUP1", ["*"]),
    Production("GROUP1", ["+"]),
    Production("GROUP1", [Epsilon()]),
]

for i in "qwertyuiopasdfghjklçzxcvbnm QWERTYUIOPASDFGHJKLÇZXCVBNM 0123456789":
    productions.append(Production("SYMBOL", [i]))

regex_grammar = Grammar(productions)
syn = Parser(regex_grammar)

tokens = list("AB|A*|b")
syn.analyze(tokens)