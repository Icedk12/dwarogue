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

    def move_and_return(self, direction_vec2):
        moved = super().move_and_return(direction_vec2)
        if moved:
            self.on_walk()
        return moved
    
    def on_walk(self):
        """Called when the player successfully walks"""
        self.skill_manager.skills["running"].add_experience(1)
        if self.game.map_manager.map.get_tile(self.pos) != None:
            self.game.asset_manager.get_sound("footstep_" + self.game.map_manager.map.get_tile(self.pos).asset_name, 0.1).play()
        else:
            print("No footstep sound can be generated for empty \"None\" tile")
        # File name for grass would be: footstep_grass.wav