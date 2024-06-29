output "output_topic_id" {
  value = google_pubsub_topic.output_topic.id
}

output "output_topic_subscription_id" {
  value = google_pubsub_subscription.output_subscription.id
}
