class Field():
    def __init__(self, id, color) -> None:
        #id := uuid for field 
        #color := integer for outer circle color
        #onfield := integer for inner circle color
        self.id = id
        #empty fields with id = -1
        if id == -1:
            self.color = ' '
            self.color_on_field = ' '
        else:
            self.color = color
            self.color_on_field = 0
        self.figure_on_field = None

    def __str__(self):
        return str(self.color)+str(self.color_on_field)

    def set_figure_on_field(self, figure):
        self.figure_on_field = figure
        self.color_on_field = figure.get_color
        if figure.get_on_field != self:
            print("Wenn Feld von Figur nicht gleich Feld: "+str(self.get_id))
            print("Füge Feld der Figur hinzu")
            figure.set_on_field(self)
        else:
            print("---Felder sollten gleich sien---")
            print(self.get_id)
            print(figure.get_on_field.get_id)

    def figure_away(self):
        self.figure_on_field = None
        self.color_on_field = 0

    @property
    def get_id(self):
        return self.id
    @property
    def get_color(self):
        return self.color
    @property
    def get_color_on_field(self):
        return self.color_on_field
    @property
    def get_name(self):
        return str(self.color)+str(self.color_on_field)
    @property
    def get_figure_on_field(self):
        return self.figure_on_field