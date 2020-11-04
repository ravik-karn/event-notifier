import json
import os
from datetime import datetime

from mailjet_rest import Client


def notify():
    todays_event = __get_todays_events()
    if len(todays_event) == 0:
        print("No events today")
        return
    __send_email(todays_event)
    print("Notification sent")


def __get_todays_events():
    with open("resources/events.json") as f:
        events = json.load(f)
    today = datetime.today().strftime("%d %b")
    todays_event = list(filter(lambda event: event['date'] == today, events))
    return todays_event[0]['events'] if len(todays_event) > 0 else []


def __send_email(todays_event):
    api_key = os.environ["API_KEY"]
    api_secret = os.environ["API_SECRET"]
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [{
            "From": {"Email": os.environ["FROM_EMAIL"], "Name": os.environ["SENDER_NAME"]},
            "To": [{"Email": os.environ["TO_EMAIL"], "Name": os.environ["RECIEVER_NAME"]}],
            "Subject": "Event Reminder.",
            "TextPart": "\n".join(todays_event),
            "CustomID": "AppGettingStartedTest"
        }]
    }
    return mailjet.send.create(data=data)


if __name__ == '__main__':
    notify()
