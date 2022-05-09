FROM dtzar/helm-kubectl:2.12.1

WORKDIR /actions

RUN CLUSTER_ID=catb3ppsdsh7vajr216f \
    && kubectl create -f sa.yaml \
    && SA_TOKEN=$(kubectl -n kube-system get secret $(kubectl -n kube-system get secret | \
    grep admin-user | \
    awk '{print $1}') -o json | \
    jq -r .data.token | \
    base64 --d) \
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
