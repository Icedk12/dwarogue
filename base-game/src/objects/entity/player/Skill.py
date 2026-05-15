class Skill:
    """Typical skill system in an RPG, level up req scales by 1.5x every level"""
    #   INFO:
    #   Author: tompl
    #   Status: Done-ish 
    #   TODO: Make it display to the play somewhere

    #################################################
    ##                    INIT                     ##
    #################################################

    def __init__(self, owner, name, max_level=100000):
        ######### SETUP #########
        self.owner = owner
        self.name = name

        ######### LEVELS #########
        self.max_level = max_level
        self.level = 1
        self.level_up_xp_modifier = 1.5 # How much the levels get harder 1.5 = (lvl 1: 100, lvl 2: 150, etc.)

        ######### XP #########
        self.xp = 0
        self.required_xp = 100
        self.modifier = 1

    #################################################
    ##                 GAINING XP                  ##
    #################################################

    def add_experience(self, add_xp):
        xp_to_add = add_xp * self.modifier  # stores xp for some calculations
        
        # Calculates how much xp is needed to level up 
        xp_chunk = min(xp_to_add, self.required_xp - self.xp)
        self.xp += xp_chunk
        xp_to_add -= xp_chunk # Subtracts the chunk from the xp reserves

        if self.xp == self.required_xp and self.level != self.max_level:
            # Leveled up
            self.xp = 0 # Sets their current progress of this levels to 0
            self.required_xp = int(self.required_xp * self.level_up_xp_modifier) # Multiplies required xp by 1.5
            self.level = min(self.level + 1, self.max_level) # Increases level by 1 while pertaining to the cap

            if xp_to_add > 0:
                self.add_experience(xp_to_add)
        else:
            # Did not level up
            pass