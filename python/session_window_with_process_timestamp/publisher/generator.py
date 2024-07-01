import os
import time
import json
from google.cloud import pubsub_v1
from dotenv import load_dotenv

ENV_FILE="/workspaces/beam-streaming/python/session_window_with_process_timestamp/.environment"

def load_config():
    load_dotenv(ENV_FILE)
    CREDENTIAL_PATH = os.getenv("CREDENTIAL_PATH")
    INPUT_FILE = os.getenv("INPUT_FILE")
    PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC")
    # Open the JSON file and load its content
    with open(CREDENTIAL_PATH, "r") as file:
        data = json.load(file)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIAL_PATH
    return INPUT_FILE,data["project_id"],PUBSUB_TOPIC

if __name__ == "__main__":
    input_file,project_id,pubsub_topic_id=load_config()
    pubsub_topic_id=f"projects/{project_id}/topics/{pubsub_topic_id}"
    pubsub_client = pubsub_v1.PublisherClient()
    with open(input_file, "rb") as ifp:
        header = ifp.readline()
        for line in ifp:
            event_data = line
            print("Publishing {0} to {1}".format(event_data, pubsub_topic_id))
            future = pubsub_client.publish(pubsub_topic_id, event_data)
            print(future.result())
            time.sleep(5)
