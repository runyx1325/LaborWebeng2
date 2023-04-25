from Player import Player
from Field import Field

class Gameboard():
    def __init__(self, playerList):
        #playerlist := list of player objects
        #gameboard := at the beginning get the startinggameboard
        #gamestatus := True if game is running
        #gamefinished := True if game is finished
        #playerCount := number of players
        #Das Spiel weiß immer, wer gerade dran ist und wer der nächste ist
        
        self.playerList = playerList
        self.gameboard = self.startingGameboard()
        self.gameStatus = False
        self.gameFinished = False
        self.playerCount = len(playerList)

        self.start()

    def start(self):
        print("Gameboard start")
        self.gameStatus = True
        #iteration over playerList till the game is finished
        while self.gameStatus:
            i = 0
            for i in range(self.playerCount):
                print(type(self.playerList))
                print("Spieler: ", i ,"ist dran!")
                #spieler darf würfeln 
                
                #spieler darf person bewegen
                #spielbrett muss sich aktualisieren
                #nächster Spieler ist dran
            self.gameStatus =False
            #TODO
            if i == self.playerCount and self.gameStatus == True:
                i = 0
            if self.checkGameStatus:
                #Game finished
                pass

    def startingGameboard(self):
        #creates gameboard at the beginning
        #all figures are at home
        #row0 = ['11', '11', '  ', '  ', '00', '00', '20', '  ', '  ', '22', '22'] 
        #row1 = ['11', '11', '  ', '  ', '00', '20', '00', '  ', '  ', '22', '22']
        #row2 = ['  ', '  ', '  ', '  ', '00', '20', '00', '  ', '  ', '  ', '  '] 
        #row3 = ['  ', '  ', '  ', '  ', '00', '20', '00', '  ', '  ', '  ', '  '] 
        #row4 = ['10', '00', '00', '00', '00', '20', '00', '00', '00', '00', '00'] 
        #row5 = ['00', '10', '10', '10', '10', '  ', '40', '40', '40', '40', '00'] 
        #row6 = ['00', '00', '00', '00', '00', '30', '00', '00', '00', '00', '40'] 
        #row7 = ['  ', '  ', '  ', '  ', '00', '30', '00', '  ', '  ', '  ', '  '] 
        #row8 = ['  ', '  ', '  ', '  ', '00', '30', '00', '  ', '  ', '  ', '  '] 
        #row9 = ['33', '33', '  ', '  ', '00', '30', '00', '  ', '  ', '44', '44'] 
        #row10= ['33', '33', '  ', '  ', '30', '00', '00', '  ', '  ', '44', '44']
        
        row0 = ['test']
        row1 = []
        row2 = []
        row3 = []
        row4 = []
        row5 = []
        row6 = []
        row7 = []
        row8 = []
        row9 = []
        row10= []
        gameboard = [row0, row1, row2, row3, row4, row5, row6, row7, row8, row9, row10]
        
        field_dict = {}
        #home and finish of all teams
        for team in range(1,5):
            for id in range(0,8):
                x = team*10+id
                field_dict[x] = Field(x, team)
        #create all nromal fields + starting fields
        for id in range(50,90):
            if id%10 == 0:
                if id%8 == 0:
                    field_dict[id] = Field(id, 3)
                elif id%7 == 0:
                    field_dict[id] = Field(id, 2)
                elif id%6 == 0:
                    field_dict[id] = Field(id, 4)
                elif id%5 == 0:
                    field_dict[id] = Field(id, 1)
            else:
                field_dict[id] = Field(id, 0)
        print(field_dict.keys())

        print("Gameboard created")
        return gameboard

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