import apache_beam as beam
from apache_beam.transforms.window import FixedWindows
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import os
import json
from dotenv import load_dotenv

ENV_FILE = (
    "/workspaces/beam-streaming/python/fixed_window_with_event_timestamp/.environment"
)


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


def calculate_profit(row):
    """
    Store_id, Store_location, Product_id, Product_category, number_of_pieces_sold, buy_rate, sell_price,unix_timestamp
    STR_2,Mumbai,PR_265,Cosmetics,8,39,66,1553578221
    """
    number_of_pieces_sold = int(row[4])
    buy_price = int(row[5])
    sell_price = int(row[6])
    profit = (sell_price - buy_price) * number_of_pieces_sold
    row.append(str(profit))
    return row


def custom_timestamp(row):
    """
    Store_id, Store_location, Product_id, Product_category, number_of_pieces_sold, buy_rate, sell_price,unix_timestamp,profit
    STR_2,Mumbai,PR_265,Cosmetics,8,39,66,1553578221,216
    """
    unix_timestamp = int(row[7].strip())
    """
    - This creates a wrapper around the record by adding event timestamps from the record for windowing
    - It does not change the record structure for further processing
    """
    timestamped_record = beam.window.TimestampedValue(row, unix_timestamp)
    return timestamped_record


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
            >> beam.io.ReadFromPubSub(
                subscription=input_subscription, timestamp_attribute=1553578219
            )
            # STR_2,Mumbai,PR_265,Cosmetics,8,39,66,1553578221/r/n
            | "Remove extra chars appended by pubsub to records"
            >> beam.Map(lambda data: data.decode("utf-8").rstrip().lstrip())
            | "split by ," >> beam.Map(lambda row: row.split(","))
            # STR_2,Mumbai,PR_265,Cosmetics,8,39,66,1553578221
            | "Filter By City: Mumbai,Bangalore"
            >> beam.Filter(lambda row: row[1] == "Mumbai" or row[1] == "Bangalore")
            # STR_2,Mumbai,PR_265,Cosmetics,8,39,66,1553578221
            | "Caclulate Profit per record and append" >> beam.Map(calculate_profit)
            # STR_2,Mumbai,PR_265,Cosmetics,8,39,66,1553578221,216
            | "Apply custom timestamp" >> beam.Map(custom_timestamp)
            # TimestampedValue(STR_2,Mumbai,PR_265,Cosmetics,8,39,66,1553578221,216)
            | "Form key value pair" >> beam.Map(lambda row: (row[0], int(row[8])))
            # TimestampedValue(STR_2,216)
            | "Fixed 20 sec Window" >> beam.WindowInto(FixedWindows(5))
            # specifies a fixed windowing strategy where elements are grouped into fixed-size windows of 20 seconds each.
            # also this is a lazy operation and is done when needed at the end of pipeline
            | "Sum profits per store_id " >> beam.CombinePerKey(sum)
            | "output" >> beam.Map(print_row)
            | "Encode from string to bytes for pubsub"
            >> beam.Map(encode_string_to_bytes)
            # converted record from string to byte because pubsub anly accepts bytes
            | "Write to pub sub" >> beam.io.WriteToPubSub(pubsub_topic)
        )
    result = pipeline.run()
    result.wait_until_finish()
