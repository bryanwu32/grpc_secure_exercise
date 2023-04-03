# grpc_secure_exercise

The program is developed using MacOS(Intel chip). The instructions and scripts are based on MacOS.

# Instructions
--------------------------------------------------------------------------------

To run the program, please ensure you have installed tools stated below:
- docker & docker-compose

Here are the steps to build the container of both client and server:

1. Git clone the repository
2. In src directory, run "generate_ssl_crt.sh" to generate certs for both client and server side
3. Go to root directory, where the docker-compose.yml is located
4. Run the command "docker-compose up -d --build"
5. Run the command "docker exec -it (container_id/name) bash" to connect to the client container by container id or name (using "docker ps")
6. The hardware_usage of server could be found in hardware_usage.log, updated at 10s interval


# How the program works?
--------------------------------------------------------------------------------

```text
The program demonstrates how server side establish a service for publishing self hardware usage (i.e. CPU, Memory) to other services under mTLS local environment.
There are 2 containers: client and server. Their functionality is described below:

Server
- To get self hardware usage on both CPU and memory
- Create a service, using GRPC, that provides GetUsage() method to get the hardware usage of server

Client
- Send GetUsage() request to get server hardware usage
- Fetch hardware usage periodically (10s interval)
- Store the response as event log to a local file

```

```text
mTLS workflow is explained below:
1. Create a directory to store the certificates
2. Generate a CA key
3. Generate a CA certificate
4. Generate a server key
5. Generate a server CSR
6. Generate a server certificate signed by the CA
7. Generate a client key
8. Generate a client CSR
9. Generate a client certificate signed by the CA


Both party shares the same root CA for mutual authentication
```