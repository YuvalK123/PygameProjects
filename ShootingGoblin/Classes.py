import Images, pygame
class Rec:
	def __init__(self,x,y,width,height,vel):
		self.x, self.y = x,y
		self.width,self.height,self.vel = width,height,vel

	def get_fields(self):
		return self.x,self.y,self.width,self.height,self.vel

	def set_xy(self,xx,yy):
		self.x, self.y = xx,yy

'''player'''

class Player(object):
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = 5
		self.is_jump = False
		self.jump_count = 5
		self.left = False
		self.right = False
		self.walk_count = 0
		self.standing = True
		self.update_hitbox() #(x,y,width,height   )

	def draw(self,win):
		walk_size, coord = len(Images.walkRight)*3,(self.x, self.y)
		if self.walk_count + 1 >= (walk_size):
			self.walk_count = 0
		#draw actions
		if not self.standing:	
			if self.left:
				win.blit(Images.walkLeft[self.walk_count//3],coord)
				self.walk_count += 1
			elif self.right:
				win.blit(Images.walkRight[self.walk_count//3],coord)
				self.walk_count += 1
		else:
			if self.left:
				win.blit(Images.walkLeft[0],coord)
			elif self.right:
				win.blit(Images.walkRight[0],coord)
			else:
				win.blit(Images.char,coord)
		#score bar
		#self.draw_score_bar()
		self.update_hitbox() #(x,y,width,height   )

		#pygame.draw.rect(win, (255,0,0),self.hitbox,2)


	def draw_score_bar(self):
		pos = (self.hitbox[0], self.hitbox[1] - 20, 50, 10)
		pygame.draw.rect(win,(255,0,0), pos)
		pygame.draw.rect(win,(0,255,0), pos)


	def update_hitbox(self):
		self.hitbox = (self.x + 17, self.y + 11, 29, 52) #(x,y,width,height   )
    
	def get_fields(self):
		return self.x, self.y, self.width, self.height

	def getVel(self):
		return self.vel

	def jump(self, keys):
		if self.jump_count >= -5:
			neg = 2
			if self.jump_count < 0 :
				neg = -2
			self.y -= (self.jump_count ** 2) * 0.5 * neg
			self.jump_count -= 1
		else:
			self.is_jump = False
			self.jump_count = 5


	def move(self, keys, boundries):
		SCREEN_WIDTH, SCREEN_HEIGHT,vel = boundries[0],boundries[1], self.vel
		x_boundry, y_boundry = SCREEN_WIDTH - vel - self.width, SCREEN_HEIGHT - vel - self.height
		if keys[pygame.K_LEFT]:
			self.right = False
			self.left = True
			self.standing = False
			if self.x > vel:
				self.x -= vel
			else:
				self.x = 0
		elif keys[pygame.K_RIGHT]:
			self.right = True
			self.left = False
			self.standing = False
			if self.x <= x_boundry:
				self.x += vel
			else:
				self.x = SCREEN_WIDTH - self.width
		else:
			self.standing = True
			self.walkCount = 0
		if not self.is_jump:
			if keys[pygame.K_UP]:
				#self.right = False
				#self.left = False
				self.walkCount = 0
				self.is_jump = True
		else:
			self.jump(keys)

	def hit(self, pg, win, SCREEN_WIDTH,SCREEN_HEIGHT):
		self.x = 60
		self.y = 410
		self.walk_count= 0
		hit_font = pygame.font.SysFont('comicsans',100,True)
		text = hit_font.render("-5",1, (255,0,0))
		win.blit(text, ((SCREEN_WIDTH/2) - (text.get_width()/2))((SCREEN_HEIGHT/2) - (text.get_height()/2)))
		pygame.display.update()
		i = 0
		for i in range(150):
			pygame.time.delay(5)
			for event in pg.events.get():
				if event.type == pygame.QUIT:
					i = 200
					pg.quit()


'''projectile'''
class Projectile(object):
	def __init__(self,x,y,radius,color,facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.facing = facing
		self.vel = 8 * facing


	def shoot(self, x_boundry):
		if self.x < x_boundry and self.x > 0:
			self.x += self.vel
			return True
		else:
			return False 


	def draw(self,win):
		pygame.draw.circle(win,self.color,(self.x,self.y), self.radius)

'''enemy'''
class Enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    
    def __init__(self, x, y, width, height, end):
    	self.x = x
    	self.y = y
    	self.width = width
    	self.height = height
    	self.end = end
    	self.walk_count = 0
    	self.vel = 3
    	self.path = [x, end]
    	self.max_walk = 33
    	self.health = 10
    	self.init_health = 10
    	self.visible = True
    	self.update_hitbox() 

    def draw(self,win):
    	self.move()
    	if not self.visible:
    		return
    	if self.walk_count + 1  >= self.max_walk:
    		self.walk_count = 0

    	coords = (self.x, self.y)
    	#right
    	if self.vel > 0:
    		win.blit(self.walkRight[self.walk_count //3], coords)
    		self.walk_count += 1
    	else:
    		win.blit(self.walkLeft[self.walk_count //3], coords)
    		self.walk_count += 1
    		
    	self.draw_score_bar(win)
    	self.update_hitbox()
    	#pygame.draw.rect(win, (255,0,0),self.hitbox,2)
    
    def draw_score_bar(self,win):
    	#pos = (x,y,width,height)
    	health_bar_width = 50
    	green_width = health_bar_width - (health_bar_width//self.init_health) * (self.init_health - self.health)
    	red_pos = (self.hitbox[0] - 10, self.hitbox[1] - 20, health_bar_width, 10)
    	green_pos = (self.hitbox[0] - 10, self.hitbox[1] - 20, green_width, 10)
    	pygame.draw.rect(win, (255,0,0), red_pos)
    	pygame.draw.rect(win, (60,255,5), green_pos)


    def update_hitbox(self):
    	#(x,y,width,height)
    	self.hitbox = (self.x + 17, self.y + 2, 31, 57) 
    
    def move(self):
    	#move right
    	if self.vel > 0:
    		if self.x + self.vel < self.path[1]:
    			self.x += self.vel
    		else:
    			#self.x = self.end
    			self.vel = self.vel*-1
    			self.walk_count = 0

    	#move left
    	else:
    		if self.x - self.vel > self.path[0]:
    			self.x += self.vel
    		else:
    			#self.x = self.path[0]
    			self.vel = self.vel*-1
    			self.walk_count = 0

    def hit(self, sound):
    	sound.hit_play()
    	if self.health > 0:
    		self.health -= 1
    	else: self.visible = False

'''sound'''
class GameSound(object):
	"""docstring for GameSound"""
	def __init__(self):
		self.is_sound = True
		self.is_music = True
		#self.bullet_sound = pygame.mixer.Sound('bullet.mp3')
		#self.hit_sound = pygame.mixer.Sound('hit.mp3')
		self.music = pygame.mixer.music.load('music.mp3')

	def play(self):
		pygame.mixer.music.play(-1) #continus play

	def bullet_play(self):
		pass
		#self.bullet_sound.play()

	def hit_play(self):
		pass
		#self.hit_sound.play()
print("w")
#pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize	
#pygame.init()