
class Gameboard():
    def __init__(self, playerList, startingGameboard):
        #Das Spielbrett enthält neben dem aktuellen Spielbrett immer die Spieleranzahl, sowie eine Liste aller Spieler.
        #Das Spiel weiß immer, wer gerade dran ist und wer der nächste ist
        
        #self.number_of_player = player
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
            
            #TODO
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