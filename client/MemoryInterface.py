'''
THIS MODULE INTERACTS WITH THE MEMORY
''' 
import config
import time, pickle
import xmlrpclib
import sys, socket

#HANDLE FOR MEMORY OPERATIONS
filesystem = [0]*config.TOTAL_NO_OF_SERVERS
alive = [False]*config.TOTAL_NO_OF_SERVERS
portOffset = int(sys.argv[1])


#REQUEST TO BOOT THE FILE SYSTEM

def Initialize_My_FileSystem():
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print ("ERROR: incorrect number of arguments, usage: python client.py server_port#")
        exit()
    print("File System Initializing......")

    raw_input("press enter after starting the servers.")

    for i in range(0, config.TOTAL_NO_OF_SERVERS):
        filesystem[i] = xmlrpclib.ServerProxy("http://localhost:" + str(portOffset + i) + "/")
        try:
            filesystem[i].ping()
        except socket.error:
            print("connection not established from server0" + str(i+1) + ".py")
            continue

        alive[i] = True
        print("connection established from server0" + str(i+1) + ".py")


    #time.sleep(2)
    #state = Memory.Initialize()
    print("File System Initialized!")


#REQUEST TO FETCH THE INODE FROM INODE NUMBER FROM SERVER
def inode_number_to_inode(inode_number):
    base_server = (inode_number // config.MAX_NUM_INODES) * 2
    for i in range(base_server, base_server + 2):
        if alive[i]:
            return pickle.loads(filesystem[i].inode_number_to_inode(pickle.dumps(inode_number % config.MAX_NUM_INODES)))

    raise Exception('you played yourself')


#REQUEST THE DATA FROM THE SERVER
def get_data_block(block_number):
    base_server = (block_number // config.TOTAL_NO_OF_BLOCKS) * 2
    for i in range(base_server, base_server + 2):
        if alive[i]:
            return ''.join(pickle.loads(filesystem[i].get_data_block(block_number % config.TOTAL_NO_OF_BLOCKS)))

    raise Exception('you played yourself')


#REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
def get_valid_data_block(server):
    base_server = (server // 2) * 2
    for i in range(base_server, base_server + 2):
        if alive[i]:
            return filesystem[i].get_valid_data_block() + (base_server // 2) * config.TOTAL_NO_OF_BLOCKS

    raise Exception('you played yourself')


#REQUEST TO MAKE BLOCKS RESUABLE AGAIN FROM SERVER
def free_data_block(block_number):
    base_server = (block_number // config.TOTAL_NO_OF_BLOCKS) * 2
    for i in range(base_server, base_server + 2):
        if alive[i]:
            filesystem[i].free_data_block(block_number % config.TOTAL_NO_OF_BLOCKS)


#REQUEST TO WRITE DATA ON THE THE SERVER
def update_data_block(block_number, block_data):
    base_server = (block_number // config.TOTAL_NO_OF_BLOCKS) * 2
    for i in range(base_server, base_server + 2):
        if alive[i]:
            filesystem[i].update_data_block(block_number % config.TOTAL_NO_OF_BLOCKS, pickle.dumps(block_data))


#REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE FROM SERVER
def update_inode_table(inode, inode_number):
    base_server = (inode_number // config.MAX_NUM_INODES) * 2
    for i in range(base_server, base_server + 2):
        if alive[i]:
            filesystem[i].update_inode_table(pickle.dumps(inode), pickle.dumps(inode_number % config.MAX_NUM_INODES))


#REQUEST FOR THE STATUS OF FILE SYSTEM FROM SERVER
def status():
    filesystem_status = ''
    for i in range(config.TOTAL_NO_OF_SERVERS):
        filesystem_status += pickle.loads(filesystem[i].status())
    
    return filesystem_status