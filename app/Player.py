
from Figure import Figure


class Player():
    def __init__(self, socketid, nickname, color):
        self.socket = socketid #zuordnung client/socket mit nickname
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