kind create cluster
kubectl apply -f ./faas-netes/namespaces.yml
kubectl -n openfaas create secret generic basic-auth \
    --from-literal=basic-auth-user=admin \
    --from-literal=basic-auth-password=admin
kubectl apply -f ./faas-netes/yaml
kubectl get pods -n openfaas
kubectl get service -n openfaas