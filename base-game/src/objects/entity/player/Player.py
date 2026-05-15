from src.objects.entity.Entity import Entity
from src.managers.entity.player.SkillManager import SkillManager

class Player(Entity):
    """The player's character, by the way I think it is a good idea not to have 2 of these..."""
    #   INFO:
    #   Author: tompl
    #   Status: In progress

    #################################################
    ##                    INIT                     ##
    ################################################# 

    def __init__(self, game, entity_settings):
        super().__init__(game, entity_settings)

        self.skill_manager = SkillManager(self)
    