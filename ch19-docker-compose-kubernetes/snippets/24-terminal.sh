docker build -t catalog:1.0.0 .
docker build --check .
kind create cluster --name catalog
kind load docker-image catalog:1.0.0 --name catalog
kubectl create secret generic catalog \
  --from-literal=DATABASE_URL='postgresql+psycopg://catalog:...@db:5432/catalog'
helm lint chart/catalog
helm template catalog chart/catalog | less        # review before applying
helm upgrade --install catalog chart/catalog --wait
kubectl rollout status deployment/catalog-web
kubectl port-forward service/catalog 8000:80
