provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file("credential/credential.json")
}

module "airbyte" {
  source                = "./modules/airbyte"
  project_id            = var.project_id
  region                = var.region
  zone                  = var.zone
  machine_type          = var.machine_type
  service_account_email = var.service_account_email
}