'''
THIS MODULE INTERACTS WITH THE MEMORY
''' 
from __future__ import print_function
import config
import time, pickle
import xmlrpclib
import sys, socket

#HANDLE FOR MEMORY OPERATIONS
filesystem = [0]*config.TOTAL_NO_OF_SERVERS
alive = [False]*config.TOTAL_NO_OF_SERVERS
server_pairs = []
portOffset = 0


#REQUEST TO BOOT THE FILE SYSTEM

def Initialize_My_FileSystem():
    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print ("ERROR: incorrect number of arguments, usage: python client.py <port> <time>")
        exit()
    print("File System Initializing......")

    global server_pairs
    portOffset = int(sys.argv[1])
    for i in range(config.TOTAL_NO_OF_SERVERS / 2):
        server_pairs += [[i*2, i*2 + 1]]

    print(server_pairs)

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
def inode_number_to_inode(inode_number, print_servers=False):
    serv_pair = server_pairs[(inode_number // config.MAX_NUM_INODES)]  

    if print_servers:
        server_pairs[(inode_number // config.MAX_NUM_INODES)] = serv_pair[::-1]
        print("Servers with data:", end='')
        for i in range(min(serv_pair), min(serv_pair) + 2):
            if alive[i]:
                print(" " + str(i + 1), end='')
        print()
        time.sleep(int(sys.argv[2]))

        print("Servers available:", end='')
        for i in range(min(serv_pair), min(serv_pair) + 2):
            if alive[i]:
                try:
                    filesystem[i].ping()
                    print(" " + str(i + 1), end='')
                except:
                    alive[i] = False
        print()


    for i in serv_pair:
        if alive[i]:
            try:
                if print_servers:
                    print("Attempting read from server " + str(i+1))
                    time.sleep(int(sys.argv[2]))
                return pickle.loads(filesystem[i].inode_number_to_inode(pickle.dumps(inode_number % config.MAX_NUM_INODES)))
            except socket.error:
                alive[i] = False
                if print_servers:
                    print("Read from server " + str(i+1) + " failed")



    raise Exception('you played yourself')


#REQUEST THE DATA FROM THE SERVER
def get_data_block(block_number):
    base_server = (block_number // config.TOTAL_NO_OF_BLOCKS) * 2
    for i in range(base_server, base_server + 2):
        if alive[i]:
            try:
                return ''.join(pickle.loads(filesystem[i].get_data_block(block_number % config.TOTAL_NO_OF_BLOCKS)))
            except socket.error:
                alive[i] = False

    raise Exception('you played yourself')


#REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
def get_valid_data_block(server):
    base_server = (server // 2) * 2
    for i in range(base_server, base_server + 2):
        if alive[i]:
            try:
                return filesystem[i].get_valid_data_block() + (base_server // 2) * config.TOTAL_NO_OF_BLOCKS
            except socket.error:
                alive[i] = False

    raise Exception('you played yourself')


#REQUEST TO MAKE BLOCKS RESUABLE AGAIN FROM SERVER
def free_data_block(block_number):
    base_server = (block_number // config.TOTAL_NO_OF_BLOCKS) * 2
    for i in range(base_server, base_server + 2):
        if alive[i]:
            try:
                filesystem[i].free_data_block(block_number % config.TOTAL_NO_OF_BLOCKS)
            except socket.error:
                alive[i] = False


#REQUEST TO WRITE DATA ON THE THE SERVER
def update_data_block(block_number, block_data):
    base_server = (block_number // config.TOTAL_NO_OF_BLOCKS) * 2
    for i in range(base_server, base_server + 2):
        if alive[i]:
            try:
                filesystem[i].update_data_block(block_number % config.TOTAL_NO_OF_BLOCKS, pickle.dumps(block_data))
            except socket.error:
                alive[i] = False

#REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE FROM SERVER
def update_inode_table(inode, inode_number, print_servers=False):
    base_server = (inode_number // config.MAX_NUM_INODES) * 2
    if print_servers:
        print("Servers with file:", end='')
        for i in range(base_server, base_server + 2):
            if alive[i]:
                print(" " + str(i + 1), end='')
        print()
        time.sleep(int(sys.argv[2]))

        print("Servers available:", end='')
        for i in range(base_server, base_server + 2):
            if alive[i]:
                try:
                    filesystem[i].ping()
                    print(" " + str(i + 1), end='')
                except:
                    alive[i] = False
        print()

    for i in range(base_server, base_server + 2):
        if alive[i]:
            try:
                if print_servers:
                    print("Attempting write on server " + str(i+1))
                    time.sleep(int(sys.argv[2]))
                filesystem[i].update_inode_table(pickle.dumps(inode), pickle.dumps(inode_number % config.MAX_NUM_INODES))
            except socket.error:
                alive[i] = False
                if print_servers:
                    print("Write to server " + str(i+1) + " failed")


#REQUEST FOR THE STATUS OF FILE SYSTEM FROM SERVER
def status():
    filesystem_status = ''
    for i in range(config.TOTAL_NO_OF_SERVERS):
        if alive[i]:
            try:
                filesystem_status += pickle.loads(filesystem[i].status())
            except socket.error:
                alive[i] = False
    
    return filesystem_status