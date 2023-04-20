from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import random, json
from Gameboard import Gameboard
from Figure import Figure
from Player import Player
from Felder import Felder



class Mensch():
    def __init__(self, data):
        data_room = json.loads(data)

        #auslesen aller Schlüssel
        self.player_sid = data_room['clients'].keys()
        i = 1   # zuweisen der Farbe der Figur
        playerlist = []
        for key in self.player_sid:
            #Nickname pro Schlüssel auslesen
            self.player_nickname = data_room['clients'][key]
            playerlist.append(Player(key, self.player_nickname, i))
            i += 1

        #1.Spieler auslesen
        player = list(data_room['clients'].keys())[0]
        self.gameboard = self.startingGameboard()

        # Gameboard erstellen
        Gameboard(player,playerlist, self.gameboard)


        #Start game
        #Mensch.start_play(data_room)

    def startingGameboard(self):
        
        row0 = ['11', '11', '  ', '  ', '00', '00', '20', '  ', '  ', '22', '22'] 
        row1 = ['11', '11', '  ', '  ', '00', '20', '00', '  ', '  ', '22', '22']
        row2 = ['  ', '  ', '  ', '  ', '00', '20', '00', '  ', '  ', '  ', '  '] 
        row3 = ['  ', '  ', '  ', '  ', '00', '20', '00', '  ', '  ', '  ', '  '] 
        row4 = ['10', '00', '00', '00', '00', '20', '00', '00', '00', '00', '00'] 
        row5 = ['00', '10', '10', '10', '10', '  ', '40', '40', '40', '40', '00'] 
        row6 = ['00', '00', '00', '00', '00', '30', '00', '00', '00', '00', '40'] 
        row7 = ['  ', '  ', '  ', '  ', '00', '30', '00', '  ', '  ', '  ', '  '] 
        row8 = ['  ', '  ', '  ', '  ', '00', '30', '00', '  ', '  ', '  ', '  '] 
        row9 = ['33', '33', '  ', '  ', '00', '30', '00', '  ', '  ', '44', '44'] 
        row10= ['33', '33', '  ', '  ', '30', '00', '00', '  ', '  ', '44', '44'] 
        gameboard = [row0, row1, row2, row3, row4, row5, row6, row7, row8, row9, row10]
        return gameboard
    
    def start_play(self, data):
        data_room = json.loads(data)
        print(data_room)
        pass