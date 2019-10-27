from creds import BOT_CLIENT_ID, BOT_CLIENT_SECRET, BOT_USER_TOKEN

import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')


if __name__ == '__main__':
    client = MyClient()
    client.run(BOT_USER_TOKEN)
