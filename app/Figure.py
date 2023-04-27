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
        self.home_field = None
        self.starting_field = None
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
        self.get_on_field.set_figure_on_field(self)

    def walk(self, number):
        self.position += number
        self.home = False
        if self.position > 40:
            self.finsish = True

    def set_home_field(self, field):
        self.home_field = field

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