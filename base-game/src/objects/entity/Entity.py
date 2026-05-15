from src.internal.createinfos.EntityCreateInfo import EntityCreateInfo

class Entity:
    """A class that is used for objects that are rendered above the map and can move on the grid.
    For example: a player, npc, dropped item, etc.
    """

    #################################################
    ##                    INIT                     ##
    #################################################

    def __init__(self, entity_settings : EntityCreateInfo):
        ######### BARE METAL SETUP #########
        self.entity_settings = entity_settings # An EntityCreateInfo object

        ######### VARIABLE SETUP #########
        self.position = self.entity_settings.position # pygame.Vector3 (x,y,z)
        self.name = self.entity_settings.name # String containing the name