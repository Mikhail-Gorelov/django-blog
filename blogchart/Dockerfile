FROM dtzar/helm-kubectl:2.12.1

WORKDIR /blogchart

COPY . /blogchart

RUN CLUSTER_ID=catb3ppsdsh7vajr216f \
    && ls \
    && MASTER_ENDPOINT=https://51.250.80.194 \
    && CERT=$(base64 -d ca.pem ) \
    && SA_TOKEN=$(base64 -d sa_token.txt ) \
    && echo "$CERT" | base64 --decode \
    && echo "$SA_TOKEN" | base64 --decode \
    && kubectl config set-cluster k8s \
               --certificate-authority=$CERT \
               --server=$MASTER_ENDPOINT \
    && kubectl config set-credentials admin-user \
                --token=$SA_TOKEN \
    && kubectl config set-context default \
               --cluster=k8s \
               --user=admin-user \
    && kubectl config use-context default \
    && echo "$MASTER_ENDPOINT" \
    && kubectl get pods --namespace=redis \
    && helm init --stable-repo-url https://charts.bitnami.com/bitnami /blogchart \
    && helm dep build /blogchart \
    && helm install blogchart /blogchart
