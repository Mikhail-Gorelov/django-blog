FROM dtzar/helm-kubectl:2.12.1

COPY . .

RUN CLUSTER_ID=catb3ppsdsh7vajr216f \
    && CERT=$(< sa_token.txt) \
    && SA_TOKEN=eyJhbGciOiJSUzI1NiIsImtpZCI6IjZtN2FRRzl0WVdyVHU4R09xUWlNU3FBcnRaLXJLSDBEN2NocFZrejgyQmcifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLWY3NWZuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiIwMDI2YmE4MC0yMjk4LTRkZDgtYTAzMC04YjRkZmM3NWM0NmIiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.dHD3BD98xDR1RPHXhk72cwnfZzLBjh2bypS_Afm3C7at1XPtAKQIRy97DOS8EltOzAX84KJeuSjp1ImGTdEKzsgeY46hPBxHt1O91wxSyaGzbQ-Xg9X47yJi2525X5DzSkeJAF2FJJ2hxeto8uGYgydh39UZQb_lnbj4pEyAD-yaBHSErQBTALGEuAQAl1lA0zm2L_DqTX7F945KK71J4bjm5CR2rM9alLP7AhdvzNk1YqUJ7320U6vvO2LhW6XxVcubXjYae801lC4cGRX3-038wjS70in5hkvqpF64ujBkFEqN21nhk1sWKVjxTRMyGtzT1hvRRwk4piodOkRdmQ \
    && MASTER_ENDPOINT=https://51.250.80.194 \
    && kubectl config set-cluster k8s \
               --certificate-authority=$CERT \
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
    && ls \
    && pwd \
    && kubectl get pods --namespace=redis --kubeconfig=test.kubeconfig \
    && helm init --stable-repo-url https://charts.bitnami.com/bitnami --kubeconfig=test.kubeconfig \
    && helm dep build --kubeconfig=test.kubeconfig \
    && helm install blogchart . --kubeconfig=test.kubeconfig
