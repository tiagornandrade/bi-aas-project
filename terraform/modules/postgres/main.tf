resource "google_sql_database_instance" "main" {
  name             = "main-instance"
  database_version = "POSTGRES_15"
  region           = var.region
  project          = var.project_id

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_service_account" "db_sa" {
  account_id   = "db-service-account"
  display_name = "Database Service Account"
}

resource "google_project_iam_member" "db_sa_role" {
  project = var.project_id
  role    = "roles/cloudsql.admin"
  member  = "serviceAccount:${google_service_account.db_sa.email}"
}
