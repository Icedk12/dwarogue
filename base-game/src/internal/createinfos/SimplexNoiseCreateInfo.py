class SimplexNoiseCreateInfo:
    def __init__(self, scale, octaves, persistence, lacunarity, seed=None):
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.seed = seed