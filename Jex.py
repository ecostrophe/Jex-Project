import random
import pygame
from pygame.locals import *
from Dijkstra import Dijkstra

class Jex:
	num_new_jex =0
	occuped_area =[]
	def __init__(self,id_num,genre,types,color,weight=10,health=100,force=5,hunger=0,speed=10,genom=""):
		#Physics
		self.ident=id_num
		self.genre=genre
		self.type=types
		self.color=color
		self.weight=weight
		self.health=health
		self.force=force
		self.position=[random.randint(10,740),random.randint(10,740)]
		#Requirement
		self.hunger=hunger
		self.speed=speed
		self.alive=self.set_isalive()
		self.genartion=1
		#Skills
		self.needs=[] #update orders and needs
		self.follow=[]#find the closest jex to him
		#Genoms
		self.genom =genom
		self.killer= False #KIL KL
		self.runner= False #RUN RN
		self.sick= False   #SIK SK
		self.lazy= False   #LZY LZ
		self.coward= False #COW CW
		self.clever= False #CLV CV
		self.tracer= False #TRC TR
		#set Genoms
		if self.genom == "SK":
			self.sick = True
			self.health -= 50
		elif self.genom == "CW":
			self.coward = True
			self.force =1
		elif self.genom == "RN":
			self.runner = True
			self.speed += 50
		elif self.genom == "KL":
			self.killer = True
			self.force += 50
		elif self.genom == "LZ":
			self.lazy = True
			self.speed -= 5
		elif self.genom == "CV":
			self.clever = True
			pass
		elif self.genom == "TR":
			self.tracer = True
			pass
		else:
			pass
		#create ADN
		self.ADN = [self.ident,self.genre,self.type,self.color,self.weight,self.health,self.force,self.hunger,self.speed,self.genom]
		#rapport of new creation
		Jex.num_new_jex +=1
		Jex.occuped_area.append(self.position)
		print("New Jex Id:",self.ident,"is created at the position (X:",self.position[0],"Y:",self.position[1],")")
		self.chromo = self.set_chromo()


	def __str__(self):
		return "\nID:"+str(self.ident)+"\nGenartion:"+str(self.genartion)+"\nGenre:"+self.genre+"\nType:"+self.type+"\nWeight:"+str(self.weight)+"\nHealth:"+str(self.health)+"\nForce:"+str(self.force)+")\n"

	def heritage(self, other, rate_GenRecomb=0):
		new_ADN=[0,"","", (0, 0, 0), 0, 0, 0, 0, 0,""]
		# id ident
		new_id=str(Jex.num_new_jex)
		new_ADN[0]=new_id
		# Genre: 2 ("Male","Female")
		if rate_GenRecomb == 0:
			new_ADN[1]=random.choice(("Male","Female"))
		else:
			#XY sex-determination system #XYSDS
			XYSDS=["X","X","X","Y"]
			chrom = random.choices(XYSDS, k = 2)
			if chrom == ["X","Y"] or chrom == ["Y","X"]:
				new_ADN[1]="Male"
			else:
				new_ADN[1]="Female"
		# Type: 5 ("White","Black","Yellow","Red","Green")
		if rate_GenRecomb == 0:
			if self.type == other.type:
				new_ADN[2]=self.type
			else:
				new_ADN[2]=random.choice(("White","Black","Yellow","Red","Green"))
		else:
			prob_type =[0,0,0,0,0]
			rate_prob_type = int(((100-rate_GenRecomb)*5)/100)
			type_list = ["White","Black","Yellow","Red","Green"]
			prob_type[type_list.index(self.type)]+=rate_prob_type
			prob_type[type_list.index(other.type)]+=rate_prob_type
			if self.type == other.type:
				type_list.remove(self.type)
			else:
				type_list.remove(self.type)
				type_list.remove(other.type)
			for n in range(len(type_list)):
				get_type = random.choice(type_list)
				if get_type == "White":
					prob_type[0]+=1
				elif get_type == "Black":
					prob_type[1]+=1
				elif get_type == "Yellow":
					prob_type[2]+=1
				elif get_type == "Red":
					prob_type[3]+=1
				elif get_type == "Green":
					prob_type[4]+=1
			type_list = ["White","Black","Yellow","Red","Green"]
			new_ADN[2]=type_list[prob_type.index(max(prob_type))]
		# Color: 5 ((255, 255, 255),(0, 0, 0),(247, 247, 0),(255, 0, 0),(0,255,0))
		if rate_GenRecomb == 0:
			new_ADN[3]=random.choice(((255, 255, 255),(0, 0, 0),(247, 247, 0),(255, 0, 0),(0,255,0)))
		else:
			prob_color =[0,0,0,0,0]
			rate_prob_color = int(((100-rate_GenRecomb)*5)/100)
			color_list = [(255, 255, 255),(0, 0, 0),(247, 247, 0),(255, 0, 0),(0,255,0)]
			prob_color[color_list.index(self.color)]+=rate_prob_color
			prob_color[color_list.index(other.color)]+=rate_prob_color
			if self.color == other.color:
				color_list.remove(self.color)
			else:
				color_list.remove(self.color)
				color_list.remove(other.color)
			for n in range(len(color_list)):
				get_color = random.choice(color_list)
				if get_color == (255, 255, 255):
					prob_color[0]+=1
				elif get_color == (0, 0, 0):
					prob_color[1]+=1
				elif get_color == (247, 247, 0):
					prob_color[2]+=1
				elif get_color == (255, 0, 0):
					prob_color[3]+=1
				elif get_color == (0,255,0):
					prob_color[4]+=1
			color_list = [(255, 255, 255),(0, 0, 0),(247, 247, 0),(255, 0, 0),(0,255,0)]
			new_ADN[3]=color_list[prob_color.index(max(prob_color))]
		# Weight: 5
		if rate_GenRecomb == 0:
			new_ADN[4]=10
		else:
			new_ADN[4]=10
		# Health: 100
		if rate_GenRecomb == 0:
			new_ADN[5]=100
		else:
			new_ADN[5]=100
		# Force: 5
		if rate_GenRecomb == 0:
			new_ADN[6]=5
		else:
			new_ADN[6]=5
		# Hunger: 0
		if rate_GenRecomb == 0:
			new_ADN[7]=0
		else:
			new_ADN[7]=0
		# Speed: 10
		if rate_GenRecomb == 0:
			new_ADN[8]=10
		else:
			new_ADN[8]=10
		# Genom:6 (killer KL,Runner RN,Sick SK,Lazy LZ,Coward CW,CleVer CV)
		if rate_GenRecomb == 0:
			if self.genom == other.genom:
				new_ADN[9]=self.genom
			else:
				new_ADN[9]=random.choice(("KL","RN","SK","LZ","CW","CV","TR",""))
		else:
			prob_genom =[0,0,0,0,0,0,0,0]
			rate_prob_genom = int(((100-rate_GenRecomb)*8)/100)
			genom_list = ["KL","RN","SK","LZ","CW","CV","TR",""]
			prob_genom[genom_list.index(self.genom)]+=rate_prob_genom
			prob_genom[genom_list.index(other.genom)]+=rate_prob_genom
			if self.genom == other.genom:
				genom_list.remove(self.genom)
			else:
				genom_list.remove(self.genom)
				genom_list.remove(other.genom)
			for n in range(len(genom_list)):
				get_genom = random.choice(genom_list)
				if get_genom == "KL":
					prob_genom[0]+=1
				elif get_genom == "RN":
					prob_genom[1]+=1
				elif get_genom == "SK":
					prob_genom[2]+=1
				elif get_genom == "LZ":
					prob_genom[3]+=1
				elif get_genom == "CW":
					prob_genom[4]+=1
				elif get_genom == "CV":
					prob_genom[5]+=1
				elif get_genom == "TR":
					prob_genom[6]+=1
				elif get_genom == "":
					prob_genom[7]+=1
			genom_list = ["KL","RN","SK","LZ","CW","CV","TR",""]
			new_ADN[9]=genom_list[prob_genom.index(max(prob_genom))]
		return new_ADN

	def move(self,direction):
		print("follow:",self.follow)
		if len(self.follow) == 0:
			pass
		else:
			direction=random.choice(self.follow)
		#remove the current postion of the jex to set it after move
		if direction == "Up" and (self.position[1]+self.speed)>10:
			self.position[1]-=self.speed
			self.hunger+=1
			self.health-=1
			Jex.occuped_area.append(self.position)
			return True

		elif direction == "Down" and (self.position[1]+self.speed)<740:
			self.position[1]+=self.speed
			self.hunger+=1
			self.health-=1
			Jex.occuped_area.append(self.position)
			return True

		elif direction == "Left" and (self.position[0]+self.speed)>10:
			self.position[0]-=self.speed
			self.hunger+=1
			self.health-=1
			Jex.occuped_area.append(self.position)
			return True
		
		elif direction == "Right" and (self.position[0]+self.speed)<740:
			self.position[0]+=self.speed
			self.hunger+=1
			self.health-=1
			Jex.occuped_area.append(self.position)
			return True

		else:
			Jex.occuped_area.append(self.position)
			return False
		
	def kill(self,window, other):
		current_pos=[int(self.position[0]/10),int(self.position[1]/10)]
		prime_pos=[int(other.position[0]/10),int(other.position[1]/10)]
		if (current_pos == prime_pos) and (self.ident != other.ident):
			while self.set_isalive() and other.set_isalive():
				other.health -= self.force
				pygame.draw.circle(window, (255, 0, 0), self.position, self.weight+25, 2)
				pygame.draw.circle(window, (255, 0, 0), other.position, other.weight+25, 2)
			self.force +=5
			self.health-=10
			print(self.ident,"Kill",other.ident)
			return True
		else:
			return False


	def skip(self,win, colony):
		# get the closest position to the jex
		x, y = self.position
		closest_pos = []
		distance = None
		for pos in Jex.occuped_area:
			delta = abs(pos[0]-x)+abs(pos[1]-y)
			if not distance or delta < distance:
				closest_pos = pos.copy()
				distance = delta
		pygame.draw.lines(win, (255,0,0), False, [self.position,closest_pos],1)
		print("there is:",len(Jex.occuped_area),"occuped area")# mouchkal henaaaaaaaaaaaaa

		#intgrate Dijkstra alg _________________________________
		points=[]
		for jj in colony:
			points.append(jj.position)
		dij=Dijkstra(self.position, closest_pos, points)
		path_dij = dij.find_path(win)
		print("path_dij",path_dij)
		for pa in path_dij:
			pygame.draw.lines(win, (0,0,0),False,[(pa[0][0],pa[0][1]),(pa[1][0],pa[1][1])], 4)
			dist_c = (dij.get_distence(self.position,closest_pos)/3)
			pygame.draw.circle(win,(0,0,0),(self.position[0],self.position[1]),dist_c,2)
			pygame.draw.circle(win,(0,0,255),(self.position[0],self.position[1]),dist_c*2,2)

		#______________________________________________________________

		# set the best direction
		self.follow.clear()#3awd khamem fiha meliha rahi tnhi lagudim
		if (self.position[0] > closest_pos[0]) and (self.position[1] > closest_pos[1]):
			self.follow.append("Left")
			self.follow.append("Up")
		elif (self.position[0] > closest_pos[0]) and (self.position[1] < closest_pos[1]):
			self.follow.append("Left")
			self.follow.append("Down")
		elif (self.position[0] < closest_pos[0]) and (self.position[1] > closest_pos[1]):
			self.follow.append("Right")
			self.follow.append("Up")
		elif (self.position[0] < closest_pos[0]) and (self.position[1] < closest_pos[1]):
			self.follow.append("Right")
			self.follow.append("Down")
		elif (self.position[0] > closest_pos[0]) and (self.position[1] == closest_pos[1]):
			self.follow.append("Left")
		elif (self.position[0] < closest_pos[0]) and (self.position[1] == closest_pos[1]):
			self.follow.append("Right")
		elif (self.position[0] == closest_pos[0]) and (self.position[1] > closest_pos[1]):
			self.follow.append("Up")
		elif (self.position[0] == closest_pos[0]) and (self.position[1] < closest_pos[1]):
			self.follow.append("Down")
		else:
			pass
		return True

	def eat(self, other):
		current_pos=[int(self.position[0]/10),int(self.position[1]/10)]
		prime_pos=[int(other.position[0]/10),int(other.position[1]/10)]
		if (current_pos == prime_pos) and (self.ident != other.ident) and (self.force >= other.force):
			other.health =0
			if self.hunger>0:
				self.hunger-=int(other.weight/2) #int(other.weight/10)
			else:
				self.weight+=int(other.weight/2) #int(other.weight/10)
			self.health += 10
			self.force +=5
			print(self.ident,"Eat",other.ident)
			Jex.occuped_area.remove(other.position)
			return True
		else:
			return False

	def reproduce(self,other,colony):
		current_pos=[int(self.position[0]/10),int(self.position[1]/10)]
		prime_pos=[int(other.position[0]/10),int(other.position[1]/10)]
		if (current_pos == prime_pos) and (self.ident != other.ident) and (self.genre != other.genre):
			adn=self.heritage(other, 10)
			new_jex=Jex(adn[0],adn[1],adn[2],adn[3],adn[4],adn[5],adn[6],adn[7],adn[8],adn[9]) #(id_num,weight=5,health=100,force=5,hunger=0,speed=10,genom="")
			new_jex.genartion =(self.genartion+other.genartion)
			colony.append(new_jex)
			print("j chromo",self.chromo)
			print("o chromo",other.chromo)
			print("n chromo",new_jex.chromo)
			return True
		else:
			return False

	def excute(self,window,order, colony, stat_actions):
		if order == "Move":
			dirc =random.choice(["Up","Right","Down","Left"])
			cmd=self.move(dirc)
			if cmd == True:
				stat_actions[0]+=1
		elif order == "Kill":
			for jexy in colony:
				cmd=self.kill(window,jexy)
				if cmd == True:
					stat_actions[1]+=1
				else:
					pass
		elif order == "Skip":
			cmd=self.skip(window,colony)
			if cmd == True:
				stat_actions[2]+=1
		elif order == "Eat":
			for jexy in colony:
				cmd=self.eat(jexy)
				if cmd == True:
					stat_actions[3]+=1
				else:
					pass
		elif order == "Reproduce":
			for jexy in colony:
				cmd=self.reproduce(jexy, colony)
				if cmd == True:
					stat_actions[4]+=1
				else:
					pass
	#Setter and Getter Funcs
	def set_isalive(self):
		if self.health>0:
			return True
		else:
			if self.position in Jex.occuped_area:
				Jex.occuped_area.remove(self.position)
			return False

	def set_needs(self):#["Move","Kill","Skip","Eat","Reproduce"]
		if self.hunger>80:
			need = random.choice(("Eat","Skip","Move","Reproduce"))
			if need not in self.needs:
				self.needs.append(need)
		if self.health<50:
			need = random.choice(("Eat","Skip","Move","Reproduce"))
			if need not in self.needs:
				self.needs.append(need)
		if self.killer:
			if "Kill" not in self.needs:
				self.needs.append(random.choice(("Kill","Move","Reproduce")))
		if self.runner:
			if "Move" not in self.needs:
				self.needs.append(random.choice(("Eat","Move","Reproduce")))
		if self.sick:
			pass
		if self.lazy:
			pass
		if self.coward:
			pass
		if self.clever:
			pass
		if self.tracer:
			pass
		print(self.ident,"needs:",self.needs)

	def set_chromo(self):
		#jADN = [genre,type,color,weight,health,force,hunger,speed,genom]
		chromo=[0,0,0,0,0,0,0,0,0]
		if self.genre == "Male":
			chromo[0] = 1
		else:
			chromo[0] = 0

		if self.type =="White":
			chromo[1] = 0
		elif self.type == "Black":
			chromo[1] = 1
		elif self.type == "Yellow":
			chromo[1] = 2
		elif self.type == "Red":
			chromo[1] = 3
		elif self.type == "Green":
			chromo[1] = 4

		if self.color == (255, 255, 255):
			chromo[2] = 0
		elif self.color == (0, 0, 0):
			chromo[2] = 1
		elif self.color == (247, 247, 0):
			chromo[2] = 2
		elif self.color == (255, 0, 0):
			chromo[2] = 3
		elif self.color == (0,255,0):
			chromo[2] = 4

		chromo[3]= self.weight
		chromo[4]= self.health
		chromo[5]= self.force
		chromo[6]= self.hunger
		chromo[7]= self.speed

		if self.genom ==  "KL":
			chromo[8] = 0
		elif self.genom == "RN":
			chromo[8] = 1
		elif self.genom == "SK":
			chromo[8] = 2
		elif self.genom == "LZ":
			chromo[8] = 3
		elif self.genom == "CW":
			chromo[8] = 4
		elif self.genom == "CV":
			chromo[8] = 5
		elif self.genom == "":
			chromo[8] = 6
		return chromo
		