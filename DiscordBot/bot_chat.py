from creds import BOT_CLIENT_TOKEN, DEMO_BOT_NICE_TOKEN, DEMO_BOT_MEAN_TOKEN

import discord
import time
import pickle
import os
import math
import pickle
import sklearn

import multiprocessing as mp
from multiprocessing.managers import BaseManager

# the multiprocessing queue
q = mp.Queue()

talk_state = 0


class MyClient(discord.Client):
    def set_id(self, the_id):
        self.id = the_id

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        global talk_state
        # don't respond to ourselves
        if message.author == self.user:
            return
        # TODO: Clean message for better ML
        if message.content == '!start':
            for i in range(10):
                if talk_state:  # MrNice
                    await message.channel.send('Yayy yayy')
                    talk_state = not talk_state
                    time.sleep(1)
                else:
                    await message.channel.send('Fuck fuck')
                    talk_state = not talk_state
                    time.sleep(1)


def mr_nice_process():
    print("Nice process")
    mrnice = MyClient()
    mrnice.set_id(0)
    mrnice.run(DEMO_BOT_NICE_TOKEN)


def mr_mean_process():
    print("Mean process")
    mrmean = MyClient()
    mrmean.set_id(1)
    mrmean.run(DEMO_BOT_MEAN_TOKEN)


if __name__ == '__main__':
    # Mr Nice
    mrnice_process = mp.Process(target=mr_nice_process)
    # Mr Mean
    mrmean_process = mp.Process(target=mr_mean_process)
    # mrnice_process.daemon = True
    # mrmean_process.daemon = True
    mrnice_process.start()
    mrmean_process.start()