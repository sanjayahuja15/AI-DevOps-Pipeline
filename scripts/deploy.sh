echo "Deploying application..."
kubectl apply -f webapp1/deployment.yaml
kubectl apply -f webapp1/service.yaml
echo "Deployment completed!"
