'''
THIS MODULE ACTS AS A INODE NUMBER LAYER. NOT ONLY IT SHARES DATA WITH INODE LAYER, BUT ALSO IT CONNECTS WITH MEMORY INTERFACE FOR INODE TABLE 
UPDATES. THE INODE TABLE AND INODE NUMBER IS UPDATED IN THE FILE SYSTEM USING THIS LAYER
'''
import InodeLayer, config, MemoryInterface, datetime, InodeOps, MemoryInterface


#HANDLE OF INODE LAYER
interface = InodeLayer.InodeLayer()

class InodeNumberLayer():

	#PLEASE DO NOT MODIFY
	#ASKS FOR INODE FROM INODE NUMBER FROM MemoryInterface.(BLOCK LAYER HAS NOTHING TO DO WITH INODES SO SEPERTAE HANDLE)
	def INODE_NUMBER_TO_INODE(self, inode_number):
		array_inode = MemoryInterface.inode_number_to_inode(inode_number)
		inode = InodeOps.InodeOperations().convert_array_to_table(array_inode)
		if inode: inode.time_accessed = datetime.datetime.now()   #TIME OF ACCESS
		return inode


	#PLEASE DO NOT MODIFY
	#RETURNS DATA BLOCK FROM INODE NUMBER
	def INODE_NUMBER_TO_BLOCK(self, inode_number, offset, length):
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		if not inode:
			print("Error InodeNumberLayer: Wrong Inode Number! \n")
			return -1
		return interface.read(inode, offset, length)
		
	#UPDATES THE INODE TO THE INODE TABLE
	def update_inode_table(self, table_inode, inode_number):
		if table_inode: table_inode.time_modified = datetime.datetime.now()  #TIME OF MODIFICATION 
		array_inode = InodeOps.InodeOperations().convert_table_to_array(table_inode)
		MemoryInterface.update_inode_table(array_inode, inode_number)


	#PLEASE DO NOT MODIFYprint
	#FINDS NEW INODE INODE NUMBER FROM FILESYSTEM
	def new_inode_number(self, type, parent_inode_number, name):
		if parent_inode_number != -1:
			parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
			if not parent_inode:
				print("Error InodeNumberLayer: Incorrect Parent Inode")
				return -1
			entry_size = config.MAX_FILE_NAME_SIZE + len(str(config.MAX_NUM_INODES))
			max_entries = (config.INODE_SIZE - 79 ) / entry_size
			if len(parent_inode.directory) == max_entries:
				print("Error InodeNumberLayer: Maximum inodes allowed per directory reached!")
				return -1
		for i in range(0, config.MAX_NUM_INODES):
			if self.INODE_NUMBER_TO_INODE(i) == False: #FALSE INDICTES UNOCCUPIED INODE ENTRY HENCE, FREEUMBER
				inode = interface.new_inode(type)
				inode.name = name
				self.update_inode_table(inode, i)
				return i
		print("Error InodeNumberLayer: All inode Numbers are occupied!\n")


	#LINKS THE INODE
	def link(self, inode_number, parent_inode_number):
		'''WRITE YOUR CODE HERE'''
		error = -1
		entry_size = config.MAX_FILE_NAME_SIZE + len(str(config.MAX_NUM_INODES))		
		max_entries = (config.INODE_SIZE - 79 ) / entry_size
		parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
		if parent_inode == False:
			return -1
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		if inode == False:
			return error
		#check if we are trying to make a hard link to a dir
		if inode.type == 1:
			print("(link) Error InodeNumberLayer: Cant link a directory")
			return error
		if parent_inode.type == 0:
			print("(link) Error InodeNumberLayer: Cant place a link in a file")
			return error
		#check if the dir is full
		if len(parent_inode.directory) == max_entries:
			print("(link) Error InodeNumberLayer: Maximum inodes allowed per directory reached!")
			return error
		inode.links += 1

		self.update_inode_table(inode, inode_number)
		return parent_inode #no error

	def remove_and_free_memory_inode(self, inode, inode_number):
		interface.free_data_block(inode,0)
		MemoryInterface.update_inode_table(False, inode_number)

	#REMOVES THE INODE ENTRY FROM INODE TABLE
	def unlink(self, inode_number, parent_inode_number):
		'''WRITE YOUR CODE HERE'''
		error = -1
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		if(inode == False):
			return error
		parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
		if(parent_inode == False):
			return error
		#unlinking dir, make sure it is empty, dir inode can only be deleted if its empty
		if inode.type == 1 and len(inode.directory) != 0:
			print("ERROR: cant unlink non empty directory")
			return error
		#if the file is an inode decrement its links
		if inode.type == 0:
			inode.links -=1
			if(inode.links == 0):
				interface.free_data_block(inode,0)
				MemoryInterface.update_inode_table(False, inode_number)
				return parent_inode
		if inode.type == 1:
			interface.free_data_block(inode,0)
			MemoryInterface.update_inode_table(False, inode_number)
			return parent_inode
		array_inode = InodeOps.InodeOperations().convert_table_to_array(inode)		
		MemoryInterface.update_inode_table(array_inode, inode_number)
		return parent_inode



	def write(self, inode_number, offset, data, parent_inode_number):
		'''WRITE YOUR CODE HERE'''
		error = -1
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		if inode == False:
			return error
		if inode.type == 1:
			print("write InodeNumberLayer: Cannot write to directory")
			return error
		updated_inode = interface.write(inode,offset, data)
		self.update_inode_table(updated_inode, inode_number) #if changed, change in read
		return updated_inode
		

	#IMPLEMENTS READ FUNCTIONALITY
	def read(self, inode_number, offset, length, parent_inode_number):
		'''WRITE YOUR CODE HERE'''
		error = -1
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		if inode == False:
			return error
		if inode.type == 1:
			print("read InodeNumberLayer: Cannot read from directory")
			return error
		updated_inode, data  = interface.read(inode, offset, length)
		self.update_inode_table(updated_inode, inode_number)
		return data