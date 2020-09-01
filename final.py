

#Check to see if bonuses have been claimed
BONUS_RED = 0
BONUS_BLUE = 0
BONUS_GREEN = 0
BONUS_ORANGE = 0
BONUS_PURPLE = 0


from cs110graphics import *
import random


class Box(EventHandler):
    '''boxes for the trucks to place dice in'''

    def __init__(self, game, window, xc, yc, color):
        '''initalize a box'''

        self._game = game
        self._window = window
        self._size = 50
        self._xc = xc
        self._yc = yc
        self._color = color

        self._body = Square(self._window, self._size, (self._xc, self._yc))

        self._body.set_depth(2)

        self._window.add(self._body)

    def get_box_color(self):
        return self._color

    def clear_box(self):
        '''Resets the color of the box to make it empty'''

        self._color = "white"
        self._body.set_fill_color(self._color)

    def change_box_color(self, color):
        '''changes the color of a box when a dice is droppedo on it'''

        self._color = color
        self._body.set_fill_color(self._color)

class Truck(EventHandler):
    '''Truck that contains three boxes'''

    def __init__(self, game, window, size, position):
        '''initalize a truck'''

        self._game = game
        self._window = window
        self._size = size
        self._xc, self._yc = position

        self._box1 = Box(self._game, self._window, self._xc, self._yc, "white")
        self._box2 = Box(self._window, self._window, self._xc + 75, self._yc, "white")
        self._box3 = Box(self._window, self._window, self._xc + 150, self._yc, "white")


    def collect(self):
        '''method of collecting the boxes from a truck'''

        if self._box1.get_box_color() != "white":
            color = self._box1.get_box_color()
            self._game.pass_color(color)
            self._box1.clear_box()

        if self._box2.get_box_color() != "white":
            color = self._box2.get_box_color()
            self._game.pass_color(color)
            self._box2.clear_box()

        if self._box3.get_box_color() != "white":
            color = self._box3.get_box_color()
            self._game.pass_color(color)
            self._box3.clear_box()

    def check_empty(self):
        '''make sure the truck isn't empty before collecting'''

        if self._box1.get_box_color() != "white" or self._box2.get_box_color() != "white" \
        or self._box3.get_box_color() != "white":
            return True
        else:
            return False

    def check_one_left(self):
        '''adds one to counter for every box that has a color in it'''

        one_left_counter = 0

        if self._box1.get_box_color() != "white":
            one_left_counter += 1

        if self._box2.get_box_color() != "white":
            one_left_counter += 1

        if self._box3.get_box_color() != "white":
            one_left_counter += 1

        return one_left_counter

    def change_box1(self, color, name):
        '''method of calling change_box_color'''

        if self._box1.get_box_color() == "white":
            self._box1.change_box_color(color)
            if name == "dice1":
                self._game.change_dice1()
            else:
                self._game.change_dice2()

    def change_box2(self, color, name):
        '''method of calling change_box_color'''

        if self._box2.get_box_color() == "white":
            self._box2.change_box_color(color)
            if name == "dice1":
                self._game.change_dice1()
            else:
                self._game.change_dice2()

    def change_box3(self, color, name):
        '''method of calling change_box_color'''

        if self._box3.get_box_color() == "white":
            self._box3.change_box_color(color)
            if name == "dice1":
                self._game.change_dice1()
            else:
                self._game.change_dice2()

class Dice(EventHandler):
    '''Dice that have 6 sides representing different scoring types'''

    def __init__(self, game, window, name, xcen, ycen):
        '''initialize the dice'''

        self._game = game
        self._window = window
        self._name = name
        self._sides = 6
        self._size = 50
        self._xcen = xcen
        self._ycen = ycen
        self._faces = ["red", "blue", "green", "orange", "purple", "grey"]

        self._body = Square(self._window, self._size, (self._xcen, self._ycen))
        self._body.add_handler(self)
        self._depth = 2
        self._dice_color = "white"

        self.draw_dice()

    def get_dice_color(self):
        return self._dice_color


    def roll_dice(self):
        '''Randomly chooses a side of the dice'''

        self._dice_color = random.choice(self._faces)
        self._body.set_fill_color(self._dice_color)


    def draw_dice(self):
        '''Method for adding the dice to the graphics window'''

        self._body.set_depth(self._depth)
        self._window.add(self._body)

    def change_to_white(self):
        '''changes dice color to white'''

        self._dice_color = 'white'
        self._body.set_fill_color(self._dice_color)

    def handle_mouse_release(self, event):
        # This code runs when the user clicks to move the dice to a truck

        if self._dice_color != "white":

            xcord = event.get_mouse_location()[0]
            ycord = event.get_mouse_location()[1]

            if 75 <= xcord <= 125:
                x = 0
            elif 150 <= xcord <= 200:
                x = 1
            elif 225 <= xcord <= 275:
                x = 2
            else:
                x=3

            if x != 3:
                if 75 <= ycord <= 125:
                    self._game.add_to_truck1(x, self._dice_color, self._name)
                    # self._dice_color = 'white'
                    # self._body.set_fill_color(self._dice_color)

                elif 175 <= ycord <= 225:
                    self._game.add_to_truck2(x, self._dice_color, self._name)
                    # self._dice_color = 'white'
                    # self._body.set_fill_color(self._dice_color)

                elif 275 <= ycord <= 325:
                    self._game.add_to_truck3(x, self._dice_color, self._name)
                    # self._dice_color = 'white'
                    # self._body.set_fill_color(self._dice_color)

                elif 375 <= ycord <= 425:
                    self._game.add_to_truck4(x, self._dice_color, self._name)
                    # self._dice_color = 'white'
                    # self._body.set_fill_color(self._dice_color)



class Player(EventHandler):
    '''Class for a player'''

    def __init__(self, game, window, xcord, ycord, name):
        '''Constructor method for Player'''

        self._game = game
        self._window = window
        self._xcord = xcord
        self._ycord = ycord
        self._name = name

        self._turn_value = 0

        self._scorecard = Scorecard(self, self._game, self._window, self._xcord, self._ycord, self._name)
        self._scorecard.draw_scorecard()

    def get_player_name(self):
        return self._name

    def add_score(self, color):
        '''method for calling the scoring functions'''

        if color == "red":
            self._scorecard.red()
        elif color == "blue":
            self._scorecard.blue()
        elif color == "green":
            self._scorecard.green()
        elif color == "orange":
            self._scorecard.orange()
        elif color == "purple":
            self._scorecard.purple()
        else:
            self._scorecard.coin()

    def get_turn_value(self):
        return self._turn_value

    def round_end(self):
        '''when a player is done for the round changes value to 1 so they get
        skipped next time around'''

        self._turn_value = 1
        self._scorecard.check_winner()
        self._scorecard.unbold()

    def new_round(self):
        '''when all players finish a round changes value to 1 so they can play
        the next round'''

        self._turn_value = 0

    def tally_scores(self):
        '''method of ending game when play is over'''

        return self._scorecard.total_score()

    def highlight(self):
        '''calls bold to show player turn'''
        self._scorecard.bold()

    def unhighlight(self):
        '''calls unbold to change player turn'''
        self._scorecard.unbold()

class Scorecard(EventHandler):
    '''Class for the Scorecard'''

    def __init__(self, player, game, win, xcen, ycen, name):
        '''Constructor method for scorecard'''

        self._game = game
        self._window = win
        self._player = player

        #locations for scores to appear on the scorecards
        self._position = (xcen, ycen)
        self._position1 = (xcen - 20, ycen - 75)
        self._position2 = (xcen - 20, ycen - 55)
        self._position3 = (xcen - 20, ycen - 38)
        self._position4 = (xcen - 20, ycen - 21)
        self._position5 = (xcen - 20, ycen - 4)
        self._position6 = (xcen - 20, ycen + 13)
        self._position7 = (xcen - 20, ycen + 30)
        self._position8 = (xcen - 20, ycen + 47)
        self._position21 = (xcen + 30, ycen - 55)
        self._name = name

        #score keeper for each of the colors
        self._red = {}
        self._blue = {}
        self._green = {}
        self._orange = {}
        self._purple = {}
        self._coin = {}

        self._bonus = 0
        self._negative = 0
        self._columns_filled = []

        self._red['red'] = 0
        self._blue['blue'] = 0
        self._green['green'] = 0
        self._orange['orange'] = 0
        self._purple['purple'] = 0
        self._coin['coin'] = 0

    def total_score(self):
        '''tallies up totals for each player'''

        return self._red['red'] + self._blue['blue'] + self._green['green'] + \
        self._orange['orange'] + self._purple['purple']  + self._bonus - \
        self._negative

    def get_score(self):
        # method of getting a player's score

        return self.total_score()

    def red(self):
        '''tallies up score for reds'''

        global BONUS_RED

        self._window.remove(self._print_red_score)
        self._window.remove(self._print_tot_num)

        if self._red['red'] < 2:
            self._red['red'] += 1

            if self._red['red'] == 2:
                self._columns_filled.append('red')

                if BONUS_RED == 0:
                    self._bonus += 1
                    BONUS_RED = 1

        else:                   #checks to see if column has extra (minus points)
            self._negative += 2


        #prints the updated score
        self._print_red_score = Text(self._window, str(self._red['red']), 10, self._position3)
        self._print_tot_num = Text(self._window, str(self.get_score()), 12, self._position21)
        self._print_red_score.set_depth(2)
        self._print_tot_num.set_depth(2)
        self._window.add(self._print_red_score)
        self._window.add(self._print_tot_num)

    def blue(self):
        '''tallies up score for blues'''

        global BONUS_BLUE

        self._window.remove(self._print_blue_score)
        self._window.remove(self._print_tot_num)

        if self._blue['blue'] < 3:
            self._blue['blue'] += 1

            if self._blue['blue'] == 3:
                self._columns_filled.append('blue')

                if BONUS_BLUE == 0:
                    self._bonus += 1
                    BONUS_BLUE = 1

        else:                   #checks to see if column has extra (minus points)
            self._negative += 2

        #prints the updated score
        self._print_blue_score = Text(self._window, str(self._blue['blue']), 10, self._position4)
        self._print_tot_num = Text(self._window, str(self.get_score()), 12, self._position21)
        self._print_blue_score.set_depth(2)
        self._print_tot_num.set_depth(2)
        self._window.add(self._print_blue_score)
        self._window.add(self._print_tot_num)

    def green(self):
        '''tallies up score for greens'''

        global BONUS_GREEN

        self._window.remove(self._print_green_score)
        self._window.remove(self._print_tot_num)

        if self._green['green'] < 4:
            self._green['green'] += 1

            if self._green['green'] == 4:
                self._columns_filled.append('green')

                if BONUS_GREEN == 0:
                    self._bonus += 1
                    BONUS_GREEN = 1

        else:                   #checks to see if column has extra (minus points)
            self._negative += 2

        #prints the updated score
        self._print_green_score = Text(self._window, str(self._green['green']), 10, self._position5)
        self._print_tot_num = Text(self._window, str(self.get_score()), 12, self._position21)
        self._print_green_score.set_depth(2)
        self._print_tot_num.set_depth(2)
        self._window.add(self._print_green_score)
        self._window.add(self._print_tot_num)

    def orange(self):
        '''tallies up score for oranges'''

        global BONUS_ORANGE

        self._window.remove(self._print_orange_score)
        self._window.remove(self._print_tot_num)

        if self._orange['orange'] < 5:
            self._orange['orange'] += 1

            if self._orange['orange'] == 5:
                self._columns_filled.append('orange')

                if BONUS_ORANGE == 0:
                    self._bonus += 1
                    BONUS_ORANGE = 1

        else:                   #checks to see if column has extra (minus points)
            self._negative += 2

        #prints the updated score
        self._print_orange_score = Text(self._window, str(self._orange['orange']), 10, self._position6)
        self._print_tot_num = Text(self._window, str(self.get_score()), 12, self._position21)
        self._print_orange_score.set_depth(2)
        self._print_tot_num.set_depth(2)
        self._window.add(self._print_orange_score)
        self._window.add(self._print_tot_num)

    def purple(self):
        '''tallies up score for purples'''

        global BONUS_PURPLE

        self._window.remove(self._print_purple_score)
        self._window.remove(self._print_tot_num)

        if self._purple['purple'] < 6:
            self._purple['purple'] += 1

            if self._purple['purple'] == 5:
                self._columns_filled.append('purple')

                if BONUS_PURPLE == 0:
                    self._bonus += 2
                    BONUS_PURPLE = 1

        else:                   #checks to see if column has extra (minus points)
            self._negative += 2

        #prints the updated score
        self._print_purple_score = Text(self._window, str(self._purple['purple']), 10, self._position7)
        self._print_tot_num = Text(self._window, str(self.get_score()), 12, self._position21)
        self._print_purple_score.set_depth(2)
        self._print_tot_num.set_depth(2)
        self._window.add(self._print_purple_score)
        self._window.add(self._print_tot_num)

    def coin(self):
        '''tallies up score for coins'''

        self._window.remove(self._print_coin_score)
        self._window.remove(self._print_tot_num)

        self._coin['coin'] += 1

        if self._coin['coin'] == 3:
            self._negative -= 1

        if self._coin['coin'] == 5:
            self._negative -= 1

        if self._coin['coin'] == 7:
            self._negative -= 1

        #prints the updated score
        self._print_coin_score = Text(self._window, str(self._coin['coin']), 10, self._position8)
        self._print_tot_num = Text(self._window, str(self.get_score()), 12, self._position21)
        self._print_coin_score.set_depth(2)
        self._print_tot_num.set_depth(2)
        self._window.add(self._print_coin_score)
        self._window.add(self._print_tot_num)

    def check_winner(self):
        '''Checks to see if a player has won by looking at length
        of _columns_filled'''

        if len(self._columns_filled) >= 4:
            self._game.end_game()

    def draw_scorecard(self):
        # method of updating scorecards on the bottom of the screen

        self._body = Rectangle(self._window, 200, 175, self._position)
        self._player_name = Text(self._window, self._name, 12, self._position1)
        self._print_tot_score = Text(self._window, "Total Score:", 10, self._position2)
        self._print_red = Text(self._window, "Red:         out of 2", 10, self._position3)
        self._print_blue = Text(self._window, "Blue:       out of 3", 10, self._position4)
        self._print_green = Text(self._window, "Green:     out of 4", 10, self._position5)
        self._print_purple = Text(self._window, "Purple:    out of 6", 10, self._position7)
        self._print_orange = Text(self._window, "Orange:   out of 5", 10, self._position6)
        self._print_coins = Text(self._window, "Coins:     out of 7", 10, self._position8)
        self._print_red_score = Text(self._window, str(self._red['red']), 10, self._position3)
        self._print_blue_score = Text(self._window, str(self._blue['blue']), 10, self._position4)
        self._print_green_score = Text(self._window, str(self._green['green']), 10, self._position5)
        self._print_orange_score = Text(self._window, str(self._orange['orange']), 10, self._position6)
        self._print_purple_score = Text(self._window, str(self._purple['purple']), 10, self._position7)
        self._print_tot_num = Text(self._window, str(self.get_score()), 12, self._position21)
        self._print_coin_score = Text(self._window, str(self._coin['coin']), 10, self._position8)



        # self._print_scores = Text(self._window, self._red /n self._blue, 10, self._position)
        # self._green /n self._orange /n self._purple /n self._score, 10, self._position)

        self._body.set_depth(10)
        self._player_name.set_depth(5)
        self._print_tot_score.set_depth(5)
        self._print_red.set_depth(5)
        self._print_blue.set_depth(5)
        self._print_green.set_depth(5)
        self._print_purple.set_depth(5)
        self._print_orange.set_depth(5)
        self._print_coins.set_depth(5)
        self._print_red_score.set_depth(5)
        self._print_blue_score.set_depth(5)
        self._print_green_score.set_depth(5)
        self._print_orange_score.set_depth(5)
        self._print_purple_score.set_depth(5)
        self._print_coin_score.set_depth(5)
        self._print_tot_num.set_depth(5)

        self._window.add(self._body)
        self._window.add(self._player_name)
        self._window.add(self._print_red)
        self._window.add(self._print_tot_score)
        self._window.add(self._print_blue)
        self._window.add(self._print_green)
        self._window.add(self._print_purple)
        self._window.add(self._print_orange)
        self._window.add(self._print_coins)
        self._window.add(self._print_red_score)
        self._window.add(self._print_blue_score)
        self._window.add(self._print_green_score)
        self._window.add(self._print_orange_score)
        self._window.add(self._print_purple_score)
        self._window.add(self._print_coin_score)
        self._window.add(self._print_tot_num)

    def bold(self):
        '''highlights the player who is up'''

        self._body.set_fill_color("gold")
        self._window.add(self._body)

    def unbold(self):
        '''unhighlights the player who finished'''

        self._body.set_fill_color("white")
        self._window.add(self._body)


class Button(EventHandler):
    #generic button class that connects a button to an external method
    #when clicked the button will call a specific method.

    def __init__(self, window, text, external_method, height, width, position, color):
        '''constructor for button class'''

        self._window = window
        self._text = text
        self._method = external_method
        self._height = height
        self._width = width
        self._position = position
        self._color = color

        self._body = Rectangle(self._window, self._height, self._width, self._position)
        self._label = Text(self._window, self._text, 12, self._position)

        self._body.set_fill_color(self._color)
        self._body.set_depth(3)
        self._label.set_depth(2)

        self._body.add_handler(self)
        self._label.add_handler(self)

        self._window.add(self._body)
        self._window.add(self._label)


    def handle_mouse_press(self, event):
        #calls _method when clicked
        self._method()


class Board(EventHandler):
    '''Class for the Board'''

    def __init__(self, game, win, xc, yc, size, num_players):
        '''Constructor method for the class Board'''

        self._game = game
        self._window = win
        self._xc = xc
        self._yc = yc
        self._size = size

        self._turn = 0

        self._num_players = num_players

        self._player1 = Player(self, self._window, 100, 600, "Player1")
        self._player2 = Player(self, self._window, 350, 600, "Player2")

        self._players = [self._player1, self._player2]

        #if there are more than two players, adds them to the game
        if self._num_players >= 3:
            self._player3 = Player(self, self._window, 600, 600, "Player3")
            self._players.append(self._player3)

            if self._num_players == 4:
                self._player4 = Player(self, self._window, 850, 600, "Player4")
                self._players.append(self._player4)

        self._players[self._turn].highlight()

        #Trucks
        self._truck1 = Truck(self, self._window, 100, (100, 100))
        self._truck2 = Truck(self, self._window, 100, (100, 200))
        self._truck3 = Truck(self, self._window, 100, (100, 300))

        self._truck_list = [self._truck1, self._truck2, self._truck3]

        if self._num_players > 2:
            self._truck4 = Truck(self, self._window, 100, (100, 400))
            self._truck_list.append(self._truck4)

        #dice
        self._dice1 = Dice(self, self._window, "dice1", 465, 250)
        self._dice2 = Dice(self, self._window, "dice2", 535, 250)

        #draws the two dice at each round
        self._dice1.draw_dice()
        self._dice2.draw_dice()

        #counter to see if the player has rolled yet
        self._roll_count = 0

        #counter to see players left in round
        self._players_left = 0

        #counter to see if any spots are available to place dice
        self._no_spots_left = 0

        #counter to see if there are any tiles placed
        self._no_tiles_placed = 1

        #check to see if player has rolled yet
        self._roll_eligible = 0

        #buttons
        self._roll_button = Button(self._window, "Roll", self.roll, 100, 75, (500, 100), "forestgreen")
        self._collect_truck1 = Button(self._window, "Truck1", self.truck1, 100, 100, (350, 100), "gold")
        self._collect_truck2 = Button(self._window, "Truck2", self.truck2, 100, 100, (350, 200), "gold")
        self._collect_truck3 = Button(self._window, "Truck3", self.truck3, 100, 100, (350, 300), "gold")

        if self._num_players > 2:
            self._collect_truck4 = Button(self._window, "Truck4", self.truck4, 100, 100, (350, 400), "gold")

        self._end_turn = Button(self._window, "End Turn", self.next_turn, 100, 75, (500, 400), "firebrick")

    def get_turn(self):
        return self._turn

    def roll(self):
        #method to roll the dice at beginning of turn

        if self._roll_eligible == 0:

            self._players_left = 0        #if last player left in round, can't roll dice

            for num in range(len(self._players)):
                self._players_left += self._players[num].get_turn_value()

            #counter to see if no spaces are left to collect
            empty_set_counter = 0
            self._no_tiles_placed = 1

            for trucks in range(len(self._truck_list)):
                if self._truck_list[trucks].check_empty() is False:
                    empty_set_counter += 1

            # If there are no spaces to collect and only one player left in round,
            # allows player to roll the dice one time.
            if empty_set_counter == len(self._truck_list):
                self._players_left = 0
                self._roll_count = 0
                self._no_tiles_placed = 0

            # counters to see if there are < 2 spaces to place dice
            one_left_counter = 0
            self._no_spots_left = 0

            for trucks in range(len(self._truck_list)):
                one_left_counter += self._truck_list[trucks].check_one_left()

            # if there are no spaces to place any dice, doesn't let you roll dice
            if one_left_counter >= (len(self._truck_list) * 3) - 1:
                self._roll_count = 0
                self._no_spots_left = 1

            if self._players_left < len(self._players) - 1:
                if self._roll_count == 0:
                    if self._no_spots_left == 0:
                        if self._dice1.get_dice_color() == "white":
                            if self._dice2.get_dice_color() == "white":
                                self._dice1.roll_dice()
                                self._dice2.roll_dice()
                                self._roll_count = 1
                                self._roll_eligible = 1
                                self._no_tiles_placed = 1

    def truck1(self):
        #method of collecting the dice from truck1

        if self._roll_count == 0 or self._no_spots_left == 1 or \
        self._no_tiles_placed == 0:
            if self._truck1.check_empty() is True:
                self._truck1.collect()
                self._players[self._turn].round_end()
                self._roll_count = 1
                self._no_spots_left = 0
                self.next_turn()

    def truck2(self):
        #method of collecting the dice from truck2

        if self._roll_count == 0 or self._no_spots_left == 1 or \
        self._no_tiles_placed == 0:
            if self._truck2.check_empty() is True:
                self._truck2.collect()
                self._players[self._turn].round_end()
                self._roll_count = 1
                self._no_spots_left = 0
                self.next_turn()

    def truck3(self):
        #method of collecting the dice from truck3

        if self._roll_count == 0 or self._no_spots_left == 1 or \
        self._no_tiles_placed == 0:
            if self._truck3.check_empty() is True:
                self._truck3.collect()
                self._players[self._turn].round_end()
                self._roll_count = 1
                self._no_spots_left = 0
                self.next_turn()

    def truck4(self):
        #method of collecting the dice from truck3

        if self._roll_count == 0 or self._no_spots_left == 1 or \
        self._no_tiles_placed == 0:
            if self._truck4.check_empty() is True:
                self._truck4.collect()
                self._players[self._turn].round_end()
                self._roll_count = 1
                self._no_spots_left = 0
                self.next_turn()

    def add_to_truck1(self, x, color, name):
        '''add to the boxes in truck 1'''

        if x == 0:
            self._truck1.change_box1(color, name)
        elif x == 1:
            self._truck1.change_box2(color, name)
        elif x ==2:
            self._truck1.change_box3(color, name)

    def add_to_truck2(self, x, color, name):
        '''add to boxes in truck 2'''

        if x == 0:
            self._truck2.change_box1(color, name)
        elif x == 1:
            self._truck2.change_box2(color, name)
        elif x ==2:
            self._truck2.change_box3(color, name)

    def add_to_truck3(self, x, color, name):
        '''add to the boxes in truck 3'''

        if x == 0:
            self._truck3.change_box1(color, name)
        elif x == 1:
            self._truck3.change_box2(color, name)
        elif x ==2:
            self._truck3.change_box3(color, name)

    def add_to_truck4(self, x, color, name):
        '''add to boxes in truck 4'''

        if x == 0:
            self._truck4.change_box1(color, name)
        elif x == 1:
            self._truck4.change_box2(color, name)
        elif x ==2:
            self._truck4.change_box3(color, name)

    def change_dice1(self):
        '''changes dice1 color after it gets moved'''

        self._dice1.change_to_white()

    def change_dice2(self):
        '''changes dice1 color after it gets moved'''

        self._dice2.change_to_white()

    def pass_color(self, color):
        '''pass color from truck to scorecard'''
        self._players[self._turn].add_score(color)

    def next_turn(self):
        #Switches it to the next eligble player for the round

        self._roll_eligible = 0

        # checks to see if the player has rolled or collected truck
        if self._roll_count == 1:

            if self._players_left < len(self._players) - 1:

                if self._no_spots_left == 0:

                    if self._dice1.get_dice_color() == "white" and self._dice2.get_dice_color() == "white":

                        players_left = 0        #if last player, can't roll dice

                        self._players[self._turn].unhighlight()
                        self._roll_count = 0

                        counter = 0

                        #Changes to next player by adding 1 to turn, or if it's last player's
                        #turn it will set it to player one's turn. If the player hasn't taken
                        #a truck this round it will break the for loop and they play, otherwise
                        #it will loop through all the players to see if anyone still has a turn.
                        for _ in range(len(self._players)):
                            if self._turn + 1 < len(self._players):
                                self._turn += 1

                                if self._players[self._turn].get_turn_value() == 0:
                                    counter = 0
                                    break
                                else:
                                    counter += 1

                            else:
                                self._turn = 0

                                if self._players[self._turn].get_turn_value() == 0:
                                    counter = 0
                                    break
                                else:
                                    counter += 1

                        #if no players have a turn left, it will move to the next round
                        if counter >= len(self._players) - 1:

                            for player in range(len(self._players)):
                                self._players[player].new_round()

                            if self._turn + 1 < len(self._players):
                                self._turn += 1
                            else:
                                self._turn = 0

                            counter = 0

                        self._players[self._turn].highlight()

    def end_game(self):
        '''calls tally score to get players' final scores and calculate winner'''

        score = 0

        for player in range(len(self._players)):

            if self._players[player].tally_scores() > score:
                score = self._players[player].tally_scores()
                winner = self._players[player].get_player_name()

        self._end_winner = Text(self._window, str(winner), 30, (500, 600))
        self._end_text = Text(self._window, "The Winner is:", 30, (500, 400))
        self._end_body = Rectangle(self._window, 1000, 1000, (500, 500))

        self._end_winner.set_depth(1)
        self._end_text.set_depth(1)
        self._end_body.set_depth(1)

        self._end_body.set_fill_color("blue")

        self._window.add(self._end_winner)
        self._window.add(self._end_text)
        self._window.add(self._end_body)


class Game(EventHandler):
    '''Class for Game'''

    def __init__(self, win, num_players):
        '''Constructor method for the class Game'''

        self._window = win
        self._my_board = Board(self, self._window, 500, 500, 500, num_players)



    def handle_mouse_press(self, event):
        """ This code runs when the user clicks on this graphical object. """




def main(window):
    """ The main function. """

    # Some graphics window setup:
    window.set_background('honeydew')
    window.set_width(1000)
    window.set_height(1000)

    print('Enter Number of players between 2-4: ')
    num_players = int(input())


    my_game = Game(window, num_players)


if __name__ == '__main__':
    StartGraphicsSystem(main)
