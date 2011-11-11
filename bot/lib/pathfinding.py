import sys
import os
sys.path.append(os.path.abspath('../'))

import variables

import logging

from Queue import Queue
import heapq

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
		if (rc+1 < self.ants.rows and self.ants.map[rc+1][cc] != -4):
			result.append((rc+1, cc))
		if (rc > 0  and self.ants.map[rc-1][cc] != -4):
			result.append((rc-1, cc))
		if (cc+1 < self.ants.cols and self.ants.map[rc][cc+1] != -4):
			result.append((rc, cc+1))
		if (cc > 0 and self.ants.map[rc][cc-1 ] != -4):
			result.append((rc, cc-1))
		return result

	def astar(self, start_r, start_c, goal_r, goal_c):
		def initialize_map():
			tab = []
			for r in range(self.ants.rows):
				tab.append([])
				for c in range(self.ants.cols):
					tab[r].append(None)
			return tab
		
		def f_miminum_set(myset, f_score):
			minimum = None
			score = None
			for (r,c) in myset:
				if minimum == None:
					minimum = (r,c)
					score = f_score[r][c]
				elif f_score[r][c] < score:
					minimum = (r,c)
					score = f_score[r][c]
			return minimum
		
		#Pseudocode from Wikipedia
		closedset = set()
		openset = set()
		openHeap = []
		openset.add((start_r, start_c))
		openHeap.append((0,(start_r, start_c)))
		came_from = initialize_map() #map of the navigated nodes
		
		g_score = initialize_map()
		h_score = initialize_map()
		f_score = initialize_map()
		g_score[start_r][start_c] = 0
		h_score[start_r][start_c] = self.ants.distance((start_r, start_c), (goal_r, goal_c))
		f_score[start_r][start_c] = g_score[start_r][start_c] + h_score[start_r][start_c]
		
		while bool(openset):
			#logging.debug("openset "+str(openset))
			#logging.debug("closedset "+str(closedset))
			#(xr, xc) = heapq.heappop(openHeap)[1]
			(xr, xc) = f_miminum_set(openset, f_score)
			if (xr, xc) == (goal_r, goal_c):
				return self.astar_reconstruct_path(came_from, came_from[goal_r][goal_c])
			openset.remove((xr, xc))
			closedset.add((xr, xc))
			for (yr, yc) in self.adjacents(xr, xc):
				if (yr, yc) in closedset:
					continue
				tentative_g_score = g_score[xr][xc] + self.ants.distance((xr, xc), (yr, yc))
				
				if (yr, yc) not in openset:
					openset.add((yr, yc))
					#heapq.heappush(openHeap, (self.ants.distance((yr, yc), (goal_r, goal_c)), (yr, yc)))
					tentative_is_better = True
				elif tentative_g_score < g_score[yr][yc]:
					tentative_is_better = True
				else:
					tentative_is_better = False
				
				if tentative_is_better == True:
					came_from[yr][yc] = (xr, xc)
					g_score[yr][yc] = tentative_g_score
					h_score[yr][yc] = self.ants.distance((yr, yc), (goal_r, goal_c))
					f_score[yr][yc] = g_score[yr][yc] + h_score[yr][yc]
		logging.error("No path from "+str((start_r, start_c))+" to "+str((goal_r, goal_c)))
		return False
		
	def astar_reconstruct_path(self, came_from, current_node):
		
		(currentr, currentc) = current_node
		if came_from[currentr][currentc]:
			p = self.astar_reconstruct_path(came_from, came_from[currentr][currentc])
			logging.debug(p)
			p.append(current_node)
			return p
		else:
			return [current_node]

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