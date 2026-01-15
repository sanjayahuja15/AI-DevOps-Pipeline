# **AI-Powered DevOps Pipeline 🚀**
**Automating Security, Scaling, & Deployment with AI**

## **📌 Project Overview**
The **AI-Powered DevOps Pipeline** is an advanced CI/CD pipeline that integrates **machine learning, automated security scanning, and intelligent scaling** to optimize software deployment. This project enables:
- **Automated security scanning** with **Trivy** before deployment.
- **AI-driven auto-scaling** based on CPU usage predictions.
- **Proactive anomaly detection** for failure prevention.
- **Self-healing deployments** with rollback on failure.

---

## **⚙️ Tech Stack**
| **Technology**  | **Purpose**  |
|----------------|-------------|
| **Python**  | AI logic, automation scripts |
| **Kubernetes**  | Deployment & auto-scaling |
| **Terraform**  | Infrastructure as Code |
| **Trivy**  | Security scanning |
| **Prometheus & Grafana**  | Monitoring & visualization |
| **Jenkins/GitHub Actions**  | CI/CD automation |
| **Docker**  | Containerization |
| **AWS Cloud (Future Roadmap)**  | Cloud-based deployment |

---

## **📂 Project Structure**
```plaintext
AI-DevOps-Pipeline/
│── agents/                 # AI-powered automation agents
│   ├── analyze_requirements.py
│   ├── build_automation_agent.py
│   ├── deployment_automation_agent.py
│   ├── monitoring_alerting_agent.py
│   ├── testing_agent.py
│
│── webapp1/                # Flask-based web application
│   ├── app.py
│   ├── deployment.yaml
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── service.yaml
│
│── logs/                   # Log storage for build, test, and monitoring
│── scripts/                # Deployment and rollback scripts
│── tests/                  # Test scripts for automated validation
│── Dockerfile              # Container specification
│── devops_pipeline.py      # Main DevOps pipeline script
│── requirements.txt        # Dependencies
│── setup.py                # Package setup
│── README.md               # Project documentation

---

## **🚀 Getting Started**

### **📋 Prerequisites**

Before running the pipeline, ensure you have the following tools installed:

#### **Required Tools**
1. **Python 3.12+** - Runtime for the pipeline and AI agents
   ```bash
   python --version  # Verify installation
   ```

2. **Docker** - Container runtime for building and running images
   ```bash
   docker --version
   # Installation: https://docs.docker.com/get-docker/
   ```

3. **Kubernetes (kubectl & Minikube)** - Deployment orchestration
   ```bash
   kubectl version --client
   minikube version
   
   # Install kubectl: https://kubernetes.io/docs/tasks/tools/
   # Install Minikube: https://minikube.sigs.k8s.io/docs/start/
   
   # Start Minikube
   minikube start
   ```

4. **Trivy** - Security vulnerability scanner
   ```bash
   trivy --version
   
   # Install on Windows (using Chocolatey):
   choco install trivy
   
   # Install on macOS:
   brew install aquasecurity/trivy/trivy
   
   # Install on Linux:
   # See: https://aquasecurity.github.io/trivy/latest/getting-started/installation/
   ```

#### **Optional Tools (For Production)**
5. **Terraform** - Infrastructure as Code (for cloud deployments)
   ```bash
   terraform --version
   # Installation: https://developer.hashicorp.com/terraform/downloads
   ```

6. **Prometheus & Grafana** - Monitoring and visualization ✅ DEPLOYED
   ```bash
   # Already deployed in this project!
   # Access via port-forward:
   kubectl port-forward -n monitoring svc/grafana 3001:3000
   kubectl port-forward -n monitoring svc/prometheus 9091:9090
   
   # Then open: http://localhost:3001 (Grafana) and http://localhost:9091 (Prometheus)
   # Default login: admin / admin123
   ```

---

## **🎯 Quick Start - Monitoring Stack**

The project now includes **enterprise-grade monitoring** with Prometheus and Grafana!

**Access the Dashboards:**
```powershell
# Grafana (login: admin/admin123)
kubectl port-forward -n monitoring svc/grafana 3001:3000
# Open: http://localhost:3001

# Prometheus
kubectl port-forward -n monitoring svc/prometheus 9091:9090
# Open: http://localhost:9091

# Flask App Metrics
kubectl port-forward -n default deploy/devops-pipeline 5002:5000
# Open: http://localhost:5002/metrics
```

**What You Get:**
- ✅ Real-time Kubernetes cluster metrics
- ✅ Flask application metrics (requests, latency, CPU, memory)
- ✅ Custom AI-DevOps dashboards
- ✅ Health and readiness monitoring
- ✅ Automated metric scraping every 15 seconds

---

### **⚙️ Installation Steps**

#### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/sanjayahuja15/AI-DevOps-Pipeline.git
cd AI-DevOps-Pipeline
```

#### **2️⃣ Set Up Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
```

#### **3️⃣ Install Python Dependencies**
```bash
pip install -r requirements.txt
```

#### **4️⃣ Build Docker Image (Optional)**
```bash
docker build -t flask-webapp1:latest ./webapp1
```

#### **5️⃣ Deploy to Kubernetes (Optional)**
```bash
# Start Minikube if not running
minikube start

# Deploy the application
kubectl apply -f webapp1/deployment.yaml
kubectl apply -f webapp1/service.yaml

# Verify deployment
kubectl get pods
kubectl get services
```

#### **6️⃣ Run the DevOps Pipeline**
```bash
python devops_pipeline.py
```

---

## **🔍 Features**
✅ AI-Driven CI/CD Pipeline
Automates build, test, deploy, and rollback processes.
Uses GitHub Actions/Jenkins for CI/CD.
✅ Security Scanning
Trivy scans container images for vulnerabilities before deployment.
Blocks deployment if critical vulnerabilities are found.
✅ AI-Powered Auto-Scaling
Machine Learning (Linear Regression) predicts required replicas.
Uses Kubernetes HPA to dynamically adjust scaling.
✅ Anomaly Detection & Self-Healing
Isolation Forest ML model detects failures before they cause downtime.
Automatic rollback on failure detection.
✅ Monitoring & Alerts
Prometheus & Grafana track system health.
Alerts are sent when CPU spikes or anomalies occur.

---

## **🛠️ Troubleshooting**

### **Common Issues**

#### **1. Trivy Not Found**
If you see: `⚠️ Trivy not found in PATH — skipping image vulnerability scan`

**Solution:**
- The pipeline will continue without security scanning
- Install Trivy to enable vulnerability scanning:
  ```bash
  # Windows (Chocolatey)
  choco install trivy
  
  # macOS (Homebrew)
  brew install aquasecurity/trivy/trivy
  
  # Linux (download binary)
  wget https://github.com/aquasecurity/trivy/releases/latest/download/trivy_Linux-64bit.tar.gz
  tar zxvf trivy_Linux-64bit.tar.gz
  sudo mv trivy /usr/local/bin/
  ```

#### **2. Kubernetes/kubectl Not Found**
If deployment commands fail:

**Solution:**
- The pipeline runs locally without Kubernetes
- For full deployment features, install kubectl and Minikube:
  ```bash
  # Verify installation
  kubectl version --client
  minikube start
  ```

#### **3. Matplotlib Plots Not Saving**
If you don't see plot files in `logs/`:

**Solution:**
- Ensure the `logs/` directory exists
- Check write permissions
- Plots are saved as:
  - `logs/build_duration_plot.png`
  - `logs/system_metrics_plot.png`

#### **4. pytest Not Found in Virtual Environment**
**Solution:**
```bash
# Activate virtual environment first
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install pytest
pip install pytest==9.0.2
```

---

## **📌 Project Requirements & Tasks**

### **Functional Requirements**
- ✅ **Automated Error Logging** - All errors are logged to respective log files
- ✅ **Error-Triggered Rollback** - Pipeline automatically rolls back on failures
- ✅ **CLI Alerts** - Real-time alerts displayed in terminal during execution
- ✅ **AI-Powered Decision Making** - ML models for scaling and anomaly detection

### **Pipeline Components**
1. **Planning Agent** - Analyzes dependencies and requirements
2. **Build Agent** - Automates build with performance tracking
3. **Testing Agent** - Runs pytest with retry logic
4. **Monitoring Agent** - Tracks CPU, memory, disk with anomaly detection
5. **Security Scanner** - Trivy scans for vulnerabilities
6. **Deployment Agent** - Self-healing deployment with rollback
7. **Auto-Scaling** - AI predicts optimal replica count

---

## **📌 Roadmap to AWS Cloud Deployment**
We plan to migrate the AI-Powered DevOps Pipeline to AWS Free Tier for scalability and cost optimization. Below is the roadmap for transitioning from a local (Minikube) setup to AWS cloud infrastructure.

🌟 Phase 1: Move to AWS CodePipeline
Migrate GitHub repository to AWS CodeCommit.
Set up AWS CodePipeline + AWS CodeBuild for CI/CD.

🌟 Phase 2: Containerization with Amazon ECS
Push Docker images to Amazon Elastic Container Registry (ECR).
Deploy Flask web application on Amazon ECS with Fargate.

🌟 Phase 3: Automated Security & Monitoring
Enable Amazon Inspector for vulnerability scanning.
Use AWS CloudWatch & AWS X-Ray for logs and monitoring.

🌟 Phase 4: AI-Driven Auto-Scaling on AWS
Replace Kubernetes HPA with AWS Auto Scaling.
Use AWS Lambda for anomaly-based auto-scaling decisions.

🌟 Phase 5: Enhance Security with AWS IAM & WAF
Implement AWS IAM roles for access control.
Protect endpoints with AWS Web Application Firewall (WAF).

## **☁️ AWS Cloud Deployment Mapping**
| **Component**          | **AWS Service**                    | **Purpose**                                          |
|------------------------|------------------------------------|------------------------------------------------------|
| **Version Control**    | AWS CodeCommit                     | Stores project source code                          |
| **CI/CD Automation**   | AWS CodePipeline + CodeBuild       | Automates build, test, and deployment               |
| **Container Registry** | Amazon ECR                         | Stores Docker container images                      |
| **Application Deployment** | Amazon ECS (Fargate)           | Manages containerized workloads                     |
| **Networking & Security** | AWS ALB + Route 53 + AWS WAF    | Manages traffic routing & security                  |
| **Database (Optional)** | Amazon RDS                        | Structured data management                          |
| **Monitoring & Logging** | AWS CloudWatch + AWS X-Ray      | Logs application health & traces requests            |
| **Auto-Scaling**       | AWS Auto Scaling + ECS Service Scaling | AI-driven scaling based on demand               |
| **Security Scanning**  | Amazon Inspector + AWS Security Hub | Detects vulnerabilities in container images        |


🎯 Expected Benefits of AWS Migration
✅ Reduced Deployment Time – Faster deployments with AWS CodePipeline.
✅ Enhanced Security – Amazon Inspector & AWS Security Hub will automate security audits.
✅ Improved Monitoring – AWS CloudWatch & X-Ray provide real-time logs and tracing.
✅ AI-Driven Cost Optimization – AWS Auto Scaling dynamically adjusts compute resources.
✅ Higher Availability – Multi-region failover support with AWS Route 53.

📌 Contribution Guidelines
Want to contribute? Follow these steps:

Fork the repository.
Create a new branch: git checkout -b feature-branch
Make your changes and commit: git commit -m "Your changes"
Push to your fork: git push origin feature-branch
Create a pull request.
🚀 Let's Build the Future of AI-Powered DevOps! 🚀

### **Key Highlights in This README:**
✅ **Project Overview** with features  
✅ **Step-by-step setup guide** for running locally  
✅ **Detailed Roadmap to AWS Cloud**  
✅ **Mapping AWS services to our DevOps pipeline**  
✅ **Contribution guidelines for future improvements**  

This **README.md** provides complete documentation for **both local and AWS cloud implementations**, making it easy to push to GitHub for others to follow. 🚀

