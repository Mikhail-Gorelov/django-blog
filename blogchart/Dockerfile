FROM dtzar/helm-kubectl:2.12.1

WORKDIR /blogchart

COPY . /blogchart

ARG CERT
ENV CERT_DOCKER=$CERT

ARG SA_TOKEN
ENV SA_TOKEN_DOCKER=$SA_TOKEN

RUN CLUSTER_ID=cat608hordqashs53228 \
    && echo "$CERT_DOCKER" >> docker_ca.pem \
    && echo "$SA_TOKEN_DOCKER" >> docker_sa.txt \
    && echo "1" \
    && kubectl config set-cluster k8s \
               --certificate-authority=docker_ca.pem \
               --server=https://51.250.80.194 \
    && echo "2" \
    && kubectl config set-credentials admin-user \
                --token=docker_sa.txt \
    && echo "3" \
    && kubectl config set-context default \
               --cluster=k8s \
               --user=admin-user \
    && echo "4" \
    && kubectl config use-context default \
    && echo "5" \
    && kubectl get pods --namespace=redis \
    && helm --client-only init --stable-repo-url https://charts.bitnami.com/bitnami \
    && helm dep build . \
    && helm install blogchart .
