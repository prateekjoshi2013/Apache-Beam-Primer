resource "google_pubsub_topic" "producer_topic" {
  name                       = var.producer_topic_name
  message_retention_duration = "86600s"
}

resource "google_pubsub_subscription" "producer_subscription" {
  name                 = var.producer_topic_subscription_name
  topic                = google_pubsub_topic.producer_topic.id
  ack_deadline_seconds = 20
}
