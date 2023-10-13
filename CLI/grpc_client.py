import grpc
import sys
from google.protobuf.empty_pb2 import Empty
import FileServices_pb2 as FileServicesStub
import FileServices_pb2_grpc as FileServices_pb2_grpc

class FileClient:
    def __init__(self, address):
        self.channel = grpc.insecure_channel(address)
        self.stub = FileServices_pb2_grpc.FileServiceStub(self.channel)

    def list_files(self):
        request = Empty()
        response = self.stub.ListFiles(request)
        return response

    def find_file(self, name):
        request = FileServicesStub.FileRequest(name=name)
        response = self.stub.FindFile(request)
        return response

    def get_file(self, name):
        request = FileServicesStub.FileRequest(name=name)
        try:
            response = { 
                "data": self.stub.GetFile(request),
                "status": 200
            }
        except:
            response = {
                "status": 500
            }

        return response

    def put_file(self, name, data):
        request = FileServicesStub.FileContent(name=name, data=bytes(data))
        response = self.stub.PutFile(request)
        return response
    
    def set_host(host):
        return FileClient(f"{host}:50051")
