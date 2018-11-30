'''
THIS MODULE ACTS LIKE FILE NAME LAYER AND PATH NAME LAYER (BOTH) ABOVE INODE LAYER.
IT RECIEVES INPUT AS PATH (WITHOUT INITIAL '/'). THE LAYER IMPLEMENTS LOOKUP TO FIND INODE NUMBER OF THE REQUIRED DIRECTORY.
PARENTS INODE NUMBER IS FIRST EXTRACTED BY LOOKUP AND THEN CHILD INODE NUMBER BY RESPECTED FUNCTION AND BOTH OF THEM ARE UPDATED
'''
import InodeNumberLayer

#HANDLE OF INODE NUMBER LAYER
interface = InodeNumberLayer.InodeNumberLayer()

class FileNameLayer():

	#PLEASE DO NOT MODIFY
	#RETURNS THE CHILD INODE NUMBER FROM THE PARENTS INODE NUMBER
	def CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(self, childname, inode_number_of_parent):
		inode = interface.INODE_NUMBER_TO_INODE(inode_number_of_parent)
		if not inode: 
			print("Error FileNameLayer: Lookup Failure!")
			return -1
		if inode.type == 0:
			print("Error FileNameLayer: Invalid Directory!")
			return -1
		if childname in inode.directory: return inode.directory[childname]
		print("Error FileNameLayer: Lookup Failure of")
		return -1

	#PLEASE DO NOT MODIFY
	#RETUNS THE PARENT INODE NUMBER FROM THE PATH GIVEN FOR A FILE/DIRECTORY 
	def LOOKUP(self, path, inode_number_cwd):   
		name_array = path.split('/')
		if len(name_array) == 1: return inode_number_cwd
		else:
			child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(name_array[0], inode_number_cwd)
			if child_inode_number == -1: return -1
			return self.LOOKUP("/".join(name_array[1:]), child_inode_number)

	#PLEASE DO NOT MODIFY
	#MAKES NEW ENTRY OF INODE
	def new_entry(self, path, inode_number_cwd, type):
		if path == '/': #SPECIAL CASE OF INITIALIZING FILE SYSTEM
			interface.new_inode_number(type, inode_number_cwd, "root")
			return True
		parent_inode_number = self.LOOKUP(path, inode_number_cwd)
		parent_inode = interface.INODE_NUMBER_TO_INODE(parent_inode_number) 
		childname = path.split('/')[-1]
		if not parent_inode: return -1
		if childname in parent_inode.directory:
			print("Error FileNameLayer: File already exists!")
			return -1
		child_inode_number = interface.new_inode_number(type, parent_inode_number, childname)  #make new child
		if child_inode_number != -1:
			parent_inode.directory[childname] = child_inode_number
			interface.update_inode_table(parent_inode, parent_inode_number)


	#IMPLEMENTS READ
	def read(self, path, inode_number_cwd, offset, length):
		'''WRITE YOUR CODE HERE'''
		parent_inode_number = self.LOOKUP(path, inode_number_cwd)
		if parent_inode_number == -1:
			return -1
		file_name = path
		if "/" in file_name:
			file_name = file_name.rsplit('/', 1)[1]
		child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(file_name, parent_inode_number)
		if child_inode_number == -1:
			return -1
		return interface.read(child_inode_number, offset, length, parent_inode_number)
	
	#IMPLEMENTS WRITE
	def write(self, path, inode_number_cwd, offset, data):
		'''WRITE YOUR CODE HERE'''
		error = -1
		parent_inode_number = self.LOOKUP(path, inode_number_cwd)
		if parent_inode_number == -1:
			return error
		file_name = path
		if "/" in file_name:
			file_name = file_name.rsplit('/', 1)[1]
		child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(file_name, parent_inode_number)
		if child_inode_number == -1:
			return error
		interface.write(child_inode_number, offset, data, parent_inode_number)
		

	#HARDLINK
	def link(self, old_path, new_path, inode_number_cwd):
		'''WRITE YOUR CODE HERE'''
		error = -1
		if old_path == "":
			print("Cant link root")
			return error
		if new_path == ""  or new_path[-1] == "/":
			print("link must have a name")
			return -1
		dir_inode_number_to_link = self.LOOKUP(old_path,inode_number_cwd)
		if dir_inode_number_to_link == -1:
			return error
		file_name_to_link = old_path
		if "/" in file_name_to_link:
			file_name_to_link = file_name_to_link.rsplit('/', 1)[1]
		inode_number_to_link = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(file_name_to_link, dir_inode_number_to_link)
		if inode_number_to_link == -1:
			return error
		new_dir = self.LOOKUP(new_path,inode_number_cwd)
		if new_dir == -1:
			return error
		hard_link_name = new_path
		if "/" in hard_link_name:
			hard_link_name = hard_link_name.rsplit('/', 1)[1]
		new_dir_inode = interface.INODE_NUMBER_TO_INODE(new_dir)
		if hard_link_name in new_dir_inode.directory:
			print("Error FileNameLayer: File already exists!")
			return -1
		inode = interface.link(inode_number_to_link, new_dir)
		if inode == -1:
			return error
		inode.directory[hard_link_name] = inode_number_to_link
		interface.update_inode_table(inode, new_dir)
		return 0 #link made


	#REMOVES THE FILE/DIRECTORY
	def unlink(self, path, inode_number_cwd):
		if path == "": 
			print("Error FileNameLayer: Cannot delete root directory!")
			return -1
		'''WRITE YOUR CODE HERE'''
		dir_inode_number_to_unlink = self.LOOKUP(path,inode_number_cwd)
		if dir_inode_number_to_unlink == -1:
			return -1
		file_name_to_unlink = path
		if "/" in file_name_to_unlink:
			file_name_to_unlink = file_name_to_unlink.rsplit('/', 1)[1]
		inode_number_to_unlink = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(file_name_to_unlink, dir_inode_number_to_unlink)
		if inode_number_to_unlink == -1:
			return -1
		dir_inode = interface.unlink(inode_number_to_unlink, dir_inode_number_to_unlink)
		if dir_inode == -1:
			return -1
		del dir_inode.directory[file_name_to_unlink]
		interface.update_inode_table(dir_inode, dir_inode_number_to_unlink)
		return 0
		#remove linked name


	#MOVE
	def mv(self, old_path, new_path, inode_number_cwd):
		'''WRITE YOUR CODE HERE'''
		#if trying to move dir return error
		error = -1
		inode_number_dir_of_file = self.LOOKUP(old_path, inode_number_cwd)
		if inode_number_dir_of_file == -1:
			return error
		file_name_to_move = old_path
		if"/" in file_name_to_move:
			file_name_to_move = file_name_to_move.rsplit('/', 1)[1]
		inode_number_of_file = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(file_name_to_move, inode_number_dir_of_file)
		if inode_number_of_file== -1:
			return error

		inode_number_of_dir_to_move_file_to = self.LOOKUP(new_path,inode_number_cwd)
		if inode_number_of_dir_to_move_file_to == -1:
			return error

		if new_path != "":
			new_dir_name = new_path
			if "/" in new_dir_name:
				new_dir_name = new_dir_name.rsplit('/', 1)[1]
			inode_number_of_dir_to_move_file_to = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(new_dir_name, inode_number_of_dir_to_move_file_to)
			if inode_number_of_dir_to_move_file_to == -1:
				return error
		
		#in the design specs, we can only move files. and we should only be able to move to dir
		inode_new_dir = interface.INODE_NUMBER_TO_INODE(inode_number_of_dir_to_move_file_to)
		if file_name_to_move in inode_new_dir.directory:
			print("Error FileNameLayer: File already exists!")
			return -1
		parent_inode = interface.link(inode_number_of_file, inode_number_of_dir_to_move_file_to)
		if parent_inode == -1:
			return error
		parent_inode.directory[file_name_to_move] = inode_number_of_file
		interface.update_inode_table(parent_inode, inode_number_of_dir_to_move_file_to)
		parent_inode = interface.unlink(inode_number_of_file, inode_number_dir_of_file)
		if parent_inode == -1:
			return error
		del parent_inode.directory[file_name_to_move]
		interface.update_inode_table(parent_inode, inode_number_dir_of_file)
		return 0
		#check if the dir is full and the dir contains a file of the same name
		



	