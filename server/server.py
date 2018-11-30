import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import pickle
import sys
import Memory

filesystem = Memory.Operations()

def inode_number_to_inode(inode_number):
    return pickle.dumps(filesystem.inode_number_to_inode(pickle.loads(inode_number)))

def get_data_block(block_number):
    return pickle.dumps(filesystem.get_data_block(block_number))
    
def get_valid_data_block():
    return filesystem.get_valid_data_block()

def free_data_block(block_number):
    filesystem.free_data_block(block_number)
    return True

def update_data_block(block_number, block_data):
    filesystem.update_data_block(block_number, pickle.loads(block_data))
    return True

def update_inode_table(inode, inode_number):
    filesystem.update_inode_table(pickle.loads(inode), pickle.loads(inode_number))
    return True

def status():
    return pickle.dumps(filesystem.status())

def ping():
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print "ERROR: incorrect number of arguments, usage: python server.py server_port#"
        exit()
    server = SimpleXMLRPCServer(("localhost", int(sys.argv[1])))
    print("Listening on port " + sys.argv[1] + "...")
    server.register_function(inode_number_to_inode, "inode_number_to_inode")
    server.register_function(get_data_block, "get_data_block")
    server.register_function(get_valid_data_block, "get_valid_data_block")
    server.register_function(free_data_block, "free_data_block")
    server.register_function(update_data_block, "update_data_block")
    server.register_function(update_inode_table, "update_inode_table")
    server.register_function(status, "status")
    server.register_function(ping, "ping")
    state = Memory.Initialize()
    server.serve_forever()





