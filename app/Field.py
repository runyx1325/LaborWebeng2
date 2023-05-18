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

    # return inner and outer color of the field
    def __str__(self):
        return str(self.color)+str(self.color_on_field)

    # change inner color of the field to color of the new figure on the current field
    def set_figure_on_field(self, figure):
        self.figure_on_field = figure
        self.color_on_field = figure.get_color
        if figure.get_on_field != self:
            figure.set_on_field(self)

    # remove figure from current field and change color to default
    def figure_away(self):
        self.figure_on_field = None
        self.color_on_field = 0

    #getter
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