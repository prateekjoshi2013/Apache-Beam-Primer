terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.34.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.6.2"
    }
  }
}

provider "google" {
  # Configuration options
  project = var.project
  region  = var.region
}

module "producer_pubsub" {
  source                           = "../modules/producer_pubsub"
  producer_topic_name              = var.my_producer_topic
  producer_topic_subscription_name = var.my_producer_subscription
}

module "output_pubsub" {
  source                         = "../modules/output_pubsub"
  output_topic_name              = var.my_output_topic
  output_topic_subscription_name = var.my_output_subscription
}
