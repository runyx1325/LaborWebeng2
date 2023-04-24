class Figure():
    def __init__(self, color, id):
        #id := id of figure (max 4)
        #color := integer teamcolor for inner circle in fields of gameboard
        #home := true if figure is home
        #finish := true if figure is in finish
        #position := 0 is home, 1 is starting field, 41/42/43/44 is finish
        self.id = id 
        self.color = color 
        self.home = True
        self.finish = False
        self.position = 0 

    def home(self):
        if self.position == 0:
            self.home = True

    def finish(self):
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