from Player import Player
from Field import Field

class Gameboard():
    def __init__(self, player_list):
        #player_list := list of player objects
        #gameboard := at the beginning get the startinggameboard
        #game_status := True if game is running
        #game_finished := True if game is finished
        #playerCount := number of players
        #Das Spiel weiß immer, wer gerade dran ist und wer der nächste ist
    
        self.player_list = player_list
        self.field_dict = self.create_gameboard()
        self.gameboard_for_view = self.get_view(self.field_dict)
        self.game_status = False
        self.game_finished = False
        self.player_count = len(self.player_list)

    def start(self):
        self.game_status = True
        #iteration over player_list till the game is finished
        while self.game_status:
            i = 0
            for i in range(self.playerCount):
                print(type(self.player_list))
                print("Spieler: ", i ,"ist dran!")
                #spieler darf würfeln 
                
                #spieler darf person bewegen
                #spielbrett muss sich aktualisieren
                #nächster Spieler ist dran
            self.game_status =False
            #TODO
            if i == self.playerCount and self.game_status == True:
                i = 0
            if self.checkGameStatus:
                #Game finished
                pass

    def create_gameboard(self):
        
        #creates gameboard at the beginning        
        field_dict = {}
        #home and finish of all teams
        for team in range(1,5):
            for id in range(0,8):
                x = team*10+id
                field_dict[x] = Field(x, team)
        #create all normal fields + starting fields
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
        #creating void fields with id = -1
        field_dict[-1] = Field(-1,-1)
        
        #set figure to home
        for player in self.player_list:
            for figure in player.get_team_dict.values():  
                figure.set_home(field_dict)
        return field_dict

    def get_view(self, field_dict):
        self.field_list = [
            field_dict.get(10), field_dict.get(11), field_dict.get(-1), field_dict.get(-1), field_dict.get(58), field_dict.get(59), field_dict.get(60), field_dict.get(-1), field_dict.get(-1), field_dict.get(40), field_dict.get(41),
            field_dict.get(12), field_dict.get(13), field_dict.get(-1), field_dict.get(-1), field_dict.get(57), field_dict.get(44), field_dict.get(61), field_dict.get(-1), field_dict.get(-1), field_dict.get(42), field_dict.get(43),
            field_dict.get(-1), field_dict.get(-1), field_dict.get(-1), field_dict.get(-1), field_dict.get(56), field_dict.get(45), field_dict.get(62), field_dict.get(-1), field_dict.get(-1), field_dict.get(-1), field_dict.get(-1),
            field_dict.get(-1), field_dict.get(-1), field_dict.get(-1), field_dict.get(-1), field_dict.get(55), field_dict.get(46), field_dict.get(63), field_dict.get(-1), field_dict.get(-1), field_dict.get(-1), field_dict.get(-1),
            field_dict.get(50), field_dict.get(51), field_dict.get(52), field_dict.get(53), field_dict.get(54), field_dict.get(47), field_dict.get(64), field_dict.get(65), field_dict.get(66), field_dict.get(67), field_dict.get(68),
            field_dict.get(89), field_dict.get(14), field_dict.get(15), field_dict.get(16), field_dict.get(17), field_dict.get(-1), field_dict.get(27), field_dict.get(26), field_dict.get(25), field_dict.get(24), field_dict.get(69),
            field_dict.get(88), field_dict.get(87), field_dict.get(86), field_dict.get(85), field_dict.get(84), field_dict.get(37), field_dict.get(74), field_dict.get(73), field_dict.get(72), field_dict.get(71), field_dict.get(70),
            field_dict.get(-1), field_dict.get(-1), field_dict.get(-1), field_dict.get(-1), field_dict.get(83), field_dict.get(36), field_dict.get(75), field_dict.get(-1), field_dict.get(-1), field_dict.get(-1), field_dict.get(-1),
            field_dict.get(-1), field_dict.get(-1), field_dict.get(-1), field_dict.get(-1), field_dict.get(82), field_dict.get(35), field_dict.get(76), field_dict.get(-1), field_dict.get(-1), field_dict.get(-1), field_dict.get(-1),
            field_dict.get(30), field_dict.get(31), field_dict.get(-1), field_dict.get(-1), field_dict.get(81), field_dict.get(34), field_dict.get(77), field_dict.get(-1), field_dict.get(-1), field_dict.get(20), field_dict.get(21),
            field_dict.get(32), field_dict.get(33), field_dict.get(-1), field_dict.get(-1), field_dict.get(80), field_dict.get(79), field_dict.get(78), field_dict.get(-1), field_dict.get(-1), field_dict.get(22), field_dict.get(23)
        ]
        gameboard_for_view = []
        for field in self.field_list:
            gameboard_for_view.append(field.get_name)
        return gameboard_for_view  
    
    def check_game_is_finished(self):
        for player in self.player_list:
            if player.get_finish:
                return True
        return False


    def get_field(self, number):
        return self.field_list[number]
    @property
    def get_gameboard(self):
        return self.get_view(self.field_dict)
    @property
    def get_finished(self):
        self.game_finished = self.check_game_is_finished()
        return self.game_finished
    @property
    def get_field_dict(self):
        return self.field_dict