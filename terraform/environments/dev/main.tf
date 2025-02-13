# module "airbyte" {
#   source                = "./modules/airbyte"
#   project_id            = var.project_id
#   region                = var.region
#   zone                  = var.zone
#   machine_type          = var.machine_type
#   service_account_email = var.service_account_email
# }

# module "postgres" {
#   source                = "../../modules/postgres"
#   project_id            = var.project_id
#   region                = var.region
#   zone                  = var.zone
#   machine_type          = var.machine_type
#   service_account_email = var.service_account_email
# }
