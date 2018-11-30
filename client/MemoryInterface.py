'''
THIS MODULE INTERACTS WITH THE MEMORY
''' 
import time, pickle
import xmlrpclib
import sys

#HANDLE FOR MEMORY OPERATIONS
filesystem = 0


#REQUEST TO BOOT THE FILE SYSTEM

def Initialize_My_FileSystem():
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print ("ERROR: incorrect number of arguments, usage: python client.py server_port#")
        exit()
    print("File System Initializing......")
    global filesystem
    filesystem = xmlrpclib.ServerProxy("http://localhost:" + sys.argv[1] + "/")
    #time.sleep(2)
    #state = Memory.Initialize()
    print("File System Initialized!")


#REQUEST TO FETCH THE INODE FROM INODE NUMBER FROM SERVER
def inode_number_to_inode(inode_number):
    return pickle.loads(filesystem.inode_number_to_inode(pickle.dumps(inode_number)))


#REQUEST THE DATA FROM THE SERVER
def get_data_block(block_number):
    return ''.join(pickle.loads(filesystem.get_data_block(block_number)))


#REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
def get_valid_data_block():
    return filesystem.get_valid_data_block()


#REQUEST TO MAKE BLOCKS RESUABLE AGAIN FROM SERVER
def free_data_block(block_number):
    filesystem.free_data_block(block_number)


#REQUEST TO WRITE DATA ON THE THE SERVER
def update_data_block(block_number, block_data):
    filesystem.update_data_block(block_number, pickle.dumps(block_data))


#REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE FROM SERVER
def update_inode_table(inode, inode_number):
    filesystem.update_inode_table(pickle.dumps(inode), pickle.dumps(inode_number))


#REQUEST FOR THE STATUS OF FILE SYSTEM FROM SERVER
def status():
    return pickle.loads(filesystem.status())