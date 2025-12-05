import pygame

pygame.mixer.init()

pygame.mixer.set_num_channels(16)

WRITING_CH = pygame.mixer.Channel(1)
MUSIC_CH  = pygame.mixer.Channel(2)
SWORD_CH = pygame.mixer.Channel(3)
RIVER_CH = pygame.mixer.Channel(4)
BREEZE_CH = pygame.mixer.Channel(5)
STEPS_CH  = pygame.mixer.Channel(6)
GROWL_CH = pygame.mixer.Channel(7)
HEART_CH = pygame.mixer.Channel(8)
BITE_CH = pygame.mixer.Channel(9)


writing_loop = pygame.mixer.Sound("soundeffects/pen.wav")
music_loop = pygame.mixer.Sound("soundeffects/darkfantasyambience.mp3")
sword_sound = pygame.mixer.Sound("soundeffects/swordhit.mp3")
river_sound = pygame.mixer.Sound("soundeffects/river.mp3")
breeze_sound = pygame.mixer.Sound("soundeffects/breeze.mp3")
footstep_sound = pygame.mixer.Sound("soundeffects/footsteps.mp3")
growl_sound = pygame.mixer.Sound("soundeffects/growl.mp3")
heartbeat_sound = pygame.mixer.Sound("soundeffects/heart.mp3")
bite_sound = pygame.mixer.Sound("soundeffects/bite.mp3")

WRITING_CH.set_volume(1)
writing_loop.set_volume(1)

music_loop.set_volume(0.2)
MUSIC_CH.set_volume(0.2)

SWORD_CH.set_volume(0.5)
sword_sound.set_volume(0.5)

##BREEZE_CH.set_volume(0.5)
##breeze_sound.set_volume(0.5)

STEPS_CH.set_volume(0.5)
footstep_sound.set_volume(0.5)

GROWL_CH.set_volume(0.5)
growl_sound.set_volume(0.5)


def start_writing_noise():
    WRITING_CH.play(writing_loop, loops=-1)

def stop_writing_noise():
    WRITING_CH.stop()

def start_bg_music():
    MUSIC_CH.play(music_loop, loops=-1)

def stop_bg_music():
    MUSIC_CH.stop()

def river_noise():
    RIVER_CH.play(river_sound, fade_ms=1000)
    RIVER_CH.fadeout(3000)

def sword_noise():
    SWORD_CH.play(sword_sound)

def growl_noise():
    GROWL_CH.play(growl_sound)

def bite_noise():
    BITE_CH.play(bite_sound)


def breeze_noise():
    BREEZE_CH.play(breeze_sound, fade_ms=1000)
    BREEZE_CH.fadeout(20000)

def footsteps_noise():
    STEPS_CH.play(footstep_sound, fade_ms=1000)
    STEPS_CH.fadeout(2000)

def heartbeat_noise():
    HEART_CH.play(heartbeat_sound)
    HEART_CH.fadeout(2000)



