helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  -n ingress-nginx --create-namespace \
  --set controller.image.repository=repo.polyus.com/k8s/ingress-nginx/controller \
  --set controller.image.tag=v1.12.6 \
  --set admissionWebhooks.patch.image.repository=repo.polyus.com/k8s/ingress-nginx/kube-webhook-certgen \
  --set admissionWebhooks.patch.image.tag=v1.5.1 \
