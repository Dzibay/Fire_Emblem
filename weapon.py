from data.weapon import weapon


class Weapon:
    def __init__(self, name):
        self.name = name
        self.mt = weapon[self.name]['mt']
        self.wt = weapon[self.name]['wt']
        self.hit = weapon[self.name]['hit']
        self.crt = weapon[self.name]['crt']
        self.range = weapon[self.name]['range']
        self.class_ = weapon[self.name]['class']

