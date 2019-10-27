from creds import BOT_CLIENT_ID, BOT_CLIENT_SECRET, BOT_USER_TOKEN

import discord
import math


class Ranker():
    def __init__(self):
        self.rank = dict()

    def save_rank(self):
        pass

    def update(self, user_id, update_score):
        score_change = update_score - 0.5

        if user_id in self.rank.keys():
            role_before = math.floor(self.rank[user_id])
            # Change score
            new_score = self.rank[user_id] + score_change
            self.rank[user_id] = self.fix_score(new_score)
            # Calculate potential role change
            new_role = math.floor(self.rank[user_id])
            self.save_rank()
            if new_role != role_before:
                return True, new_role
            else:
                return False, 0
        else:
            self.rank[user_id] = self.fix_score(score_change)
            print(type(self.rank[user_id]))
            self.save_rank()
            return True, math.floor(self.rank[user_id])

    def fix_score(self, new_score):
        """ Makes sure score within range """
        if new_score < 0:
            new_score = 0
        if new_score > 4:
            new_score = 4
        return new_score

    def get_rank(self, user_id):
        return 1


class Model():
    # FIXME: FAKE
    def __init__(self):
        pass

    def get_score(self, msg_content):
        print(f"MLing: score for {msg_content}")
        return int(msg_content)


class MyClient(discord.Client):
    def set_processor(self, ranker, model):
        self.ranker = ranker
        self.model = model

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        # TODO: Clean message for better ML
        await self.handle_message(message, message.channel)
        if message.content == '!rank':
            await message.channel.send('display whatever')

    async def update_role(self, user_id, new_role, broadcast_ch):
        await broadcast_ch.send(f"{user_id} gets new role {new_role}!")
        # raise NotImplementedError()

    async def handle_message(self, message, channel):
        user_id = message.author
        msg_content = message.content
        msg_score = self.model.get_score(msg_content)
        await channel.send(f"Score {msg_score}")
        do_update_role, new_role = self.ranker.update(user_id, msg_score)
        if do_update_role:
            await self.update_role(user_id, new_role, channel)


if __name__ == '__main__':
    client = MyClient()
    client.set_processor(Ranker(), Model())
    client.run(BOT_USER_TOKEN)
