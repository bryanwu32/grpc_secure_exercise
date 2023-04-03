import grpc
import psutil
import hardware_pb2
import hardware_pb2_grpc
from concurrent import futures

class HardwareServicer(hardware_pb2_grpc.HardwareServiceServicer):
    def GetUsage(self, request, context):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        return hardware_pb2.HardwareResponse(cpu_usage=cpu_usage, memory_usage=memory_usage)

def serve():
    server_key = open('certs/server.key', 'rb').read()
    server_cert = open('certs/server.crt', 'rb').read()

    # Load the root certificate
    with open('certs/ca.crt', 'rb') as f:
        root_certificates = f.read()

    credentials = grpc.ssl_server_credentials([(server_key, server_cert)], root_certificates, True)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hardware_pb2_grpc.add_HardwareServiceServicer_to_server(HardwareServicer(), server)
    server.add_secure_port('[::]:50051', credentials)
    print('Starting server. Listening on port 50051.')
    server.start()
    print('Server started!')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
