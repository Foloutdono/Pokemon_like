class Pokemon:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def __repr__(self):
        return f"{self.name} (HP: {self.hp}, ATK: {self.attack})"