from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room
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
        self.playerDict = {}
        self.playerturn = 0
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
            self.playerDict[player.get_sid] = player

        
        
    def start(self):
        #choose current player
        player = self.playerturn % len(self.player_sid)
        #for next move
        self.playerturn +=1
        self.cur_player = list(self.player_sid)[player]
        return self.cur_player
        
    def start_play(self, data):
        data_room = json.loads(data)
        print(data_room)
        pass

    def game_move(self, sid, field_number):
        number = self.get_cur_dice
        player = self.playerDict[sid]
        field = self.get_gameboard.get_field(field_number)
        if self.check_move(player, field, number):
            return True
        return False
    
    def check_move(self, player, old_field, number):
        #check feld mit eigener figur
            #check ist feld ein homefeld
                #check hat er ne 6 und ist startfeld nicht mit eigener figur
                    #mach move
            #check feld ist nicht homefeld
                #check schritte + number > 40 and < 45
                    #achtung zielbereich  
                #check feld + number ist nicht mit eigener figur belegt
                    #mach move
        if old_field.get_color_on_field == player.get_color:
            if old_field.get_id in player.get_home_fields:
                if number == 6 and list(player.get_starting_field.values())[0].get_color_on_field != player.get_color:
                    newfield = list(player.get_starting_field.values())[0]
                    self.make_move(old_field, newfield, number)
            else:
                if old_field.get_figure_on_field.get_position + number > 40 and old_field.get_figure_on_field.get_position + number < 45:
                    if old_field.get_figure_on_field.get_position + number < 44 or list(player.get_finish_fields.values())[3].get_color_on_field != 0:
                        if old_field.get_figure_on_field.get_position + number < 43 or list(player.get_finish_fields.values())[2].get_color_on_field != 0:
                            if old_field.get_figure_on_field.get_position + number < 42 or list(player.get_finish_fields.values())[1].get_color_on_field != 0:
                                if list(player.get_finish_fields.values())[0].get_color_on_field != 0:
                                    newfield = list(player.get_finish_fields.values())[old_field.get_figure_on_field.get_position + number - 41]
                                    self.make_move(old_field, newfield, number)
                else:
                    if old_field.get_id + number > 89:
                        newfield = self.gameboard.get_field_dict.get(old_field.get_id + number - 40)
                        self.make_move(old_field, newfield, number)

    def make_move(self, old_field, new_field, number):
        cur_figure = old_field.get_figure_on_field
        if new_field.get_color_on_field == 0:
            old_field.set_color_on_field(0)
            new_field.set_color_on_field(cur_figure.get_color)
            cur_figure.set_on_field(new_field)
            cur_figure.walk(number)
        else:
            new_field.get_figure_on_field.set_home(self.gameboard.get_field_dict)
            new_field.set_figure_on_field(old_field.get_figure_on_field)
            old_field.figure_away()
        return True



    #setter
    def set_waiting(self, bool):
        self.waiting = bool
    def set_cur_dice(self, number):
        self.cur_dice = number

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