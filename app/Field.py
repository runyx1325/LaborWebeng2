class Field():
    def __init__(self, id, color) -> None:
        #id := uuid for field 
        #color := integer for outer circle color
        #onfield := integer for inner circle color
        self.id = id
        #empty fields with id = -1
        if id == -1:
            self.color = ' '
            self.onfield = ' '
        else:
            self.color = color
            self.onfield = 0
        self.name = str(self.color)+str(self.onfield)

    def __str__(self):
        return self.name

    def figureOnField(self, color):
        self.onfield = color

    @property
    def get_id(self):
        return self.id
    @property
    def get_color(self):
        return self.color
    @property
    def get_onfield(self):
        return self.onfield
    @property
    def get_name(self):
        return self.name
   