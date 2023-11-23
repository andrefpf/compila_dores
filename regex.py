from automata import FiniteAutomata, State
from tokenizer import Tokenizer, Token
from grammar import Grammar, Production, EPSILON
from parser_ll1 import Parser

from collections import defaultdict
from collections import defaultdict, deque
from itertools import count
from treelib import Tree
from collections.abc import Generator


DIGITS = "0123456789"
LOWER_CASE = "abcdefghijklmnopqrstuvxwyz"
UPPER_CASE = "ABCDEFGHIJKLMNOPQRSTUVXWYZ"
ACCENTUATED = "áãàâãéêíóôúüçÁÀÂÉÊÍÓÔÚÜÇ"
ALPHANUMERIC = DIGITS + LOWER_CASE + UPPER_CASE

any_digit = "|".join(DIGITS)
any_lower_case = "|".join(LOWER_CASE)
any_upper_case = "|".join(UPPER_CASE)
any_alphanumeric = "|".join(ALPHANUMERIC)

class RegexNode:
    def __init__(self, *children):
        self.children = list(children)
        self.firstpos = set()
        self.lastpos = set()
        self.nullable = False

    def tree_str(self):
        """
        Returns a string that represents the tree graphically.
        """
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

    def __str__(self) -> str:
        return str(self.tree_str())

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
    unity.syn_tree = UnionNode(EpsilonNode(), unity.her_tree)

def op5_unity(unity, _):
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
    Production("UNITY1", ["?", op4_unity]),
    Production("UNITY1", [EPSILON, op5_unity]),

    Production("GROUP", ["(", "EXPRESSION", ")", op1_group]),
    Production("GROUP", ["SYMBOL", op0_group]),
]

for i in ALPHANUMERIC + " ":
    prod = Production("SYMBOL", [i, op_symbol])
    productions.append(prod)

class RegexTokenizer(Tokenizer):
    simplifications = {
        "[0-9]": f"({any_digit})",
        "[a-z]": f"({any_lower_case})",
        "[A-Z]": f"({any_upper_case})",
        "[a-Z]": f"({any_lower_case}|{any_upper_case})",
        "[a-zA-Z]": f"({any_lower_case}|{any_upper_case})",
    }

    def run(self, string: str) -> Generator[Token]:
        for shortcut, replacement in self.simplifications.items():
            string = string.replace(shortcut, replacement)

        special = False
        for i in string:
            if special:
                yield Token(f"\\{i}", f"\\{i}")

            elif i == "\\":
                special = True
                continue

            else:
                yield Token(name=i, lexema=i)

regex_tokenizer = RegexTokenizer()
regex_grammar = Grammar(productions)
regex_parser = Parser(regex_tokenizer, regex_grammar)

# for i in regex_grammar.first.items():
#     print(i)
# print()

# for i in regex_grammar.follow.items():
#     print(i)
# print()

# for a, b in syn.table.items():
#     print(a, "\t", b)
# print()

def anotate_tree(tree: RegexNode) -> RegexNode:
    tree = ConcatNode(tree, EndMarkerNode())
    _recursive_anotate_tree(tree, 0)
    return tree


def calculate_followpos(tree: RegexNode) -> defaultdict[int, set]:
    followpos = defaultdict(set)
    _recursive_followpos(tree, followpos)
    return dict(followpos)

def _recursive_followpos(tree: RegexNode, followpos: defaultdict[int, set]):
    if tree is None:
        return

    if isinstance(tree, ClosureNode):
        for i in tree.lastpos:
            for j in tree.firstpos:
                followpos[i].add(j)
        _recursive_followpos(tree.children[0], followpos)

    elif isinstance(tree, ConcatNode):
        left_node = tree.children[0]
        right_node = tree.children[1]
        for i in left_node.lastpos:
            for j in right_node.firstpos:
                followpos[i].add(j)
        _recursive_followpos(left_node, followpos)
        _recursive_followpos(right_node, followpos)

    elif isinstance(tree, UnionNode):
        left_node = tree.children[0]
        right_node = tree.children[1]
        _recursive_followpos(left_node, followpos)
        _recursive_followpos(right_node, followpos)


def _recursive_anotate_tree(tree: RegexNode, tag: int) -> int:
    """
    Recursive function to calculate firstpos and lastpos for all trees.
    """
    if isinstance(tree, EpsilonNode):
        tree.nullable = True
        return tag

    if isinstance(tree, (SymbolNode, EndMarkerNode)):
        tree.firstpos = {tag}
        tree.lastpos = {tag}
        tree.nullable = False
        return tag + 1

    if isinstance(tree, UnionNode):
        for node in tree.children:
            tag = _recursive_anotate_tree(node, tag)
        tree.firstpos = set.union(*[node.firstpos for node in tree.children])
        tree.lastpos = set.union(*[node.lastpos for node in tree.children])
        tree.nullable = any([node.nullable for node in tree.children])
        return tag

    if isinstance(tree, ConcatNode):
        for node in tree.children:
            tag = _recursive_anotate_tree(node, tag)
        
        left_node = tree.children[0]
        right_node = tree.children[1]

        if left_node.nullable:
            tree.firstpos = left_node.firstpos | right_node.firstpos
        else:
            tree.firstpos = left_node.firstpos

        if right_node.nullable:
            tree.lastpos = left_node.lastpos | right_node.lastpos
        else:
            tree.lastpos = right_node.lastpos

        tree.nullable = left_node.nullable and right_node.nullable
        return tag

    if isinstance(tree, ClosureNode):
        tag = _recursive_anotate_tree(tree.children[0], tag)
        tree.nullable = True
        tree.firstpos = tree.children[0].firstpos
        tree.lastpos = tree.children[0].lastpos
        return tag

def _get_automata_parameters(*, first_tagset, final_leaf_tag, alphabet, followpos, symbol_tags):
    states = []
    transitions = []

    tagset_to_index = defaultdict(count().__next__)  # gives a new index for new elements
    tagset_queue = deque()
    tagset_queue.appendleft(first_tagset)

    while tagset_queue:
        tagset = tagset_queue.pop()

        i = tagset_to_index[tagset]
        is_final = final_leaf_tag in tagset
        states.append(State(f"q{i}", is_final))

        for symbol in alphabet:
            u = frozenset()
            for i in tagset & symbol_tags[symbol]:
                u |= followpos[i]

            if u not in tagset_to_index:
                tagset_queue.appendleft(u)

            transition = (tagset_to_index[tagset], symbol, tagset_to_index[u])
            transitions.append(transition)

    return states, transitions


def get_leafs(tree):
    if isinstance(tree, SymbolNode):
        return [tree]

    leafs = []
    for node in tree.children:
        leafs.extend(get_leafs(node))
    return leafs


def compiles(expression: str) -> FiniteAutomata:
    """
    Converts a regular expression into equivalent Finite Automata.
    """

    node = regex_parser.analyze(expression)
    tree = node.syn_tree

    tree = anotate_tree(tree)
    followpos = calculate_followpos(tree)
    leafs = get_leafs(tree)

    alphabet = [leaf.symbol for leaf in leafs]

    symbol_tags = defaultdict(set)
    for leaf in leafs:
        symbol_tags[leaf.symbol] |= leaf.firstpos

    states, transitions = _get_automata_parameters(
        first_tagset=frozenset(tree.firstpos),
        final_leaf_tag=tuple(tree.children[1].firstpos)[0],
        alphabet=alphabet,
        followpos=followpos,
        symbol_tags=symbol_tags,
    )

    return FiniteAutomata(
        states=states, transitions=transitions, alphabet=alphabet, initial_state_index=0
    )




# tokens = "ab|a(bc)d*"
# print(s.syn_tree)

# automata = compiles(r"abc?")

# word = "ab"
# result = automata.evaluate(word)
# print(result)

# word = "abc"
# result = automata.evaluate(word)
# print(result)

