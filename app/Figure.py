class Figure():
    def __init__(self, color, id):
        self.id = id #1, 2, 3, 4 mehr ids gibts nicht pro Team
        self.color = color #ist eine Zahl die für die Farbe innerhalb des Kreises verantwortlich ist
        self.home = True
        self.finish = False
        self.position = 0

    def home(self):
        if self.position == 0:
            self.home = True

    def finish(self):
        if self.position > 40:
            self.finish = True

    def walk(self, number):
        self.position = self.position + number
    
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