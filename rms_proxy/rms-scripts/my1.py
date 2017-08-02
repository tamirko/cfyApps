

import requests
import json


def send_slack_message(incoming_slack_webhook, channel, sender_name, msg, **kwargs):
    headers = {'Content-type': 'application/json', }
    payload = json.dumps(
            {"channel": channel,
             "username": sender_name,
             "text": msg}
    )
    requests.post(incoming_slack_webhook, headers=headers, data=payload, )


rms_response = "{0}Failure{0}".format(chr(96))
resource_type = "car"
cost = 234988
message_from_rms = "The {2:,} response from RMS for adding *{0}* is *{1}*".format(resource_type, rms_response, cost)
sender_name = "Tamir"
channel = "operations"
incoming_slack_webhook ="https://hooks.slack.com/services/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"
send_slack_message(incoming_slack_webhook, channel, sender_name, message_from_rms)