import time
import os
import json
from google.cloud import pubsub_v1
from dotenv import load_dotenv

ENV_FILE="/workspaces/beam-streaming/python/global_windows_with_process_timestamp/.environment"

def load_config():
    load_dotenv(ENV_FILE)
    CREDENTIAL_PATH = os.getenv("CREDENTIAL_PATH")
    OUTPUT_SUBSCRIPTION = os.getenv("OUTPUT_SUBSCRIPTION")
    with open(CREDENTIAL_PATH, "r") as file:
        data = json.load(file)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIAL_PATH
    return OUTPUT_SUBSCRIPTION, data["project_id"]


def reciever_callback(message):
    print(f"recieved message: {message}")
    message.ack()


if __name__ == "__main__":
    output_subscription_id, project_id = load_config()
    output_subscription = (
        f"projects/{project_id}/subscriptions/{output_subscription_id}"
    )
    subscriber_client = pubsub_v1.SubscriberClient()
    subscriber_client.subscribe(output_subscription, callback=reciever_callback)

    while True:
        time.sleep(60)
