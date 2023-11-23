DEAD_STATE_INDEX = -1


from dataclasses import dataclass


@dataclass
class State:
    name: str
    is_final: bool
    tag: str = ""

class FiniteAutomata:
    def __init__(
            self, 
            states: list, 
            transitions: list[int, str, int], 
            alphabet: str, 
            initial_state_index: int = 0
        ):
        self.states = states
        self.initial_state_index = initial_state_index
        self.alphabet = alphabet
        self.transition_map = self._create_transition_map(transitions)
    
    def iterate(self, string: str):
        """
        Iterates over a string yielding the current state of the automata.
        """

        current_state_index = self.initial_state_index
        yield current_state_index

        if current_state_index is DEAD_STATE_INDEX:
            return

        for symbol in string:
            current_state_index = self.compute(current_state_index, symbol)
            yield current_state_index
            if current_state_index is DEAD_STATE_INDEX:
                break
    
    def evaluate(self, string: str):
        """
        Checks if the string bellows to the automata language.
        """

        for state_index in self.iterate(string):
            last_state_index = state_index

        if last_state_index == DEAD_STATE_INDEX:
            return False
        else:
            state = self.states[last_state_index]
            return state.is_final

    def compute(self, origin, symbol):
        """
        Executes a single step of computation from a origin state through a symbol, then returns the next state.
        The symbol & is used to mark epsilon transitions. If the symbol to match in the string is & we look for
        a transition through "\\&", this way we can handle this symbol with the automata.
        """

        if symbol == "&":
            transition = (origin, "\\&")
        else:
            transition = (origin, symbol)

        return self.transition_map.get(transition, DEAD_STATE_INDEX)

    def _create_transition_map(self, transitions):
        """
        Turns a list of transitions in the format [(origin, symbol, state), ..., (origin, symbol, state)] into a dict
        """
        transition_map = dict()
        for origin, symbol, target in transitions:
            transition_map[(origin, symbol)] = target
        return transition_map