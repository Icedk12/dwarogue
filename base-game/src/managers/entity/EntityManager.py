

class EntityManager:

    #   INFO:
    #   Author: tompl
    #   Status: Done until further notice

    #################################################
    ##                    INIT                     ##
    #################################################    
    def __init__(self, game):
        self.game = game
        self.entities = []
        self.player = None

    #################################################
    ##                 MANAGEMENT                  ##
    #################################################

    def add(self, entity):
        """Adds a set entity to entity list, do not use on player directly."""
        self.entities.append(entity)

    def set_player(self, player):
        """Adds player to entity list"""
        self.player = player
        self.add(player)

    #################################################
    ##                    FUNC                     ##
    #################################################

    def update_turn(self):
        """Calls the update_turn function for all entities and increases turn counter."""
        for e in self.entities:
            if e != self.player:
                e.update_turn(self.game)

        self.game.turn += 1

    def draw(self, surface, scale=1.0):
        """Draws all entities."""
        for e in self.entities:
            e.draw(scale)