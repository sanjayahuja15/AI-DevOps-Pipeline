# Terraform Configuration README

## 🚀 AI-DevOps Pipeline - Terraform Infrastructure

This directory contains Infrastructure as Code (IaC) configurations using Terraform to automate the deployment of the AI-DevOps Pipeline to Kubernetes.

### 📋 Prerequisites

1. **Terraform** (v1.0+)
2. **Minikube** (Kubernetes cluster)
3. **Docker** (for container management)
4. **kubectl** (configured to access Minikube)

### 🗂️ File Structure

```
terraform/
├── main.tf           # Main Terraform configuration
├── variables.tf      # Variable definitions
└── README.md         # This file
```

### ⚙️ Configuration Files

#### `main.tf`
Defines the infrastructure resources:
- **Docker Image**: Manages the Flask webapp Docker image
- **Kubernetes Namespace**: Creates a dedicated namespace `ai-devops-pipeline`
- **Kubernetes Deployment**: Deploys Flask app with 2 replicas
- **Kubernetes Service**: Exposes the app via NodePort (30080)

#### `variables.tf`
Configurable parameters:
- `flask_app_replicas`: Number of pod replicas (default: 2)
- `flask_app_port`: Application port (default: 5000)
- `namespace_name`: Kubernetes namespace (default: ai-devops-pipeline)
- `cpu_limit`: CPU resource limit (default: 500m)
- `memory_limit`: Memory resource limit (default: 512Mi)

### 🚀 Usage

#### 1. Initialize Terraform
```bash
cd terraform
terraform init
```

#### 2. Review the Plan
```bash
terraform plan
```

#### 3. Apply the Configuration
```bash
terraform apply
```

#### 4. Verify Deployment
```bash
kubectl get all -n ai-devops-pipeline
```

#### 5. Access the Application
```bash
minikube service flask-webapp-service -n ai-devops-pipeline
```

#### 6. Destroy Resources (when done)
```bash
terraform destroy
```

### 📊 Outputs

After applying, Terraform will output:
- `deployment_name`: Name of the Kubernetes deployment
- `service_name`: Name of the Kubernetes service
- `namespace`: The Kubernetes namespace used

### 🔧 Customization

To customize the deployment, create a `terraform.tfvars` file:

```hcl
flask_app_replicas = 3
cpu_limit = "1000m"
memory_limit = "1Gi"
```

Then apply with:
```bash
terraform apply -var-file="terraform.tfvars"
```

### 🎯 Benefits of Using Terraform

1. **Version Control**: Infrastructure changes are tracked in Git
2. **Reproducibility**: Same configuration creates identical environments
3. **Automation**: Deploy/update/destroy with single commands
4. **State Management**: Terraform tracks resource state
5. **Plan Before Apply**: Preview changes before execution

### 🔄 Integration with DevOps Pipeline

This Terraform configuration can be integrated into the AI-DevOps pipeline by:

1. Adding a Terraform stage after the build phase
2. Using `terraform plan` in the planning agent
3. Applying infrastructure changes automatically
4. Rolling back with `terraform destroy` on failures

### 📝 Example Workflow

```bash
# Step 1: Build Docker image
docker build -t flask-webapp1:latest ./webapp1

# Step 2: Start Minikube
minikube start

# Step 3: Apply Terraform configuration
cd terraform
terraform init
terraform apply -auto-approve

# Step 4: Verify deployment
kubectl get pods -n ai-devops-pipeline

# Step 5: Test the application
minikube service flask-webapp-service -n ai-devops-pipeline --url
```

### ⚠️ Notes

- Ensure Minikube is running before applying Terraform
- The Docker image must be built before Terraform runs
- Use `imagePullPolicy: Never` for local images
- NodePort 30080 is exposed for external access

### 🌟 Future Enhancements

- Add Horizontal Pod Autoscaler (HPA) resource
- Integrate Prometheus monitoring
- Add ConfigMaps and Secrets management
- Multi-environment support (dev, staging, prod)
- AWS/Azure cloud provider configurations
