import pygame
import os

class AssetManager:
    """Manages the loading and caching of assets."""

    #   INFO:
    #   Author: tompl
    #   Status: Done until further notice

    #################################################
    ##                    INIT                     ##
    #################################################

    def __init__(self, graphic_set):
        """Pass in a string of a graphic set (i.e, "base-set")."""
        self.graphic_set = graphic_set # A string joined with the asset dir to find alternate graphic set assets
        self.images = {} # A dictionary holding images with key (asset_name, scale, alpha)
        self.sounds = {} # A dictionary holding sounds with key (asset_name, scale, alpha)
        
    #################################################
    ##                IMAGE LOADING                ##
    #################################################
    
    def get_image(self, asset_name, scale=1.0, alpha=None):
        """Returns a loaded image which can be used in blitting."""
        scale = round(float(scale), 1) # Round the scale to a whole number
        key = (asset_name, scale, alpha) # Assemble the key for the dictionary

        if key not in self.images:

            #### HANDLE ASSET LOADING ####
            if asset_name not in self.images:
                # Create the full path of the graphic set specific asset, to be added to self.images
                asset_path = os.path.join('base-game', 'assets', self.graphic_set, 'images', asset_name + '.png')

                # Add to self.images dictionary
                self.images[asset_name] = pygame.image.load(asset_path).convert_alpha()
                
            base_asset_image = self.images[asset_name] # Add base image to self.images

            #### HANDLE ASSET SCALING ####
            if scale != 1.0:
                width, height = base_asset_image.get_size() # Get the width and height of image
                new_size = (int(width * scale), int(height * scale)) # Calculate scaled size

                applied_asset_image = pygame.transform.scale(base_asset_image, new_size) # Transform image to scaled size
            else:
                applied_asset_image = base_asset_image.copy() # If no scaling then just keep the same!
            
            #### HANDLE ALPHA ####
            if alpha is not None:
                applied_asset_image.set_alpha(alpha) # Set alpha if given
            
            #### HANDLE CACHING ####
            self.images[key] = applied_asset_image # Cache the modified image

        return self.images[key] # Return it to be blitted to the screen!
    
    #################################################
    ##                SOUND LOADING                ##
    #################################################

    def get_sound(self, asset_name, volume=1.0):
        """Returns a loaded sound which can be played."""
        key = (asset_name, volume) # Key for self.sounds dictionary

        if key not in self.sounds:

            #### HANDLE ASSET LOADING ####
            if asset_name not in self.sounds:
                # Using .wav because it is much more storage efficient
                asset_path = os.path.join('base-game', 'assets', self.graphic_set, 'sounds', asset_name + '.wav')
                sound = pygame.mixer.Sound(asset_path) # Create sound object

            #### HANDLE VOLUME ####
            if volume != 1.0:
                sound.set_volume(volume)
            
            #### HANDLE CACHING ####
            self.sounds[key] = sound # Cache the sound

        return self.sounds[key] # Return it to be played!
    
    #################################################
    ##               CACHE MANAGEMENT              ##
    #################################################

    def clear_sound_cache(self):
        """Clears sound dicitionary"""
        self.sounds.clear()
    
    def clear_image_cache(self):
        """Clears image dictionary"""
        self.images.clear()

    def clear_all_caches(self):
        """Clears all dictionaries"""
        self.clear_image_cache()
        self.clear_sound_cache()