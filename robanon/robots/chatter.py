from . import Robot
from chatterbot import ChatBot

class ChatterRobot(Robot):
    async def ready(self):
        self.cb = ChatBot(self.client.user.name,
            storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
            database="./database.db")

    def message(self, message):
        return self.cb.get_response(message.content)
