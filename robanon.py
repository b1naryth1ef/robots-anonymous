import time
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
        self.last_message = time.time()

    @Plugin.schedule(120, init=False)
    def keepalive(self):
        # TODO for over channels
        if time.time() - self.last_message > 75:
            self.send_one(
                    self.state.channels.get(self.config.channel_ids[0]),
                    random.choice(RESET_LINES))

    def send_one(self, channel, seed):
        res = self.get_cb_response(seed)
        if not res:
            raise Exception('WTF')

        channel.send_message(res)
        self.last_message = time.time()

    def get_cb_response(self, msg):
        for _ in range(10):
            try:
                res = self.cb.ask(msg)

                if PREVIOUS_LINES.count(res) > 3:
                    self.log.info('Resetting due to repeats: `%s`', res)
                    self.cb = Cleverbot()
                    msg = random.choice(RESET_LINES)
                    continue

                PREVIOUS_LINES.append(res)
                return res
            except:
                self.log.exception('Error: ')
                self.cb = Cleverbot()
                gevent.sleep(2)

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
        self.send_one(event.channel, event.content)
