import boto3
import json


class AWS:
    def __init__(self):
        self.comprehend = boto3.client(service_name='comprehend', region_name='us-east-2')

    def sentiment(self, sentence):
        return self.comprehend.detect_sentiment(Text=sentence, LanguageCode='en')



if __name__ == '__main__':
    text = "It is raining today in Seattle"
    aws = AWS()
    print('Calling DetectSentiment')
    print(json.dumps(aws.sentiment(text), sort_keys=True, indent=4))
    print('End of DetectSentiment\n')
