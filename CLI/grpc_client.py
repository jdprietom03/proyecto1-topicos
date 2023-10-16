import grpc
import sys
from google.protobuf.empty_pb2 import Empty
import FileServices_pb2 as FileServicesStub
import FileServices_pb2_grpc as FileServices_pb2_grpc
CHUNK_SIZE = 1024 #TODO: read from config

class FileClient:
    def __init__(self, address):
        self.channel = grpc.insecure_channel(address)
        self.stub = FileServices_pb2_grpc.FileServiceStub(self.channel)
        self.chunk_count = 0

    def list_files(self):
        request = Empty()
        return self.stub.ListFiles(request)

    def find_file(self, name):
        request = FileServicesStub.FileRequest(name=name)
        return self.stub.FindFile(request)

    def get_file(self, name):
        try:
            request = FileServicesStub.FileRequest(name=name)
            file_data = b""

            self.chunk_count = 0
            filename = None
            response = self.stub.GetFile(request)
            for chunk in response:
                filename = chunk.name
                self.chunk_count += 1
                file_data += chunk.data
        except:
            return {
                "status": 500
            }

        return {
            "status": 200,
            "data": file_data,
            "filename": filename
        }

    def put_file(self, filename):
        chunks_generated = self.__generate_chunks(filename)

        return self.stub.PutFile(chunks_generated)
    
    def __generate_chunks(self, name):
        self.chunk_count = 0
        with open(name, 'rb') as f:
            while (chunk := f.read(CHUNK_SIZE)):
                yield FileServicesStub.FileContent(name=name, data=chunk)
                self.chunk_count += 1
            
    def set_host(host):
        return FileClient(f"{host}:50051")