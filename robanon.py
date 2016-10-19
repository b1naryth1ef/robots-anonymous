import gevent
import random

from collections import deque

from cleverbot import Cleverbot
from disco.bot import Plugin, Config


PREVIOUS_LINES = deque(maxlen=50)
RESET_LINES = [
    'How is the weather?',
    'Who are you?',
    'lol',
    'wtf',
    'lmao',
    'you suck',
    'ok',
]


def get_delay():
    return random.randint(2000, 4500) / 1000.0


class RobanonConfig(Config):
    bot_cycle = {}

    channel_ids = []


@Plugin.with_config(RobanonConfig)
class RobanonPlugin(Plugin):
    def load(self):
        super(RobanonPlugin, self).load()
        self.cb = Cleverbot()

    @Plugin.listen('MessageCreate')
    def on_message_create(self, event):
        if event.channel.id not in self.config.channel_ids:
            return

        if event.author.id not in self.config.bot_cycle:
            return

        if self.state.me.id != self.config.bot_cycle[event.author.id]:
            return

        self.client.api.channels_typing(event.channel.id)
        gevent.sleep(get_delay())
        for _ in range(10):
            try:
                msg = self.cb.ask(event.content)

                # If we've sent the message more than 3 times, reset
                if PREVIOUS_LINES.count(msg) > 3:
                    self.cb = Cleverbot()
                    msg = self.cb.ask(random.choice(RESET_LINES))

                PREVIOUS_LINES.append(msg)
                event.reply(msg)
                break
            except:
                self.log.exception('Error hitting CB:')
                self.cb = Cleverbot()
                gevent.sleep(2)
        else:
            event.reply('halp me :(')
