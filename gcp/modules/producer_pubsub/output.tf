output "producer_topic_id" {
  value = google_pubsub_topic.producer_topic.id
}

output "producer_topic_subscription_id" {
  value = google_pubsub_subscription.producer_subscription.id
}
