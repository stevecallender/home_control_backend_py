import boto3
from Casting import *
import time
import sys

class AlexaConnection(Caster):

        def __init__(self):
                ownIdentifier = "LightsCommand"
                super(AlexaConnection,self).__init__()           
                self.configureCaster(ownIdentifier,True)
                f= open("AlexaKey","r")
                access_key = "AKIAU7PSH5VX2SM4HM7E"
                access_secret = ""
                if f.mode == "r":
                    access_secret = f.read()[:-1]
                region ="us-east-2"
                self.queue_url = "https://sqs.us-east-2.amazonaws.com/342494801263/HomeControlCommands.fifo"
                self.client = boto3.client('sqs', aws_access_key_id = access_key, aws_secret_access_key = access_secret, region_name = region)


        def post_message(self,client, message_body, url):
                response = client.send_message(QueueUrl = url, MessageBody= message_body,MessageGroupId="Lights",MessageDeduplicationId="1")

        def pop_message(self,client, url):
                response = client.receive_message(QueueUrl = url, MaxNumberOfMessages = 10)
                #last message posted becomes messages
                message = response['Messages'][0]['Body']
                receipt = response['Messages'][0]['ReceiptHandle']
                client.delete_message(QueueUrl = url, ReceiptHandle = receipt)
                return message

        def run(self):
                while True:
                        time.sleep(3)
                        try:
                            message = self.pop_message(self.client, self.queue_url)
                            print(message)
                            self.cast(message)
                        except:
                            continue


if __name__ == "__main__":
        alexaCon = AlexaConnection()
        alexaCon.run()
