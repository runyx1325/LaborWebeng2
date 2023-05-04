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
    
    def set_endgame(self):
        counter = 0
        for figure in self.team_dict.values():
            counter += 1
            for field in list(reversed(list(self.finish_fields.values()))):
                if field.get_color_on_field != self.color:
                    figure.get_on_field.figure_away()
                    figure.set_on_field(field)
                    figure.set_steps(41 + counter)
                    break
            if counter == 3:
                break

    def clear_possible_moves(self):
        self.possible_moves = {}
    
    def add_possible_move(self, figure, new_field):
        self.possible_moves[figure.get_nr] = new_field
    
    def is_finish(self):
        for figure in list(self.team_dict.values()):
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
        #return True wenn man 3 Mal würfeln darf
        #return False wenn man nicht 3 Mal würfeln darf

        #Ist noch jemand zu Hause?
            #ja - ist die Anzahl der Figuren zu Hause + die Figuren im Ziel == 4
                #ja - Sind alle Figuren im Ziel eingerückt?
                    #ja - return True
                    #nein - return False
                #nein - return False
            #nein - return False

        counter_home = 0
        counter_finish = 0
        moved_up = False
        for field in self.get_home_fields.values():
            if field.get_color_on_field == self.get_color:
                counter_home += 1
        for field in self.get_finish_fields.values():
            if field.get_color_on_field == self.get_color:
                counter_finish += 1
        # print("---")
        for field in range(4 - counter_finish):
            # print(field)
            # print("Feld ID: "+str((list(self.get_finish_fields.values()))[field].get_id))
            # print("Farbe auf Feld: "+str((list(self.get_finish_fields.values()))[field].get_color_on_field))
            if (list(self.get_finish_fields.values()))[field].get_color_on_field == self.get_color:
                moved_up = False
            else:
                moved_up = True
        # print("---")
        # print("Counter Home: "+str(counter_home))
        # print("Counter Finish: "+str(counter_finish))
        # print("Aufgerückt? "+str(moved_up))
        if counter_home > 0 and counter_home < 4:
            # print("1 - 3 Spieler im Haus")
            if counter_home + counter_finish == 4:
                # print("Alle sind im Haus oder Ziel")
                if moved_up == True:
                    # print("Alle sind auufgerückt im Haus")
                    return True
                return False
            return False
        elif counter_home == 4:
            # print("4 Spieler im Haus")
            return True
        # print("else")
        return False     
    
    def set_fields(self, gameboard):
        if self.color == 1:
            home_fields = [10,11,12,13]
            finish_fields = [14,15,16,17]
            self.starting_field[50] = gameboard.get(50)
        elif self.color == 2:
            home_fields = [20,21,22,23]
            finish_fields = [24,25,26,27]
            self.starting_field[70] = gameboard.get(70)
        elif self.color == 3:
            home_fields = [30,31,32,33]
            finish_fields = [34,35,36,37]
            self.starting_field[80] = gameboard.get(80)
        elif self.color == 4:
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
        self.finish = self.is_finish()
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