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

    def __str__(self):
        return str(self.color)+str(self.color_on_field)

    def set_figure_on_field(self, figure):
        self.figure_on_field = figure
        self.color_on_field = figure.get_color

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