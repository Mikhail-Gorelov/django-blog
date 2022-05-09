ARG CERT
ARG SA_TOKEN

FROM dtzar/helm-kubectl:2.12.1

WORKDIR /blogchart

COPY . /blogchart

ENV CERT_DOCKER=$CERT

ENV SA_TOKEN_DOCKER=$SA_TOKEN

RUN CLUSTER_ID=cat608hordqashs53228 \
    && echo "1" \
    && kubectl config set-cluster k8s \
               --certificate-authority=$CERT \
               --server=https://51.250.80.194 \
               --kubeconfig=test.kubeconfig \
    && echo "2" \
    && kubectl config set-credentials admin-user \
                --token=$SA_TOKEN \
                --kubeconfig=test.kubeconfig \
    && echo "3" \
    && kubectl config set-context default \
               --cluster=k8s \
               --user=admin-user \
               --kubeconfig=test.kubeconfig \
    && echo "4" \
    && kubectl config use-context default \
               --kubeconfig=test.kubeconfig \
    && echo "5" \
    && cat test.kubeconfig \
    && kubectl get pods --namespace=redis --kubeconfig=test.kubeconfig \
    && helm --client-only init --stable-repo-url https://charts.bitnami.com/bitnami \
    && helm dep build . \
    && helm install blogchart .
