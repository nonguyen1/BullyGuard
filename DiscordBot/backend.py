from creds import BOT_CLIENT_TOKEN, DEMO_BOT_NICE_TOKEN, DEMO_BOT_MEAN_TOKEN

import discord
import pickle
import os
import math
import pickle
import sklearn


class Data():
    pass


class Ranker():
    def __init__(self, rank_data_file='ranking.pkl'):
        self.rank_data_file = rank_data_file
        self.rank = {}
        if os.path.exists(rank_data_file):
            self.rank = pickle.load(open(self.rank_data_file, 'rb'))

    def save_rank(self):
        pickle.dump(self.rank, open(self.rank_data_file, 'wb'))

    def reset_all(self):
        for key in self.rank.keys():
            self.rank[key] = 0

    def update(self, user_id, update_score):
        user_id = user_id.__str__()
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
    def __init__(self):
        # How to load the model on the server
        #MODEL_FILENAME = "../ml/saved_models/classifier.pkl"
        MODEL_FILENAME = "../ml/saved_models/classifier3.pkl"
        SENTIMENT_FILENAME = "../ml/saved_models/sentiment3.pkl"
        #SENTIMENT_FILENAME = "../ml/saved_models/sentiment.pkl"
        # Import our machine learning model here.
        self.model = pickle.load(open(MODEL_FILENAME, 'rb'))
        self.sent = pickle.load(open(SENTIMENT_FILENAME, 'rb'))

    def get_score(self, msg_content):
        # import pdb; pdb.set_trace()
        msg = self.sent.count_vect.transform([msg_content])
        result = self.model.predict_proba(msg)
        return result[0][1]


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
        await self.handle_message(message)
        if message.content == '!rank':
            await message.channel.send('display whatever')
        if message.content == '!clean':
            self.ranker.reset_all()

    async def update_role(self, user_id, new_role, message):
        await message.channel.send(f"{user_id} gets new role {new_role}!")
        guild = message.author.guild
        # import pdb; pdb.set_trace()
        for i in range(5):
            await message.author.remove_roles(discord.utils.get(guild.roles, name=str(i)))
        await message.author.add_roles(discord.utils.get(guild.roles, name=str(new_role)))

        # raise NotImplementedError()

    async def handle_message(self, message):
        channel = message.channel
        user_id = message.author
        msg_content = message.content
        msg_score = self.model.get_score(msg_content)
        await channel.send(f"Score {msg_score}")
        do_update_role, new_role = self.ranker.update(user_id, msg_score)
        if do_update_role:
            await self.update_role(user_id, new_role, message)


if __name__ == '__main__':
    client = MyClient()
    client.set_processor(Ranker(), Model())
    client.run(BOT_CLIENT_TOKEN)
