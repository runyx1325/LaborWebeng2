import random, json
from Gameboard import Gameboard
from Figure import Figure
from Player import Player
from Field import Field

class Mensch():
    def __init__(self, data):
        #data_room := dict with room data
        #waiiting := is True if somebody making a move till player finsished move
        #player_sid := list with sid of players
        #playerlist := list with player objects
        #gameboard := gameboard object for this game
        #playerturn := current player
        self.data_room = json.loads(data)
        self.waiting = False
        self.player_sid = self.data_room.keys()
        self.playerlist = []
        self.player_dict = {}
        self.playerturn = 0
        self.counter_bad_moves = 0
        self.cur_dice = "default"
        

        i = 1
        if len(self.player_sid) == 4:
            orderFour = [1, 4, 2, 3]
            i = 0
            for sid in self.player_sid:               
                self.player_nickname = self.data_room[sid]
                self.playerlist.append(Player(sid, self.player_nickname, orderFour[i]))
                i += 1
        else: 
            for sid in self.player_sid:
                #save nickname from data_room dict
                self.player_nickname = self.data_room[sid]
                player = Player(sid, self.player_nickname, i)
                self.playerlist.append(player)
                i += 1
        self.gameboard = Gameboard(self.playerlist)

        for player in self.playerlist:
            player.set_fields(self.gameboard.get_field_dict)
            self.player_dict[player.get_sid] = player
        
    def start(self):
        #choose current player
        player = self.playerturn % len(self.player_sid)
        #for next move
        self.playerturn +=1
        self.cur_player = list(self.player_sid)[player]
        return self.cur_player

    def get_possible_moves(self, sid):
        number = self.get_cur_dice
        player = self.player_dict[sid]
        player.clear_possible_moves()
        empty_home = player.empty_home()
        empty_start = player.empty_start()
        
        
        if int(number) == 6:
            ##print("rolled a 6")
            if not empty_home:
                ##print("home is not empty")
                if not empty_start:
                    ##print("start is not empty")
                    old_field = list(player.get_starting_field.values())[0]
                    if self.check_is_move_possible(old_field, number, player) == True:#gibt true zurück wenn zug möglich und sonst field welches blockiert hat
                        new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                        figure = old_field.get_figure_on_field
                        player.add_possible_move(figure, new_field)
                        return player.get_possible_moves
                    else:
                        old_field = self.check_is_move_possible(old_field, number, player)
                        if self.check_is_move_possible(old_field, number, player) == True:
                            new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                            figure = old_field.get_figure_on_field
                            player.add_possible_move(figure, new_field)
                            return player.get_possible_moves
                        else:
                            old_field = self.check_is_move_possible(old_field, number, player)
                            if self.check_is_move_possible(old_field, number, player) == True:
                                new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                                figure = old_field.get_figure_on_field
                                player.add_possible_move(figure, new_field)
                                return player.get_possible_moves
                            ##print("nobody can move")
                            return player.get_possible_moves
                else:
                    ##print("start is empty")
                    #all figures in home can move
                    for home_field in list(player.get_home_fields.values()):
                        if home_field.get_color_on_field != 0:
                            new_field = list(player.get_starting_field.values())[0]
                            figure = home_field.get_figure_on_field
                            player.add_possible_move(figure, new_field)
                    return player.get_possible_moves
            else:
                ##print("home is empty")
                for figure in list(player.get_team_dict.values()):
                    old_field = figure.get_on_field
                    if figure.get_steps < 35:#landet nicht im zielbereich
                        if self.check_is_move_possible(old_field, number, player) == True:
                            new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                            figure = old_field.get_figure_on_field
                            player.add_possible_move(figure, new_field)
                    elif figure.get_steps < 39:#landen alle im zielbereich
                        x = int(number)
                        while figure.get_steps + x > 40:
                            if self.check_is_move_possible(old_field, x, player) == True:
                                x -= 1
                                if figure.get_steps + x == 40:
                                    new_field = list(player.get_finish_fields.values())[old_field.get_figure_on_field.get_steps + number - 41]
                                    ##print("neue ")
                                    #print(new_field.get_id)
                                    figure = old_field.get_figure_on_field
                                    player.add_possible_move(figure, new_field)
                            else:
                                break
                return player.get_possible_moves
        else:
            #print("No 6")
            if player.in_home() != 4:               
                if not empty_home and not empty_start:
                    ##print("home is not empty")
                    ##print("start is not empty")
                    old_field = list(player.get_starting_field.values())[0]
                    if self.check_is_move_possible(old_field, number, player) == True:#gibt true zurück wenn zug möglich und sonst field welches blockiert hat
                        new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                        figure = old_field.get_figure_on_field
                        player.add_possible_move(figure, new_field)
                        return player.get_possible_moves    
                    else:
                        old_field = self.check_is_move_possible(old_field, number, player)
                        if self.check_is_move_possible(old_field, number, player) == True:
                            new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                            figure = old_field.get_figure_on_field
                            player.add_possible_move(figure, new_field)
                            return player.get_possible_moves
                        else:
                            old_field = self.check_is_move_possible(old_field, number, player)
                            if self.check_is_move_possible(old_field, number, player) == True:
                                new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                                figure = old_field.get_figure_on_field
                                player.add_possible_move(figure, new_field)
                                return player.get_possible_moves
                            ##print("nobody can move")
                            return player.get_possible_moves
                elif empty_home or (not empty_home and empty_start):
                    ##print("home is empty or home is not empty but start is empty")
                    for figure in list(player.get_team_dict.values()):
                        print("----")
                        if figure.get_steps != 0:
                            old_field = figure.get_on_field
                            if figure.get_steps + number < 41:#landet nicht im zielbereich
                                if self.check_is_move_possible(old_field, number, player) == True:
                                    new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                                    figure = old_field.get_figure_on_field
                                    player.add_possible_move(figure, new_field)
                            elif figure.get_steps > 40:#bewegung im zielbereich
                                if figure.get_steps + number < 45:
                                    x = 1
                                    while figure.get_steps + x <= figure.get_steps + number:
                                        if self.check_is_move_possible(old_field, x, player):
                                            x += 1
                                            if x > number:
                                                new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
                                                figure = old_field.get_figure_on_field
                                                player.add_possible_move(figure, new_field)
                                        else:
                                            break
                            elif figure.get_steps + number > 40 and figure.get_steps + number < 45:#landet im zielbereich
                                x = int(number)
                                while figure.get_steps + x > 40:
                                    if self.check_is_move_possible(old_field, x, player):
                                        x -= 1
                                        if figure.get_steps + x == 40:
                                            y = figure.get_steps + number - 41
                                            new_field = list(player.get_finish_fields.values())[y]
                                            figure = old_field.get_figure_on_field
                                            player.add_possible_move(figure, new_field)
                                    else:
                                        break
                    return player.get_possible_moves
            return player.get_possible_moves
            
    def check_is_move_possible(self, old_field, number, player):
        #checking is new_field blocked
        #return blocked field or true
        new_steps = old_field.get_figure_on_field.get_steps + number
        if old_field.get_id in player.get_home_fields:
            new_field = list(player.get_home_field.values())[0]
        else:
            if new_steps > 40:
                x = new_steps - 41
                new_field = list(player.get_finish_fields.values())[x]
                if new_field.get_color_on_field == 1:
                    return False
            else:
                if old_field.get_id + number > 89:
                    new_field = self.gameboard.get_field_dict.get(old_field.get_id + number - 40)
                new_field = self.gameboard.get_field_dict.get(old_field.get_id + number)
        if new_field.get_color_on_field != old_field.get_color_on_field:
            return True
        return new_field

    def game_move(self, sid, field_number):     
        number = self.get_cur_dice
        player = self.player_dict[sid]
        old_field = self.get_gameboard.get_field(field_number)
        figure = old_field.get_figure_on_field

        if figure.get_nr in player.get_possible_moves:
            new_field = player.get_possible_moves[figure.get_nr]
            if self.make_move(old_field, new_field, number):
                return True
            return True
        return False

    def make_move(self, old_field, new_field, number):
        cur_figure = old_field.get_figure_on_field
        if new_field.get_color_on_field == 0:
            old_field.figure_away()
            cur_figure.set_on_field(new_field)
            cur_figure.walk(number)
            return True
        else:
            new_field.get_figure_on_field.set_home(self.gameboard.get_field_dict)
            new_field.set_figure_on_field(old_field.get_figure_on_field)
            old_field.figure_away()
            return True

    def update_counter_bad_moves(self):
            self.counter_bad_moves += 1
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