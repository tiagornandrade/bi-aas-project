output "airbyte_vm_ip" {
  description = "IP público da VM do Airbyte"
  value       = google_compute_instance.airbyte_vm.network_interface.0.access_config.0.nat_ip
}

output "airbyte_web_url" {
  description = "URL para acessar o Airbyte"
  value       = "http://${google_compute_instance.airbyte_vm.network_interface.0.access_config.0.nat_ip}:8000"
}
