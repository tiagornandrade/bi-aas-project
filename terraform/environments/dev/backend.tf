terraform {
  backend "gcs" {
    bucket = "terraform-tf-states-bi-aas-project"
    prefix = "terraform/state"
  }
}
