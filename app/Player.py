from Figure import Figure

class Player():
    def __init__(self, socketid, nickname, color):
        #socket := socketid of client
        #nickanme := nickname of client
        #color := integer teamcolor
        #team := dict with 4 figures
        self.socket = socketid 
        self.nickname = nickname
        self.color = color
        self.team_dict = {}
        i = 1
        for i in range(4):
            self.team_dict[i] = Figure(color, i)
            i += 1
        self.finish = False
    
    def finish(self):
        for figure in self.team_dict.values():
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
    def get_team_dict(self):
        return self.team_dict
    @property
    def get_finish(self):
        return self.finish