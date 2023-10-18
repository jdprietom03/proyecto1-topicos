import grpc
import protobufs.python.Add2Index_pb2 as Add2Index_pb2Stub
import protobufs.python.Add2Index_pb2_grpc as Add2Index_pb2_grpc
import os
import configparser
import urllib.request
from dotenv import load_dotenv

load_dotenv()

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config', '.config'))

SERVER_ADDRESS = os.getenv('GRPC_HOST')

ASSETS_DIR = config['PATHS']['ASSETS_DIR']
RETRIES = int(config['RETRY']['RETRIES_ADD_IP'])

class IndexClient:
    def __init__(self):
        self.channel = grpc.insecure_channel(SERVER_ADDRESS)
        self.stub = Add2Index_pb2_grpc.Add2IndexStub(self.channel)

    def bootIndex(self):
        ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
        print("Booting index, following paths are at local asset:")
        print("ip: ",ip)
        for path in os.listdir(ASSETS_DIR):
            print("path: ", path)
            for i in range(RETRIES):
                request = Add2Index_pb2Stub.add2IndexRequest(dataNodeIP=ip,path2Add=path)
                statusCode = self.stub.add_2_index(request).statusCode
                if statusCode == 200:
                    break
        return statusCode

    def addToIndex(self, path):
        ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
        print("forwarding path to namenode, following path will be forwarded:")
        print("ip: ",ip)
        print("path: ", path)

        for i in range(RETRIES):
                request = Add2Index_pb2Stub.add2IndexRequest(dataNodeIP=ip,path2Add=path)
                statusCode = self.stub.add_2_index(request).statusCode
                if statusCode == 200:
                    break
        return statusCode
