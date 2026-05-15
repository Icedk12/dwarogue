from src.objects.entity.player.Skill import Skill

class SkillManager:
    """Holds a dictionary of all available skills in the game"""

    #   INFO:
    #   Author: tompl
    #   Status: Done, maybe add more content

    #################################################
    ##                    INIT                     ##
    #################################################

    def __init__(self, owner):

        # THE dictionary xD
        self.skills = {
            "running": Skill(owner, "running"),
            "jumping": Skill(owner, "jumping"),
            "climbing": Skill(owner, "climbing"),
            "swimming": Skill(owner, "swimming"),
            "wrestling": Skill(owner, "wrestling"),
            "striking": Skill(owner, "striking"),
            "dodging": Skill(owner, "dodging"),
            "shield_user": Skill(owner, "shield_user"),
            "archery": Skill(owner, "archery"),
            "woodcrafting": Skill(owner, "woodcrafting"),
            "stone_shaping": Skill(owner, "stone_shaping"),
            "blacksmithing": Skill(owner, "blacksmithing"),
            "weaving": Skill(owner, "weaving"),
            "tailoring": Skill(owner, "tailoring"),
            "leatherworking": Skill(owner, "leatherworking"),
            "gem_cutting": Skill(owner, "gem_cutting"),
            "glassblowing": Skill(owner, "glassblowing"),
            "pottery": Skill(owner, "pottery"),
            "mechanics": Skill(owner, "mechanics"),
            "mining": Skill(owner, "mining"),
            "woodcutting": Skill(owner, "woodcutting"),
            "herbalism": Skill(owner, "herbalism"),
            "farming": Skill(owner, "farming"),
            "fishing": Skill(owner, "fishing"),
            "butchery": Skill(owner, "butchery"),
            "animal_training": Skill(owner, "animal_training"),
            "tracking": Skill(owner, "tracking"),
            "brewing": Skill(owner, "brewing"),
            "cooking": Skill(owner, "cooking"),
            "leadership": Skill(owner, "leadership"),
            "negotiation": Skill(owner, "negotiation"),
            "intimidation": Skill(owner, "intimidation"),
            "lying": Skill(owner, "lying"),
            "teaching": Skill(owner, "teaching"),
            "observation": Skill(owner, "observation"),
            "appraisal": Skill(owner, "appraisal"),
            "organization": Skill(owner, "organization"),
            "medical_diagnosis": Skill(owner, "medical_diagnosis"),
            "surgery": Skill(owner, "surgery"),
            "poetry": Skill(owner, "poetry"),
            "music_composition": Skill(owner, "music_composition"),
            "dancing": Skill(owner, "dancing"),
            "storytelling": Skill(owner, "storytelling"),
            "engraving": Skill(owner, "engraving"),
        }

    #################################################
    ##                 NEW SKILLS                  ##
    #################################################
    def add(self, skill):
        """Takes in a skill object and adds it to the list of skills in game"""
        # TODO: Add JSON support
        self.skills[skill.name] = skill