echo "Rolling back application..."
kubectl delete -f webapp1/deployment.yaml
kubectl delete -f webapp1/service.yaml
echo "Rollback completed!"
