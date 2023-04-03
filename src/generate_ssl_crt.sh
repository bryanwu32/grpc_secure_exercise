#!/bin/bash
cd certs
# Generate a CA key
openssl genrsa -out ca.key 2048

# Generate a CA certificate
openssl req -x509 -new -nodes -key ca.key -subj "/CN=MyCA" -days 365 -out ca.crt

# Generate a server key
openssl genrsa -out server.key 2048

# Generate a server CSR
openssl req -new -key server.key -subj "/CN=localhost" -out server.csr

# Generate a server certificate signed by the CA
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365

# Generate a client key
openssl genrsa -out client.key 2048

# Generate a client CSR
openssl req -new -key client.key -subj "/CN=client" -out client.csr

# Generate a client certificate signed by the CA
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365
