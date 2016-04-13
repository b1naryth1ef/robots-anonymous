from . import Robot
from cleverbot import Cleverbot

class CleverRobot(Robot):
    async def ready(self):
        self.cb = Cleverbot()

    def message(self, message):
        return self.cb.ask(message.content)
