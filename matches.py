'''
From https://en.wikipedia.org/wiki/Nim :

Nim is a mathematical game of strategy in which two players
take turns removing objects from distinct heaps.
On each turn, a player must remove at least one object,
and may remove any number of objects provided they all come
from the same heap. The goal of the game is to avoid being the player
who must remove the last object.
Nim has been mathematically solved for any number of initial heaps and objects,
and there is an easily calculated way to determine which player will win and
what winning moves are open to that player.

The key to the theory of the game is the binary digital sum of the heap sizes,
that is, the sum (in binary) neglecting all carries from one digit to another.
This operation is also known as "exclusive or" (xor) or "vector addition over
GF(2)". Within combinatorial game theory it is usually called the nim-sum, as
it will be called here.

In normal play, the winning strategy is to finish every move with a
nim-sum of 0. This is always possible if the nim-sum is not zero before
the move. If the nim-sum is zero, then the next player will lose if the
other player does not make a mistake.
'''
# Imports
import pygame
import random
import time

# Initialize game engine
pygame.init()

# Window
SIZE = (800, 600)
TITLE = "Nim Game"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 30

# Colors
GREEN = (33, 124, 62)

DARK_RED = (102, 0, 0)
LIGHT_RED = (120, 0, 0)
LIGHTEST_RED = (150, 0, 0)

DARK_STICK = (150, 126, 55)
LIGHT_STICK = (216, 181, 75)


#this list contains the number of matches in each of the four rows
match_rows = [1, 3, 5, 7]


#draw a single match at location
def draw_match(loc):
    x = loc[0]
    y = loc[1]
    
    pygame.draw.rect(screen, LIGHT_STICK, [x+18, y+10, 5, 90], 0)
    pygame.draw.polygon(screen, DARK_STICK, [[x+15, y+10], [x+18, y+10], [x+18, y+99], [x+15, y+96]], 0)
    pygame.draw.ellipse(screen, DARK_RED, [x+9, y, 20, 40], 0)
    pygame.draw.ellipse(screen, LIGHT_RED, [x+14, y+2, 14, 29], 0)
    pygame.draw.ellipse(screen, LIGHTEST_RED, [x+17, y+7, 10, 15], 0)
    
#draws a single row with the specific amount of matches
def draw_row(row, num_matches):
    start_x = 20
    offset_x = 30
    start_y = -100
    offset_y = 120
    
    for m in range(num_matches):
        draw_match([start_x + (offset_x * m), start_y + (row * offset_y)])

#checks number of remaining matches, returns true is only one remains
def is_one_match_left():
    total = 0
    for m in match_rows:
        total += m
    if total == 1:
        return True
    return False

#this function handles end game situations to force the player to
#take the last match
def can_win_now():
    zero_counts = 0
    one_counts = 0
    big_row = 0
    for i in range(len(match_rows)):
        if match_rows[i] == 0:
            zero_counts += 1
        elif match_rows[i] == 1:
            one_counts += 1
        elif match_rows[i] >=1:
            big_row = i
    #determines if two rows have 0, one row has 1, and the other row has some number
    #OR if three rows have 1 and the other has a number greater than 0        
    if (zero_counts == 2 and one_counts == 1) or (one_counts == 3 and zero_counts == 0):
        print("I removed %d match(es) from row %d." % (match_rows[big_row], big_row))
        match_rows[big_row] = 0
        return True
    #checks to see if two rows have 1, one row has 0, and the other has a number greater than 0
    #if so, leave the user with 1, 1, 1
    if one_counts == 2 and zero_counts == 1:
        print("I removed %d match(es) from row %d." % (match_rows[big_row]-1, big_row))
        match_rows[big_row] = 1
        return True
    #if three rows are empty and one row has more than one, take all but one 
    if zero_counts == 3:
        print("I removed %d match(es) from row %d." % (match_rows[big_row]-1, big_row))
        match_rows[big_row] = 1
        return True
    
    return False
    
#draws the matches on the screen
def draw_board():
    screen.fill(GREEN)
    for r in range(len(match_rows)):
        draw_row(r+1, match_rows[r])
    pygame.display.flip()
        
#gets the player input
def get_player_input():
    input_is_invalid = True
    while input_is_invalid:
        #makes sure the input is a number not a word
        input_string = input("What row?")
        if input_string.isdigit() == False:
            print("That's not a number!")
        else:   
            row_number = int(input_string)
        
            #if that row doesnt exist, tell player to get another row
            if row_number <= 0 or row_number > len(match_rows):
                print("Whoops! That's not a row!")
            
            #if they try to take matches from an empty row,
            #make them pick another row
            elif match_rows[row_number-1] <= 0:
                print("Oopsie! That row is empty.")
            
            #if it works, then good
            else:
                input_is_invalid = False

            
    input_is_invalid = True
    while input_is_invalid:
        match_count = int(input("How many matches?"))
        
        #if they try to take none or negative, then say no
        if match_count <= 0:
            print("Can't pass!")
            
        #if they try to take too many matches from a row that has matches,
        #tell player no
        elif match_count > match_rows[row_number-1]:
            print("That's too many matches!")
            
        #if they're good, then good
        else:
            input_is_invalid = False

    #takes away the matches the player wants to remove
    match_rows[row_number-1] -= match_count 

# calculates the nim sum using xor
def nim_sum(numbers):
    nim = 0
    for m in numbers:
        nim ^= m
    return nim

#computes the computers move
def compute_pc_move():
    #make it wait a second
    time.sleep(1)
    #if the computers in a position where he can win, then do the win
    if can_win_now():
        return

    #if nim sum is not 0, we should be able to find a good move to make it 0
    if nim_sum(match_rows) != 0:
        #for each row, remove matches 1 by 1 until we find nim sum = 0
        #at that point, use that as the move, notify the user, and return
        for i in range(len(match_rows)):
            test = list(match_rows)
            for j in range(test[i]):
                test[i] -= 1
                if nim_sum(test)== 0:
                    print("I removed %d match(es) from row %d." % (match_rows[i]- test[i],i+1))
                    #found it so make the move and return
                    match_rows[i] = test[i]
                    return
                
        #this shouldnt ever show unless theres a problem
        print("Note: I could not find a good move")            

    #if the computer is in a losing position, just do something random
    random_pc_move()
    
    
#choses pc move when the player is allowed to win
def random_pc_move():
    for m in range(len(match_rows)):
        if match_rows[m] >= 1:
            match_rows[m] -= 1
            print("I removed 1 match from row %d." % (m+1,))
            return 
    
    
#game loop
done = False

print("Choose a row and take as many matches as you want from that row. The goal is to make the other player pick the last match.")

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    ''' for now, we'll just check to see if the X is clicked '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    #show the board
    draw_board()

    #see what the player wants to do
    get_player_input()

    #redraw players move
    draw_board()

    #see if player won
    if is_one_match_left():
        print("you wins")
        input("Press ENTER to end the game")
        done = True
        
    #computer plays
    compute_pc_move()

    #redraw computers move
    draw_board()

    #see if computer won
    if is_one_match_left():
        print("me wins")
        input("Press ENTER to end the game")
        done = True

                    

# Close window on quit
pygame.quit()
