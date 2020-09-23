import pygame,os, random, time
pygame.font.init()

#game init
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Tutorial")

#assets
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))
#main player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))

#Lasers
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))

COLOR_MAP = {
	"red": (RED_SPACE_SHIP, RED_LASER),
	"blue": (BLUE_SPACE_SHIP, BLUE_LASER),
	"green": (GREEN_SPACE_SHIP, GREEN_LASER),
	"yellow": (YELLOW_SPACE_SHIP, YELLOW_LASER)
}

#bg
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))

class Laser:
	def __init__(self, x, y, img, vel = 25):
		self.x = x
		self.y = y
		self.img = img
		self.vel = vel
		self.mask = pygame.mask.from_surface(self.img)

	def draw(self, win):
		win.blit(self.img, (self.x, self.y))

	def move(self, vel):
		self.y += vel

	def off_screen(self, height):
		return not(self.y <= height and self.y >= -150)

	def collision(self, obj):
		return collide(self, obj)

class Ship:
	COOLDOWN = 6

	def __init__(self, x, y, vel, health = 100):
		self.x = x
		self.y = y
		self.vel = vel
		self.health = health
		self.ship_img = None
		self.laser_img = None
		self.lasers = []
		self.laser_lvl = 1
		self.cool_down_counter = 0

	def set_ship(self, img):
		self.ship_img, self.laser_img = img

	def get_width(self):
		return self.ship_img.get_width()

	def get_height(self):
		return self.ship_img.get_height()

	def move(self, keys):
		if keys[pygame.K_LEFT]:
			if self.x - self.vel > 0:
				self.x -= self.vel
			else:
				self.x = 0
		if keys[pygame.K_RIGHT]:
			if self.x + self.vel < WIDTH - self.get_width():
				self.x += self.vel
			else:
				self.x = WIDTH - self.get_width()
		if keys[pygame.K_UP]:
			if self.y - self.vel > 0:
				self.y -= self.vel
			else:
				self.y = 0
		if keys[pygame.K_DOWN]:
			if self.y + self.vel < HEIGHT - self.get_height() - 22:
				self.y += self.vel
			else:
				self.y = HEIGHT - self.get_height() - 22
		if keys[pygame.K_SPACE]:
			self.shoot()


	def cooldown(self):
		if self.cool_down_counter >= self.COOLDOWN:
			self.cool_down_counter = 0
		elif self.cool_down_counter > 0:
			self.cool_down_counter += 1

	def shoot_lvl3(self):
		laser = Laser(self.x - 30, self.y, self.laser_img)
		self.lasers.append(laser)
		laser = Laser(self.x + 30, self.y, self.laser_img)
		self.lasers.append(laser)
		laser = Laser(self.x, self.y, self.laser_img)
		self.lasers.append(laser)
		self.cool_down_counter = 1


	def shoot_lvl2(self):
		laser = Laser(self.x - 20, self.y, self.laser_img)
		self.lasers.append(laser)
		laser = Laser(self.x + 20, self.y, self.laser_img)
		self.lasers.append(laser)
		self.cool_down_counter = 1


	def shoot(self):
		if self.laser_lvl == 2 and self.cool_down_counter == 0:
			self.shoot_lvl2()
		elif self.laser_lvl >= 3 and self.cool_down_counter == 0:
			self.shoot_lvl3()
		elif self.cool_down_counter == 0:
			laser = Laser(self.x, self.y, self.laser_img)
			self.lasers.append(laser)
			self.cool_down_counter = 1

	def draw(self, win):
		if self.ship_img is None:
			pygame.draw.rect(win, (255,0,0), (self.x, self.y, 50, 50))
		else:
			win.blit(self.ship_img, (self.x, self.y))
		for laser in self.lasers:
			laser.draw(win)

	def move_lasers(self, obj):
		self.cooldown()
		for laser in self.lasers:
			laser.move(self.vel + 10)
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			elif laser.collision(obj):
				obj.health -= 10
				self.lasers.remove(laser)

class Player(Ship):
	def __init__(self, x, y, vel = 5, health=11600, lives = 100):
		super().__init__(x,y,vel,health)
		self.set_ship(COLOR_MAP["yellow"])
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.max_health = health
		self.lives = lives

	def move_lasers(self, objs):
		self.cooldown()
		for laser in self.lasers:
			laser.move(-self.vel)
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			else:
				for obj in objs:
					if laser.collision(obj):
						objs.remove(obj)
						if laser in self.lasers: self.lasers.remove(laser)

	def draw(self, win):
		super().draw(win)
		self.health_bar(win)

	def health_bar(self, win):
		pygame.draw.rect(win, (255,0,0), (self.x, self.y + self.get_height() + 10, self.get_width(), 10))
		if self.health <= 0:
			return
		pygame.draw.rect(win, (0,255,0), (self.x, self.y + self.get_height() + 10, 
			self.get_width() * ((self.health/self.max_health)), 10))

class Enemy(Ship):

	def __init__(self, x, y, color, vel = 1, health=100):
		super().__init__(x, y, vel, health)
		self.set_ship(COLOR_MAP[color])
		self.mask = pygame.mask.from_surface(self.ship_img)

	def enemy_move(self):
		self.y += self.vel

	def shoot(self):
		if self.cool_down_counter == 0:
			laser = Laser(self.x - 15, self.y, self.laser_img)
			self.lasers.append(laser)
			self.cool_down_counter = 1

def collide(obj1, obj2):
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	# collide return (x,y) or None
	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None 

def start(run, FPS):
	level, lost, lost_count, won = 9, False, 0, False
	main_font = pygame.font.SysFont("comicsans", 50)
	lost_font = pygame.font.SysFont("comicsans", 60)
	player, enemies = Player(300, 620, 20), []
	wave_length, ret_val = 0, True
	print(player.laser_lvl)
	mons = 4
	def draw_window():
		#bg
		WIN.blit(BG, (0,0))

		player.draw(WIN)

		for enemy in enemies:
			enemy.draw(WIN)

		#draw text
		lives_label = main_font.render(f"Lives: {player.lives}", 1, (255,255,255))
		level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
		WIN.blit(lives_label, (10, 10))
		WIN.blit(level_label, (WIDTH - level_label.get_width() - 20, 10))
		if lost:
			lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
			pos = (int(WIDTH/2 - lost_label.get_width()/2), 350)
			WIN.blit(lost_label, pos)
		
		elif won:
			lost_label = lost_font.render("You WON :)", 1, (255,255,255))
			pos = (int(WIDTH/2 - lost_label.get_width()/2), 350)
			
			WIN.blit(lost_label, pos)

		pygame.display.update()

	clock = pygame.time.Clock()
	while (run):
		clock.tick(24)

		if level >= 113:
			won = True
		draw_window()
		if player.lives <= 0 or player.health <=0:
			lost = True

		if lost or won: 
			lost_count += 1
			if lost_count > FPS * 20:
				run = False
			else:
				continue

		if len(enemies) == 0:
			level += 1
			player.laser_lvl = level//5 + 1
			if player.health + 50 <= player.max_health:
				player.health += 50
			wave_length = level * mons
			for i in range(wave_length):
				enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), 
					random.choice(["red", "blue", "green"]), random.randrange(3, 12))
				enemies.append(enemy)
		

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				ret_val = False
		keys = pygame.key.get_pressed()
		player.move(keys)
		for enemy in enemies:
			enemy.enemy_move()
			enemy.move_lasers(player)

			if random.randrange(0,70) == 1:
				enemy.shoot()

			if collide(enemy, player):
				player.health -= 10
				enemies.remove(enemy)

			elif enemy.y + enemy.get_height() > HEIGHT:
				player.lives -= 1
				enemies.remove(enemy)

		player.move_lasers(enemies)

	return ret_val
		



def main_menu():
	title_font = pygame.font.SysFont("comicsans", 80)
	run = True
	while run:
		WIN.blit(BG, (0,0))
		title_label = title_font.render("Press any key to begin...", 1, (255, 255, 255))
		WIN.blit(title_label, ((WIDTH - title_label.get_width())/2,(HEIGHT - title_label.get_height())/2))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				continue
			elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
				run = main()
	pygame.quit()


def main():
	run, FPS = 24,True
	return start(run, FPS)

main_menu()