import pygame


# Initialize the music
# def init():
# Setup for music and sounds. Defaults are good.
pygame.mixer.init()

# Load and play background music
# Sound source: Chris Bailey - artist Tripnet
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("sound/Sky_dodge_theme.ogg")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)

# Load and play the special effects
move_up_sound = pygame.mixer.Sound("sound/Jet_up.ogg")
move_down_sound = pygame.mixer.Sound("sound/Jet_down.ogg")
collision_sound = pygame.mixer.Sound("sound/Boom.ogg")
bullet_sound = pygame.mixer.Sound("sound/kill.flac")
turning_sound = pygame.mixer.Sound("sound/bigmonster_die.wav")

# Setting up the volume
move_down_sound.set_volume(0.2)
move_up_sound.set_volume(0.2)
collision_sound.set_volume(0.5)
bullet_sound.set_volume(0.2)
turning_sound.set_volume(0.5)

# # All done! Stop and quit the mixer.
# pygame.mixer.music.stop()
# pygame.mixer.quit()
