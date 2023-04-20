from game import Gameboard, Felder, Figure, Player 


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
    
    def start_play(self, data):
        pass