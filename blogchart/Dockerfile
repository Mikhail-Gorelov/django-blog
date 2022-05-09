FROM dtzar/helm-kubectl:2.12.1


RUN CLUSTER_ID=catb3ppsdsh7vajr216f \
    && CERT=$(cat <<-EndOfMessage
-----BEGIN CERTIFICATE-----
MIIC5zCCAc+gAwIBAgIBADANBgkqhkiG9w0BAQsFADAVMRMwEQYDVQQDEwprdWJl
cm5ldGVzMB4XDTIyMDUwODA4MzAyN1oXDTMyMDUwNTA4MzAyN1owFTETMBEGA1UE
AxMKa3ViZXJuZXRlczCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJ5t
6bR29Yzou4Z0ZzeAhU7xErNL3fPg/iTPskTxZ3ODotDms/3+ffzUeQ0lBae+fog9
QYKXYnNYmdS8B/YgEkJy4Rv3xdAgFJz+1TPpWK036mOVgzNiUsjoDvvuJjIpFfzV
GQiAIcWWBYWSx+j5LR7KRsSkKGZuaPwkSyFqBrOQGvuz1V1NLnODQswYI8NnPdDT
ZKHBXQPz+wGeJpQTuLXblky9xQlxvjxHWFOXTQZ5k7iblVw5ztpzSKvU8MpJEZrd
UASxNqk2h3jKdVuHtFJTW0fXsbo3SvjaLAZ0NoyznnpPXsZ0q0+xMivy5zagsxoS
VIBQ1rF/awwrwXHtHhMCAwEAAaNCMEAwDgYDVR0PAQH/BAQDAgKkMA8GA1UdEwEB
/wQFMAMBAf8wHQYDVR0OBBYEFLgUs8+ebONsEHbP8VEuLjqFHutLMA0GCSqGSIb3
DQEBCwUAA4IBAQAWCsqj/cxtE04/No1H/hHOIi9xo980/UCmE+F+VLn0kRWnKN1f
An0gSz0zOrBf7v5qk8doyruiKxTQIshk7RlaOxLO3t4Kp8VARhpRz9uQFN8vZ8q7
EOIvl/DNsy98s0yBCXgwDogyTIurPe/6Ib1L41VWBNXchS3W62JEffzP99anlqkv
BmvxnzprN4UKZ2iVLqLtDm3EWzNDCbe8hyZwXg0DuPZEob3ZPe7sew0IdAuvSNE+
muTQn4sKiXMdXPWVDIvLt/WypYOZitMgvaHvJ8a63WykdzLeSrlTmeYSoe5bPuMh
Bmf+DV7Vd4K/wz/xY+pljsGJ0IDEpr3d3mXo
-----END CERTIFICATE-----
EndOfMessage
    ) \
    && SA_TOKEN=eyJhbGciOiJSUzI1NiIsImtpZCI6IjZtN2FRRzl0WVdyVHU4R09xUWlNU3FBcnRaLXJLSDBEN2NocFZrejgyQmcifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLWY3NWZuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiIwMDI2YmE4MC0yMjk4LTRkZDgtYTAzMC04YjRkZmM3NWM0NmIiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.dHD3BD98xDR1RPHXhk72cwnfZzLBjh2bypS_Afm3C7at1XPtAKQIRy97DOS8EltOzAX84KJeuSjp1ImGTdEKzsgeY46hPBxHt1O91wxSyaGzbQ-Xg9X47yJi2525X5DzSkeJAF2FJJ2hxeto8uGYgydh39UZQb_lnbj4pEyAD-yaBHSErQBTALGEuAQAl1lA0zm2L_DqTX7F945KK71J4bjm5CR2rM9alLP7AhdvzNk1YqUJ7320U6vvO2LhW6XxVcubXjYae801lC4cGRX3-038wjS70in5hkvqpF64ujBkFEqN21nhk1sWKVjxTRMyGtzT1hvRRwk4piodOkRdmQ \
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
    && helm init --stable-repo-url https://charts.bitnami.com/bitnami \
    && helm dep build \
    && helm install blogchart .
