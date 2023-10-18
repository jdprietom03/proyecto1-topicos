import grpc
import protobufs.python.Add2Index_pb2 as Add2Index_pb2Stub
import protobufs.python.Add2Index_pb2_grpc as Add2Index_pb2_grpc
import protobufs.python.FileServices_pb2 as FileServices_pb2Stub
import protobufs.python.FileServices_pb2_grpc as FileServices_pb2_grpc
import os
import configparser
import urllib.request
import logging

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config', '.config'))

NAME_NODE_ADDRESS = os.getenv('NAME_NODE_HOST')

ASSETS_DIR = config['PATHS']['ASSETS_DIR']
RETRIES = int(config['RETRY']['RETRIES_ADD_IP'])

#Must be environment variables
NODES_TO_REPLICATE = config['NODES']['NODES_ADDRESSES']
LEADER_NODE = config['NODES']['LEADER_NODE']

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InfoClient:
    def __init__(self):
        self.name_node = NameNodeClient(self.ip)
        self.followers = []
        self.leader = None
        self.isLeader = False

    def process_boot(self):
        if not len(LEADER_NODE): #Means it is a leader node
            self.isLeader = True
            return
        
        self.leader = DataNodeClient(LEADER_NODE)
        self.leader.handle_redundancy_boot() #Starts to retrieve all files from its leader

        self.name_node.handle_index_boot(self.isLeader) #Once all the files are in this node, report to NameNode

    def process_new_file(self, path, data):
        self.name_node.handle_index_new_file(path)

        if not self.isLeader: #Means it is a follower node
            return
        elif not len(self.data_nodes): #Singleton
            for address in NODES_TO_REPLICATE:
                self.followers.append(DataNodeClient(address)) 
        
        for dn in self.followers: #Starts to send file to n followers nodes
            dn.handle_redundancy_new_file(path, data)
    
#Interactions with NameNode
class NameNodeClient:

    def __init__(self, ip):
        self.channel = grpc.insecure_channel(NAME_NODE_ADDRESS)
        self.stub = Add2Index_pb2_grpc.Add2IndexStub(self.channel)
        self.ip = self.__get_ip__
    
    def handle_index_new_file(self, path, isLeader):
        logging.info("Forwarding path to namenode, following path will be forwarded:\nIP:{self.ip}\nPath:{path}")
        for i in range(RETRIES):
                request = Add2Index_pb2Stub.add2IndexRequest(dataNodeIP=self.ip,path2Add=path,isLeader=isLeader)
                status_code = self.stub.add_2_index(request).statusCode
                if status_code == 200:
                    break
        return status_code
    
    def handle_index_boot(self, isLeader):
        logging.info("Booting index, following paths are at local asset:\nIP:{self.ip}")
        for path in os.listdir(ASSETS_DIR):
            print("path: ", path)
            for i in range(RETRIES):
                request = Add2Index_pb2Stub.add2IndexRequest(dataNodeIP=self.ip,path2Add=path,isLeader=isLeader)
                status_code = self.stub.add_2_index(request).statusCode
                if status_code == 200:
                    break
        return status_code
    
    def __get_ip__(self):
        return urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
    
#Interactions with other DataNodes
class DataNodeClient:

    def __init__(self, destination_address):
        self.channel = grpc.insecure_channel(destination_address)
        self.stub = FileServices_pb2_grpc.FileServiceStub(self.channel)

    #Push strategy
    def handle_redundancy_new_file(self, path, data):
        #He must send the file to this follower (destination_address).
        #So it must PUT the file. Build the message and send it.
        return
    
    #Pull strategy
    def handle_redundancy_boot(self):
        #Asks for its leader all the files it has.
        #So it has to LIST files directly with the leader address
        #Then it must GET all files from that node using the previous response.
        return