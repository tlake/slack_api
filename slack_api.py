"""
A tiny Flask api app for the Import Campaign Slack team.

Does things like rolling dice.
"""

from flask import Flask, request
from flask_misaka import Misaka
from helpers import eprint
from slacker import Slacker

# import requests
import random
# import json
# import os


################################
# APP SETTINGS
################################

app = Flask(__name__)
Misaka(app)
app.config.update(
    DEBUG=True,
    SECRET_KEY="man, who knows?",
)


################################
# API ROUTES
################################

@app.route("/roll", methods=["POST"])
def roll():
    cmd = request.form['text']
    cmd = cmd.replace(" ", "")
    roll = ""
    operator = "+"
    modifier = 0

    if "+" in cmd:
        roll, modifier = cmd.split("+")
    elif "-" in cmd:
        operator = "-"
        roll, modifier = cmd.split("-")
    else:
        roll = cmd

    number, sides = roll.split("d")
    modifier = int(modifier)
    number = int(number)
    sides = int(sides)
    roll_result = 0
    for x in range(0, number):
        roll_result += random.randint(1, sides)
    roll_plus_mods = "{} {} {}".format(
            str(roll_result),
            operator,
            str(modifier)
    )
    result = roll_result + modifier if operator == "+" else roll_result - modifier

    final_result = "*{} rolls a {}* _({} = {})_".format(
            request.form['user_name'],
            result,
            cmd,
            roll_plus_mods
        )

    bot_token = 'xoxb-71214811344-NPIQodp1purOHDsTQaMUcC6N'
    s = Slacker(bot_token)
    bot_entry = [x for x in s.users.list().body['members'] if 'U236APVA4' in x['id']][0]
    bot_name = bot_entry['name']

    channel = request.form['channel_id']

    s.chat.post_message(
        channel,
        final_result,
        username=bot_name,
        icon_url="https://avatars.slack-edge.com/2016-08-19/71252185058_c239c22e9866f8a9d48f_48.png"
    )

    eprint("sent to slack")
    eprint(request.form)

    #  send_to_slack = {
    #      "text": final_result,
    #  }

    #  slack_headers = {"content-type": "application/json"}

    # req = requests.post(
    #     "https://hooks.slack.com/services/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",
    #     data = json.dumps(send_to_slack),
    #     headers = slack_headers,
    #  )

    return ('', 204)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5005)
