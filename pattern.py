from typing import List, Tuple


class Pattern:
    ALPHA_DICT = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7,
        'i': 8,
        'j': 9,
        'k': 10,
        'l': 11,
        'm': 12,
        'n': 13,
        'o': 14,
        'p': 15,
        'q': 16,
        'r': 17,
        's': 18,
        't': 19,
        'u': 20,
        'v': 21,
        'w': 22,
        'x': 23,
        'y': 24,
        'z': 25,
        '': 26
    }

    ALPHA_LEN = len(ALPHA_DICT.keys())

    def __init__(self, pattern):
        self.pattern = pattern
        self.len = len(pattern)
        self.items = []
        self.states = 0
        self.itemize()
        self.fsa = None
        self.fsa_tablize()
        self.agenda = []

    def itemize(self):
        ppointer = 0
        while ppointer < self.len:
            a_item = ''
            a_item += self.pattern[ppointer]
            if ppointer < self.len - 1:
                if self.pattern[ppointer + 1] == '*':
                    a_item += '*'
                    ppointer += 1
            self.items.append(a_item)

            ppointer += 1
        self.states = len(self.items)

    def append_state(self, state_num, alpha, corr_state):
        list_p = self.fsa[state_num][self.ALPHA_DICT[alpha]]
        if len(list_p) and corr_state == list_p[-1]:
            append = False
        else:
            append = True
        if append:
            self.fsa[state_num][self.ALPHA_DICT[alpha]].append(corr_state)

    def append_all_alpha_state(self, state_num, corr_state):
        for i in range(self.ALPHA_LEN - 1):
            list_p = self.fsa[state_num][i]
            if len(list_p) and corr_state == list_p[-1]:
                append = False
            else:
                append = True
            if append:
                self.fsa[state_num][i].append(corr_state)

    def fill_single_alpha_state(self, state_num, alpha, corr_state=-1):
        if corr_state < 0:
            corr_state = state_num + 1
        if alpha != '.':
            self.append_state(state_num, alpha, corr_state)
        else:
            self.append_all_alpha_state(state_num, corr_state)

    def fill_alpha_state_conditional(self, state_num, alpha, corr_state, condition=lambda: True):
        if alpha != '.':
            self.append_state(state_num, alpha, corr_state)
        else:
            for i in range(self.ALPHA_LEN):
                if condition():
                    self.fsa[state_num][i].append(corr_state)

    def fsa_tablize_without_empty(self):
        self.fsa = [[[] for _ in range(self.ALPHA_DICT.keys().__len__())] for _ in range(self.states)]
        state_num = 0
        while state_num < self.states:
            state = self.items[state_num]
            if len(state) == 1:
                self.fill_single_alpha_state(state_num, state)
                if state_num < self.states - 1:
                    count = 1
                    append_end = False
                    while state_num + count < self.states:
                        next_state = self.items[state_num + count]
                        next_state_alpha = next_state[0]

                        if len(next_state) == 1:
                            break
                        else:
                            if state_num + count + 1 == self.states:
                                append_end = True
                            count += 1
                    if append_end:
                        self.fill_single_alpha_state(state_num, state, self.states)

            else:
                state_alpha = state[0]
                if state[1] == '*':

                    self.fill_single_alpha_state(state_num, state_alpha, state_num)
                    self.fill_single_alpha_state(state_num, state_alpha)

                    if state_num < self.states - 1:
                        count = 1
                        append_end = False
                        while state_num + count < self.states:
                            next_state = self.items[state_num + count]
                            next_state_alpha = next_state[0]

                            if len(next_state) == 1:
                                self.fill_single_alpha_state(state_num, next_state_alpha, state_num + count + 1)
                                break
                            else:
                                if not (next_state_alpha == state_alpha and state_num + count == state_num + 1):
                                    self.fill_single_alpha_state(state_num, next_state_alpha, state_num + count)
                                if next_state_alpha != state_alpha:
                                    self.fill_single_alpha_state(state_num, next_state_alpha, state_num + count + 1)
                                if state_num + count + 1 == self.states:
                                    append_end = True
                            count += 1
                        if append_end:
                            for count_more in range(count):
                                state = self.items[state_num + count_more]
                                state_alpha = state[0]
                                self.fill_single_alpha_state(state_num, state_alpha, self.states)

            state_num += 1

        for i in range(self.states):
            print(self.fsa[i])

    def fsa_tablize(self):
        self.fsa = [[[] for _ in range(self.ALPHA_LEN)] for _ in range(self.states)]

        state_num = 0
        while state_num < self.states:
            state = self.items[state_num]
            len_state = len(state)
            state_alpha = state[0]
            if len_state == 1:
                self.fill_single_alpha_state(state_num, state)
            elif len_state == 2:
                if state[1] == '*':
                    self.fill_single_alpha_state(state_num, state_alpha, state_num)
                    self.fill_single_alpha_state(state_num, state_alpha, state_num + 1)
                    self.fill_single_alpha_state(state_num, '', state_num + 1)

            state_num += 1

        for i in range(self.states):
            print(self.fsa[i])

    def next_agenda(self):
        if len(self.agenda) > 0:
            yield self.agenda[-1]
        else:
            yield StopIteration

    @staticmethod
    def accept_state(search_state: Tuple[int, int], len_s: int, accept_states: List[int]) -> bool:
        current_node, index = search_state

        if index == len_s and current_node in accept_states:
            return True
        else:
            return False

    def generate_states(self, search_state: Tuple[int, int], string):
        current_node, index = search_state

        if current_node < self.states:
            for i in self.fsa[current_node][self.ALPHA_DICT['']]:
                self.agenda.append((i, index))
            if index < len(string):
                c = string[index]
                for i in self.fsa[current_node][self.ALPHA_DICT[c]]:
                    self.agenda.append((i, index + 1))

    def match(self, string: str) -> bool:
        self.agenda.append((0, 0))
        len_s = len(string)

        while len(self.agenda) > 0:
            current_state = self.agenda.pop(0)
            if self.accept_state(current_state, len_s, [self.states]):
                return True
            else:
                self.generate_states(current_state, string)

            print(self.agenda)

        return False


if __name__ == '__main__':
    # for ps in ['abc', '.', 'a*', '.*', 'ab*c', 'ab*bc', 'ab*c*d', 'ab*c*d*e', 'ab*c*d*']:
    #     pat = Pattern(ps)
    #     print()

    # pat = Pattern('abc')
    # print(pat.match('abc'))
    #
    # pat = Pattern('.')
    # print(pat.match('a'))
    #
    # pat = Pattern('a*')
    # print(pat.match('a'))
    #
    # pat = Pattern('a*')
    # print(pat.match('aaaa'))
    #
    # pat = Pattern('a*aa')
    # print(pat.match('aaaa'))

    pat = Pattern("a*a*a*a*a*a*a*a*a*c")
    print(pat.match("aaaaaaaaaaaaaaaaaaab"))

    # pat = Pattern("a*a*a*a*a*a*a*a*a*a*")
    # pat.match("aaaaaaaaaaaaaaaaaaab")

    # pat = Pattern(".*ab.a.*a*a*.*b*b*")
    # print(pat.match("abcaaaaaaabaabcabac"))

    # pat = Pattern("a*a*.*b*b*")
