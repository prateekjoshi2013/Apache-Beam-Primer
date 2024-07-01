import apache_beam as beam
from apache_beam.transforms.window import Duration, Sessions
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import os
import json
from dotenv import load_dotenv

ENV_FILE = "/workspaces/beam-streaming/python/session_window_with_process_timestamp/.environment"
window_size = Duration.of(10)  # Window size of 10 seconds


def load_config():
    load_dotenv(ENV_FILE)
    CREDENTIAL_PATH = os.getenv("CREDENTIAL_PATH")
    PUBSUB_INPUT_SUBSCRIPTION = os.getenv("PUBSUB_INPUT_SUBSCRIPTION")
    OUTPUT_TOPIC = os.getenv("OUTPUT_TOPIC")
    # Open the JSON file and load its content
    with open(CREDENTIAL_PATH, "r") as file:
        data = json.load(file)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIAL_PATH
    return OUTPUT_TOPIC, data["project_id"], PUBSUB_INPUT_SUBSCRIPTION


def print_row(row):
    print(row)
    return row


def encode_string_to_bytes(row):
    row = str(row)
    return row.encode("utf-8")


if __name__ == "__main__":
    output_topic_id, project_id, pubsub_input_subscription_id = load_config()
    pubsub_topic = f"projects/{project_id}/topics/{output_topic_id}"
    input_subscription = (
        f"projects/{project_id}/subscriptions/{pubsub_input_subscription_id}"
    )
    options = PipelineOptions()
    options.view_as(StandardOptions).streaming = True
    with beam.Pipeline(options=options) as pipeline:
        pubsub_data = (
            pipeline
            | "Read from pub sub"
            >> beam.io.ReadFromPubSub(subscription=input_subscription)
            # STR_2,Mumbai,PR_265,Cosmetics,8,39,66/r/n
            | "Remove extra chars appended by pubsub to records"
            >> beam.Map(lambda data: data.decode("utf-8").rstrip().lstrip())
            | "split by ," >> beam.Map(lambda row: row.split(","))
            # STR_2,Mumbai,PR_265,Cosmetics,8,39,66
            | "Filter By City: Mumbai,Bangalore"
            >> beam.Filter(lambda row: row[1] == "Mumbai" or row[1] == "Bangalore")
            # STR_2,Mumbai,PR_265,Cosmetics,8,39,66,216
            | "Form key value pair" >> beam.Map(lambda row: (row[3], int(row[4])))
            # Session Window of window_size sec
            | "Session Window of window_size sec"
            >> beam.WindowInto(Sessions(window_size))
            | "Sum profits per store_id " >> beam.CombinePerKey(sum)
            | "output" >> beam.Map(print_row)
            | "Encode from string to bytes for pubsub"
            >> beam.Map(encode_string_to_bytes)
            # converted record from string to byte because pubsub anly accepts bytes
            | "Write to pub sub" >> beam.io.WriteToPubSub(pubsub_topic)
        )
    result = pipeline.run()
    result.wait_until_finish()
