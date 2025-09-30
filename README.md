kubectl -n cattle-system patch settings.management.cattle.io server-url --type=merge -p '{"value":"https://mos-s-madptst09:30443"}'

--set controller.service.type=NodePort --set controller.service.nodePorts.http=30080 --set controller.service.nodePorts.https=30443

kubectl get svc -n cattle-system
kubectl expose deployment rancher --name=rancher-lb --port=443 --type=LoadBalancer -n cattle-system
kubectl get svc -n cattle-system

[Service]
Environment="CONTAINERD_LOG_LEVEL=debug"
# 1) Поды с метками релиза (если были)
kubectl -n <ns> get pods -l app.kubernetes.io/instance=<release> -o wide --show-labels

# 2) Узнать владельца конкретного пода
kubectl -n <ns> describe pod <pod-name> | sed -n '/Owner References/,$p'

# 3) Посмотреть, что создавали хуки Helm
helm get hooks <release> -n <ns> | less

# 4) Посмотреть все манифесты релиза (что именно должно было удалиться)
helm get manifest <release> -n <ns> | less



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

kubectl -n cattle-system create secret tls tls-rancher --cert=server.crt --key=server.key
