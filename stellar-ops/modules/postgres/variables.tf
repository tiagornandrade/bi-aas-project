variable "project_id" {
  description = "ID do projeto no GCP"
  type        = string
}

variable "region" {
  description = "Região do GCP onde os recursos serão criados"
  type        = string
}

variable "zone" {
  description = "Zona do GCP onde a instância será criada"
  type        = string
}

variable "machine_type" {
  description = "Tipo de máquina da instância"
  type        = string
}

variable "service_account_email" {
  description = "E-mail da Service Account usada na instância"
  type        = string
}
