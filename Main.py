import random
import pygame
from pygame.locals import *
from Jex import Jex


# initiate pygame and give permission
# create the display surface object of specific dimension.
pygame.init()
window = pygame.display.set_mode((1080, 800),pygame.RESIZABLE)
pygame.display.set_caption("Jex colony simulator")

#varible
run = True
clock=pygame.time.Clock()
total_jexs=0
num_round = 0
stat_type=[0,0,0,0,0,0,0] #by color and genre
stat_actions=[0,0,0,0,0] #by actions
farm=[]
num_genrate=0
genrate = True

#-----------------------------------------------------------
def start_genrate(num_jexs=10, num_gen=0, num_keep=0):
	global num_genrate, total_jexs
	if num_genrate < num_gen and len(farm)<=num_keep:
		for n in range(num_jexs):
			genres=random.choice(["Male","Female"])
			types=random.choice(["White","Black","Yellow","Red","Green"])
			colors=random.choice([(255, 255, 255),(0, 0, 0),(247, 247, 0),(255, 0, 0),(0,255,0)])
			#(id_num,genre,typpe,color,weight=5,health=100,force=5,hunger=0,speed=10,genom="")
			j=Jex(n,genres,types,colors)
			farm.append(j)
		total_jexs+=len(farm)
		num_genrate +=1
	if len(farm)== num_keep and num_keep > 0:
		for n in range(num_jexs):
			genres=random.choice(["Male","Female"])
			types=random.choice(["White","Black","Yellow","Red","Green"])
			colors=random.choice([(255, 255, 255),(0, 0, 0),(247, 247, 0),(255, 0, 0),(0,255,0)])
			#(id_num,genre,typpe,color,weight=5,health=100,force=5,hunger=0,speed=10,genom="")
			j=Jex(n,genres,types,colors)
			farm.append(j)
		total_jexs+=len(farm)

#Func calculate stats data
def calculate_stats(colony):
	stat_type=[0,0,0,0,0,0,0]
	for jex in colony:
		#count them by color
		if jex.type == "White":
			stat_type[0] +=1
		elif jex.type == "Black":
			stat_type[1] +=1
		elif jex.type == "Yellow":
			stat_type[2] +=1
		elif jex.type == "Red":
			stat_type[3] +=1
		elif jex.type == "Green":
			stat_type[4] +=1
		#count them by genre
		if jex.genre == "Male":
			stat_type[5] +=1
		elif jex.genre == "Female":
			stat_type[6] +=1
	return stat_type

#Func to show stats data
def showstats(num_round): 
	# Fonts
	font= pygame.font.Font('freesansbold.ttf',15)
	pygame.draw.circle(window, (225,225,225),(850,300), 30, 0)#view the model Jex
	model_info1= font.render("   Gen            Genom",True,(0,0,0))
	model_info2= font.render("Force  Health  Hunger",True,(0,0,0))
	model_info3= font.render("ID-gen weight Genre",True,(0,0,0))
	font_title= pygame.font.Font('freesansbold.ttf',30)
	title_colony= font_title.render("Jex colony simulator",True,(255,0,0))
	num_genartion= font.render("Generation:"+str(num_genrate),True,(0,0,0))
	num_round= font.render("Round:"+str(num_round),True,(0,0,0))
	num_jex= font.render("Total(JCC): "+str(len(farm))+"/"+str(total_jexs)+" Toltal(NPD): "+str(stat_actions[4]),True,(255,0,0))
	statsC_jex= font.render("Total by Colors & Types:",True,(0,0,0))
	white_jex= font.render("White(Type A):"+str(num_white_jex),True,(255, 255, 255))
	black_jex= font.render("Black(Type B):"+str(num_black_jex),True,(0, 0, 0))
	yellow_jex= font.render("Yellow(Type C):"+str(num_yellow_jex),True,(247, 247, 0))
	red_jex= font.render("Red(Type D):"+str(num_red_jex),True,(255, 0, 0))
	green_jex= font.render("Green(Type E):"+str(num_green_jex),True,(0,255,0))
	statsG_jex= font.render("Total by Genres:",True,(0,0,0))
	male_jex= font.render("Male(M):"+str(num_Male),True,(14,75,239))
	female_jex= font.render("Female(F):"+str(num_Female),True,(225,0,0))
	statsA_jex= font.render("Actions:",True,(0,0,0))
	move_jex= font.render(str(stat_actions[0]),True,(255, 0, 0))
	kill_jex= font.render(str(stat_actions[1]),True,(255, 0, 0))
	skip_jex= font.render(str(stat_actions[2]),True,(255, 0, 0))
	eat_jex= font.render(str(stat_actions[3]),True,(255, 0, 0))
	reproduce_jex= font.render(str(stat_actions[4]),True,(255, 0, 0))
	#Blit the texts to screen
	window.blit(model_info1,(780,260))
	window.blit(model_info2,(780,290))
	window.blit(model_info3,(780,330))
	window.blit(title_colony,(100,870))
	window.blit(num_genartion,(770,10))
	window.blit(num_round,(770,30))
	window.blit(num_jex,(10,770))
	window.blit(statsC_jex,(810,50)) #by color
	window.blit(white_jex,(770,70))
	window.blit(black_jex,(770,90))
	window.blit(yellow_jex,(770,110))
	window.blit(red_jex,(770,130))
	window.blit(green_jex,(770,150))
	window.blit(statsG_jex,(810,170)) #by genre
	window.blit(male_jex,(770,190))
	window.blit(female_jex,(770,210))
	window.blit(statsA_jex,(10,790)) #by actions
	window.blit(move_jex,(80,800))
	window.blit(kill_jex,(180,800))
	window.blit(skip_jex,(280,800))
	window.blit(eat_jex,(380,800))
	window.blit(reproduce_jex,(480,800))

#func to show the comand in screen
def rest_cmd_button():
	fontcommand= pygame.font.Font('freesansbold.ttf',15)
	pygame.draw.circle(window, (225,225,225),(50,825), 20, 0)
	pygame.draw.circle(window, (225,225,225),(150,825), 20, 0)
	pygame.draw.circle(window, (225,225,225),(250,825), 20, 0)
	pygame.draw.circle(window, (225,225,225),(350,825), 20, 0)
	pygame.draw.circle(window, (225,225,225),(450,825), 20, 0)
	logo_cmd_move= fontcommand.render("Move",True,(0,0,0))
	logo_cmd_kill= fontcommand.render("Kill",True,(0,0,0))
	logo_cmd_skip= fontcommand.render("Skip",True,(0,0,0))
	logo_cmd_eat= fontcommand.render("Eat",True,(0,0,0))
	logo_cmd_reproduce= fontcommand.render("Reproduce",True,(0,0,0))
	window.blit(logo_cmd_move,(50,820))
	window.blit(logo_cmd_kill,(150,820))
	window.blit(logo_cmd_skip,(250,820))
	window.blit(logo_cmd_eat,(350,820))
	window.blit(logo_cmd_reproduce,(450,820))

def anime_order(order):
	fontcommand= pygame.font.Font('freesansbold.ttf',15)
	if order == "Move":
		logo_cmd_move= fontcommand.render("Move",True,(217, 33, 33))
		window.blit(logo_cmd_move,(50,820))
	elif order == "Kill":
		logo_cmd_kill= fontcommand.render("Kill",True,(217, 33, 33))
		window.blit(logo_cmd_kill,(150,820))
	elif order == "Skip":
		logo_cmd_skip= fontcommand.render("Skip",True,(217, 33, 33))
		window.blit(logo_cmd_skip,(250,820))
	elif order == "Eat":
		logo_cmd_eat= fontcommand.render("Eat",True,(217, 33, 33))
		window.blit(logo_cmd_eat,(350,820))
	elif order == "Reproduce":
		logo_cmd_reproduce= fontcommand.render("Reproduce",True,(217, 33, 33))
		window.blit(logo_cmd_reproduce,(450,820))
	else:
		pass
#Start tests
while run:
	start_genrate(num_jexs=100,num_gen=4,num_keep=20)
	#calculate stats data by colors and genres
	stat_type = calculate_stats(farm)
	num_white_jex=stat_type[0]
	num_black_jex=stat_type[1]
	num_yellow_jex=stat_type[2]
	num_red_jex=stat_type[3]
	num_green_jex=stat_type[4]
	num_Male=stat_type[5]
	num_Female=stat_type[6]

	# Fill the screen with color and show the stats
	window.fill((136, 140, 141))
	showstats(num_round)
	#draw the rect "zone of experience" on the screen
	win = pygame.draw.rect(window, (255,0,0), [0,0,750,750], 2)
	
	for j in farm:
		rest_cmd_button()
		j.set_needs()
		if j.set_isalive() and len(j.needs)==0:
			order =random.choice(["Move","Kill","Skip","Eat","Reproduce"])
			anime_order(order)
			j.excute(window,order, farm, stat_actions)
		elif j.set_isalive() and len(j.needs)>0:
			order =random.choice(j.needs)
			j.needs.remove(order)
			anime_order(order)
			j.excute(window,order, farm, stat_actions)
		else:
			farm.remove(j)
			rest_cmd_button()
			print(j.ident,"is dead")

		#draw the Jex and his indecators on the screen 
		pygame.draw.circle(window, j.color, j.position, j.weight, 0)
		#add effects by genoms
		if j.killer is True:
			pygame.draw.circle(window, (255, 0, 0), j.position, j.weight, 2)
		if j.runner is True:
			pygame.draw.circle(window, (247, 247, 0), j.position, j.weight+2, 2)
		if j.clever is True:
			pygame.draw.circle(window, (0, 0, 255), j.position, j.weight+4, 2)
		if j.tracer is True:
			pygame.draw.circle(window, (0, 0, 0), j.position, 25, 2)

		#show the symbol of generation
		if j.genartion>1:
			fontgen= pygame.font.Font('freesansbold.ttf',10)
			logo_gen= fontgen.render(str(j.genartion),True,j.color)
			window.blit(logo_gen,((j.position[0]+j.weight)-25,(j.position[1]+j.weight)-25))
		else:
			pass
		#show the symbol of genre
		if j.genre == "Male":
			fontgenre= pygame.font.Font('freesansbold.ttf',10)
			logo_genre= fontgenre.render("M",True,(14,75,239))
			window.blit(logo_genre,((j.position[0]+j.weight),(j.position[1]+j.weight)))
		elif j.genre == "Female":
			fontgenre= pygame.font.Font('freesansbold.ttf',10)
			logo_genre= fontgenre.render("F",True,(255,0,0))
			window.blit(logo_genre,((j.position[0]+j.weight),(j.position[1]+j.weight)))
		else:
			pass
		#show the symbol of genom
		if j.genom == "":
			pass
		else:
			fontgenom = pygame.font.Font('freesansbold.ttf',10)
			logo_genom= fontgenom.render(str(j.genom),True,(0,0,0))
			window.blit(logo_genom,((j.position[0]+j.weight),(j.position[1]+j.weight)-25))
		#show the id of jex
		fontidjex = pygame.font.Font('freesansbold.ttf',10)
		logo_idjex= fontidjex.render(str(j.ident),True,(0,0,0))
		window.blit(logo_idjex,((j.position[0]+j.weight)-25,(j.position[1]+j.weight)))
		#show the health of jex
		fonthealth = pygame.font.Font('freesansbold.ttf',10)
		logo_health= fonthealth.render(str(j.health),True,(0,100,255))
		window.blit(logo_health,(j.position[0]-5,j.position[1]-5))
		#show the force of jex
		fontforce = pygame.font.Font('freesansbold.ttf',10)
		logo_force= fonthealth.render(str(j.force),True,(255,0,0))
		window.blit(logo_force,(j.position[0]-20,j.position[1]-5))
		#show the hunger of jex
		fonthunger = pygame.font.Font('freesansbold.ttf',10)
		logo_hunger= fonthunger.render(str(j.hunger),True,(0,255,0))
		window.blit(logo_hunger,(j.position[0]+15,j.position[1]-5))
		#show the weight of jex
		fontweight = pygame.font.Font('freesansbold.ttf',10)
		logo_weight= fontweight.render(str(j.weight),True,(255,255,0))
		window.blit(logo_weight,(j.position[0]-5,j.position[1]+15))

	num_round +=1
	pygame.display.update()
	clock.tick(50)
	print("\nil rest:",len(farm),"Jex\n")
	#the differents events of the jex simulator
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()
