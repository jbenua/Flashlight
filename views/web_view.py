from tornado.web import RequestHandler
from .abstracts import AbstractFlashlightView
import json


class WebViewHandler(RequestHandler, AbstractFlashlightView):
    def initialize(self):
        self.isOn = False
        self.color = [0, 0, 0]

    def get(self):
        self.draw()

    def post(self):
        body = json.loads(self.request.body.decode('utf-8'))
        if not body:
            self.draw()
        for command in body:
            getattr(self, command[0])(command[1])

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
        color = self.color if self.isOn else [0, 0, 0]
        self.render('flashlight.html',
            r=color[0], g=color[1], b=color[2])
