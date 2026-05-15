class SimplexNoiseCreateInfo:
    def __init__(self, scale, octaves, persistence, lacunarity):
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity