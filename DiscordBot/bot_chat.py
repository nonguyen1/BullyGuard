from creds import BOT_CLIENT_TOKEN, DEMO_BOT_NICE_TOKEN, DEMO_BOT_MEAN_TOKEN

import discord
import time

import multiprocessing as mp

# TODO: Change this from hard code
MR_NICE = "MrNice#5609"
MR_MEAN = "MrMean#4769"
MR_NICE_CONV = ['You best think twice before you try to steal my stuff bitch.',
                'Yeah you did you lying two faced whore.', 'DUMB FUCK. ']
MR_MEAN_CONV = ['I didn\'t steal anything dude.', 'Please. Don\'t use mean words like that.', 'You hurt my feelings']
DEMO_CONV_LEN = 3


class MyClient(discord.Client):
    def set_id(self, the_id):
        self.id = the_id
        if the_id == 0:
            self.respond_to = MR_MEAN
            self.conv = MR_NICE_CONV
            self.current_msg_idx = 0
        elif the_id == 1:
            self.respond_to = MR_NICE
            self.conv = MR_MEAN_CONV
            self.current_msg_idx = -1
        else:
            raise NotImplementedError("Only 2 chatters are implemented")

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        global talk_state
        # don't respond to ourselves
        if message.author == self.user:
            return
        elif message.author.__str__() == self.respond_to:
            time.sleep(2)
            conv_msg = self.get_next_msg()
            if conv_msg:
                await message.channel.send(conv_msg)
        if message.content == '!start':
            if self.id == 0:  # Starter of this conversation
                self.current_msg_idx = -1
                conv_msg = self.get_next_msg()
                if conv_msg:
                    await message.channel.send(conv_msg)

    def get_next_msg(self):
        # TODO: Fix this nasty logic
        self.current_msg_idx += 1
        if self.current_msg_idx >= DEMO_CONV_LEN:
            return None
        else:
            if self.id == 1 and self.current_msg_idx == DEMO_CONV_LEN - 1:
                conv = self.conv[self.current_msg_idx]
                self.current_msg_idx = -1
                return conv
            else:
                return self.conv[self.current_msg_idx]


def bot_process(pid):
    print(f"Process{pid}")
    bot = MyClient()
    bot.set_id(pid)
    if pid == 0:
        bot.run(DEMO_BOT_NICE_TOKEN)
    elif pid == 1:
        bot.run(DEMO_BOT_MEAN_TOKEN)


if __name__ == '__main__':
    mrnice_process = mp.Process(target=bot_process, args=[0])
    mrmean_process = mp.Process(target=bot_process, args=[1])
    # mrnice_process.daemon = True
    # mrmean_process.daemon = True
    mrnice_process.start()
    mrmean_process.start()
