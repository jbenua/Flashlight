from views.abstracts import *
from struct import *


class FlashlightController(AbstractFlashlightController):

    def __init__(self, view=None):
        self.view = view

    def execute_tlv(self, tlv):
        commands = self._decompose_tlv(tlv)
        for t, v in commands.items():
            method = Commands[t]["method"]
            getattr(self.view, method)(v)

    def get_sequence(self, tlv):
        commands = self._decompose_tlv(tlv)
        sequence = []
        for c in commands:
            sequence.append((Commands[c]["method"], commands[c]))
        return sequence

    def _decompose_tlv(self, tlv):
        commands = dict()
        chars = (char for char in tlv)
        try:
            for c in chars:
                try:
                    command = unpack('>c', chr(c).encode())[0]  # 1-byte
                except error:
                    break
                if command not in Commands:
                    pass
                else:
                    t = command
                    length = ''.join([
                        chr(next(chars)), chr(next(chars))]).encode()  # 2-byte
                    l = unpack('>h', length)[0]
                    v = None
                    if l == Commands[t]["length"] and l > 0:
                        v = [next(chars) for i in range(l)]  # l-byte
                    if correct_tlv(t, l, v):
                        commands[t] = v
        except StopIteration:
            pass

        return commands


def correct_tlv(t, l, v):
    if t not in Commands:
        return False

    if Commands[t]["length"] != l:
        return False

    values_template = Commands[t]["value"]
    for i in range(l):
        if type(v[i]) is not values_template[i]:
            return False

    return True
