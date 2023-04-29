from Figure import Figure

class Player():
    def __init__(self, socketid, nickname, color):
        #socket := socketid of client
        #nickanme := nickname of client
        #color := integer teamcolor
        #team := dict with 4 figures
        self.sid = socketid 
        self.nickname = nickname
        self.color = color
        self.finish = False
        self.team_dict = {}
        self.possible_moves = {}

        self.starting_field = {}
        self.home_fields = {}
        self.finish_fields = {}

        i = 1
        for i in range(4):
            self.team_dict[i] = Figure(color, i)
            i += 1

    def __str__(self):
        return self.nickname

    def clear_possible_moves(self):
        self.possible_moves = {}
    
    def add_possible_move(self, figure):
        self.possible_moves[figure.get_nr] = figure
    
    def finish(self):
        for figure in self.team_dict.values():
            if figure.get_finish == False:
                return False
        self.finish = True
        return True

    def in_home(self):
        counter = 0
        for field in list(self.home_fields.values()):
            if field.get_color_on_field == self.color:
                counter += 1
        return counter
    
    def empty_home(self):
        for field in list(self.home_fields.values()):
            if field.get_color_on_field == self.color:
                return False
        return True
    
    def empty_start(self):
        if list(self.starting_field.values())[0].get_color_on_field == self.get_color:
            return False
        return True
    
    def ready(self):
        if self.finish:
            return True
        else:
            #how many figures are at home
            counter = 0
            for figure in self.team_dict.values():
                if figure.get_home:
                    counter += 1
            field = 4 - counter
            #is the rest in finish?
            while field > 0:
                if list(self.finish_fields.values())[4 - field].get_color_on_field == self.color:
                    counter += 1
                field -= 1
            if counter == 4:
                return True
            return False
        
    
    def set_fields(self, gameboard):
        match self.color:
            case 1:
                home_fields = [10,11,12,13]
                finish_fields = [14,15,16,17]
                self.starting_field[50] = gameboard.get(50)
            case 2:
                home_fields = [20,21,22,23]
                finish_fields = [24,25,26,27]
                self.starting_field[70] = gameboard.get(70)
            case 3:
                home_fields = [30,31,32,33]
                finish_fields = [34,35,36,37]
                self.starting_field[80] = gameboard.get(80)
            case 4:
                home_fields = [40,41,42,43]
                finish_fields = [44,45,46,47]
                self.starting_field[60] = gameboard.get(60)

        for x in home_fields:
            self.home_fields[x] = gameboard.get(x)
        for x in finish_fields:
            self.finish_fields[x] = gameboard.get(x)
        for figure in list(self.team_dict.values()):
            figure.set_home_field(gameboard.get(int(figure.get_id)))
            figure.set_starting_field(list(self.starting_field.values())[0])
            figure.set_finish_fields(self.finish_fields)
           

    @property
    def get_sid(self):
        return self.sid
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
    def get_possible_moves(self):
        return self.possible_moves
    @property
    def get_finish(self):
        return self.finish
    @property
    def get_home_fields(self):
        return self.home_fields
    @property
    def get_finish_fields(self):
        return self.finish_fields
    @property
    def get_starting_field(self):
        return self.starting_field