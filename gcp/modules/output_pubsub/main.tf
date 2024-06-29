resource "google_pubsub_topic" "output_topic" {
  name                       = var.output_topic_name
  message_retention_duration = "86600s"
}

resource "google_pubsub_subscription" "output_subscription" {
  name                 = var.output_topic_subscription_name
  topic                = google_pubsub_topic.output_topic.id
  ack_deadline_seconds = 20
}
