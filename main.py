import minesweeper
import pygame
import sys
import button

pygame.init()
screen = pygame.display.set_mode()
pygame.display.set_caption("Mr. Kinney is making me make this game")
font = pygame.font.SysFont("comicsansms", 30)
scr_w = screen.get_size()[0] - 2
scr_h = screen.get_size()[1] - 27
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 100)
darker_unswept = (162,209,73)
lighter_unswept = (202, 253, 100)
darker_swept = (196,170,122)
lighter_swept = (237,205,145)
text_color = (0,0,255)
tile_size = 40
game_over = False
game_over_message = ""

button_width = scr_w / 3
button_height = scr_h/8
button_starting_x = scr_w / 2 -button_width / 2
easy_button = button.Button(button_starting_x, 3*scr_h / 16, button_width, button_height, text = "EASY", color = darker_unswept)
medium_button = button.Button(button_starting_x, 7*scr_h / 16, button_width, button_height, text = "MEDIUM", color = darker_unswept)
hard_button = button.Button(button_starting_x, 11*scr_h / 16, button_width, button_height, text = "HARD", color = darker_unswept)
game = minesweeper.Minesweeper("easy")
current_screen = "menu"

def start_game(difficulty):
	global game_over, game_over_message, current_screen, game
	game_over = False
	game_over_message = ""
	current_screen = "game"
	game = minesweeper.Minesweeper(difficulty)

def draw_menu():
	easy_button.draw(screen)
	hard_button.draw(screen)
	medium_button.draw(screen)

def draw_game():
	x = 0
	y = 0
	for row in range(game.rows):
		for col in range(game.cols):
			tile_color = darker_unswept
			text = ""
			tile = game.grid[row][col]
			# #for testing:
			# if tile.mine:
			# 	text = "M"
				
			if tile.visible:
				if not tile.mine and tile.nearby_mines > 0:
					text = str(tile.nearby_mines)
				tile_color = darker_swept
				if (row+col) % 2 ==0:
					tile_color = lighter_swept 
			else:
				if tile.flagged:
					text = "F"
				if (row+col) %2 ==0:
					tile_color = lighter_unswept

				#if game is over reveal minesweeper
			if game_over and tile.mine:
				text += "M"
				
			#make a rect
			rect = [x,y,tile_size,tile_size]
			#draw rect
			pygame.draw.rect(screen,tile_color,rect)
			#render and draw text
			text_render = font.render(text, True, text_color)
			text_rect = text_render.get_rect(center = (x + tile_size/2, y + tile_size/2))
			screen.blit(text_render, text_rect)
				
			#move starting x over
			x += tile_size
		#at end of row, reset x and increase y
		x = 0
		y += tile_size
	#draw messages under the board, flags remaining
	text_render = font.render("Flags: " + str(game.remaining_flags), True, lighter_unswept)
	text_rect = text_render.get_rect(center = (tile_size * game.cols / 2, y + tile_size / 2))
	screen.blit(text_render, text_rect)
	y += tile_size
	#display game over message
	text_render = font.render(game_over_message, True, darker_unswept)
	text_rect = text_render.get_rect(center = (tile_size * game.cols / 2, y + tile_size / 2))
	screen.blit(text_render, text_rect)

while True:
	#checking for user input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit() #don't forget to import sys
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse = pygame.mouse.get_pos()
			if current_screen == "game":
				
				row = mouse[1]//tile_size
				col = mouse[0]//tile_size
	
				if not game_over:
					#left click:
					if pygame.mouse.get_pressed()[0]:
						if 0 <= row < game.rows and 0 <= col < game.cols:
							if game.sweep(row, col):
								game_over = True
								game_over_message = "You lost"
							elif game.check_for_win():
								game_over = True
								game_over_message = "You win"
					if pygame.mouse.get_pressed()[2]:
						if 0 <= row < game.rows and 0 <= col < game.cols:
							game.flag(row,col)
				else:
					current_screen = "menu"
			elif current_screen == "menu":
				if easy_button.contains(mouse):
					start_game("easy")
				elif medium_button.contains(mouse):
					start_game("medium")
				elif hard_button.contains(mouse):
					start_game("hard")
	#draw stuff
	screen.fill((0,0,0))
	if current_screen == "menu":	
		draw_menu()
	elif current_screen == "game":
		draw_game()
	pygame.display.update()
	clock.tick(10)