#The basic unit of the AVL tree
class Node:
	def __init__(self, key, value):
		self.left = None
		self.right = None
		self.key = key
		self.value = [value]
		self.root = self
		
	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return str(self.value)

#The AVL tree class
class AVLTree():

	def __init__(self):
		self.node = None
		self.height = -1
		self.balance = 0

	#insert function
	def insert(self, key, value):

		if not self.node:
			self.node = Node(key,value)
			self.node.left = AVLTree()
			self.node.right = AVLTree()
		elif key < self.node.key:
			self.node.left.insert(key,value)
		
		elif key > self.node.key:
			self.node.right.insert(key, value)
		else:
			self.node.value.append(value)

		self.rebalance()

	def rebalance(self):
        # if rebalancing required update height balance tree non recursive

		self.update_heights(recursive=False)
		self.update_balances(recursive=False)

		# For each node checked, 
		while self.balance < -1 or self.balance > 1: 
			# Left subtree is larger than right subtree
			if self.balance > 1:

				# Left Right Case -> rotate y,z to the left
				if self.node.left.balance < 0:
					self.node.left.rotate_left()
					self.update_heights()
					self.update_balances()

				self.rotate_right()
				self.update_heights()
				self.update_balances()
            
            # Right subtree is larger than left subtree
			if self.balance < -1:
                
                # Right Left Case -> rotate x,z to the right
				if self.node.right.balance > 0:
					self.node.right.rotate_right() # we're in case III
					self.update_heights()
					self.update_balances()

				self.rotate_left()
				self.update_heights()
				self.update_balances()
	
	def update_heights(self, recursive=True):
		
		if self.node:
			if recursive: 
				if self.node.left: 
					self.node.left.update_heights()
				if self.node.right:
					self.node.right.update_heights()
            
			self.height = 1 + max(self.node.left.height, self.node.right.height)
		else: 
			self.height = -1

	def update_balances(self, recursive=True):
		if self.node:
			if recursive:
				if self.node.left:
					self.node.left.update_balances()
				if self.node.right:
					self.node.right.update_balances()

			self.balance = self.node.left.height - self.node.right.height
		else:
			self.balance = 0
	
	def rotate_right(self):
		new_root = self.node.left.node
		new_left_sub = new_root.right.node
		old_root = self.node

		self.node = new_root
		old_root.left.node = new_left_sub
		new_root.right.node = old_root

	def rotate_left(self):
		new_root = self.node.right.node
		new_left_sub = new_root.left.node
		old_root = self.node

		self.node = new_root
		old_root.right.node = new_left_sub
		new_root.left.node = old_root


	def __setitem__(self,key,value):
		self.insert(key,value)

	def get(self, key):
		if not self.node:
			return None
		elif self.node.key == key:
			return self.node.value
		elif key < self.node.key:
			return self.node.left.get(key)
		else:
			return self.node.right.get(key)

	def find_range(self,i,j):

		if not self.node:
			return []
		#Special case
		if self.node.key == i and self.node.key == j:
			return self.node.value
		if self.node.key <= j and self.node.key >= i:
			return self.node.value + self.node.left.find_range(i,j) + self.node.right.find_range(i, j)
		elif self.node.key < i:
			return self.node.right.find_range(i, j)
		else:
			return self.node.left.find_range(i,j)

	def count_range(self,i,j):
		return len(self.find_range(i,j))

	def __getitem__(self,key):
		return self.get(key)

	def __getslice__(self,i,j):
		return self.find_range(i,j)

	def print_tree(self):
		
		if self.node.left.node:
			self.node.left.print_tree()
		print str(self.node.key) + "\t" + str(self.node.value)
		if self.node.right.node:
			self.node.right.print_tree()
		
class GenAVLTree:
	
	def __init__(self):
		self.chroms = {}
						
	def print_genome(self,key='all'):
		if key == 'all':
			for key in self.chroms:
				print key
				self.chroms[key].print_tree()
		else:
			print key
			self.chroms[key].print_tree()

	def __setitem__(self,key,value):
		self.insert(key,value)

	def __getslice__(self,i,j):
		return self.find_range(i,j)

	def __getitem__(self,key):
		#print key
		if key in self.chroms:
			return self.chroms[key]
		else:
			self.chroms[key] = AVLTree()
			return self.chroms[key]

	def put(self,chrom,key,value):
		if chrom in self.chroms:
			self.chroms[chrom].insert(key,value)
		else:
			self.chroms[chrom] = AVLTree()
			self.chroms[chrom].insert(key,value)
