import pygame
import math

# constants
DISPLAY_SIZE = (600, 600)
RADIUS       = int(DISPLAY_SIZE[0] / 2)
CENTRE       = list(map(int, [DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 2]))

CLEAR_COLOUR = [0  , 20 , 40 ]
DARKRED      = [150, 10 , 10 ]
BRIGHTRED    = [250, 10 , 10 ]
FONT_COL     = [155, 155, 10 ]
FONT_COL2    = [10 , 155, 10 ]
BLUE         = [110, 110, 220]
YELLOW       = [220, 220, 110]
PURPLE       = [220, 110, 220]
OFFWHITE     = [230, 230, 230]
GREEN        = [190, 230, 190]

# variables
ap = [0, 0] # auto point
mp = CENTRE # manual point

angle_deg_auto = 0
angle_deg_manual = 0
manual = False
mouse_down = False
clicked = False
font = None

def get_pos_on_circumference(angle_deg: int) -> list:
	pos = [
		math.cos(math.radians(angle_deg)),
		-math.sin(math.radians(angle_deg))
	]
	pos = [i * RADIUS for i in pos]
	pos = [i + RADIUS for i in pos]

	return list(map(int, pos))

def normalise_point(point: list) -> list:
	point = [i - RADIUS for i in point] # remove offset (pretend the origin is 0, 0 instead of 300, 300)
	point = [i / RADIUS for i in point] # normalise
	return point

# ________________________________________________________
# ϴ = tan-1(opposite / adjacent)
# opposite = Y pos
# adjacent = X pos
# ________________________________________________________
def point_to_angle(point: list) -> int:
	return -math.degrees(math.atan2(point[1], point[0]))

def draw_base(display):
	# circle
	pygame.draw.circle(display, DARKRED, list(map(int, CENTRE)), RADIUS, 1)

	# axes
	pygame.draw.line(display, OFFWHITE, (0, RADIUS), (DISPLAY_SIZE[0], RADIUS), 2)
	pygame.draw.line(display, OFFWHITE, (RADIUS, 0), (RADIUS, DISPLAY_SIZE[1]), 2)

def draw_point(display, point):
	# line from centre to clicked point (aka hypotenuse)
	pygame.draw.aaline(display, OFFWHITE, CENTRE, point)

	# line from X axis to clicked point
	pygame.draw.line(display, YELLOW, (point[0], RADIUS), point, 1)
	# circle on X axis
	pygame.draw.circle(display, YELLOW, (point[0], RADIUS), 5)

	# line from Y axis to clicked point
	pygame.draw.line(display, PURPLE, (RADIUS, point[1]), point, 1)
	# circle on Y axis
	pygame.draw.circle(display, PURPLE, (RADIUS, point[1]), 5)

	# circle at clicked point
	pygame.draw.circle(display, BLUE, point, 5)

def run():
	global manual, font, smallfont, clicked, mouse_down, angle_deg_auto, angle_deg_manual, ap, mp

	pygame.init()
	pygame.font.init()

	font = pygame.font.SysFont("Noto Mono", 22)
	smallfont = pygame.font.SysFont("Noto Mono", 16)

	display = pygame.display.set_mode(DISPLAY_SIZE)
	pygame.display.set_caption("Circle")

	clock = pygame.time.Clock()

	should_run = True

	auto_text = font.render("AUTO", False, FONT_COL)
	manual_text =  font.render("MANUAL", False, FONT_COL)

	paused = False

	while should_run:
		# events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				should_run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if manual:
						if clicked:
							clicked = False
						manual = False
					else:
						manual = True
				elif event.key == pygame.K_q:
					should_run = False
				elif event.key == pygame.K_p:
					paused = not paused
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if manual:
					mouse_down = True
					clicked = True
					angle_deg_manual = point_to_angle(normalise_point(list(event.pos)))
					mp = get_pos_on_circumference(angle_deg_manual)
			elif event.type == pygame.MOUSEBUTTONUP:
				mouse_down = False
			elif event.type == pygame.MOUSEMOTION:
				if manual and mouse_down:
					clicked = True
					angle_deg_manual = point_to_angle(normalise_point(list(event.pos)))
					mp = get_pos_on_circumference(angle_deg_manual)

		# update
		if not manual and not paused:
			angle_deg_auto = (angle_deg_auto + 1) % 360
			ap = get_pos_on_circumference(angle_deg_auto)

		# draw
		display.fill(CLEAR_COLOUR)

		draw_base(display)

		if manual:
			draw_point(display, mp)
			display.blit(manual_text, [0, 0])

			# info
			angle_str = str(int(angle_deg_manual))

			angle_text = font.render(angle_str + '°', False, FONT_COL)
			display.blit(angle_text, (0, 22))

			sinTheta = math.sin(math.radians(angle_deg_manual))
			sinTheta_text = smallfont.render("sin("+angle_str+") = {0:.1f}".format(sinTheta), False, FONT_COL2)
			display.blit(sinTheta_text, [RADIUS, max(0, min(mp[1], DISPLAY_SIZE[1] - 22))])

			cosTheta = math.cos(math.radians(angle_deg_manual))
			cosTheta_text = smallfont.render("cos("+angle_str+") = {0:.1f}".format(cosTheta), False, FONT_COL2)
			display.blit(cosTheta_text, [max(0, min(mp[0], DISPLAY_SIZE[0] - 160)), RADIUS])
		else:
			draw_point(display, ap)
			display.blit(auto_text, [0, 0])

			# info
			angle_str = str(int(angle_deg_auto))
			angle_text = font.render(angle_str + '°', False, FONT_COL)
			display.blit(angle_text, (0, 22))

			sinTheta = math.sin(math.radians(angle_deg_auto))
			sinTheta_text = smallfont.render("sin("+angle_str+") = {0:.1f}".format(sinTheta), False, FONT_COL2)
			display.blit(sinTheta_text, [RADIUS, max(0, min(ap[1], DISPLAY_SIZE[1] - 22))])

			cosTheta = math.cos(math.radians(angle_deg_auto))
			cosTheta_text = smallfont.render("cos("+angle_str+") = {0:.1f}".format(cosTheta), False, FONT_COL2)
			display.blit(cosTheta_text, [max(0, min(ap[0], DISPLAY_SIZE[0] - 160)), RADIUS])
			
		pygame.display.update()
		clock.tick(30)

if __name__ == "__main__":
	run()
else:
	run()
