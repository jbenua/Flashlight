from .abstracts import AbstractFlashlightView


class ConsoleView(AbstractFlashlightView):
    def __init__(self):
        self.isOn = False
        self.color = [0, 0, 0]

    def ON(self, *args):
        if not self.isOn:
            self.isOn = True
            if self.color == [0, 0, 0]:
                self.color = [255, 255, 153]
            self.draw()

    def OFF(self, *args):
        if self.isOn:
            self.isOn = False
            self.draw()

    def COLOR(self, color):
        if len(color) != 3:
            return
        for val in color:
            if val < 0 or val > 255:
                return
        self.color = color
        self.draw()

    def draw(self):
        self.status = "ON" if self.isOn else "OFF"
        print("Flashlight:", self.status, self.color if self.isOn else '')
