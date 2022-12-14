import pygame as d
import pygame.gfxdraw as gfxd
from os import path
from math import floor, sin, atan, sqrt
import copy
import time

# TODO make a start menu with PvP (same device (≅ autoflip) or local or distant), PvC, computer analysis, AI trainer (hidden window ?), local app for playing on chess.com or lichess.org or …
# TODO make a menu bar
# TODO add different resolutions (1 big and others are smallered img resolutions ? Or vector image ?) (permanent ?)
# TODO timed games + rules with it
# TODO show coordinates on board
# TODO let user customize squares colors (and what else ?)
# TODO user choice to show possible squares when piece is clicked or not 
# TODO (user choice draw arrows to only on possible squares)
# TODO animate end of game lost king flip on red square, won king on green, particle stars around ; Draw = 360° kings
# TODO premoves
# TODO other promotions
# TODO end chess rules
# TODO sometimes check if comfortable to play when devving
# TODO add other colors with right click and alt / ctrl    // custom color
# TODO user choice to rotate board
# TODO sound with pieces
# TODO make it NOFRAME -> make custom frame
# TODO user can choose fullscreen
# TODO describe when hovered element
# TODO Ctrl+click to get keyboard shortcut of any element
# TODO in boring situations, let user choose to draw mirrored arrows :)
# TODO let choose settings yes/no : colored when changed / when YES + reset button
# TODO (offer to) save data in a file to keep it for next launch
# TODO random quote goodbye message
# TODO SQL settings database ?


# def list_to_str(chess_board):
# 	"""Turns the list of lists (the chessboard position) given into a FEN string, useful for chess problems"""
# 	pass

# def count_combinations(n):
# 	"""Counts the number of possible move combinations from the beginning of the game after n total moves"""
# 	pass

# def count_positions(n):
# 	"""Counts the number of possible board positions after n moves"""
# 	pass



# CLASSES


#class …



# VARIABLES


# Colors                    # Make all colors changeable according to the theme (parameter)
grey = d.Color(29, 38, 46)
grey2 = d.Color(33, 43, 51)
lightgrey = d.Color(43, 57, 69)
lightergrey = d.Color(57, 76, 92)
lightestgrey = d.Color(85, 114, 138)
lightestergrey = d.Color(113, 152, 184)
darkgrey = d.Color(24, 32, 39)
darkergrey = d.Color(21, 27, 33)
darkestgrey = d.Color(20, 26, 31)
light = d.Color(172, 115, 57)
dark = d.Color(102, 51, 0)
lightblue = d.Color(100, 100, 255)
darkblue = d.Color(40, 40, 100)
lightorange = d.Color(120, 80, 40)
darkorange = d.Color(60, 30, 0)
red = d.Color(150,0,0)
green = d.Color(0, 125, 0)

# Resolution
maxwidth = 15360
maxheight = 8640
downscale = 8
scaledwidth, scaledheight = maxwidth/downscale, maxheight/downscale
quitwidth = 104/downscale

# Graphics
d.init()
window = d.display.set_mode((scaledwidth, scaledheight), d.FULLSCREEN | d.SCALED | d.NOFRAME)
board = d.surface.Surface((800,800))
icon = d.image.load("Assets/Graphics/WindowIconGrey.png").convert_alpha()  
settingsicon = d.image.load("Assets/Graphics/settings.png").convert_alpha() 
settingsicon = d.transform.scale(settingsicon,(80,80))
reverseicon = d.image.load("Assets/Graphics/reverse.png").convert_alpha() 
reverseicon = d.transform.scale(reverseicon,(80,80))
quiticon = d.image.load("Assets/Graphics/quit.png").convert_alpha() 
quiticon = d.transform.scale(quiticon,(quitwidth, quitwidth))
hideicon = d.image.load("Assets/Graphics/minimize.png").convert_alpha() 
hideicon = d.transform.scale(hideicon,(quitwidth, quitwidth/5))
wasted = d.image.load("Assets/Graphics/wasted.png").convert_alpha() 
wasted = d.transform.scale(wasted,(100,100))
settings_yes = d.image.load("Assets/Graphics/settings_yes.png").convert_alpha()
settings_no = d.image.load("Assets/Graphics/settings_no.png").convert_alpha()
dropdown_isclosed = d.image.load("Assets/Graphics/dropdown_isclosed.png").convert_alpha()
dropdown_isopen = d.image.load("Assets/Graphics/dropdown_isopen.png").convert_alpha()
confirm_closing = d.image.load("Assets/Graphics/confirm_closing.png").convert_alpha()
confirm_closing_cancel = d.image.load("Assets/Graphics/confirm_closing_cancel.png").convert_alpha()
confirm_closing_close = d.image.load("Assets/Graphics/confirm_closing_close.png").convert_alpha()

for x in ["bp", "wP", "bn", "wN", "bb", "wB", "br", "wR", "bq", "wQ", "bk", "wK"]:
	globals()[x[1]] = d.image.load(path.join('Assets', 'Pieces', x+'.png')).convert_alpha()     # { "JohnPablok's improved Cburnett chess set" on opengameart.org
pxy = Pxy = (23,18)
nxy = Nxy = (21,18)
bxy = Bxy = kxy = Kxy = (18,18)
rxy = Rxy = (20,18)
qxy = Qxy = (15,18)

# Local
bglist = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]
all_pieces = [["P","N","B","R","Q","K"], ["p","n","b","r","q","k"]]
dragged = False
isfinished = False
colored = False
isdropped = False
possible_squares = []
list = []
game_positions = []
arrows_list = []
startartsquare = []
buttons = 0
startsquarex = 0
startsquarey = 0
wastedking = False
testsquarex = 0
testsquarey = 0
piece = "A"
start_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
clock = d.time.Clock()
isflipped = False

# Settings
selectedtab = [0, -1]
selecteddropdown = ""
currentdropdowntop = 0
chosendropdownoption = -1
fonts = [d.font.SysFont('cambria', 20), d.font.SysFont('cambria', 25), d.font.SysFont('cambria', 30)]
dropdowns = { 
	"default_settings_tab": ['General', 'Shortcuts', 'Display', 'Customise', '………', 'Contact/Feedback', 'Latest'],
}

default_settings_info = [ # Order settings here
	[       # Tab 1
        ["show_shortcuts", "Show shortcut when hovering", "YN", True],
        ["default_settings_tab", "Default Settings Tab", "DD", 'Latest'],
        ["validate_before_closing", "Confirm when exiting", "YN", True],
        ["say_goodbye", "Get a goodbye message", "YN", False]
    ],  
    [       # Tab 2

    ],  
    [       # Tab 3

    ],
    [       # Tab 4
	    ["show_possible_squares", "Show possible squares", "YN", True]
    ],
    [       # Tab 5
    
    ],
    [       # Tab 6
    
    ]

] 

usesavedsettings = False
try:
	if usesavedsettings:
		pass # get data
	else:
		settings_info = default_settings_info
except:
	settings_info = default_settings_info # ?
	raise "Error while getting data ; default settings restored"

# Launching
display = "game"
running = False



# FUNCTIONS


# General

def draw_frame():
	global running
	global window
	global buttons
	global display
	clicked = buttons[0]==False and d.mouse.get_pressed(5)[0]==True
	if (event.type == d.KEYDOWN and event.key == d.K_ESCAPE and d.key.get_mods() in [4097, 4098] ) or (d.mouse.get_pos()[1]<=33 and d.mouse.get_pos()[0]>=scaledwidth-65 and clicked) or (displaying == "menu" and event.type == d.KEYDOWN and (event.key == d.K_ESCAPE or event.key == d.K_BACKSPACE)):
		if settings_info[0][2][3]==True:
			display = displaying
			d.draw.rect(window, grey, (scaledwidth-65, 0, 65, 33))
			d.draw.rect(window, grey, (scaledwidth-130, 0, 65, 33))
			window.blit(hideicon, (scaledwidth-quitwidth*8,15))
			window.blit(quiticon, (scaledwidth-quitwidth*3,10))
			windowcopy = window.copy()
			
			drawconfirmbox(windowcopy)
			clicked = False
		else:
			running = False
	window.fill(grey)
	d.draw.rect(window, grey, (scaledwidth-65, 0, 65, 33))
	d.draw.rect(window, grey, (scaledwidth-130, 0, 65, 33))
	if d.mouse.get_pos()[1]<=33 and d.mouse.get_pos()[0]>=scaledwidth-65:
		d.draw.rect(window, red, (scaledwidth-65, 0, 65, 33))
		if settings_info[0][0][3]==True:
			pass
	else:
		if d.mouse.get_pos()[1]<=33 and scaledwidth-65>=d.mouse.get_pos()[0]>=scaledwidth-130:
			d.draw.rect(window, lightgrey, (scaledwidth-130, 0, 65, 33))
			if clicked:
				d.display.iconify()

	window.blit(hideicon, (scaledwidth-quitwidth*8,15))
	window.blit(quiticon, (scaledwidth-quitwidth*3,10))
	
	

def drawconfirmbox(bgimg):
	global buttons
	global running
	global event

	buttons = d.mouse.get_pressed(5)
	validatingclosing = True
	gfxd.box(bgimg, (0, 0, scaledwidth, scaledheight), (0, 0, 0, 100))

	window.blit(bgimg, (0, 0))
	window.blit(confirm_closing, (803, 356))

	if d.mouse.get_pos()[1]<=33 and d.mouse.get_pos()[0]>=scaledwidth-65:
		d.draw.rect(window, red, (scaledwidth-65, 0, 65, 33))
	elif d.mouse.get_pos()[1]<=33 and scaledwidth-65>=d.mouse.get_pos()[0]>=scaledwidth-130:
		d.draw.rect(window, lightgrey, (scaledwidth-130, 0, 65, 33))

	window.blit(quiticon, (scaledwidth-quitwidth*3,10))
	window.blit(hideicon, (scaledwidth-quitwidth*8,15))

	d.display.update()

	while running and validatingclosing:
		for event in d.event.get():

			mousex, mousey = d.mouse.get_pos()
			clicked = buttons[0]==False and d.mouse.get_pressed(5)[0]==True
			window.blit(bgimg, (0, 0))

			if event.type == d.QUIT or (event.type == d.KEYDOWN and (event.key == d.K_KP_ENTER or event.key == d.K_RETURN)):
				running = False

			elif event.type == d.KEYDOWN and (event.key == d.K_ESCAPE or event.key == d.K_BACKSPACE):
				validatingclosing = False

			elif (mousey<=33 and mousex>=scaledwidth-65):
				d.draw.rect(window, red, (scaledwidth-65, 0, 65, 33))
				if clicked:
					running = False

			elif mousey<=33 and scaledwidth-65>=mousex>=scaledwidth-130:
				d.draw.rect(window, lightgrey, (scaledwidth-130, 0, 65, 33))
				if clicked:
					d.display.iconify()
			
			elif clicked and not (803<=mousex<=1118 and 356<=mousey<=540):
				validatingclosing = False

			window.blit(hideicon, (scaledwidth-quitwidth*8,15))
			window.blit(quiticon, (scaledwidth-quitwidth*3,10))
			if 450<=mousey<=500:
				if 833<=mousex<=945:
					window.blit(confirm_closing_cancel, (803, 356))
					if clicked:
						validatingclosing = False
				elif 975<=mousex<=1088:
					window.blit(confirm_closing_close, (803, 356))
					if clicked:
						running = False
				else:
					window.blit(confirm_closing, (803, 356))
			else:
				window.blit(confirm_closing, (803, 356))

			d.display.update()
			buttons = d.mouse.get_pressed(5)
		clock.tick(60)

# Board

def str_to_list(FEN_string):
	"""Turns the FEN string given into a list of 8 lists with each a length of 8, representing the chessboard"""
	FEN_list = FEN_string.split(" ")
	position_list = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,[0,0],[0,0],[0,0],0], [[0,0],[0,0]], [0,0]]
	position_listx = 0
	position_listy = 0
	numbers = ["1","2","3","4","5","6","7","8"]
	for x in FEN_list[0]:
		if (x) == "/":
			position_listx=0
			position_listy+=1
		elif any(x==n for n in numbers):
			x=int(x)
			position_listx+=x
		else:
			position_list[position_listy][position_listx] = x
			position_listx+=1
	if FEN_list[1] == "w":
		position_list[8][0] = 0
	elif FEN_list[1] == "b":
		position_list[8][0] = 1
	if "K" in FEN_list[2]:
		position_list[8][1][0]=1
	if "Q" in FEN_list[2]:
		position_list[8][1][1]=1
	if "k" in FEN_list[2]:
		position_list[8][2][0]=1
	if "q" in FEN_list[2]:
		position_list[8][2][1]=1
	globals()["game_positions"].append(copy.deepcopy([position_list[:8], position_list[8][0]%2, position_list[8][1:4], 1]))
	return position_list

def draw_board(list, possibilities=[], kingmoving = False, startsquarey=-17, startsquarex=-1):
	global dragged
	global arrows_list
	if not isflipped:
		for y in range(8):
			for x in range(8):
				if (x+y)%2==1:
					d.draw.rect(window, dark, (x*100+560, y*100+140, 100, 100))
				else:
					d.draw.rect(window, light, (x*100+560, y*100+140, 100, 100))
		kingsquareyx = king_coor(list) if not kingmoving else [startsquarey,startsquarex]
		if ischeck(list, kingsquareyx[0], kingsquareyx[1], list[8][0]%2):
			d.draw.rect(window, red, (kingsquareyx[1]*100+560, kingsquareyx[0]*100+140, 100, 100))
			if not isfinished:
				if (kingsquareyx[1]+kingsquareyx[0])%2==1:
					d.draw.circle(window, dark, (kingsquareyx[1]*100+610, kingsquareyx[0]*100+190), 50)
				else:
					d.draw.circle(window, light, (kingsquareyx[1]*100+610, kingsquareyx[0]*100+190), 50)
		if list[8][0]>=1:
			for c in list[9]:
				if (c[0]+c[1])%2==1:
					d.draw.rect(window, darkorange, (c[1]*100+560, c[0]*100+140, 100, 100))
				else:
					d.draw.rect(window, lightorange, (c[1]*100+560, c[0]*100+140, 100, 100))
		for y in range(8):
			for x in range(8):
				if globals()["bglist"][y][x]==1:
					if (x+y)%2==1:
						d.draw.rect(window, darkblue, (x*100+560, y*100+140, 100, 100))
					else:
						d.draw.rect(window, lightblue, (x*100+560, y*100+140, 100, 100))
		for y in range(8):
			for x in range(8):
				if list[y][x]!=0:
					window.blit(globals()[list[y][x]], (100*x+560+globals()[list[y][x]+"xy"][0],100*y+140+globals()[list[y][x]+"xy"][1]))
		for p in possibilities:
			gfxd.filled_circle(window, 100*p[1]+608,100*p[0]+188, 15, (50,50,50,100))
		if arrows_list!=[]:
			for tuuuple in arrows_list:
				xdiff = tuuuple[2]-tuuuple[0]
				ydiff = tuuuple[3]-tuuuple[1]
				if not (xdiff==0 and ydiff==0):
					if xdiff==0:
						if ydiff>0:
							gfxd.filled_polygon(window, ((100*tuuuple[0]+598,100*tuuuple[1]+228),(100*tuuuple[0]+618,100*tuuuple[1]+228),(100*tuuuple[2]+618,100*tuuuple[3]+148),(100*tuuuple[2]+628,100*tuuuple[3]+148),(100*tuuuple[2]+608,100*tuuuple[3]+178),(100*tuuuple[2]+588,100*tuuuple[3]+148),(100*tuuuple[2]+598,100*tuuuple[3]+148)), (0,100,0,150))
						else:
							gfxd.filled_polygon(window, ((100*tuuuple[0]+598,100*tuuuple[1]+148),(100*tuuuple[0]+618,100*tuuuple[1]+148),(100*tuuuple[2]+618,100*tuuuple[3]+228),(100*tuuuple[2]+628,100*tuuuple[3]+228),(100*tuuuple[2]+608,100*tuuuple[3]+198),(100*tuuuple[2]+588,100*tuuuple[3]+228),(100*tuuuple[2]+598,100*tuuuple[3]+228)), (0,100,0,150))
					elif ydiff==0:
						if xdiff>0:
							gfxd.filled_polygon(window, ((100*tuuuple[0]+648,100*tuuuple[1]+198),(100*tuuuple[0]+648,100*tuuuple[1]+178),(100*tuuuple[2]+568,100*tuuuple[3]+178),(100*tuuuple[2]+568,100*tuuuple[3]+168),(100*tuuuple[2]+598,100*tuuuple[3]+188),(100*tuuuple[2]+568,100*tuuuple[3]+208),(100*tuuuple[2]+568,100*tuuuple[3]+198)), (0,100,0,150))
						else:
							gfxd.filled_polygon(window, ((100*tuuuple[0]+568,100*tuuuple[1]+198),(100*tuuuple[0]+568,100*tuuuple[1]+178),(100*tuuuple[2]+648,100*tuuuple[3]+178),(100*tuuuple[2]+648,100*tuuuple[3]+208),(100*tuuuple[2]+618,100*tuuuple[3]+188),(100*tuuuple[2]+648,100*tuuuple[3]+168),(100*tuuuple[2]+648,100*tuuuple[3]+198)), (0,100,0,150))
					else:
						sine = sin(atan(ydiff/xdiff))
						ypixels = 10*sine
						xpixels = 10*sqrt(1-sine**2)
						if xdiff>0:
							gfxd.filled_polygon(window, ((100*tuuuple[0]+608+ypixels+4*xpixels,100*tuuuple[1]+188-xpixels+4*ypixels),(100*tuuuple[0]+608-ypixels+4*xpixels,100*tuuuple[1]+188+xpixels+4*ypixels),(100*tuuuple[2]+608-ypixels-4*xpixels,100*tuuuple[3]+188+xpixels-4*ypixels),(100*tuuuple[2]+608-2*ypixels-4*xpixels,100*tuuuple[3]+188+2*xpixels-4*ypixels),(100*tuuuple[2]+608-xpixels,100*tuuuple[3]+188-ypixels),(100*tuuuple[2]+608+2*ypixels-4*xpixels,100*tuuuple[3]+188-2*xpixels-4*ypixels),(100*tuuuple[2]+608+ypixels-4*xpixels,100*tuuuple[3]+188-xpixels-4*ypixels)), (0,100,0,150))
						elif xdiff<0:
							gfxd.filled_polygon(window, ((100*tuuuple[0]+608+ypixels-4*xpixels,100*tuuuple[1]+188-xpixels-4*ypixels),(100*tuuuple[0]+608-ypixels-4*xpixels,100*tuuuple[1]+188+xpixels-4*ypixels),(100*tuuuple[2]+608-ypixels+4*xpixels,100*tuuuple[3]+188+xpixels+4*ypixels),(100*tuuuple[2]+608+2*ypixels+4*xpixels,100*tuuuple[3]+188-2*xpixels+4*ypixels),(100*tuuuple[2]+608+xpixels,100*tuuuple[3]+188+ypixels),(100*tuuuple[2]+608-2*ypixels+4*xpixels,100*tuuuple[3]+188+2*xpixels+4*ypixels),(100*tuuuple[2]+608+ypixels+4*xpixels,100*tuuuple[3]+188-xpixels+4*ypixels)), (0,100,0,150))
		window.blit(settingsicon,(1370,150))
		window.blit(reverseicon,(1370,250))		
		if dragged:
			blit_on_cursor(piece)
		if wastedking:
			window.blit(wasted, (560+100*list[10][0], 140+100*list[10][1]))
	elif isflipped:
		for y in range(8):
			for x in range(8):
				if (x+y)%2==1:
					d.draw.rect(window, dark, (1260-x*100, 840-y*100, 100, 100))
				else:
					d.draw.rect(window, light, (1260-x*100, 840-y*100, 100, 100))
		kingsquareyx = king_coor(list) if not kingmoving else [startsquarey,startsquarex]
		if ischeck(list, kingsquareyx[0], kingsquareyx[1], list[8][0]%2):
			d.draw.rect(window, red, (1260-kingsquareyx[1]*100, 840-kingsquareyx[0]*100, 100, 100))
			if not isfinished:
				if (kingsquareyx[1]+kingsquareyx[0])%2==1:
					d.draw.circle(window, dark, (1310-kingsquareyx[1]*100, 890-kingsquareyx[0]*100), 50)
				else:
					d.draw.circle(window, light, (1310-kingsquareyx[1]*100, 890-kingsquareyx[0]*100), 50)
		if list[8][0]>=1:
			for c in list[9]:
				if (c[0]+c[1])%2==1:
					d.draw.rect(window, darkorange, (1260-c[1]*100, 840-c[0]*100, 100, 100))
				else:
					d.draw.rect(window, lightorange, (1260-c[1]*100, 840-c[0]*100, 100, 100))
		for y in range(8):
			for x in range(8):
				if globals()["bglist"][y][x]==1:
					if (x+y)%2==1:
						d.draw.rect(window, darkblue, (1260-x*100, 840-y*100, 100, 100))
					else:
						d.draw.rect(window, lightblue, (1260-x*100, 840-y*100, 100, 100))
		for y in range(8):
			for x in range(8):
				if list[y][x]!=0:
					window.blit(globals()[list[y][x]], (1260-100*x+globals()[list[y][x]+"xy"][0],840-100*y+globals()[list[y][x]+"xy"][1]))
		for p in possibilities:
			gfxd.filled_circle(window, 1308-100*p[1],888-100*p[0], 15, (50,50,50,100))
		if arrows_list!=[]:
			for tuuuple in arrows_list:
				xdiff = tuuuple[2]-tuuuple[0]
				ydiff = tuuuple[3]-tuuuple[1]
				if not (xdiff==0 and ydiff==0):
					if xdiff==0:
						if ydiff>0:
							gfxd.filled_polygon(window, ((1318-100*tuuuple[0],848-100*tuuuple[1]),(1298-100*tuuuple[0],848-100*tuuuple[1]),(1298-100*tuuuple[2],928-100*tuuuple[3]),(1288-100*tuuuple[2],928-100*tuuuple[3]),(1308-100*tuuuple[2],898-100*tuuuple[3]),(1328-100*tuuuple[2],928-100*tuuuple[3]),(1318-100*tuuuple[2],928-100*tuuuple[3])), (0,100,0,150))
						else:
							gfxd.filled_polygon(window, ((1298-100*tuuuple[0],928-100*tuuuple[1]),(1318-100*tuuuple[0],928-100*tuuuple[1]),(1318-100*tuuuple[2],848-100*tuuuple[3]),(1328-100*tuuuple[2],848-100*tuuuple[3]),(1308-100*tuuuple[2],878-100*tuuuple[3]),(1288-100*tuuuple[2],848-100*tuuuple[3]),(1298-100*tuuuple[2],848-100*tuuuple[3])), (0,100,0,150))
					elif ydiff==0:
						if xdiff>0:
							gfxd.filled_polygon(window, ((1268-100*tuuuple[0],878-100*tuuuple[1]),(1268-100*tuuuple[0],898-100*tuuuple[1]),(1348-100*tuuuple[2],898-100*tuuuple[3]),(1348-100*tuuuple[2],908-100*tuuuple[3]),(1318-100*tuuuple[2],888-100*tuuuple[3]),(1348-100*tuuuple[2],868-100*tuuuple[3]),(1348-100*tuuuple[2],878-100*tuuuple[3])), (0,100,0,150))
						else:
							gfxd.filled_polygon(window, ((1348-100*tuuuple[0],878-100*tuuuple[1]),(1348-100*tuuuple[0],898-100*tuuuple[1]),(1268-100*tuuuple[2],898-100*tuuuple[3]),(1268-100*tuuuple[2],868-100*tuuuple[3]),(1298-100*tuuuple[2],888-100*tuuuple[3]),(1268-100*tuuuple[2],908-100*tuuuple[3]),(1268-100*tuuuple[2],878-100*tuuuple[3])), (0,100,0,150))
					else:
						sine = sin(atan(ydiff/xdiff))
						ypixels = 10*sine
						xpixels = 10*sqrt(1-sine**2)
						if xdiff>0:
							gfxd.filled_polygon(window, ((1308-100*tuuuple[0]-ypixels-4*xpixels,888-100*tuuuple[1]+xpixels-4*ypixels),(1308-100*tuuuple[0]+ypixels-4*xpixels,888-100*tuuuple[1]-xpixels-4*ypixels),(1308-100*tuuuple[2]+ypixels+4*xpixels,888-100*tuuuple[3]-xpixels+4*ypixels),(1308-100*tuuuple[2]+2*ypixels+4*xpixels,888-100*tuuuple[3]-2*xpixels+4*ypixels),(1308-100*tuuuple[2]+xpixels,888-100*tuuuple[3]+ypixels),(1308-100*tuuuple[2]-2*ypixels+4*xpixels,888-100*tuuuple[3]+2*xpixels+4*ypixels),(1308-100*tuuuple[2]-ypixels+4*xpixels,888-100*tuuuple[3]+xpixels+4*ypixels)), (0,100,0,150))
						elif xdiff<0:
							gfxd.filled_polygon(window, ((1308-100*tuuuple[0]-ypixels+4*xpixels,888-100*tuuuple[1]+xpixels+4*ypixels),(1308-100*tuuuple[0]+ypixels+4*xpixels,888-100*tuuuple[1]-xpixels+4*ypixels),(1308-100*tuuuple[2]+ypixels-4*xpixels,888-100*tuuuple[3]-xpixels-4*ypixels),(1308-100*tuuuple[2]-2*ypixels-4*xpixels,888-100*tuuuple[3]+2*xpixels-4*ypixels),(1308-100*tuuuple[2]-xpixels,888-100*tuuuple[3]-ypixels),(1308-100*tuuuple[2]+2*ypixels-4*xpixels,888-100*tuuuple[3]-2*xpixels-4*ypixels),(1308-100*tuuuple[2]-ypixels-4*xpixels,888-100*tuuuple[3]+xpixels-4*ypixels)), (0,100,0,150))
		window.blit(settingsicon,(1370,150))
		window.blit(reverseicon,(1370,250))		
		if dragged:
			blit_on_cursor(piece)
		if wastedking:
			window.blit(wasted, (1260-100*list[10][0], 840-100*list[10][1]))
	else:
		print("Flipping Error")
		d.quit()

def blit_on_cursor(piece):
	coordinates = (d.mouse.get_pos()[0]-((100-2*globals()[piece+"xy"][0])/2-2), d.mouse.get_pos()[1]-((100-2*globals()[piece+"xy"][1])//2-2))
	window.blit(globals()[piece], coordinates)

def bgcolors(squarex, squarey):
	if globals()["bglist"][squarey][squarex]==0:
		if (squarex+squarey)%2==1:
			d.draw.rect(window, darkblue, (squarex*100+560, squarey*100+140, 100, 100))
		else:
			d.draw.rect(window, lightblue, (squarex*100+560, squarey*100+140, 100, 100))
		globals()["bglist"][squarey][squarex]=1
	elif globals()["bglist"][squarey][squarex]==1:
		if (squarex+squarey)%2==1:
			d.draw.rect(window, dark, (squarex*100+560, squarey*100+140, 100, 100))
		else:
			d.draw.rect(window, light, (squarex*100+560, squarey*100+140, 100, 100))
		globals()["bglist"][squarey][squarex]=0

def draw_arrow(artsquarey, artsquarex, squarey, squarex): 
	global colored
	global list
	global arrows_list
	global startartsquare
	global isdropped
	if isdropped and arrows_list!=[]:
		if arrows_list.count((startartsquare[1], startartsquare[0], squarex, squarey))>=2:
			arrows_list.remove((startartsquare[1], startartsquare[0], squarex, squarey))
			arrows_list.remove((startartsquare[1], startartsquare[0], squarex, squarey))
		draw_board(list)
		if [startartsquare[1], startartsquare[0]] == [squarex, squarey]:
			if list[squarey][squarex]!=0:
				window.blit(globals()[list[squarey][squarex]], (100*squarex+560+globals()[list[squarey][squarex]+"xy"][0],100*squarey+140+globals()[list[squarey][squarex]+"xy"][1]))
	if [artsquarey, artsquarex] != [squarey, squarex]:
		if not colored:
			bgcolors(artsquarex, artsquarey)
			colored = True
		if arrows_list!=[]:
			if arrows_list[-1]==(startartsquare[1], startartsquare[0], artsquarex, artsquarey):
				arrows_list.pop(-1)
		arrows_list.append((startartsquare[1], startartsquare[0], squarex, squarey))
		draw_board(list)

def possible_squares(list,piece,squarey,squarex):
	possible_squares = [] 

	if piece == "P":
		if list[squarey-1][squarex]==0:
			possible_squares.append([squarey-1,squarex])
			if squarey == 6:
				if list[4][squarex]==0:
					possible_squares.append([4,squarex])
		if squarex>=1:
			if list[squarey-1][squarex-1] in all_pieces[1]:
				possible_squares.append([squarey-1,squarex-1])
		if squarex<=6:
			if list[squarey-1][squarex+1] in all_pieces[1]:
				possible_squares.append([squarey-1,squarex+1])
		if list[8][3][0] ==squarey and (list[8][3][1] ==squarex-1 or list[8][3][1] ==squarex+1):
			possible_squares.append([list[8][3][0]-1, list[8][3][1]])
	elif piece == "p":
		if list[squarey+1][squarex]==0:
			possible_squares.append([squarey+1,squarex])
			if squarey == 1:
				if list[3][squarex]==0:
					possible_squares.append([3,squarex])
		if squarex>=1:
			if list[squarey+1][squarex-1] in all_pieces[0]:
				possible_squares.append([squarey+1,squarex-1])
		if squarex<=6:
			if list[squarey+1][squarex+1] in all_pieces[0]:
				possible_squares.append([squarey+1,squarex+1])
		if list[8][3][0] ==squarey and (list[8][3][1] ==squarex-1 or list[8][3][1] ==squarex+1):
			possible_squares.append([list[8][3][0]+1, list[8][3][1]])

	elif piece == "N" or piece == "n":
		conditions = ["squarex>=1 and squarey>=2", "squarex>=2 and squarey>=1", "squarex>=2 and squarey<=6", "squarex>=1 and squarey<=5", "squarex<=6 and squarey<=5", "squarex<=5 and squarey<=6", "squarex<=5 and squarey>=1", "squarex<=6 and squarey>=2"]
		verify_squares = [[squarey-2, squarex-1], [squarey-1, squarex-2], [squarey+1, squarex-2], [squarey+2, squarex-1], [squarey+2, squarex+1], [squarey+1, squarex+2], [squarey-1, squarex+2], [squarey-2, squarex+1]]
		for i in range(8):
			if eval(conditions[i]):
				if list[verify_squares[i][0]][verify_squares[i][1]] not in all_pieces[list[8][0]%2]:
					possible_squares.append([verify_squares[i][0], verify_squares[i][1]])

	elif piece == "B" or piece == "b":
		squareyop = ["testsquarey+1", "testsquarey+1", "testsquarey-1", "testsquarey-1"]
		squarexop = ["testsquarex+1", "testsquarex-1", "testsquarex+1", "testsquarex-1"]
		for i, j in zip(squareyop, squarexop):
			testsquarex, testsquarey = squarex, squarey
			keepon = True
			while keepon:
				testsquarey, testsquarex = eval(i), eval(j)
				if testsquarex<=7 and testsquarex>=0 and testsquarey<=7 and testsquarey>=0 and list[testsquarey][testsquarex] not in all_pieces[list[8][0]%2]:
					possible_squares.append([testsquarey, testsquarex])
					if list[testsquarey][testsquarex] in all_pieces[(list[8][0]+1)%2]:
						keepon = False
				else:
					keepon = False
	
	elif piece == "R" or piece == "r":
		squareyop = ["testsquarey+1", "testsquarey", "testsquarey", "testsquarey-1"]
		squarexop = ["testsquarex", "testsquarex-1", "testsquarex+1", "testsquarex"]
		for i, j in zip(squareyop, squarexop):
			testsquarex, testsquarey = squarex, squarey
			keepon = True
			while keepon:
				testsquarey, testsquarex = eval(i), eval(j)
				if testsquarex<=7 and testsquarex>=0 and testsquarey<=7 and testsquarey>=0 and list[testsquarey][testsquarex] not in all_pieces[list[8][0]%2]:
					possible_squares.append([testsquarey, testsquarex])
					if list[testsquarey][testsquarex] in all_pieces[(list[8][0]+1)%2]:
						keepon = False
				else:
					keepon = False
			else:
				keepon = False

	elif piece == "Q" or piece == "q":
		squareyop = ["testsquarey+1", "testsquarey+1", "testsquarey-1", "testsquarey-1", "testsquarey+1", "testsquarey", "testsquarey", "testsquarey-1"]
		squarexop = ["testsquarex+1", "testsquarex-1", "testsquarex+1", "testsquarex-1", "testsquarex", "testsquarex-1", "testsquarex+1", "testsquarex"]
		for i, j in zip(squareyop, squarexop):
			testsquarex, testsquarey = squarex, squarey
			keepon = True
			while keepon:
				testsquarey, testsquarex = eval(i), eval(j)
				if testsquarex<=7 and testsquarex>=0 and testsquarey<=7 and testsquarey>=0 and list[testsquarey][testsquarex] not in all_pieces[list[8][0]%2]:
					possible_squares.append([testsquarey, testsquarex])
					if list[testsquarey][testsquarex] in all_pieces[(list[8][0]+1)%2]:
						keepon = False
				else:
					keepon = False
	
	elif piece == "K" or piece == "k":
		squareyop = ["squarey+1", "squarey+1", "squarey-1", "squarey-1", "squarey+1", "squarey", "squarey", "squarey-1"]
		squarexop = ["squarex+1", "squarex-1", "squarex+1", "squarex-1", "squarex", "squarex-1", "squarex+1", "squarex"]
		for i, j in zip(squareyop, squarexop):
			testsquarey, testsquarex = eval(i), eval(j)
			if testsquarex<=7 and testsquarex>=0 and testsquarey<=7 and testsquarey>=0 and list[testsquarey][testsquarex] not in all_pieces[list[8][0]%2]:
				possible_squares.append([testsquarey, testsquarex])
		if piece == "K":
			if list[8][1][0]==1 and list[7][5]==0 and list[7][6]==0 and not (ischeck(list, 7, 4, 0) or ischeck(list, 7, 5, 0) or ischeck(list, 7, 6, 0)):
				possible_squares.append([squarey, squarex+2])
			if list[8][1][1]==1 and list[7][3]==0 and list[7][2]==0 and list[7][1]==0 and not (ischeck(list, 7, 4, 0) or ischeck(list, 7, 3, 0) or ischeck(list, 7, 2, 0)):
				possible_squares.append([squarey, squarex-2])
		if piece == "k":
			if list[8][2][0]==1 and list[0][5]==0 and list[0][6]==0 and not (ischeck(list, 0, 4, 1) or ischeck(list, 0, 5, 1) or ischeck(list, 0, 6, 1)):
				possible_squares.append([squarey, squarex+2])
			if list[8][2][1]==1 and list[0][3]==0 and list[0][2]==0 and list[0][1]==0 and not (ischeck(list, 0, 4, 1) or ischeck(list, 0, 3, 1) or ischeck(list, 0, 2, 1)):
				possible_squares.append([squarey, squarex-2])
	
	for coor in reversed(possible_squares):
		savecoor = list[coor[0]][coor[1]]
		list[squarey][squarex]=0
		list[coor[0]][coor[1]]=piece
		if ischeck(list, king_coor(list)[0], king_coor(list)[1], list[8][0]%2):
			possible_squares.remove(coor)
		list[squarey][squarex]=piece
		list[coor[0]][coor[1]]=savecoor
	return possible_squares

def king_coor(list): # place of the king which color has to play
	if list[8][0]%2==0:
		king="K"
	else:
		king="k"
	for y in range(8):
		for x in range(8):
			if list[y][x]==king:
				return y, x

def ischeck(list, squarey, squarex, squaredefender):
	ischeck = False
	conditions = ["squarex>=1 and squarey>=2", "squarex>=2 and squarey>=1", "squarex>=2 and squarey<=6", "squarex>=1 and squarey<=5", "squarex<=6 and squarey<=5", "squarex<=5 and squarey<=6", "squarex<=5 and squarey>=1", "squarex<=6 and squarey>=2"]
	verify_squares = [[squarey-2, squarex-1], [squarey-1, squarex-2], [squarey+1, squarex-2], [squarey+2, squarex-1], [squarey+2, squarex+1], [squarey+1, squarex+2], [squarey-1, squarex+2], [squarey-2, squarex+1]]
	for i in range(8):
		if eval(conditions[i]):
			if list[verify_squares[i][0]][verify_squares[i][1]] == all_pieces[(squaredefender+1)%2][1]:
				ischeck = True
	if ischeck==False:
		ways=0
		squareyop = ["testsquarey+1", "testsquarey+1", "testsquarey-1", "testsquarey-1", "testsquarey+1", "testsquarey", "testsquarey", "testsquarey-1"]
		squarexop = ["testsquarex+1", "testsquarex-1", "testsquarex+1", "testsquarex-1", "testsquarex", "testsquarex-1", "testsquarex+1", "testsquarex"]
		for i, j in zip(squareyop, squarexop):
			testsquarex, testsquarey = squarex, squarey
			keepon = True
			while keepon and ischeck==False:
				testsquarey, testsquarex = eval(i), eval(j)
				if testsquarex<=7 and testsquarex>=0 and testsquarey<=7 and testsquarey>=0:
					if list[testsquarey][testsquarex] in all_pieces[squaredefender]:
						keepon = False
					elif list[testsquarey][testsquarex] in all_pieces[(squaredefender+1)%2]:
						keepon = False
						if ways<=3:
							if list[testsquarey][testsquarex]==all_pieces[(squaredefender+1)%2][4] or list[testsquarey][testsquarex]==all_pieces[(squaredefender+1)%2][2]:
								ischeck = True
						else:
							if list[testsquarey][testsquarex]==all_pieces[(squaredefender+1)%2][4] or list[testsquarey][testsquarex]==all_pieces[(squaredefender+1)%2][3]:
								ischeck = True
				else:
					keepon = False
			ways+=1
		if ischeck == False:
			squareyop = ["squarey+1", "squarey+1", "squarey-1", "squarey-1", "squarey+1", "squarey", "squarey", "squarey-1"]
			squarexop = ["squarex+1", "squarex-1", "squarex+1", "squarex-1", "squarex", "squarex-1", "squarex+1", "squarex"]
			for i, j in zip(squareyop, squarexop):
				testsquarey, testsquarex = eval(i), eval(j)
				if testsquarex<=7 and testsquarex>=0 and testsquarey<=7 and testsquarey>=0 and list[testsquarey][testsquarex]==all_pieces[(squaredefender+1)%2][5]:
						ischeck = True
			if ischeck == False:
				if squaredefender==0:
					if squarey>=1:
						if squarex>=1:
							if list[squarey-1][squarex-1]=="p":
								ischeck = True
						if squarex<=6:
							if list[squarey-1][squarex+1]=="p":
								ischeck = True
				elif squaredefender==1:
					if squarey<=6:
						if squarex>=1:
							if list[squarey+1][squarex-1]=="P":
								ischeck = True
						if squarex<=6:
							if list[squarey+1][squarex+1]=="P":
								ischeck = True
	return ischeck

def aftermove(list, piece, squarey, squarex, startsquarey, startsquarex):
	global game_positions
	global isfinished
	global wastedking
	if list[squarey][squarex] in all_pieces[0] or list[squarey][squarex] in all_pieces[1]:
		game_positions=[game_positions[-1]]
	list[squarey][squarex] = piece
	if piece == "p" or piece == "P":
		game_positions=[game_positions[-1]]
		if (piece == "P" and squarey == list[8][3][0]-1 and squarex == list[8][3][1]) or (piece == "p" and squarey == list[8][3][0]+1 and squarex == list[8][3][1]):
			list[list[8][3][0]][list[8][3][1]] = 0
		if squarey == startsquarey-2 or squarey == startsquarey+2:
			list[8][3] = [squarey, squarex]
		else:
			list[8][3] = [-1, -1]
		if "P" in list[0]: 
			list[0][list[0].index("P")]="Q"
		elif "p" in list[7]:
			list[7][list[7].index("p")]="q"
	elif piece == "K":
		if squarey==7 and squarex ==6 and list[8][1][0]==1:
			list[7][7]=0
			list[7][5]="R"
		elif squarey==7 and squarex ==2 and list[8][1][1]==1:
			list[7][0]=0
			list[7][3]="R"
		list[8][1][0], list[8][1][1] = 0, 0
	elif piece == "k":
		if squarey==0 and squarex ==6 and list[8][2][0]==1:
			list[0][7]=0
			list[0][5]="r"
		elif squarey==0 and squarex ==2 and list[8][2][1]==1:
			list[0][0]=0
			list[0][3]="r"
		list[8][2][0], list[8][2][1] = 0, 0
	elif piece == "R" and (list[8][1][0]==1 or list[8][1][1]==1):
		if list[7][7]==0:
			list[8][1][0]=0
		if list[7][0]==0:
			list[8][1][1]=0
	elif piece == "r" and (list[8][2][0]==1 or list[8][2][1]==1):
		if list[0][7]==0:
			list[8][2][0]=0
		if list[0][0]==0:
			list[8][2][1]=0
	list[9] = [[startsquarey, startsquarex], [squarey, squarex]]
	addposition = True
	repetition_draw_transformed_list = [list[:8], list[8][0]%2, list[8][1:4], 1]
	for n in range(len(game_positions)):
		if repetition_draw_transformed_list[:3]==game_positions[n][:3]:
			addposition = False
			game_positions[n][3]+=1
			if game_positions[n][3]>=5:
				print("Draw : Repetition !")
				d.display.set_caption('No one\'s game')
				isfinished = True
			break
	if addposition:
		game_positions.append(copy.deepcopy(repetition_draw_transformed_list))
	list[8][0]+=1
	if not canmove(list, list[8][0]%2):
		if ischeck(list, king_coor(list)[0], king_coor(list)[1], list[8][0]%2):
			if list[8][0]%2==0:
				print("Black wins !")
				d.display.set_caption('Black\'s game')
				d.display.set_icon(d.image.load("Assets/Graphics/WindowIconBlack.png"))
				isfinished = True
			else:
				print("White wins !")
				d.display.set_caption('White\'s game')
				d.display.set_icon(d.image.load("Assets/Graphics/WindowIconWhite.png"))
				isfinished = True
			wastedking = True
			list[10][1], list[10][0] = king_coor(list)
		else:
			print("Draw : Stalemate !")
			d.display.set_caption('No one\'s game')
			isfinished = True
	if list[8][4]>=50:
		print("Draw : 50 moves rule !")
		d.display.set_caption('No one\'s game')
		isfinished = True

def canmove(list, whotoplay):
	for y in range(8):
		for x in range(8):
			if list[y][x] in all_pieces[whotoplay]:
				if possible_squares(list, list[y][x], y, x)!=[]:
					return True
	return False


# Menu

def drawmenu():
	pass


# Settings

def settings_yesno(yindex):
	val = settings_info[selectedtab[0]][yindex][3]
	if val==True:
		window.blit(settings_yes, (1250, 135+60*yindex))
	else:
		window.blit(settings_no, (1250, 135+60*yindex))

def settings_dropdown(yindex):

	val = settings_info[selectedtab[0]][yindex][3]
	id_dd = settings_info[selectedtab[0]][yindex][0]

	if selecteddropdown==id_dd:
		d.draw.rect(window, darkergrey, (1100, 128+60*yindex, 200, 35*len(dropdowns[id_dd])), 0, 5)
		window.blit(fonts[0].render(val, True, lightergrey), (1110,132+60*yindex))

		dropdownlist = dropdowns[id_dd][:]
		dropdownlist.remove(val)

		for i, j in enumerate(dropdownlist, 1):
			if chosendropdownoption==i-1:
				d.draw.rect(window, grey2, (1100, 128+60*yindex+35*(chosendropdownoption+1), 200, 35), 0, 5)
				window.blit(fonts[0].render(j, True, lightergrey), (1110,132+60*yindex+35*i))
			else:
				window.blit(fonts[0].render(j, True, lightgrey), (1110,132+60*yindex+35*i))

		window.blit(dropdown_isopen, (1275, 140+60*yindex))

	else:
		d.draw.rect(window, darkergrey, (1100, 128+60*yindex, 200, 35), 0, 5)
		window.blit(fonts[0].render(val, True, lightergrey), (1110,132+60*yindex))
		window.blit(dropdown_isclosed, (1275, 140+60*yindex))

def settings_numinput(yindex):
	pass

def settings_textinput(yindex):
	pass

def settings_picinput(yindex):
	pass

def settings_colorpicker(yindex):
	pass

def settings_disjunction(yindex, datatype):
	match datatype:
		case "YN": 
			settings_yesno(yindex)
		case "DD": 
			settings_dropdown(yindex)
		case "NI": 
			settings_numinput(yindex)
		case "TI": 
			settings_textinput(yindex)
		case "PI": 
			settings_picinput(yindex)
		case "CP": 
			settings_colorpicker(yindex)
		case "TT": 
			pass
		case _: 
			print("Wrong setting type")


# Diplays 

def initboard(FEN_string):
	"""Initializes board with a FEN string or a custom-format list from this file"""
	global list
	global isfinished
	global dragged
	global colored
	global arrows_list
	global isdropped
	global display
	global running
	global window
	global startartsquare
	global buttons
	global piece
	global startsquarex
	global startsquarey
	global isflipped
	global event
	if list==[]:
		if "/" in FEN_string:
			list = str_to_list(FEN_string)

		# Init (in launch() ?)
		window = d.display.set_mode((scaledwidth, scaledheight), d.FULLSCREEN | d.SCALED | d.NOFRAME)
	d.display.set_icon(icon)
	d.display.set_caption('Chess')
	d.event.post(d.event.Event(d.MOUSEMOTION))
	buttons = d.mouse.get_pressed(5)
	possibilities = []
	possibilitieson = False
	dragged = False
	drawing = False
	while running and display == "local":
		for event in d.event.get():

			if not isflipped:
				squarey=floor((d.mouse.get_pos()[1]-140)/100)
				squarex=floor((d.mouse.get_pos()[0]-560)/100)
			elif isflipped:
				squarey=floor((940-d.mouse.get_pos()[1])/100)
				squarex=floor((1360-d.mouse.get_pos()[0])/100)
			else:
				print("Flipping Error")
				d.quit()
			clicked = buttons[0]==False and d.mouse.get_pressed(5)[0]==True

			if event.type == d.QUIT:
				running = False
			
			elif event.type == d.KEYDOWN and (event.key == d.K_ESCAPE or event.key == d.K_BACKSPACE): # Save game before initting
				display = "menu" # TODO here
			
			elif (clicked and d.mouse.get_pos()[0]>1360 and d.mouse.get_pos()[0]<=1460 and d.mouse.get_pos()[1]>=140 and d.mouse.get_pos()[1]<=239) or (event.type == d.KEYDOWN and event.key == d.K_s):
				display = "settings"

			elif (clicked and d.mouse.get_pos()[0]>1360 and d.mouse.get_pos()[0]<=1460 and d.mouse.get_pos()[1]>=240 and d.mouse.get_pos()[1]<=339) or (event.type == d.KEYDOWN and event.key == d.K_f):
				if d.mouse.get_pos()[1]>240:
					isflipped= not isflipped

			elif clicked and d.mouse.get_pos()[0]>=560 and d.mouse.get_pos()[0]<=1360 and d.mouse.get_pos()[1]>=140 and d.mouse.get_pos()[1]<=940:
				arrows_list = []
				globals()["bglist"] = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]
				if possibilitieson and [squarey, squarex] in possibilities:
					if piece == "p" or piece == "P" or list[squarey][squarex] in all_pieces[0] or list[squarey][squarex] in all_pieces[0]:
						list[8][4]=0
					else:
						list[8][4]+=1
					list[startsquarey][startsquarex] = 0
					possibilities = []
					possibilitieson = False
					aftermove(list, piece, squarey, squarex, startsquarey, startsquarex)
				possibilities = []
				possibilitieson = False
				dragged = False
				drawing = False
				colored = False
				arrows_list = []
				if list[squarey][squarex] in all_pieces[list[8][0]%2]:
					startsquarey, startsquarex = squarey, squarex
					piece = list[squarey][squarex]
					if isfinished == False:
						possibilities = possible_squares(list,piece,squarey,squarex)
						possibilitieson = True
					list[squarey][squarex] = 0
					blit_on_cursor(piece)
					dragged = True
			
			elif event.type == d.MOUSEMOTION and dragged:
				blit_on_cursor(piece)

			elif d.mouse.get_pressed(5)[0]==False and dragged:
				if [squarey, squarex] in possibilities:
					if piece == "p" or piece == "P" or list[squarey][squarex] in all_pieces[0] or list[squarey][squarex] in all_pieces[0]:
						list[8][4]=0
					else:
						list[8][4]+=1
					possibilities = []
					possibilitieson = False
					aftermove(list, piece, squarey, squarex, startsquarey, startsquarex)
				else:
					list[startsquarey][startsquarex] = piece
				dragged = False

			elif d.mouse.get_pos()[0]>560 and d.mouse.get_pos()[0]<1360 and d.mouse.get_pos()[1]>140 and d.mouse.get_pos()[1]<940:
				if buttons[2]==False and d.mouse.get_pressed(5)[2]==True: 
					if dragged:
						list[startsquarey][startsquarex] = piece
						possibilities = []
						possibilitieson = False
					startartsquare = [squarey, squarex]
					dragged = False
					drawing = True
					colored = False
					artsquarey, artsquarex = squarey, squarex
					bgcolors(squarex, squarey)
				
				elif event.type == d.MOUSEMOTION and drawing:
					draw_arrow(artsquarey, artsquarex, squarey, squarex)

				elif drawing and d.mouse.get_pressed(5)[2]==False:
					isdropped = True
					draw_arrow(artsquarey, artsquarex, squarey, squarex)
					isdropped = False
					drawing = False

				artsquarey, artsquarex = squarey, squarex

			draw_frame()
			draw_board(list, possibilities if settings_info[3][0][3]==True else [], True if piece == "k" or piece == "K" else False, startsquarey, startsquarex)
			d.display.update()
			buttons = d.mouse.get_pressed(5)
		clock.tick(60)

def initmenu(): # opens when escape on chess game
	global window
	global running
	global display
	global buttons
	global event
	d.display.set_icon(icon) # TODO Change when HOME svg is done
	d.display.set_caption('Chess - Menu')
	d.event.post(d.event.Event(d.MOUSEMOTION))
	buttons = d.mouse.get_pressed(5)
	while running and display == "menu":

		for event in d.event.get():
			if event.type == d.QUIT:
				running = False

			elif event.type == d.KEYDOWN and event.key == d.K_s:
				display = "settings"
			 # if click on any interactive image -> init___

			draw_frame()
			d.display.update()
			buttons = d.mouse.get_pressed(5)
		clock.tick(60)

def initsettings(): # Miscellaneous : when op. settings, go to General/latest tab
	global window
	global running
	global display
	global buttons
	global selectedtab
	global settings_info
	global selecteddropdown
	global chosendropdownoption
	global currentdropdowntop
	global event
	d.display.set_icon(settingsicon)
	d.display.set_caption('Chess - Settings')
	if not settings_info[0][1][3]=='Latest':
		selectedtab[0]=dropdowns["default_settings_tab"].index(settings_info[0][1][3])
	activeitem=[]
	while running and display == "settings":
		for event in d.event.get():

			clicked = buttons[0]==False and d.mouse.get_pressed(5)[0]==True

			if event.type == d.QUIT or (event.type == d.KEYDOWN and event.key == d.K_BACKSPACE):
				running = False

			elif event.type == d.KEYDOWN and event.key == d.K_ESCAPE:
				display = "local"
			
			elif event.type == d.KEYDOWN and activeitem==[] and event.key in [d.K_1, d.K_2, d.K_3, d.K_4, d.K_5, d.K_6]:

				selectedtab[0] = event.key-49

			mousex, mousey = d.mouse.get_pos()
			draw_frame()
			d.draw.rect(window, darkgrey, (0,0,654,1080), 0, 0)
			d.draw.rect(window, lightgrey, (650,50,8,980), 0, 15)
			
			# Tabs
			if 350<=mousex<=650:
				if 100<=mousey<=400:
					for i in range(6):
						if 101+50*i<=mousey<=150+50*i:
							selectedtab[1] = i
							d.draw.rect(window, darkergrey, (360,100+50*i,280,50), 0, 13)
							if d.mouse.get_pressed(5)[0]==True and buttons[0]==False:
								selectedtab[0] = i

			window.blit(fonts[2].render(dropdowns["default_settings_tab"][selectedtab[0]], True, lightestergrey), (750,30))

			for i, j in enumerate(dropdowns["default_settings_tab"][:-1]):
				if selectedtab[0]==i:
					img = fonts[0].render(j, True, lightestergrey)
				elif selectedtab[1]==i:
					img = fonts[0].render(j, True, lightestgrey)
				else:
					img = fonts[0].render(j, True, lightergrey)
				window.blit(img, (380,110+50*i))
			selectedtab[1]=-1


			if selecteddropdown!="":
				indropdown = (1100<=mousex<=1300 and currentdropdowntop<=mousey<=currentdropdowntop+35*len(dropdowns[selecteddropdown]))
			else:
				indropdown = False

			# Active items variables
			chosendropdownoption = -1
			activeitem = []
			saveselecteddropdown = selecteddropdown

			# In-Tab data
			for yindex, data in enumerate(settings_info[selectedtab[0]]):
				isitemactive = False
				
				if data[2] != "TT":
					
					if selecteddropdown==data[0]: # Or CP, etc. : anything that is WIDE and must be displayed last
						activeitem = [data, yindex]
						isitemactive = True

					# Rectangles
					if 690<=mousex<=1310 and 120+60*yindex<=mousey<=170+60*yindex and not indropdown:
						d.draw.rect(window, grey2, (690, 120+60*yindex, 620, 50), 0, 10)
						if clicked:
							# State/Value changing
							match data[2]:
								case "YN":
									settings_info[selectedtab[0]][yindex][3] = not data[3]
								case "DD":
									if selecteddropdown!=data[0]:
										selecteddropdown=data[0]
										currentdropdowntop=125+60*yindex
										activeitem = [data, yindex]
										isitemactive = True

					window.blit(fonts[1].render(data[1], True, lightestgrey), (700,130+60*yindex))
				else:
					window.blit(fonts[1].render(data[2], True, lightestgrey), (750,130+60*yindex))
				

				# Display disjunction
				if not isitemactive:
					settings_disjunction(yindex, data[2])
			
			if indropdown:
				chosendropdownoption = (mousey-163-60*activeitem[1])//35
				if clicked:
					if 163+60*activeitem[1]<=mousey:
						dropdownlist = dropdowns[activeitem[0][0]][:]
						dropdownlist.remove(activeitem[0][3])
						settings_info[selectedtab[0]][activeitem[1]][3] = dropdownlist[chosendropdownoption]
					selecteddropdown=""

			elif clicked and saveselecteddropdown == selecteddropdown:
				selecteddropdown=""

			if activeitem!=[]:
				settings_disjunction(activeitem[1], activeitem[0][2])

			d.display.update()
			buttons = d.mouse.get_pressed(5)
		clock.tick(60)


# Just not being rude

def goodbye():
	global window
	d.quit()
	d.init()
	window = d.display.set_mode((scaledwidth/3, scaledheight/5), d.NOFRAME)
	window.fill(grey)
	font = d.font.SysFont('chalkduster', 400//downscale)
	img = font.render('Have a wonderful hour !', True, lightorange)
	text_rect = img.get_rect(center=(scaledwidth/6, scaledheight/10))
	window.blit(img, text_rect)
	d.display.update()
	time.sleep(1)


# Launching

def launch():
	global display
	global displaying
	global running
	running = True
	display = "local"
	chess_position = start_position
	while running:
		if display == "local":
			displaying = "local"
			initboard(chess_position)
		elif display == "menu":
			displaying = "menu"
			initmenu()
		elif display == "settings":
			displaying = "settings"
			initsettings()
		elif display == "sssettings":
			displaying = "sssettings"
	if settings_info[0][3][3]:
		goodbye()
	d.quit()



# INITIALIZING WHOLE PROGRAM


if __name__ == "__main__":
	launch()