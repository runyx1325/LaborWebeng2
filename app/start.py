import json
from Gameboard import Gameboard
from Figure import Figure
from Player import Player
from Field import Field

class Mensch():
    def __init__(self, data, settings_endgame):
        # data_room := dict with room data
        # waiting := is True if somebody making a move till player finsished move
        # player_sid := list with sid of players
        # playerlist := list with player objects
        # player_dict:= dict with player objects and socket ids
        # gameboard := gameboard object for this game
        # playerturn := current player
        # counter_bad_moves := count how often the player can not move in one turn
        # cur_dice := current rolled dice number

        self.data_room = json.loads(data)
        self.waiting = False
        self.player_sid = self.data_room.keys()
        self.playerlist = []
        self.player_dict = {}
        self.playerturn = 0
        self.counter_bad_moves = 0
        self.cur_dice = "default"

        # create all players
        if len(self.player_sid) == 4:
            orderFour = [1, 4, 2, 3]
            i = 0
            for sid in self.player_sid:               
                self.player_nickname = self.data_room[sid]
                self.playerlist.append(Player(sid, self.player_nickname, orderFour[i]))
                i += 1
        else: 
            color = 1
            for sid in self.player_sid:
                #save nickname from data_room dict
                self.player_nickname = self.data_room[sid]
                player = Player(sid, self.player_nickname, color)
                self.playerlist.append(player)
                color += 1
        # create gameboard with playerlist
        self.gameboard = Gameboard(self.playerlist)

        # initialize special fields of every player
        for player in self.playerlist:
            player.set_fields(self.gameboard.get_field_dict)
            self.player_dict[player.get_sid] = player

        # Test purposes if settings_endgame is True
        if settings_endgame:
            for player in self.playerlist:
                player.set_endgame()
    


    # get the current player in order
    def start(self):
        player = self.playerturn % len(self.player_sid)
        self.playerturn +=1
        self.cur_player = list(self.player_sid)[player]
        return self.cur_player



    # check possible moves
    def get_possible_moves(self, sid):
        number = self.get_cur_dice
        player = self.player_dict[sid]
        player.clear_possible_moves()
        empty_home = player.empty_home()
        empty_start = player.empty_start()
        
        if int(number) == 6:
            # rolled a 6
            if not empty_home:
                # home is not empty
                if not empty_start:
                    # starting field is not empty
                    # move figure at start field
                    old_field = list(player.get_starting_field.values())[0]
                    # if move is not possible, function returns occupied field
                    if self.check_is_move_possible(old_field, number, player) == True:
                        # calculate new field with old field and dice number
                        new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                        figure = old_field.get_figure_on_field
                        # add figure and calculated new field to possible moves
                        player.add_possible_move(figure, new_field)
                        return player.get_possible_moves
                    
                    else:
                        # old field is now occupied field
                        old_field = self.check_is_move_possible(old_field, number, player)
                        # if move is not possible, function returns occupied field
                        if self.check_is_move_possible(old_field, number, player) == True:
                            # calculate new field with old field and dice number
                            new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                            figure = old_field.get_figure_on_field
                            # add figure and calculated new field to possible moves
                            player.add_possible_move(figure, new_field)
                            return player.get_possible_moves
                        
                        else:
                            # old field is now occupied field
                            old_field = self.check_is_move_possible(old_field, number, player)
                            # if move is not possible, function returns occupied field
                            if self.check_is_move_possible(old_field, number, player) == True:
                                # calculate new field with old field and dice number
                                new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                                figure = old_field.get_figure_on_field
                                # add figure and calculated new field to possible moves
                                player.add_possible_move(figure, new_field)
                                return player.get_possible_moves
                            
                            return player.get_possible_moves
                        
                else:
                    # starting field is empty
                    # all figures in home can move
                    for home_field in list(player.get_home_fields.values()):
                        if home_field.get_color_on_field != 0:
                            # new field is starting field
                            new_field = list(player.get_starting_field.values())[0]
                            figure = home_field.get_figure_on_field
                            # add figure and new field to possible moves
                            player.add_possible_move(figure, new_field)

                    return player.get_possible_moves
                
            else:
                # home is empty
                for figure in list(player.get_team_dict.values()):
                    old_field = figure.get_on_field
                    # if steps < 35 new field is not in finish
                    if figure.get_steps < 35:
                        if self.check_is_move_possible(old_field, number, player) == True:
                            # if new field id is > 89, substract 40
                            if old_field.get_id + number > 89:
                                new_field = self.gameboard.get_field_dict.get(old_field.get_id + number - 40)

                            # else calculate new field with dice number
                            else:
                                new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)

                            figure = old_field.get_figure_on_field
                            # add figure and new field to possible moves
                            player.add_possible_move(figure, new_field)

                    # elif steps < 39 new field is in finish
                    elif figure.get_steps < 39:
                        x = int(number)
                        # loop to check is new field blocked or fields in finish before
                        while figure.get_steps + x > 40:
                            if self.check_is_move_possible(old_field, x, player) == True:
                                x -= 1
                                # if all fields till 40 are not occupied, move is possible
                                if figure.get_steps + x == 40:
                                    new_field = list(player.get_finish_fields.values())[old_field.get_figure_on_field.get_steps + number - 41]
                                    figure = old_field.get_figure_on_field
                                    # add figure and new field to possible moves
                                    player.add_possible_move(figure, new_field)

                            else:
                                # cancel loop if one finish field is occupied
                                break

                return player.get_possible_moves
        else:
            # rolled no 6
            if player.in_home() != 4:
                # not all figures are in home               
                if not empty_home and not empty_start:
                    # home and start field are not empty
                    # move figure at start field
                    old_field = list(player.get_starting_field.values())[0]
                    # if move is not possible, function returns occupied field
                    if self.check_is_move_possible(old_field, number, player) == True:
                        # calculate new field with old field and dice number
                        new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                        figure = old_field.get_figure_on_field
                        # add figure and calculated new field to possible moves
                        player.add_possible_move(figure, new_field)
                        return player.get_possible_moves    
                    
                    else:
                        old_field = self.check_is_move_possible(old_field, number, player)
                        # if move is not possible, function returns occupied field
                        if self.check_is_move_possible(old_field, number, player) == True:
                            # calculate new field with old field and dice number
                            new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                            figure = old_field.get_figure_on_field
                            # add figure and calculated new field to possible moves
                            player.add_possible_move(figure, new_field)
                            return player.get_possible_moves
                        
                        else:
                            old_field = self.check_is_move_possible(old_field, number, player)
                            # if move is not possible, function returns occupied field
                            if self.check_is_move_possible(old_field, number, player) == True:
                                # calculate new field with old field and dice number
                                new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                                figure = old_field.get_figure_on_field
                                # add figure and calculated new field to possible moves
                                player.add_possible_move(figure, new_field)
                                return player.get_possible_moves
                            
                            return player.get_possible_moves
                        
                elif empty_home or (not empty_home and empty_start):
                    # home is empty or (home is not empty but start is empty)
                    # iterate over all figures
                    for figure in list(player.get_team_dict.values()):  
                        # ignore figures in home       
                        if figure.get_steps != 0:
                            old_field = figure.get_on_field
                            # if steps + number < 41 not in finish
                            if figure.get_steps + number < 41:
                                if self.check_is_move_possible(old_field, number, player) == True:
                                    # if new field id is > 89, substract 40
                                    if old_field.get_id + number > 89:
                                        new_field = self.gameboard.get_field_dict.get(old_field.get_id + number - 40)
                                    # else calculate new field with dice number
                                    else:    
                                        new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                                    
                                    figure = old_field.get_figure_on_field
                                    # add figure and calculated new field to possible moves
                                    player.add_possible_move(figure, new_field)

                            # elif steps > 40 and steps + number < 45 moving figure in finish
                            elif figure.get_steps > 40:
                                if figure.get_steps + number < 45:
                                    x = 1
                                    # loop to check is next field occupied till new field
                                    while figure.get_steps + x <= figure.get_steps + number:
                                        if self.check_is_move_possible(old_field, x, player):
                                            x += 1
                                            # if all fields are checked move is possible
                                            if x > number:
                                                new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                                                figure = old_field.get_figure_on_field
                                                # add figure and calculated new field to possible moves
                                                player.add_possible_move(figure, new_field)

                                        else:
                                            break

                            # if steps + number > 40 and < 45 new field in finish
                            elif figure.get_steps + number > 40 and figure.get_steps + number < 45:
                                x = int(number)
                                # loop to check is new field or fields before in finish occupied
                                while figure.get_steps + x > 40:
                                    if self.check_is_move_possible(old_field, x, player):
                                        x -= 1
                                        # if all fields till 40 are not occupied, move is possible
                                        if figure.get_steps + x == 40:
                                            y = figure.get_steps + number - 41
                                            new_field = list(player.get_finish_fields.values())[y]
                                            figure = old_field.get_figure_on_field
                                            # add figure and calculated new field to possible moves
                                            player.add_possible_move(figure, new_field)

                                    else:
                                        break

                    return player.get_possible_moves
            return player.get_possible_moves



    # check is move possible with old field, dice number and player
    def check_is_move_possible(self, old_field, number, player):
        #checking is new_field occupied
        #return occupied field or true
        new_steps = old_field.get_figure_on_field.get_steps + number
        # if old field is home field from player
        if old_field.get_id in player.get_home_fields:
            # new field is starting field
            new_field = list(player.get_starting_field.values())[0]

        else:
            # if new_steps > 40, new field is finish field
            if new_steps > 40:
                x = new_steps - 41
                new_field = list(player.get_finish_fields.values())[x]
                # if new_field occupied return False
                if new_field.get_color_on_field == player.get_color:
                    return False
                
            else:
                # if new field id is > 89, substract 40
                if old_field.get_id + number > 89:
                    new_field = self.gameboard.get_field_dict.get(old_field.get_id + number - 40)
                # else calculate new field with dice number
                else:
                    new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)

        # if new_field is not occupied return True
        if new_field.get_color_on_field != old_field.get_color_on_field:
            return True
        # else return occupied field
        return new_field



    # check if choosen figure is moveable
    def game_move(self, sid, field_number):     
        number = self.get_cur_dice
        player = self.player_dict[sid]
        old_field = self.get_gameboard.get_field(field_number)
        figure = old_field.get_figure_on_field

        # if correct  player choosed the figure
        if figure.get_color == player.get_color:   
            # check is figure in possible moves dictionary 
            if figure.get_nr in player.get_possible_moves:
                new_field = player.get_possible_moves[figure.get_nr]
                # make move
                if self.make_move(old_field, new_field, number):

                    return True
                
                return True
            
        return False



    # make move update figures and fields
    def make_move(self, old_field, new_field, number):
        cur_figure = old_field.get_figure_on_field
        # if new field is empty
        if new_field.get_color_on_field == 0:
            old_field.figure_away()
            cur_figure.set_on_field(new_field)
            cur_figure.walk(number)
            return True
        
        # else if new field occupied by enemy
        else:
            new_field.get_figure_on_field.set_home(self.gameboard.get_field_dict)
            new_field.set_figure_on_field(cur_figure)
            old_field.figure_away()
            cur_figure.walk(number)
            return True



    # count 1 higher if no move is possible
    def update_counter_bad_moves(self):
            self.counter_bad_moves += 1


    # when player is again
    def again(self):
        self.playerturn -= 1



    #setter
    def set_waiting(self, bool):
        self.waiting = bool
    def set_cur_dice(self, number):
        self.cur_dice = int(number)
    def set_counter_bad_moves(self):
        self.counter_bad_moves = 0

    #getter
    @property
    def get_gameboard(self):
        return self.gameboard
    @property
    def get_waiting(self):
        return self.waiting
    @property
    def get_cur_player(self):
        return self.cur_player
    @property 
    def get_cur_dice(self):
        return self.cur_dice
    @property
    def get_player_dict(self):
        return self.player_dict  
    @property
    def get_counter_bad_moves(self):
        return self.counter_bad_moves
    # check if 1 player finished the game
    @property
    def get_winner(self):
        if self.gameboard.get_finished:
            for player in self.player_dict.values():
                if player.get_finish:
                    self.winner = player
        return self.winner