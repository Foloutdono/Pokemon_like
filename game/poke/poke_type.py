class PokeType():
    def __init__(self, name, id, attack_coefs):
        self.name = name
        self.id = id
        self.attack_coefs = attack_coefs

    def __str__(self):
        return f'Type : {self.name}'