class Entity:
    def __init__(self, entity_id: int, position: tuple):
        self.entity_id = entity_id
        self.position = position
        self.health = 100
        self.damage = 10

    def move(self, new_position: tuple):
        self.position = new_position