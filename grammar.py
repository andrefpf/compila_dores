from collections import defaultdict
from itertools import pairwise


class EndMarkerSymbol(str):
    def __repr__(self) -> str:
        return "$"

    def __str__(self) -> str:
        return "$"


class EpsilonSymbol(str):
    def __repr__(self) -> str:
        return "Є"

    def __str__(self) -> str:
        return "Є"

EPSILON = EpsilonSymbol()
END_MARKER = EndMarkerSymbol()

class GrammarSymbol(str):
    def __init__(self, *args, **kwargs):
        str.__init__(*args, **kwargs)

class Production:
    def __init__(self, origin: str, target: str | tuple[str], *, before_run=None, after_run=None):
        self.origin = GrammarSymbol(origin)
        self.target = self._fix_target_types(target)

    def get_target_symbols(self):
        return [i for i in self.target if not callable(i)]

    def get_non_empty_symbols(self):
        return [i for i in self.get_target_symbols() 
                if not isinstance(i, (EpsilonSymbol, EndMarkerSymbol))]

    def _fix_target_types(self, target):
        new_target = []
        for data in target:
            if callable(data):
                new_target.append(data)
            elif isinstance(data, (EpsilonSymbol, EndMarkerSymbol)):
                new_target.append(data)
            else:
                new_target.append(GrammarSymbol(data))
        return tuple(new_target)

    def __str__(self) -> str:
        targets = " ".join(str(i) for i in self.get_target_symbols())
        return f"{self.origin} → {targets}"


class Grammar:
    def __init__(self, productions: list[Production]):
        self.set_productions(productions)

    def start_symbol(self):
        return self.productions[0].origin

    def set_productions(self, productions: list[Production]):
        self.productions = productions
        self.calculate_terminal_symbols()
        self.calculate_first()
        self.calculate_follow()

    def calculate_terminal_symbols(self):
        self.terminal = set()
        self.non_terminal = set()
        for production in self.productions:
            for symbol in production.get_target_symbols():
                self.terminal.add(symbol)
            self.non_terminal.add(production.origin)
        self.terminal = self.terminal - self.non_terminal
        self.terminal = self.terminal - {EPSILON}

    def calculate_first(self):
        first = defaultdict(set)

        for symbol in self.terminal:
            first[symbol].add(symbol)

        modified = True
        while modified:
            modified = False

            for production in self.productions:           
                for symbol in production.get_target_symbols():
                    if symbol == EPSILON:
                        modified |= EPSILON not in first[production.origin]
                        first[production.origin].add(EPSILON)

                    to_append = first[symbol] - {EPSILON}
                    modified |= not to_append.issubset(first[production.origin])
                    first[production.origin] |= to_append

                    if EPSILON not in first[symbol]:
                        break

                else:
                    modified |= EPSILON not in first[production.origin]
                    first[production.origin].add(EPSILON)
        
        first.pop(EPSILON, None)
        self.first = dict(first)

    def calculate_follow(self):
        follow = defaultdict(set)

        start_symbol = self.productions[0].origin
        follow[start_symbol].add(END_MARKER)

        modified = True
        while modified:
            modified = False

            for production in self.productions:
                target_symbols = production.get_target_symbols()

                for sym_a, sym_b in pairwise(target_symbols):
                    to_append = self.first[sym_b] - {EPSILON}
                    modified |= not to_append.issubset(follow[sym_a])
                    follow[sym_a] |= to_append

                if target_symbols:
                    last_symbol = target_symbols[-1]
                    modified |= not follow[production.origin].issubset(follow[last_symbol])
                    follow[last_symbol] |= follow[production.origin]
                
                if len(target_symbols) >= 2:
                    if EPSILON in self.first[sym_b]:
                        follow[sym_a] |= follow[production.origin]

        follow.pop(EPSILON, None)
        self.follow = dict(follow)

    def __str__(self) -> str:
        string = "\n\t".join(str(i) for i in self.productions)
        return f"Grammar(\n\t{string}\n)"
