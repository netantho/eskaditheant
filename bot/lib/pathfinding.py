import sys
import os
sys.path.append(os.path.abspath('../'))

import variables

import logging

from Queue import Queue

class Pathfinding():
	def __init__(self, ants):
		"""
		Constructor
		
		\param self
		\param object instance of the ants class
		"""
		self.ants = ants
		self.costs = {}

	def adjacents(self, rc, cc):
		result = []
		if (rc+1 < self.ants.rows):
			result.append((rc+1, cc))
		if (rc > 0):
			result.append((rc-1, cc))
		if (cc+1 < self.ants.cols):
			result.append((rc, cc+1))
		if (cc > 0):
			result.append((rc, cc-1))
		return result

	def bfs(self, fromNode, toNode, nodes):
		#http://stackoverflow.com/questions/1753257/can-this-breadth-first-search-be-made-faster
		def getNeighbours(current, nodes):
			return nodes[current] if current in nodes else []
		
		def make_path(toNode, graph):
			result = []
			while 'Root' != toNode:
					result.append(toNode)
					toNode = graph[toNode]
			result.reverse()
			return result

		q = Queue()
		q.put(fromNode)
		graph = {fromNode: 'Root'}

		while not q.empty():
			# get the next node and add its neighbours to queue
			current = q.get()
			for neighbor in getNeighbours(current, nodes):
					# use neighbor only continue if not already visited
					if neighbor not in graph:
							graph[neighbor] = current
							q.put(neighbor)

			# check if destination
			if current == toNode:
					return make_path(toNode, graph)
		return []

	def print_hash(self, my_hash, rows, cols):
		for r in range(rows):
			pr = ""
			for c in range(cols):
				if my_hash.has_key((r, c)):
					pr += str(my_hash[(r,c)])+" "
				else:
					pr += "error "
			logging.debug(pr)
			
	def print_hash_graph(self, my_hash, rows, cols):
		for r in range(rows):
			for c in range(cols):
				pr = ""
				if my_hash.has_key((r, c)):
					pr += str((r, c))+": "+str(my_hash[(r,c)])
				else:
					pr += "error "
				logging.debug(pr)
			
	def generate_graph(self):
		graph = {}
		for rc in range(self.ants.rows):
			for cc in range(self.ants.cols):
				graph[(rc,cc)] = []
				for (r,c) in self.adjacents(rc, cc):
					if self.ants.map[r][c] != -4:
						graph[(rc,cc)].append((r,c))
		#self.print_hash_graph(graph, self.ants.rows, self.ants.cols)
		return graph
	
	def coordinates_to_directions(self, coordinates):
		(rc,cc) = coordinates[0]
		result = []
		#coordinates = coordinates[1:len(coordinates)-1]
		coordinates = coordinates[1:]
		#logging.debug(len(coordinates))
		for (rn,cn) in coordinates:
			#logging.debug((rn,cn))
			if (rn,cn) == (rc-1,cc):
				result.append('n')
			elif (rn,cn) == (rc+1,cc):
				result.append('s')
			elif (rn,cn) == (rc,cc-1):
				result.append('w')
			elif (rn,cn) == (rc,cc+1):
				result.append('e')
			(rc,cc)=(rn,cn)
		return result