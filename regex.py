from automata import FiniteAutomata
from grammar import Grammar, Production, EPSILON
from parser_ll1 import Parser

from treelib import Tree


class RegexNode:
    def __init__(self, *children):
        self.children = list(children)
        self.firstpos = set()
        self.lastpos = set()
        self.nullable = False

    def tree_str(self):
        def representation(node):
            if isinstance(node, UnionNode):
                return "or"
            elif isinstance(node, ConcatNode):
                return "."
            elif isinstance(node, SymbolNode):
                return node.symbol
            elif isinstance(node, ClosureNode):
                return "*"
            else:
                return ""

        tree = Tree()
        stack = [self]

        tree.create_node(representation(self), hash(self))
        while stack:
            node = stack.pop()
            for child in node.children:
                tree.create_node(representation(child), hash(child), parent=hash(node))
                stack.append(child)

        return tree

class UnionNode(RegexNode):
    pass


class ConcatNode(RegexNode):
    pass


class ClosureNode(RegexNode):
    pass


class EpsilonNode(RegexNode):
    pass


class EndMarkerNode(RegexNode):
    pass


class SymbolNode(RegexNode):
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol

# 
def op0_group(group, symbol):
    group.syn_tree = symbol.syn_tree

def op1_group(group, _0, expression, _1):
    group.syn_tree = expression.syn_tree

# 
def op0_unity(unity, group, unity1):
    unity1.her_tree = group.syn_tree

def op1_unity(unity, group, unity1):
    unity.syn_tree = unity1.syn_tree

def op2_unity(unity, _):
    unity.syn_tree = ClosureNode(unity.her_tree)

def op3_unity(unity, _):
    unity.syn_tree = ConcatNode(unity.her_tree, ClosureNode(unity.her_tree))

def op4_unity(unity, _):
    unity.syn_tree = unity.her_tree

#
def op0_and(_and, unity, and1):
    and1.her_tree = unity.syn_tree

def op1_and(_and, unity, and1):
    _and.syn_tree = and1.syn_tree

def op2_and(_and, unity, and1):
    and1.her_tree = ConcatNode(_and.her_tree, unity.syn_tree)

def op3_and(_and, _):
    _and.syn_tree = _and.her_tree

#
def op0_or(_or, _and, or1):
    or1.her_tree = _and.syn_tree

def op1_or(_or, _and, or1):
    _or.syn_tree = or1.syn_tree

def op2_or(or1_0, _, _and, or1_1):
    or1_1.her_tree = UnionNode(or1_0.her_tree, _and.syn_tree)

def op3_or(or1_0, _, _and, or1_1):
    or1_0.syn_tree = or1_1.syn_tree

def op4_or(or1, _):
    or1.syn_tree = or1.her_tree

# 
def op_expression(expression, _or):
    expression.syn_tree = _or.syn_tree

def op_symbol(symbol, char):
    symbol.syn_tree = SymbolNode(char)

productions = [
    Production("EXPRESSION", ["OR", op_expression]),

    Production("OR", ["AND", op0_or, "OR1", op1_or]),
    Production("OR1", ["|", "AND", op2_or, "OR1", op3_or]),
    Production("OR1", [EPSILON, op4_or]),

    Production("AND", ["UNITY", op0_and, "AND1", op1_and]),
    Production("AND1", ["UNITY", op2_and, "AND1", op1_and]),
    Production("AND1", [EPSILON, op3_and]),

    Production("UNITY", ["GROUP", op0_unity, "UNITY1", op1_unity]),
    Production("UNITY1", ["*", op2_unity]),
    Production("UNITY1", ["+", op3_unity]),
    Production("UNITY1", [EPSILON, op4_unity]),

    Production("GROUP", ["(", "EXPRESSION", ")", op1_group]),
    Production("GROUP", ["SYMBOL", op0_group]),
]

for i in "qwertyuiopasdfghjklçzxcvbnm QWERTYUIOPASDFGHJKLÇZXCVBNM 0123456789":
    prod = Production("SYMBOL", [i, op_symbol])
    productions.append(prod)

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

tokens = "ab|a(bc)d*"
s = syn.analyze(tokens)
