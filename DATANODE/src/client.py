import grpc
import sys
from google.protobuf.empty_pb2 import Empty
import protobufs.python.FileServices_pb2 as FileServicesStub
import protobufs.python.FileServices_pb2_grpc as FileServices_pb2_grpc

SERVER_ADDRESS = 'localhost:50051'

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
        response = self.stub.GetFile(request)
        return response

    def put_file(self, name, data):
        request = FileServicesStub.FileContent(name=name, data=bytes(data))
        response = self.stub.PutFile(request)
        return response

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
        print(f"File: {file_content.name}, Data: {file_content.data}")

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
