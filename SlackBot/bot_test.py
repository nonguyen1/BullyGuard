import re
import slack
import time
import asyncio
import concurrent
from datetime import datetime
from tokens import slack_token


@slack.RTMClient.run_on(event='message')
async def say_hello(**payload):
    data = payload['data']
    print(f"USER={data['user']} on CHANNEL={data['channel']}, said:{data['text']}")


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
