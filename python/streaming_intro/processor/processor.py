import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import os
import json
from dotenv import load_dotenv

ENV_FILE="/workspaces/beam-streaming/python/streaming_intro/.environment"

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
            | "Write to pub sub" >> beam.io.WriteToPubSub(pubsub_topic)
        )
    result = pipeline.run()
    result.wait_until_finish()
