
class AbstractFlashlightController(object):

    def execute_tlv(tlv):
        raise NotImplementedError


class AbstractFlashlightView(object):

    def ON(self, *args):
        raise NotImplementedError

    def OFF(self, *args):
        raise NotImplementedError

    def COLOR(self, color):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

Commands = {
    b"\x12": {"length": 0,
             "value": None,
             "method": "ON"},
    b"\x13": {"length": 0,
             "value": None,
             "method": "OFF"},
    b"\x20": {"length": 3,
             "value": [int, int, int],
             "method": "COLOR"}}
