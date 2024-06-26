provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}

terraform {
  backend "local" {}

  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.57.0"
    }
  }
}
