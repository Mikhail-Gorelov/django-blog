FROM dtzar/helm-kubectl:3.8.1

RUN kubectl config set-cluster k8s --server=${{ secrets.K8S_API }} \
    kubectl config set clusters.k8s.certificate-authority-data ${{ secrets.K8S_CA_DATA }} \
    kubectl config set-credentials yc-service-account --token=${{ secrets.K8S_TOKEN }} \
    kubectl config set-context default --cluster=k8s --user=yc-service-account \
    kubectl config use-context default \
    helm init https://charts.bitnami.com/bitnami \
    helm dep build \
    helm upgrade --install blogchart .
