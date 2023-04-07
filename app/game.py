import random, json

class Mensch():
    def __init__(self, data):
        self.player = data['player']
        self.playerDict = {}
        for player in data['playerList']:
            self.playerDict['player'] = Player()
        
        self.gameboard = self.startingGameboard()
        Gameboard(self.player, self.playerDict, self.gameboard)

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

class Felder():
    def __init__(self) -> None:
        self.id = id #bekommt jedes Feld und ist nicht die aktuelle Position für eine Figur
        self.color = color #ist eine Zahl für die Farbe des äußeren Rings

class Player():
    def __init__(self, nickname, color ):
        self.nickname = nickname
        self.color = color #kann integer sein für die entsprechende Farbe
        self.team = {}
        i = 1
        for i in range(4):
            self.team[i] = Figure(color, i)
            i += 1
        self.finish = False
    
    def finish(self):
        for figure in self.team:
            if figure.get_finish == False:
                return False
        self.finish = True
        return True
    
    @property
    def get_nickname(self):
        return self.nickname
    @property
    def get_color(self):
        return self.color
    @property
    def get_team(self):
        return self.team
    @property
    def get_finish(self):
        return self.finish


class Figure():
    def __init__(self, color, id):
        self.id = id #1, 2, 3, 4 mehr ids gibts nicht pro Team
        self.color = color #ist eine Zahl die für die Farbe innerhalb des Kreises verantwortlich ist
        self.home = True
        self.finish = False
        self.position = 0

    def home(self):
        if self.position == 0:
            self.home = True

    def finish(self):
        if self.position > 40:
            self.finish = True

    def walk(self, number):
        self.position = self.position + number
    
    @property
    def get_id(self):
        return self.id
    @property
    def get_color(self):
        return self.color
    @property
    def get_home(self):
        return self.home
    @property
    def get_finish(self):
        return self.finish
    @property
    def get_position(self):
        return self.position

class Gameboard():
    def __init__(self, player, playerList, startingGameboard):
        #Das Spielbrett enthält neben dem aktuellen Spielbrett immer die Spieleranzahl, sowie eine Liste aller Spieler.
        #Das Spiel weiß immer, wer gerade dran ist und wer der nächste ist
        self.number_of_player = player
        self.playerList = playerList
        self.gameboard = startingGameboard
        self.gameStatus = False
        self.gameFinished = False

    def start(self):
        self.gameStatus = True
        #iteration over playerList till the game is finished
        while self.gameStatus:
            i = 0
            for i in self.playerList:
                print("Spieler: "+ i + "ist dran!")
                #spieler darf würfeln 
                #spieler darf person bewegen
                #spielbrett muss sich aktualisieren
                #nächster Spieler ist dran
            
            if i == self.number_of_player and self.gameStatus == True:
                i = 0
            if self.checkGameStatus:
                #Game finished
                pass

    def checkGameStatus(self):
        for player in self.playerList:
            if player.get_finish == True:
                self.gameFinished = True
                self.gameStatus = False
                return True
        return False

    def updateGameboard(self, piece, number):
        #aktuelle position von piece mit number addieren
        #newposition check, ist auf dem Feld ein Gegner, niemand oder ein Mitspieler? Überspringe iich im eigenen Haus jemanden? Oder ist die Zahl zu groß?
        #broadcast an alle
        pass