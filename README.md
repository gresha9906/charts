helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  -n ingress-nginx --create-namespace \
  --set controller.image.repository=repo.polyus.com/k8s/ingress-nginx/controller \
  --set controller.image.tag=v1.12.6 \
  --set admissionWebhooks.patch.image.repository=repo.polyus.com/k8s/ingress-nginx/kube-webhook-certgen \
  --set admissionWebhooks.patch.image.tag=v1.5.1 \


Вариант A. Быстрый (NodePort, без TLS)

Подходит для закрытой тестовой сети. Для pull/push с узлов придётся разрешить insecure registry в containerd.

1) Namespace + PVC
kubectl create ns registry
cat <<'YAML' | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: registry-pvc
  namespace: registry
spec:
  accessModes: ["ReadWriteOnce"]
  resources:
    requests:
      storage: 20Gi
YAML

2) Config (опционально)

Можно пропустить — по умолчанию registry работает без аутентификации. Для минимума не нужен ConfigMap.

3) Deployment + Service (NodePort)
cat <<'YAML' | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: registry
  namespace: registry
spec:
  replicas: 1
  selector:
    matchLabels: { app: registry }
  template:
    metadata:
      labels: { app: registry }
    spec:
      containers:
      - name: registry
        image: registry:2
        ports:
        - containerPort: 5000
        env:
        - { name: REGISTRY_STORAGE_DELETE_ENABLED, value: "true" }
        volumeMounts:
        - name: data
          mountPath: /var/lib/registry
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: registry-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: registry
  namespace: registry
spec:
  type: NodePort
  selector: { app: registry }
  ports:
  - name: http
    port: 5000
    targetPort: 5000
    nodePort: 30500
YAML

4) Настроить containerd на рабочих/мастер-узлах (insecure)

Добавь в /etc/containerd/certs.d/<NODE_IP>:30500/hosts.toml:

server = "http://<NODE_IP>:30500"
[host."http://<NODE_IP>:30500"]
  capabilities = ["pull","resolve","push"]
  skip_verify = true


Перезапусти:

sudo systemctl restart containerd kubelet

5) Проверка с узла
# пример с nerdctl
nerdctl tag busybox:1.36 <NODE_IP>:30500/test/busybox:1.36
nerdctl push <NODE_IP>:30500/test/busybox:1.36
nerdctl pull <NODE_IP>:30500/test/busybox:1.36
