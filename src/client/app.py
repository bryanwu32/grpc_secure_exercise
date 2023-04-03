import grpc
import hardware_pb2
import hardware_pb2_grpc
import schedule
import datetime
import time
import os
import logging
import pytz
from constants import TIME_ZONE, FETCH_SECOND_INTERVAL

# create a logger with a file handler
logger = logging.getLogger('hardware_usage')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('hardware_usage.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def fetch_hardware_usage():
    # Load the client key and certificate chain
    with open('certs/client.key', 'rb') as f:
        private_key = f.read()
    with open('certs/client.crt', 'rb') as f:
        certificate_chain = f.read()

    # Load the root certificate
    with open('certs/ca.crt', 'rb') as f:
        root_certificates = f.read()

    # Create client credentials with mutual authentication enabled
    client_credentials = grpc.ssl_channel_credentials(root_certificates=root_certificates, private_key=private_key, certificate_chain=certificate_chain)

    # Create a gRPC channel with the server address and credentials


    server_address = os.environ.get("SERVER_HOST", "server") + ":50051"
    channel = grpc.secure_channel(server_address, client_credentials)
    # channel = grpc.secure_channel('localhost:50051', client_credentials)
    
    
    
    try:
        stub = hardware_pb2_grpc.HardwareServiceStub(channel)
        response = stub.GetUsage(hardware_pb2.HardwareRequest())
        time_zone = TIME_ZONE
        # Create a dictionary with the CPU and memory usage and the current time
        usage_dict = {
            'cpu_usage_percentage': round(response.cpu_usage,4),
            'memory_usage_percentage': round(response.memory_usage,4),
            'fetch_time': datetime.datetime.now(pytz.timezone(time_zone)).strftime("%Y-%m-%d %H:%M:%S")
        }

        # Print the dictionary
        print(usage_dict)
        logger.info(usage_dict)
        
    except grpc.RpcError as e:
        print(f"An error occurred: {e}")
        logger.info({"error": f"An error occurred: {e}"})


def run():

    fetch_second_interval = FETCH_SECOND_INTERVAL

    # Fetch the hardware usage once before scheduling the task
    fetch_hardware_usage()
    # Schedule the fetch_hardware_usage function to run every 10 seconds
    schedule.every(fetch_second_interval).seconds.do(fetch_hardware_usage)
    # Loop indefinitely and run scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run()
