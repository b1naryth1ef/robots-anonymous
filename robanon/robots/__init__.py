import discord
import asyncio

class Robot(object):
    def __init__(self, token, ids=None):
        self.token = token
        self.ids = ids or []
        self.client = discord.Client()
        self.client.event(self.on_ready)
        self.client.event(self.on_message)

    def run(self):
        return self.client.run(self.token)

    async def on_ready(self):
        print("Logged in as {} ({})".format(self.client.user.name, self.client.user.id))
        await self.ready()

    async def on_message(self, message):
        if message.channel.id == message.server.id:
            return

        if message.author.id not in self.ids:
            return

        for _ in range(6):
            try:
                await self.client.send_typing(message.channel)
                await asyncio.sleep(3)
                await self.client.send_message(message.channel, self.message(message))
                break
            except discord.errors.HTTPException:
                pass
            await asyncio.sleep(1)

    async def ready(self):
        raise NotImplementedError

    def message(self, message):
        raise NotImplementedError
