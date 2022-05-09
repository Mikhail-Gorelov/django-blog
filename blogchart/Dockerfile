FROM dtzar/helm-kubectl:2.12.1

ARG CERT
ARG SA_TOKEN

ENV CERT_DOCKER=$CERT

ENV SA_TOKEN_DOCKER=$SA_TOKEN

WORKDIR /blogchart

COPY . /blogchart


RUN CLUSTER_ID=cat608hordqashs53228 \
    && echo "${CERT_DOCKER}" >> cert.pem \
    && echo "1" \
    && kubectl config set-cluster k8s \
               --certificate-authority=cert.pem \
               --server=https://51.250.80.194 \
               --kubeconfig=test.kubeconfig \
    && echo "2" \
    && kubectl config set-credentials admin-user \
                --token="${SA_TOKEN_DOCKER//[$'\t\r\n ']}" \
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
    && helm init --stable-repo-url https://charts.bitnami.com/bitnami --kubeconfig=test.kubeconfig \
    && echo "6" \
    && helm dep build . --kubeconfig=test.kubeconfig \
    && echo "7" \
    && helm install blogchart . --kubeconfig=test.kubeconfig
