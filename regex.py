from automata import FiniteAutomata
from grammar import Grammar, Production, Epsilon
from syntactic import Syntactic


productions = [
    Production("S", ["OR"]),
    Production("OR", ["AND", "OR1"]),
    Production("OR1", ["|", "OR"]),
    Production("OR1", [Epsilon()]),

    Production("AND", ["STAR", "AND1"]),
    Production("AND1", ["AND"]),
    Production("AND1", [Epsilon()]),

    Production("GROUP", ["(", "S", ")"]),
    Production("GROUP", ["[", "S", "]"]),
    Production("GROUP", ["SYMBOL", "GROUP1"]),
    Production("GROUP1", ["*"]),
    Production("GROUP1", ["+"]),
    Production("GROUP1", [Epsilon()]),
]

# for i in "qwertyuiopasdfghjklçzxcvbnm QWERTYUIOPASDFGHJKLÇZXCVBNM 0123456789":
for i in "AB|":
    productions.append(Production("SYMBOL", [i]))

regex_grammar = Grammar(productions)
syn = Syntactic(regex_grammar)

print(syn.table)

tokens = list("AB|A")
syn.analyze(tokens)