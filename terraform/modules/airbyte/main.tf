provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_compute_instance" "airbyte_vm" {
  name         = "airbyte-vm"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.image
      size  = 50
    }
  }

  network_interface {
    network = "default"

    access_config {
    }
  }

  tags = ["airbyte-server"]

  service_account {
    email  = var.service_account_email
    scopes = ["cloud-platform"]
  }
}

resource "google_compute_firewall" "allow_airbyte" {
  name    = "allow-airbyte"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8000"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["airbyte-server"]
}

resource "google_compute_disk" "airbyte_data" {
  name  = "airbyte-data"
  type  = "pd-standard"
  size  = 100
  zone  = var.zone
}

resource "google_compute_attached_disk" "airbyte_data_attachment" {
  disk     = google_compute_disk.airbyte_data.id
  instance = google_compute_instance.airbyte_vm.id
}