import os
import json
import re
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request
import facebook
import zalgoify
import datetime
import upsidedown


app = Flask(__name__)
F_PATTERN = re.compile('can i get an? (.+) in the chat', flags=re.IGNORECASE | re.MULTILINE)
SUFFIX = '❤️'
GROUP_ID = 1140136552771525
BDD_TIME = datetime.datetime(year=2019, month=4, day=15)
BOOLA_BOOLA = """Bulldog!  Bulldog!
Bow, wow, wow
Eli Yale
Bulldog!  Bulldog!
Bow, wow, wow
Our team can never fail

When the sons of Eli
Break through the line
That is the sign we hail
Bulldog!  Bulldog!
Bow, wow, wow
Eli Yale!"""

@app.route("/", methods=["POST"])
def webhook():
    """
    Receive callback to URL when message is sent in the group.
    """
    # Retrieve data on that single GroupMe message.
    message = request.get_json()
    print("Message received: %s" % message)
    matches = F_PATTERN.match(message["text"])
    if matches is not None and len(matches.groups()):
        reply(matches.groups()[0] + ' ' + SUFFIX)
    if message["sender_type"] != "bot":
        if message["text"].lower().startswith("zalgo"):
            reply(zalgoify.process(message["text"][6:]))
        if message["text"].lower().startswith("flip"):
            reply(upsidedown.transform(message["text"][5:]))
        if "bulldog days" in message["text"].lower():
            reply(bulldog_countdown())
        if "thank" in message["text"].lower() and "yalebot" in message["text"].lower():
            reply("You're welcome! :)")
        if "polls" in message["text"].lower():
            reply("There have been way too goddamn many polls in this chat.")
        if "favorite song" in message["text"].lower():
            reply(BOOLA_BOOLA)
        if "dad" in message["text"].lower():
            new_text = message["text"].strip().replace("dad", "dyd").replace("Dad", "Dyd").replace("DAD", "DYD")
            reply("Hey " + message["name"] + ", did you mean \"" + new_text + "\"?")
    if message["system"]:
        print("System message!")

    return "ok", 200

def bulldog_countdown():
    """
    Get time until Bulldog Days.
    """
    delta = BDD_TIME - datetime.datetime.now()
    seconds = delta.total_seconds()
    weeks, seconds = divmod(seconds, 60*60*24*7)
    days, seconds = divmod(seconds, 60*60*24)
    hours, seconds = divmod(seconds, 60*60)
    minutes, seconds = divmod(seconds, 60)
    string = 'There are '
    string += '%d weeks, ' % weeks
    string += '%d days, ' % days
    string += '%d hours, ' % hours
    string += '%d minutes, ' % minutes
    string += 'and %d seconds left until Bulldog Days.' % seconds
    return string

def reply(text):
    """
    Reply in chat.
    """
    url = "https://api.groupme.com/v3/bots/post"
    data = {
        "bot_id": os.environ["BOT_ID"],
        "text": text,
    }
    request = Request(url, urlencode(data).encode())
    response = urlopen(request).read().decode()
    print("Response after message send: %s" % response)

def vet_user(name: str):
    """
    Check Facebook to determine if user is part of the Yale '23 group.
    """
    os.environ['FACEBOOK_TOKEN']

