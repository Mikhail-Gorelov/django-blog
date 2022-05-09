FROM dtzar/helm-kubectl:2.12.1

COPY sa_token.txt /sa_token.txt
COPY ca.pem /ca.pem

RUN CLUSTER_ID=catb3ppsdsh7vajr216f \
    && SA_TOKEN=$(< sa_token.txt) \
    && MASTER_ENDPOINT=https://51.250.80.194 \
    && kubectl config set-cluster k8s \
               --certificate-authority=ca.pem \
               --server=$MASTER_ENDPOINT \
               --kubeconfig=test.kubeconfig \
    && kubectl config set-credentials admin-user \
                --token=$SA_TOKEN \
                --kubeconfig=test.kubeconfig \
    && kubectl config set-context default \
               --cluster=k8s \
               --user=admin-user \
               --kubeconfig=test.kubeconfig \
    && kubectl config use-context default \
               --kubeconfig=test.kubeconfig \
    && helm init --stable-repo-url https://charts.bitnami.com/bitnami \
    && helm dep build \
    && helm install blogchart .
