class Dog:
    def say_gaw(self):
        if self.angry:
            print('GAW-GAW')
        else:
            print('Gaw-gaw')

    def ping(self):
        self.angry = True

    def feed(self, food_count):
        if food_count > 10:
            self.angry = False