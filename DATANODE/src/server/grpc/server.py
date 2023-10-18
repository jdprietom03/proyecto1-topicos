from concurrent import futures
import os
import grpc
import logging
import protobufs.python.FileServices_pb2 as FileServicesStub
import protobufs.python.FileServices_pb2_grpc as FileServices_pb2_grpc
from IndexClient import IndexClient
from common.services import Service

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HOST = '[::]:50051'

class FileService(FileServices_pb2_grpc.FileServiceServicer):

    def __init__(self):
        self.indexClient = IndexClient()

    def ListFiles(self, request, context):
        logging.info("LIST request was received: %s", str(request))
        response = []

        for f in Service.listFiles():
            fileInfo = FileServicesStub.FileMetadata(name=f['name'],
                                                size=f['size'],
                                                timestamp=f['timestamp'])
            response.append(fileInfo)

        return FileServicesStub.FileList(metadata=response)

    def FindFile(self, request, context):
        logging.info("FIND request was received: %s", str(request))
        response = []

        data, err = Service.findFiles(request.name)
        if type(err) is PermissionError:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('You are trying to do path traversal. Denied')
            logging.warning("Path traversal: %s", request.name)
            return FileServicesStub.FileList(metadata=response)

        for f in data:
            fileInfo = FileServicesStub.FileMetadata(name=f['name'],
                                                size=f['size'],
                                                timestamp=f['timestamp'])
            response.append(fileInfo)

        return FileServicesStub.FileList(metadata=response)

    def GetFile(self, request, context):
        logging.info("GET request was received: %s", str(request))

        for name, chunk, e in Service.getFile(request.name):
            if e is not None:
                if isinstance(e, FileNotFoundError):
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('File not found')
                    logging.warning("File not found: %s", request.name)
                elif isinstance(e, PermissionError):
                    context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                    context.set_details('You are trying to do path traversal. Denied')
                    logging.warning("Path traversal: %s", request.name)
                else:
                    context.set_code(grpc.StatusCode.INTERNAL)
                    context.set_details(str(e))
                    logging.error("Error getting file: %s. Error: %s", request.name, str(e))
                return
            else:
                yield FileServicesStub.FileContent(name=name, data=chunk)

    def PutFile(self, request_iterator, context):
        logging.info("PUT request was received ")
        chunks = []
        name = ""
        for chunk in request_iterator:
            name = chunk.name 
            chunks.append(chunk.data)
        
        logging.info("%s chunks were received in the PUT request", len(chunks))
        message, exception = Service.putFile(name, chunks)

        if exception is not None:
            if isinstance(exception, FileNotFoundError):
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('File not found')
                logging.warning("File not found: %s", name)
            elif isinstance(exception, PermissionError):
                context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                context.set_details('You are trying to do path traversal. Denied')
                logging.warning("Path traversal: %s", name)
            else:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(exception))
                logging.error("Error putting file: %s. Error: %s", name, str(exception))
            return FileServicesStub.OperationStatus(code=context.code(), message=context.details())
        else:
            self.indexClient.addToIndex(name)
            return FileServicesStub.OperationStatus(code=grpc.StatusCode.OK.value[0], message=message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    FileServices_pb2_grpc.add_FileServiceServicer_to_server(
        FileService(), server)
    server.add_insecure_port(HOST)
    print("DataNode is running... ")
    indexClient = IndexClient().bootIndex()
    server.start()
    server.wait_for_termination()


def run():
    serve()
