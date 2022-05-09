FROM dtzar/helm-kubectl:2.12.1

WORKDIR /blogchart

COPY . /blogchart

ARG CERT
ENV CERT_DOCKER=$CERT

ARG SA_TOKEN
ENV SA_TOKEN_DOCKER=$SA_TOKEN

RUN CLUSTER_ID=catb3ppsdsh7vajr216f \
    && ls \
    && echo "$SA_TOKEN_DOCKER" \
    && echo "$CERT_DOCKER" \
    && MASTER_ENDPOINT=https://51.250.80.194 \
    && kubectl config set-cluster k8s \
               --certificate-authority=$CERT_DOCKER \
               --server=$MASTER_ENDPOINT \
    && kubectl config set-credentials admin-user \
                --token=$SA_TOKEN_DOCKER \
    && kubectl config set-context default \
               --cluster=k8s \
               --user=admin-user \
    && kubectl config use-context default \
    && echo "$MASTER_ENDPOINT" \
    && kubectl get pods --namespace=redis \
    && helm init --stable-repo-url https://charts.bitnami.com/bitnami \
    && helm dep build . \
    && helm install blogchart .
