FROM dtzar/helm-kubectl:2.12.1

WORKDIR /blogchart

COPY . .

RUN CLUSTER_ID=catb3ppsdsh7vajr216f \
    && CERT=$(cat ca.pem) \
    && SA_TOKEN=$(cat sa_token.txt) \
    && MASTER_ENDPOINT=https://51.250.80.194 \
    && kubectl config set-cluster k8s \
               --certificate-authority=$CERT \
               --server=$MASTER_ENDPOINT \
    && kubectl config set-credentials admin-user \
                --token=$SA_TOKEN \
    && kubectl config set-context default \
               --cluster=k8s \
               --user=admin-user \
    && kubectl config use-context default \
    && cat sa_token.txt \
    && cat $CERT \
    && kubectl get pods --namespace=redis \
    && helm init --stable-repo-url https://charts.bitnami.com/bitnami \
    && helm dep build \
    && helm install blogchart .
