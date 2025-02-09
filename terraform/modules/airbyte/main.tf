# resource "google_compute_instance" "airbyte_vm" {
#   name         = "airbyte-vm"
#   machine_type = var.machine_type
#   zone         = var.zone

#   boot_disk {
#     initialize_params {
#       image = "debian-cloud/debian-11"
#       size  = 50
#     }
#   }

#   network_interface {
#     network = "default"
#     access_config {}
#   }

#   service_account {
#     email  = var.service_account_email
#     scopes = ["cloud-platform"]
#   }
# }