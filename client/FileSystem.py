import MemoryInterface, AbsolutePathNameLayer
import time, sys

allowed_commands = ["mkdir", "create", "mv", "read", "write", "status", "rm", "exit"]

def Initialize_My_FileSystem():
    MemoryInterface.Initialize_My_FileSystem()
    AbsolutePathNameLayer.AbsolutePathNameLayer().new_entry('/', 1)

#HANDLE TO ABSOLUTE PATH NAME LAYER
interface = AbsolutePathNameLayer.AbsolutePathNameLayer()

class FileSystemOperations():

    #MAKES NEW DIRECTORY
    def mkdir(self, path):
        interface.new_entry(path, 1)

    #CREATE FILE
    def create(self, path):
        interface.new_entry(path, 0)
        

    #WRITE TO FILE
    def write(self, path, data, offset=0):
        interface.write(path, offset, data)
      

    #READ
    def read(self, path, offset=0, size=-1):
        read_buffer = interface.read(path, offset, size)
        if read_buffer != -1: print(path + " : " + read_buffer)

    
    #DELETE
    def rm(self, path):
        interface.unlink(path)


    #MOVING FILE
    def mv(self, old_path, new_path):
        interface.mv(old_path, new_path)


    #CHECK STATUS
    def status(self):
        print(MemoryInterface.status())


def test_write_1D(arg= ""):
    Initialize_My_FileSystem()
    my_object = FileSystemOperations()
    files_to_write_to = ["/A/A_file1", "/B/B_file1", "/C/C_file1"]
    data_to_write = []
    for file in files_to_write_to:
        data_to_write.append("data in " + file.rsplit('/', 1)[1])
    my_object.mkdir("/A")
    my_object.mkdir("/B")
    my_object.mkdir("/C")
    for i in range(len(files_to_write_to)):
        my_object.create(files_to_write_to[i])
        my_object.write(files_to_write_to[i], data_to_write[i], 0)
    if arg == "print":
        my_object.status()
    return my_object, files_to_write_to, data_to_write

def test_write_2D(arg= ""):
    Initialize_My_FileSystem()
    my_object = FileSystemOperations()
    files_to_write_to = ["/A/B/AB_file", "/A/A_file1"]
    data_to_write = []
    for file in files_to_write_to:
        data_to_write.append("data in " + file.rsplit('/', 1)[1])
    my_object.mkdir("/A")
    my_object.mkdir("/A/B")
    for i in range(len(files_to_write_to)):
        my_object.create(files_to_write_to[i])
        my_object.write(files_to_write_to[i], data_to_write[i], 0)
    if arg == "print":
        my_object.status()
    return my_object, files_to_write_to, data_to_write

def test_read_1D():
    my_object, files_to_write_to, data_to_write = test_write_1D()
    for i in range(len(files_to_write_to)):
        my_object.read(files_to_write_to[i], 0, len(data_to_write[i]) + 1)

def test_read_2D():
    my_object, files_to_write_to, data_to_write = test_write_2D()
    for i in range(len(files_to_write_to)):
        my_object.read(files_to_write_to[i], 0, len(data_to_write[i]) + 1)


def test_read_and_write(arg= ""):
    my_object, files_to_write_to, data_to_write = test_write_2D()
    #my_object.status()
    interface.link("/A/B/AB_file", "/A/lol")
    #my_object.status()
    my_object.write("/A/lol", "mem", 2)
    #my_object.status()
    my_object.create("/fi_ro")
    my_object.write("/fi_ro","data in root file", 0)
    my_object.read("/A/lol",0, 4)
    my_object.write("/A/B/AB_file", "lolplswork",0)
    my_object.read("/A/lol",0, 4)
    my_object.write("/A/lol", "should change in AB_file", 0)
    my_object.read("/A/B/AB_file", 0,10)
    my_object.mv("/A/A_file1","/A/B" )
    #my_object.status()
    my_object.read("/A/B/A_file1",0)

    my_object.write("/A/B/A_file1","writing to moved file", 0)
    my_object.read("/A/B/A_file1",0)
    #error
    my_object.read("/A", 0)
    my_object.write("/", "asdf",0)
    my_object.read("/fi_ro", 0)
    if arg == "print":
        my_object.status()

def test_link_and_unlink():
    my_object, files_to_write_to, data_to_write = test_write_2D()
    my_object.create("/A/B/AB_file2")
    my_object.create("/A/B/AB_file3")
    my_object.create("/root_f")
    #my_object.status()
    #interface.link("/root_f", "/A/b")
    #my_object.status()
    interface.link("/A/B/AB_file", "/A/link")
    #my_object.status()
    my_object.rm("/A/link")
    #my_object.status()
    my_object.rm("/A/B/AB_file")
    my_object.status()
    my_object.rm("/A/A_file1")
    my_object.status()
    my_object.create( "/1")
    my_object.create("/2")
    my_object.create("/3")
    interface.link("/A/B/AB_file3", "/4")
    my_object.rm("/A/B")
    my_object.rm("/A/B/AB_file2")
    my_object.rm("/A/B/AB_file3")
    my_object.rm("/A/B")
    my_object.status()

    my_object.rm("/A")
    my_object.status()

def test_move():
    my_object, files_to_write_to, data_to_write = test_write_2D()
    my_object.create("/A/B/AB_file2")
    my_object.create("/A/B/AB_file3")
    my_object.create("/A/AB_file3")
    my_object.mkdir("/A/B/C")
    my_object.status()
    #my_object.mv("/A/B/C","/A")
    #my_object.mv("/A/AB_file3", "/A/B")
    #interface.link("/A/AB_file3", "/root_F")
    my_object.mv("/A/AB_file3", "/")
    my_object.status()
    my_object.mv("/AB_file3", "/A")
    my_object.status()













    
def test_link():
    my_object, files_to_write_to, data_to_write = test_write_2D()
    #my_object.status()
    #my_object.create("/A/B/meme1")
    #my_object.create("/A/B/meme2")
    #my_object.rm("/A/B/AB_file")
    #my_object.status()
    my_object.create("/A/B/meme1")
    my_object.write("/A/B/meme1", "data in meme1",0)
    #my_object.status()

    interface.link("/A/B/AB_file", "/A/new!")
    my_object.read("/A/B/AB_file", 0, 15)
    my_object.read("/A/new!", 0, 15)
    my_object.status()
    my_object.mv("/A/A_file1", "/A/B/")
    my_object.status()


def client():
    Initialize_My_FileSystem()
    interface_client = FileSystemOperations()

    while(1):
        user_input = raw_input("$ ")
        tokenized_input = user_input.split()
        if len(tokenized_input) == 0:
            print("Error: input mismatch")
        elif tokenized_input[0] not in allowed_commands:
            print("Error: " + tokenized_input[0] + " is not an allowed_command")
        else:
            if tokenized_input[0] == allowed_commands[0]: #mkdir
                del tokenized_input[0]
                if(len(tokenized_input) != 1):
                    print("Error: argument mismatch")
                else:
                    interface_client.mkdir(tokenized_input[0])
                


            elif tokenized_input[0] == allowed_commands[1]: #create
                del tokenized_input[0]
                if(len(tokenized_input) != 1):
                    print("Error: argument mismatch")
                else:
                    interface_client.create(tokenized_input[0])



            elif tokenized_input[0] == allowed_commands[2]: #mv
                del tokenized_input[0]
                if(len(tokenized_input) != 2):
                    print("Error: argument mismatch")
                else:
                    interface_client.mv(tokenized_input[0], tokenized_input[1])



            elif tokenized_input[0] == allowed_commands[3]: #read
                del tokenized_input[0]
                if ((len(tokenized_input) not in range(1,4))):
                    print("Error: argument mismatch")
                elif (len(tokenized_input) == 3) and (not tokenized_input[1].isdigit() or not  tokenized_input[2].isdigit()):
                    print("Error: argument mismatch")

                elif(len(tokenized_input) == 2) and not tokenized_input[1].isdigit():
                    print("Error: argument mismatch")
                else:
                    offset = 0
                    size = -1
                    if(len(tokenized_input) == 2):
                        offset = int(tokenized_input[1])
                    elif(len(tokenized_input) == 3):
                        offset = int(tokenized_input[1])
                        size = int(tokenized_input[2])
                    interface_client.read(tokenized_input[0],offset, size)



            elif tokenized_input[0] == allowed_commands[4]: #write
                del tokenized_input[0]
                if(len(tokenized_input) < 2):
                    print("Error: argument mismatch")
                else:
                    interface_client.write(tokenized_input[0], user_input.split(' ', 2)[-1], 0)


            elif tokenized_input[0] == allowed_commands[5]: #status
                del tokenized_input[0]
                if(len(tokenized_input) != 0):
                    print("Error: argument mismatch")
                else:
                    #do 
                    interface_client.status()



            elif tokenized_input[0] == allowed_commands[6]: #rm
                del tokenized_input[0]
                if(len(tokenized_input) != 1):
                    print("Error: argument mismatch")
                else:
                    interface_client.rm(tokenized_input[0])


            elif tokenized_input[0] == allowed_commands[7]: #exit
                del tokenized_input[0]
                if(len(tokenized_input) != 0):
                    print("Error: argument mismatch")
                else:
                    exit()
 
if __name__ == '__main__':
    #test_move()
    # test_link()
    #test_write_2D("print")
    client()
    '''
    start_time = time.time()
    Initialize_My_FileSystem()
    my_object = FileSystemOperations()
    my_object.mkdir("/A")
    my_object.mkdir("/B")
    my_object.create("/A/1.txt")
    my_object.write("/A/1.txt", "POCSD", 0)
    my_object.read("/A/1.txt",0, 5)
    print("Execution time: " + str(time.time() - start_time))
    my_object.mv("/A/1.txt", "/B")
    my_object.status()
    my_object.rm("A/1.txt")
    my_object.status()
    '''


