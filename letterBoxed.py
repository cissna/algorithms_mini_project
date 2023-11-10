import time
import pygame
import sys
from find_graph import letter_boxed_solver

# Colors
salmon = (250, 166, 164)
pink = (249, 181, 171)
gray = (100, 100, 100)
light_pink = (254, 240, 235)
white = (255, 255, 255)
black = (0, 0, 0)


letters = 'UGH TIO PRS MNC'
path = letter_boxed_solver(letters)
letters_of_path = ['end'] + list(reversed(''.join(path)))  # backwards for popping


def draw_dotted_line(start_point, end_point, color=pink):
    """Draws dotted line"""
    if start_point[0] == end_point[0]:  # VEC = Vertical Edge Case
        height = end_point[1] - start_point[1]
        if height < 0:
            VEC_segment_len = -37
        else:
            VEC_segment_len = 37
        VEC_number_of_segments = height / VEC_segment_len  # round up in the below line
        VEC_number_of_segments = int(VEC_number_of_segments) + 1 if VEC_number_of_segments % 1 else int(VEC_number_of_segments)
        VEC_last_coord = start_point
        VEC_coord = list(start_point)
        for _ in range(VEC_number_of_segments):
            VEC_coord[1] += VEC_segment_len
            if VEC_last_coord[1] < end_point[1] < start_point[1] or VEC_last_coord[1] > end_point[1] > start_point[1]:
                return  # just says if the x and y are further than the end point, end
            VEC_dash_end = VEC_coord[0], VEC_coord[1] - int((17/37) * VEC_segment_len)
            pygame.draw.line(screen, color, VEC_last_coord, VEC_dash_end, 10)
            VEC_last_coord = VEC_coord
        return


    slope = (end_point[1] - start_point[1]) / (end_point[0] - start_point[0])
    y_int = start_point[1] - slope * start_point[0]

    distance = int(((start_point[0] - end_point[0])**2 + (start_point[1] - end_point[1])**2)**.5)
    segment_len_goal = 37  # not actually going to be the distance, I'm favoring consistent line lengths over being 37
    segment_x_distance = (segment_len_goal**2/(1 + slope**2))**.5 // 1
    segment_x_distance *= -1 if start_point[0] > end_point[0] else 1
    space_x_len = 20/37 * segment_x_distance // 1
    segment_len_actual = (segment_x_distance**2 * (slope**2 + 1))**.5
    number_of_segments = (end_point[0] - start_point[0]) / segment_x_distance
    number_of_segments = int(number_of_segments) + 1 if number_of_segments % 1 else int(number_of_segments)  # round up

    coord = list(start_point)
    last_coord = tuple(coord)
    for x_segment in range(1, number_of_segments + 1):
        if (last_coord[0] < end_point[0] < start_point[0] or last_coord[0] > end_point[0] > start_point[0]) and \
                (last_coord[1] < end_point[1] < start_point[1] or last_coord[1] > end_point[1] > start_point[1]):
            return  # just says if the x and y are further than the end point, end

        coord[0] += segment_x_distance
        coord[1] += slope * segment_x_distance
        dash_end = coord[0] - space_x_len, coord[1] - space_x_len * slope
        pygame.draw.line(screen, color, last_coord, dash_end, 10)

        last_coord = tuple(coord)


def draw_line_part(start_point, end_point, line_counter, color=pink, dotted=False, delay=.0005):
    """Meant to be inside a while loop. Draws a line, up until where the line_counter dictates, which increases
    with each pass through the while loop."""
    x_change = end_point[0] - start_point[0]
    y_change = end_point[1] - start_point[1]
    distance = max(abs(x_change), abs(y_change))

    step_x = x_change / distance
    step_y = y_change / distance

    current_x, current_y = start_point
    current_x += step_x * line_counter
    current_y += step_y * line_counter

    if dotted:
        draw_dotted_line(start_point, (int(current_x + step_x), int(current_y + step_y)))  # assumes color is pink
    else:
        pygame.draw.line(screen,
                         color,
                         start_point,
                         (int(current_x + step_x), int(current_y + step_y)),
                         10)
    if line_counter == distance:
        return 0
    time.sleep(delay)
    return line_counter + 1


# Initialize Pygame
pygame.init()

# Create the screen
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Letter Boxed")
font = pygame.font.Font(None, 75)
font2 = pygame.font.Font(None, 35)

# White Square in middle
square_size = 405
square_x = (screen_width - square_size) // 2
square_y = (screen_height - square_size) // 2


# Coordinates for the text centered around each position
positions = [(150, 250), (150, 400), (150, 550), (550, 650), (400, 650), (250, 650),
             (650, 550), (650, 400), (650, 250), (550, 150), (400, 150), (250, 150)]

circle_color = white
outline_color = black
circle_radius = 15
circle_positions = [(200, 250), (200, 400), (200, 550), (550, 600), (400, 600), (250, 600),
                    (600, 550), (600, 400), (600, 250), (550, 200), (400, 200), (250, 200)]
letter_position_circle_d = {}
for i, letter in enumerate(letters.replace(' ', '').strip().lower()):
    letter_position_circle_d[letter] = (positions[i], circle_positions[i])

    if i > 11:  # debugging because this seems a little precarious
        print(f'SOMETHING WRONG WITH LETTERS, LENGTH GREATER THAN 12: {letters}')
        pygame.quit()
        sys.exit()

counter = 0
# Main game loop
ending_word = True
line_part = 0
line_part2 = 0
line_part3 = 0
current_letter = letters_of_path.pop()
next_letter = letters_of_path.pop()
one_word_lines = []
one_word_lines_counter = 0
past_word_lines = []
current_lines = []
write_words = path[0][0]
while counter := counter + 1:  # counter increments by 1, starting from 1. Also, the while loop will end if counter = -1
    # from here —————————————————————————————————————————————————————————————————————————————————————↓
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            counter = -1
    screen.fill(salmon)
    pygame.draw.rect(screen, black, (square_x, square_y, square_size, square_size))
    pygame.draw.rect(screen, white, (square_x + 5, square_y + 5, square_size - 10, square_size - 10))
    for coord1, coord2 in past_word_lines:
        pygame.draw.line(screen, light_pink, coord1, coord2, 10)
    for coord1, coord2 in one_word_lines:
        draw_dotted_line(coord1, coord2)
    for coord1, coord2 in current_lines:
        pygame.draw.line(screen, pink, coord1, coord2, 10)
    for letter, values in letter_position_circle_d.items():
        # if current_letter == letter:  # maybe fix later, maybe not.
        #     pygame.draw.circle(screen, pink, circle_center, circle_radius, 5)
        #     pygame.draw.circle(screen, black, circle_center, circle_radius - 5)
        if letter in write_words:
            if letter in write_words.split()[-1]:
                text_surface = font.render(letter.upper(), True, black)
            else:
                text_surface = font.render(letter.upper(), True, gray)
        else:
            text_surface = font.render(letter.upper(), True, white)
        position, circle_center = values
        text_rect = text_surface.get_rect()
        text_rect.center = position
        screen.blit(text_surface, text_rect.topleft)
    text_surface = font2.render(write_words.upper(), True, black)
    screen.blit(text_surface, (10, 50))
    # to here ———————————————————————————————————————————————————————————————————————————————————————↑
    # is just background stuff to make it look right
    if counter == 1:
        pygame.display.flip()  # updates frame
        time.sleep(.5)  # starts too fast, otherwise


    if not letters_of_path:
        current_letter = 'end'
        next_letter = 'end'
    if current_letter == next_letter:

        if ending_word:
            ending_word = False
            line = one_word_lines[0]
        line_part2 = draw_line_part(line[0], line[1], line_part2, delay=.00001)
        if line_part2 == 0 and one_word_lines_counter < len(one_word_lines):
            current_lines.append(line)
            line = one_word_lines[one_word_lines_counter]
            one_word_lines_counter += 1

        elif line_part2 == 0:
            if current_letter == 'end':
                line_part3 = draw_line_part(current_coords, next_coords, line_part3, dotted=True)
                if line_part3 == 0:
                    counter = -1
            if not letters_of_path:
                break
            write_words += ' — ' + next_letter
            next_letter = letters_of_path.pop()
            ending_word = True
            current_lines = []
            one_word_lines_counter = 0
            [past_word_lines.append(one_word_lines.pop()) for i in range(len(one_word_lines))]
    else:
        current_coords = letter_position_circle_d[current_letter][-1]
        next_coords = letter_position_circle_d[next_letter][-1]  # -1 index is the circle's coordinate
        line_part = draw_line_part(current_coords, next_coords, line_part, dotted=True)
        if line_part == 0:  # this will serve to loop through the letters
            one_word_lines.append((current_coords, next_coords))
            write_words += next_letter
            current_letter = next_letter
            next_letter = letters_of_path.pop()

    # from here —————————————————————————————————————————————————————————————————————————————————————↓
    for letter, values in letter_position_circle_d.items():
        position, circle_center = values
        pygame.draw.circle(screen, outline_color, circle_center, circle_radius, 5)
        pygame.draw.circle(screen, circle_color, circle_center, circle_radius - 5)
    # to here ———————————————————————————————————————————————————————————————————————————————————————↑
    # is just background stuff to make it look right

    pygame.display.flip()  # updates frame

line_part3 = 0
while True:
    second_to_last, last = path[-1][-2:]
    second_to_last, last = letter_position_circle_d[second_to_last][-1], letter_position_circle_d[last][-1]
    line_part3 = draw_line_part(second_to_last, last, line_part3, delay=0.00001)
    if line_part3 == 0:
        time.sleep(3)
        break  # final stuff here
    # from here —————————————————————————————————————————————————————————————————————————————————————↓
    for letter, values in letter_position_circle_d.items():
        position, circle_center = values
        pygame.draw.circle(screen, outline_color, circle_center, circle_radius, 5)
        pygame.draw.circle(screen, circle_color, circle_center, circle_radius - 5)
    # to here ———————————————————————————————————————————————————————————————————————————————————————↑
    # is just background stuff to make it look right
    pygame.display.flip()  # updates frame
# Quit Pygame
pygame.quit()
sys.exit()
