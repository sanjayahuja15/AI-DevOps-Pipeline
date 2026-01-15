# Terraform Configuration for AI-DevOps Pipeline Infrastructure
# This demonstrates Infrastructure as Code for the DevOps pipeline

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

# Provider Configuration for Kubernetes (Minikube)
provider "kubernetes" {
  config_path = "~/.kube/config"
}

# Provider Configuration for Docker
provider "docker" {
  host = "npipe:////./pipe/docker_engine"
}

# Docker Image Resource
resource "docker_image" "flask_webapp" {
  name         = "flask-webapp1:latest"
  keep_locally = true
}

# Kubernetes Namespace
resource "kubernetes_namespace" "devops" {
  metadata {
    name = "ai-devops-pipeline"
    labels = {
      app = "ai-devops"
    }
  }
}

# Kubernetes Deployment for Flask App
resource "kubernetes_deployment" "flask_app" {
  metadata {
    name      = "flask-webapp-deployment"
    namespace = kubernetes_namespace.devops.metadata[0].name
    labels = {
      app = "flask-webapp"
    }
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "flask-webapp"
      }
    }

    template {
      metadata {
        labels = {
          app = "flask-webapp"
        }
      }

      spec {
        container {
          image = docker_image.flask_webapp.name
          name  = "flask-webapp"
          
          image_pull_policy = "Never"

          port {
            container_port = 5000
          }

          resources {
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "256Mi"
            }
          }
        }
      }
    }
  }
}

# Kubernetes Service
resource "kubernetes_service" "flask_service" {
  metadata {
    name      = "flask-webapp-service"
    namespace = kubernetes_namespace.devops.metadata[0].name
  }

  spec {
    selector = {
      app = kubernetes_deployment.flask_app.spec[0].template[0].metadata[0].labels.app
    }

    port {
      port        = 80
      target_port = 5000
      node_port   = 30080
    }

    type = "NodePort"
  }
}

# Outputs
output "deployment_name" {
  value       = kubernetes_deployment.flask_app.metadata[0].name
  description = "The name of the Kubernetes deployment"
}

output "service_name" {
  value       = kubernetes_service.flask_service.metadata[0].name
  description = "The name of the Kubernetes service"
}

output "namespace" {
  value       = kubernetes_namespace.devops.metadata[0].name
  description = "The Kubernetes namespace"
}
