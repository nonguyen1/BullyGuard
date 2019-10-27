from creds import BOT_CLIENT_TOKEN, DEMO_BOT_NICE_TOKEN, DEMO_BOT_MEAN_TOKEN

import discord
import time

import multiprocessing as mp

# TODO: Change this from hard code
MR_NICE = "MrNice#5609"
MR_MEAN = "MrMean#4769"
# the multiprocessing queue
q = mp.Queue()

talk_state = 0


class MyClient(discord.Client):
    def set_id(self, the_id):
        self.id = the_id
        self.respond_to = MR_NICE if the_id == 1 else MR_MEAN

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        global talk_state
        # don't respond to ourselves
        if message.author == self.user:
            return
        elif message.author.__str__() == self.respond_to:
            time.sleep(2)
            await message.channel.send("Responder")
        if message.content == '!start':
            if self.id == 0:  # Starter of this conversation
                await message.channel.send('Starter')


def bot_process(pid):
    print(f"Process{pid}")
    bot = MyClient()
    bot.set_id(pid)
    if pid == 0:
        bot.run(DEMO_BOT_NICE_TOKEN)
    elif pid == 1:
        bot.run(DEMO_BOT_MEAN_TOKEN)


#
#
# def mr_mean_process():
#     print("Mean process")
#     mrmean = MyClient()
#     mrmean.set_id(1)
#     mrmean.run(DEMO_BOT_MEAN_TOKEN)


if __name__ == '__main__':
    mrnice_process = mp.Process(target=bot_process, args=[0])
    mrmean_process = mp.Process(target=bot_process, args=[1])
    # mrnice_process.daemon = True
    # mrmean_process.daemon = True
    mrnice_process.start()
    mrmean_process.start()
