import Images
from Images import pygame as pygame
from Classes import Rec, Player, Projectile, Enemy, GameSound
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

clock = pygame.time.Clock()
class Game(object):
	def __init__(self, window):
		self.win = window
		self.run = True
		self.player = None
		self.goblin = None
		self.bullets = []
		self.shoot_loops = 0
		self.score = 0
		self.sound = GameSound()
		self.font = pygame.font.SysFont('comicsans', 30, True, True)

	def add_player(self,player):
		self.player = player

	def add_enemy(self, enemy):
		self.goblin = enemy

	def start(self):
		#self.sound.play()
		player, run = self.player, self.run
		if player == None: run = False
		if self.goblin == None: run = False
		#game loop
		while run:
			clock.tick(27)
			# making a timer for shooting
			if self.shoot_loops > 0:
				self.shoot_loops += 1 
			if self.shoot_loops > 3:
				self.shoot_loops = 0
			pygame.time.delay(28)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

			for bullet in self.bullets:
				if hit(bullet, self.goblin, self.sound):
					self.score += 1
					self.bullets.pop(self.bullets.index(bullet))

				if not bullet.shoot(500):
					self.bullets.pop(self.bullets.index(bullet))

			#init
			keys, boundries = pygame.key.get_pressed(), (SCREEN_WIDTH, SCREEN_HEIGHT)
			#shoot
			if keys[pygame.K_SPACE] and self.shoot_loops == 0:
				self.sound.bullet_play()
				facing = 1
				if self.player.left:
					facing = -1
				if len(self.bullets) < 8:
					self.bullets.append(Projectile(round(self.player.x + self.player.width //2), 
						round(self.player.y + self.player.height //2), 6, (0,0,0),facing))
				self.shoot_loops = 1
			#move
			player.move(keys, boundries)
			
			#draw
			self.drawGameWindow()

	def drawGameWindow(self):
		#background
		self.win.blit(Images.bg, (0,0))
		#score
		text = self.font.render('Score ' + str(self.score), 1, (0, 0, 0))
		self.win.blit(text,(15,15))
		#enemy
		if self.goblin != None:
			self.goblin.draw(self.win)
		#player
		self.player.draw(self.win)
		#bullet
		for bullet in self.bullets:
			bullet.draw(self.win)
		pygame.display.update()


def hit(bullet, goblin, sound):
		below = goblin.hitbox[1] #below the hitbox
		above = below + goblin.hitbox[3] #above the enemy 
		bullet_y_pos_above, bullet_y_pos_below  = bullet.y - bullet.radius, bullet.y + bullet.radius
		bullet_x_left_pos, bullet_x_right_pos = bullet.x + bullet.radius, bullet.x - bullet.radius
		left = goblin.hitbox[0]
		right = left + goblin.hitbox[2]
		#if hit the collision
		if bullet_y_pos_above < above and bullet_y_pos_below > below:
			if bullet_x_left_pos > left and bullet_x_right_pos < right:
				goblin.hit(sound)
				return True
		return False

def main():
	#init
	win = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
	pygame.display.set_caption("First Game")
	game = Game(win)
	game.add_player(Player(300,410,64,64))
	game.add_enemy(Enemy(100,410,64,64,450))
	game.start()
	pygame.quit()

if __name__ == '__main__':
	pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize

	pygame.init()
	main()