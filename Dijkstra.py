import math
from Vertex import Vertex
import random
import pygame
import time


class Dijkstra:
	def __init__(self, vertexS, vertexT, points):
		self.startvx = Vertex(vertexS, start= True)
		self.targetvx = Vertex(vertexT,  target= True)
		self.all_vertex = list(Vertex(p) for p in points)
		self.all_vertex.append(self.startvx)
		self.all_vertex.append(self.targetvx)
		self.visited_list = []
		self.unvisited_list = []
		self.scan()

	def get_distence(self, v1, v2):
		distance =math.sqrt((v2[0]-v1[0])**2 +(v2[1]-v1[1])**2)
		return distance
	
	def unvisited(self,vtx):
		if vtx.isvisited:
			return False
		else:
			return True

	def set_unvisited_list(self):
		self.unvisited_list.clear()
		self.visited_list.clear()
		for v in self.all_vertex:
			if v.isvisited == True:
				self.visited_list.append(v)
			else:
				self.unvisited_list.append(v)
				
	def scan(self):
		start = self.startvx
		target = self.targetvx
		dist_index = (self.get_distence(start.vertex,target.vertex)/3)
		for vx in self.all_vertex:
			self.set_unvisited_list()
			if vx.vertex == start.vertex or vx.vertex == target.vertex:
				pass
			else:
				dist_vx = self.get_distence(start.vertex,vx.vertex)
				if dist_vx <= dist_index:
					vx.zone1 = True
				elif dist_vx <= (dist_index*2):
					vx.zone2 = True
				elif dist_vx > (dist_index*2):
					vx.zone3 = True
	
	def get_neighbors(self, step):
		neighbors1 = []
		neighbors2 = []
		neighbors3 = []
		for vx in self.all_vertex:
			if vx.zone1 and step==1:
				neighbors1.append(vx)
			elif vx.zone2 and step==2:
				neighbors2.append(vx)
			elif vx.zone3 and step==3:
				neighbors3.append(vx)
		if step ==1:
			return neighbors1
		elif step ==2:
			return neighbors2
		elif step ==3:
			return neighbors3
		
	def find_path(self,win):
		current_vx = [self.startvx]
		all_paths = [[],[],[],[]]
		for step in range(1,4):
			neighbor_vx = self.get_neighbors(step)
			for current in current_vx:
				for n in neighbor_vx:
					dist_n = (self.get_distence(current.vertex, n.vertex))+current.value
					#time.sleep(2)
					if n.value == 0 or n.value >= dist_n:
						n.value = dist_n
						n.isvisited = True
						n.previous_vertex = current.vertex
						if len(all_paths[step-1])>0:
							if all_paths[step-1][1]>dist_n:
								all_paths[step-1].clear()
								all_paths[step-1].append(n.vertex)
								all_paths[step-1].append(dist_n)
							else:
								pass
						else:
							all_paths[step-1].append(n.vertex)
							all_paths[step-1].append(dist_n)
					else:
						n.isvisited = True
			current_vx.clear()
			current_vx= neighbor_vx.copy()
		target_vx= self.targetvx
		for current in current_vx:
			dist_n = (self.get_distence(current.vertex, target_vx.vertex))+current.value
			if target_vx.value == 0 or target_vx.value >= dist_n:
				target_vx.value = dist_n
				target_vx.isvisited = True
				target_vx.previous_vertex = current.vertex
				if len(all_paths[3])>0:
					if all_paths[3][1]>dist_n:
						all_paths[3].clear()
						all_paths[3].append(target_vx.vertex)
						all_paths[3].append(dist_n)
					else:
						pass
				else:
					all_paths[3].append(target_vx.vertex)
					all_paths[3].append(dist_n)
			else:
				target_vx.isvisited = True
		#
		retro_path=[]
		for vtx in self.all_vertex:
			retro_path.append([vtx.vertex,vtx.previous_vertex])
		
		#
		go = True
		path = []
		now_pos= self.targetvx.vertex
		next_pos = []
		while go:
			for retro in retro_path:
				if retro[0] == now_pos:
					next_pos = retro[1]
					if now_pos == self.startvx.vertex or next_pos == [0,0]:
						go = False
						break
					path.append([now_pos,next_pos])
					now_pos = next_pos
				else:
					pass
		else:
			return path
		

