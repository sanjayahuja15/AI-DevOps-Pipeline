# Terraform Variables for AI-DevOps Pipeline

variable "flask_app_replicas" {
  description = "Number of Flask application replicas"
  type        = number
  default     = 2
}

variable "flask_app_port" {
  description = "Port on which Flask application runs"
  type        = number
  default     = 5000
}

variable "namespace_name" {
  description = "Kubernetes namespace for the application"
  type        = string
  default     = "ai-devops-pipeline"
}

variable "cpu_limit" {
  description = "CPU limit for container"
  type        = string
  default     = "500m"
}

variable "memory_limit" {
  description = "Memory limit for container"
  type        = string
  default     = "512Mi"
}

variable "enable_monitoring" {
  description = "Enable Prometheus monitoring"
  type        = bool
  default     = true
}
