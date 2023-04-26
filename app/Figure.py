class Figure():
    def __init__(self, color, nr):
        #nr := nr of figure (max 4)
        #color := integer teamcolor for inner circle in fields of gameboard
        #id := unmique id of figure in this game (team_color + figure_nr)
        #home := true if figure is home
        #finish := true if figure is in finish
        #position := 0 is home, 1 is starting field, 41/42/43/44 is finish
        #on_field := field object
        self.nr = nr 
        self.color = color
        self.id = str(self.color)+str(self.nr)
        self.homefield = int(self.id)
        match color:
            case 1:
                self.startfield = 50
            case 2:
                self.startfield = 70
            case 3: 
                self.startfield = 80
            case 4:
                self.startfield = 60
        self.home = True
        self.finish = False
        self.position = 0 
        self.on_field = None

    def __str__(self):
        return self.id

    def set_on_field(self, field):
        self.on_field = field
        field.set_figure_on_field(self)

    def set_home(self, field_dict):
        self.position = 0
        self.home = True
        self.homefield = field_dict[self.homefield]
        self.startfield = field_dict[self.startfield]
        self.set_on_field(self.homefield)
        self.get_on_field.set_figure_on_field(self)

    def is_home(self):
        if self.position == 0:
            self.home = True

    def is_finish(self):
        if self.position > 40:
            self.finish = True

    def walk(self, number, gameboardpositions):
        #number of dice
        #gameboardpositions := list of blocked position
        #if figure is home and walk 6 => starting field
        #if postion + dicenumber > max position
        #positioncheck if newposition is blocked
        if self.position == 0 and number == 6:
            newposition = 1
            if self.positioncheck(newposition, gameboardpositions):
                self.position = newposition
                return True
            return False
        #if postion + dicenumber > 44 (max position)
        elif (self.position + number) > 44:
            return False 
        else:
            newposition = self.position + number
            if self.positioncheck(newposition, gameboardpositions):
                self.position = newposition
                return True
            return False
    
    def positioncheck(self, newpos, gameboard):
        #checks if newpos is blocked of teamfigure
        for i in gameboard:
            if i == self.color:
                if newpos == gameboard[i]:
                    return False
        return False

    @property
    def get_id(self):
        return self.id
    @property
    def get_nr(self):
        return self.nr
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
    @property
    def get_on_field(self):
        return self.on_field