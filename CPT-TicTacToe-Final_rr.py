'''
Tic-Tac-Toe
Create Performance Task
Made on macOS. Should work fine on Linux, but may require
modifications on Windows.

Code written by Ryan Ruiz (allthesquares). When crediting, please use my
online name in parentheses. Do not plagiarize this code. Not only is it
potentially illegal but it will result in your AP score getting cancelled.
'''

# --- Imports --- #
# chooses indices or items at random
from random import randint, choice
# used to pass a turtle to function when clicked
from functools import partial
# Adds delays
from time import sleep
# Graphics library
from turtle import Screen, Turtle
# Clear terminal
from os import system

''' Using the partial function from functools comes from a user on StackOverflow. Review the thread here:
https://stackoverflow.com/questions/61436645/use-a-function-that-needs-an-argument-for-onclick-event-python-turtle '''

# --- Variables --- #
# screen setup
window = Screen()
line_graphics = Turtle()
text_graphics = Turtle()
turtle_board = []
for row in range(3):
    row = []
    for col in range(3):
        row.append(Turtle())
    turtle_board.append(row)

# game info tracking
player_scores = [0.0] * 2
current_player = ''

# computer settings
computer_preferences = ["Difficulty", "Opponent Mark"]
is_computer_playing = False

# enable/disable clicking the screen
can_click_squares = False
game_over = [False, False]

# drawing preferences:
square_locations = (-105, 0, 105)
line_locations = [[-50, 150], [50, 150]]

# --- Functions --- #
def setup_game(launch_config):
    global player_board, turtle_board, available_spaces, window
    global player_marks, current_player, can_click_squares

    # gameplay and board-keeping
    player_board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
    available_spaces = 9

    player_marks = ['x', 'o']       # First index is always the current player
    current_player = ''             # Intentionally empty
    can_click_squares = False       # Disables ability to click the turtles

    line_graphics.penup()
    line_graphics.clear()

    text_graphics.penup()
    text_graphics.hideturtle()
    text_graphics.goto(0, 200)

    if launch_config:
        window.title("[Tic-Tac-Toe]")
        write_text("GAME SETUP: Go check your terminal!", "Black")
        game_config()

    text_graphics.clear()
    window.title(
        f"{player_scores[0]} - X    [Tic-Tac-Toe]   O - {player_scores[1]}")

    for line_coordinates in (line_locations):
        for direction in (90, 0):
            draw_line(line_coordinates, direction, -300, 3, 'fast')
            line_coordinates.reverse()

    for row in turtle_board:
        for turtle in row:
            turtle.color("white")
            turtle.showturtle()

    start_turn()

def draw_line(coordinates, direction, distance, pen_size, speed):
    ''' Changes properties of the line_graphics turtle and draws a nice line. '''
    window.tracer(True)
    line_graphics.pensize(pen_size)
    line_graphics.speed(speed)
    line_graphics.goto(coordinates)
    line_graphics.setheading(direction)
    line_graphics.pendown()
    line_graphics.forward(distance)
    line_graphics.penup()

def draw_mark(player_mark, turtle):
    ''' Draws either the X or O mark on where the user clicked. '''
    # Sequencing
    if player_mark == 'x':              # Selection
        turtle.hideturtle()
        turtle.speed('normal')
        turtle.color('blue')
        for angle in (45, 135):              # Iteration
            turtle.setheading(angle)
            turtle.forward(-40)
            turtle.pendown()
            turtle.forward(80)
            turtle.penup()
            turtle.forward(-40)
        turtle.setheading(0)
    elif player_mark == 'o':            # Selection
        turtle.hideturtle()
        turtle.speed('fast')
        turtle.color('red')
        turtle.sety(turtle.ycor() - 35)
        turtle.pendown()
        turtle.circle(35, 360)
        turtle.penup()
        turtle.sety(turtle.ycor() + 35)

def write_text(text, color, clear=True):
    # Text writing system. First argument determines whether it should clear the screen or not.
    if clear:
        text_graphics.clear()
    text_graphics.color(color)
    text_graphics.write(text, font=('Arial', 24, 'bold'), align='center')

def clicked_square(turtle, x, y):
    global win, can_click_squares, available_spaces, game_over
    if can_click_squares or can_click_squares == 'computer':
        # Disable ability to click on turtles.
        can_click_squares = False
        # Get location of turtle on board:
        location = []
        for index_row, row in enumerate(turtle_board):
            if turtle in row:
                location = [index_row, row.index(turtle)]
                break

        # Update the score-tracking board to indicate square is now taken.
        player_board[location[0]][location[1]] = current_player
        available_spaces -= 1
        player_marks.reverse()

        # Draw the mark on the square, then switch the players around.
        window.tracer(True)
        draw_mark(current_player, turtle)
        window.tracer(False)

        # Check if there are either no available spaces on the board or if someone won.
        win = check_for_win(current_player)
        if win or available_spaces == 0:
            if win:
                color = 'blue' if current_player == 'x' else 'red'
                write_text(f"{current_player.capitalize()} wins!",
                           color, clear=True)
                update_score(current_player)

            elif available_spaces == 0:
                write_text("It's a tie!", 'black', clear=True)
                update_score("tie")
            text_graphics.goto(0, -225)
            write_text(
                "Click anywhere to play again,\nor right-click to change settings!", "black", clear=False)
            game_over[0] = True

        else:
            # Start a new turn.
            start_turn()

def check_for_win(player):
    ''' Checks if a player won if their mark covers all the squares on a row, diagonal, or column. '''
    possible_outcomes = {
        "rows": [player_board[0], player_board[1], player_board[2]],
        "columns": [[player_board[0][0], player_board[1][0], player_board[2][0]],
                    [player_board[0][1], player_board[1][1], player_board[2][1]],
                    [player_board[0][2], player_board[1][2], player_board[2][2]]],
        "diagonals": [[player_board[0][0], player_board[1][1], player_board[2][2]],
                      [player_board[2][0], player_board[1][1], player_board[0][2]]],
    }

    # Get the key and outcome.
    for outcome_type, outcomes in possible_outcomes.items():
        # iterate through all possibilities for a win.
        for index, outcome in enumerate(outcomes):

            # check if outcome is all controlled by the current player.
            if outcome == [player, player, player]:
                # Draw accordingly depending on the index and outcome type.
                for row in turtle_board:
                    for turtle in row:
                        turtle.hideturtle()

                if outcome_type == 'rows':
                    draw_line((-150, 105 + (-105 * index)),
                              0, 300, 4, 'fast')
                elif outcome_type == 'columns':
                    draw_line((-105 + (105 * index), 150), -
                              90, 300, 4, 'fast')
                elif outcome_type == 'diagonals':
                    coord_multiplier = -1 if index == 0 else 1
                    draw_line((-150, 150 * -coord_multiplier), 45 *
                              coord_multiplier, 425, 4, 'fast')

                return True
    return False

def start_turn():
    ''' Switches turns between the two players. X will always go if this is the first turn. '''

    global current_player, can_click_squares
    # as the marks are flipped before starting the next turn, the current turn will always be the first index.
    current_player = player_marks[0]
    write_text(f"It is {current_player.capitalize()}'s turn!", "black")

    # The computer will be able to click squares on its own.
    if current_player == computer_preferences[1] and is_computer_playing:
        can_click_squares = 'computer'
        sleep(.5)
        computer_turn(computer_preferences[0])
    else:
        can_click_squares = True

def computer_turn(difficulty):
    ''' Computer-controlled player for the game. '''
    coordinates = [-1, -1]
    opponent = player_marks[1]

    ''' In difficulties other than easy, the computer can check every row, diagonal, or column if either player is close to winning. 
        The computer will fill in the remaining square if both are true. '''

    if difficulty in ['hard', 'impossible']:
        # depending on the difficulty, the odds are determined: 100% for impossible and 75% (3/4 True) for Hard
        odds = [True] if difficulty == 'impossible' else [True] * 3 + [False]
        coordinates = computer_check_board(opponent, odds)

    # If the computer cannot check for any wins or is set to easy, it will pick a square randomly.
    # This continues picking until it selects an empty square.
    while player_board[coordinates[0]][coordinates[1]] != '-':
        coordinates = [randint(0, 2), randint(0, 2)]

    turtle = turtle_board[coordinates[0]][coordinates[1]]
    clicked_square(turtle, 0, 0)

def computer_check_board(opponent, odds):
    ''' Check all outcomes and see if either the opponent or the computer is about to win. Fill in the remaining square.'''
    possible_outcomes = {
        "rows": [player_board[0], player_board[1], player_board[2]],
        "columns": [[player_board[0][0], player_board[1][0], player_board[2][0]], [player_board[0][1], player_board[1][1], player_board[2][1]], [player_board[0][2], player_board[1][2], player_board[2][2]]],
        "diagonals": [[player_board[0][0], player_board[1][1], player_board[2][2]], [player_board[2][0], player_board[1][1], player_board[0][2]]],
    }
    # Iterate through all possible outcomes.
    for player in (current_player, opponent):
        for outcome, possibilities in possible_outcomes.items():
            for index, result in enumerate(possibilities):
                # Check if there is one empty space left on this outcome AND if either the opponent or player has two marks on the outcome.
                if result.count('-') == 1 and (result.count(player) == 2) and choice(odds):
                    # Depending on what kind of outcome it is, fill in the empty square.
                    if outcome == 'rows':
                        return [index, result.index('-')]
                    elif outcome == 'columns':
                        return [result.index('-'), index]
                    elif outcome == 'diagonals':
                        return [result.index('-'), result.index('-')] if index == 0 else [2 - result.index('-'), result.index('-')]

    # Otherwise, return a random square.
    return [randint(0, 2), randint(0, 2)]

def game_config():
    ''' Ask the player a series of questions that determine how they want to play. '''
    global computer_preferences, is_computer_playing, player_scores
    option_choices = {
        "Who do you want to play against?\n(1) Another person\n(2) The Computer ": ["human", "computer"],
        "Set your preferred difficulty level for the computer:\n(1) Easy\n(2) Hard\n(3) Impossible": ['easy', 'hard', "impossible"],
        "What do you prefer playing as?\n(1) X\n(2) O": player_marks,
    }

    selections = []
    if sum(player_scores) > 0.0:
        while True:
            print("Do you want to reinitialize the scores? (y/n)")
            user_choice = input("-> ").strip().lower()
            if user_choice in ['y', 'n']:
                player_scores = [
                    0.0, 0.0] if user_choice == 'y' else player_scores
                break
            else:
                print("Please type either 'y' or 'n'.")

    for question, choices in option_choices.items():
        while True:
            print(question)
            user_choice = input("-> ").strip()
            if user_choice.isdigit() and int(user_choice) in range(1, len(choices) + 1):
                system('clear')
                user_choice = choices[int(user_choice) - 1]
                if user_choice not in ['human', 'computer']:
                    selections.append(user_choice)
                break
            else:
                print("Please type a number from 1 to %s." % len(choices))

        # FOR FIRST ITERATION
        if user_choice == 'human':
            is_computer_playing = False
            break
        else:
            is_computer_playing = True
            computer_preferences = selections

    if is_computer_playing:
        selections[1] = 'x' if selections[1] == 'o' else 'o'

def reset_game(launch_setup, x, y):
    ''' Reinitializes the game after it ends.
    Why is "game_over" a list? Upon winning, the screen is flagged as "clicked". To combat this, the additional registered "click" 
    instead sets the second Boolean of the list to True. This would mean that it would require TWO clicks to reset the game, however
    it is presented as one because the first click is made in the final move of the game.'''

    global game_over, turtle_board, can_click_squares
    if game_over == [True, True]:
        game_over = [False, False]
        can_click_squares = False
        # Clear the turtle's markings before redrawing the board.
        for row in turtle_board:
            for turtle in row:
                turtle.clear()
        setup_game(launch_setup)
    elif game_over[0] == True:
        game_over[1] = True

def update_score(winner):
    if winner == 'x':
        player_scores[0] += 1
    elif winner == 'o':
        player_scores[1] += 1
    else:
        player_scores[0] += .5
        player_scores[1] += .5

    window.title(
        f"{player_scores[0]} - X    [Tic-Tac-Toe]   O - {player_scores[1]}")

# Set up the screen and terminal
line_graphics.hideturtle()
system('clear')

# Place the squares:
window.tracer(False)
for row_index, row in enumerate(square_locations):
    for col_index, column in enumerate(square_locations):
        turtle = turtle_board[row_index][col_index]
        turtle.hideturtle()
        turtle.penup()
        turtle.color("white")
        turtle.shape("square")
        turtle.shapesize(4)
        turtle.pensize(3)
        turtle.goto(column, -row)
        turtle.onclick(partial(clicked_square, turtle))

window.tracer(True)
setup_game(True)    # Launch first-time setup.

''' macOS, Linux, and Windows all recognize BTN1 as left-click. However, macOS (and probably Linux) recognizes right-click as BTN2
while Windows recognizes BTN3 as right-click.'''

# Controls replaying the game when game ends on left-click.
window.onscreenclick(partial(reset_game, False), btn=1)

# Controls launching initial game setup when game ends. Middle- and right-clicking will do the same action.
window.onscreenclick(partial(reset_game, True), btn=2)
window.onscreenclick(partial(reset_game, True), btn=3)

window.mainloop()


