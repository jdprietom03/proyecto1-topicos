import grpc
import sys
from google.protobuf.empty_pb2 import Empty
import protobufs.python.FileServices_pb2 as FileServicesStub
import protobufs.python.FileServices_pb2_grpc as FileServices_pb2_grpc
import logging

logging.basicConfig(level=logging.DEBUG)

SERVER_ADDRESS = 'localhost:50051'

class FileClient:
    def __init__(self, address):
        self.channel = grpc.insecure_channel(address)
        self.stub = FileServices_pb2_grpc.FileServiceStub(self.channel)

    def list_files(self):
        request = Empty()
        return self.stub.ListFiles(request)

    def find_file(self, name):
        request = FileServicesStub.FileRequest(name=name)
        return self.stub.FindFile(request)

    def get_file(self, name):
        request = FileServicesStub.FileRequest(name=name)
        file_data = b""
        chunk_count = 0

        for chunk in self.stub.GetFile(request):
            chunk_count += 1
            #print(f"New chunk {chunk_count}:", chunk)
            file_data += chunk.data

        print(f"Total chunks received: {chunk_count}")
        return file_data

    def put_file(self, name, data):
        request = FileServicesStub.FileContent(name=name, data=bytes(data))
        return self.stub.PutFile(request)

def main():
    client = FileClient(SERVER_ADDRESS)

    if len(sys.argv) != 2:
        print("Usage: python3 main.py [list|find|get|put]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "list":
        files = client.list_files()
        for file in files.metadata:
            print(f"{file.name}, {file.size} bytes, modified at {file.timestamp}")

    elif action == "find":
        name = input("Enter the name of the file to find: ")
        found_files = client.find_file(name)
        for file in found_files.metadata:
            print(f"{file.name}, {file.size} bytes, modified at {file.timestamp}")

    elif action == "get":
        name = input("Enter the name of the file to get: ")
        file_content = client.get_file(name)
        #print(f"File: {name}, Data: {file_content}")

    elif action == "put":
        name = input("Enter the name of the file to upload: ")

        # Leer los datos del archivo
        try:
            with open(name, 'rb') as f:
                data = f.read()
        except FileNotFoundError:
            print(f"No such file: '{name}'")
            sys.exit(1)
        except IOError as e:
            print(f"Error reading file: {str(e)}")
            sys.exit(1)

        status = client.put_file(name, data)
        print(f"Status: {status.code}, Message: {status.message}")

    else:
        print("Invalid action. Usage: python3 main.py [list|find|get|put]")

if __name__ == "__main__":
    main()
