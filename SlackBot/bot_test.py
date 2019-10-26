import re
import slack
import time
import asyncio
import concurrent
from datetime import datetime
from tokens import slack_token
import traceback
import pickle
import re
import html

# Clean up message
RE_BRACKET = "\<.*?\>"  # Direct Mentions
RE_COLON = "\:.*?\:"  # Emoji
STR_REMOVE = '*_~`'
RE_REMOVE = [RE_BRACKET, RE_COLON]


@slack.RTMClient.run_on(event='message')
async def say_hello(**payload):
    data = payload['data']
    is_message = 'client_msg_id' in data.keys()
    if is_message:
        try:
            user_id = data['user']
            channel_id = data['channel']
            user_message = clean_msg(data['text'])
            print(f"{user_message}<-USER={user_id}\tCH={channel_id}")
        except:
            traceback.print_exc()
            pickle.dump(data, open("error_data.pkl", 'wb'))


def clean_msg(message_str):
    # Delete direct mentions and emoji
    for re_expr in RE_REMOVE:
        message_str = re.sub(re_expr, '', message_str)
    # Delete special formatting characters
    for i in STR_REMOVE:
        message_str = message_str.replace(i, '')
    # HTML unescape
    return html.unescape(message_str)


def sync_loop():
    while True:
        print("Hi there: ", datetime.now())
        time.sleep(5)


async def slack_main():
    loop = asyncio.get_event_loop()
    rtm_client = slack.RTMClient(token=slack_token, run_async=True, loop=loop)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    await asyncio.gather(
        loop.run_in_executor(executor, sync_loop),
        rtm_client.start()
    )


if __name__ == "__main__":
    asyncio.run(slack_main())
