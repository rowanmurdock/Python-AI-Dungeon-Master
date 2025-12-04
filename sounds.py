import pygame
import tkinter as tk
import random
pygame.mixer.init()

pygame.mixer.set_num_channels(16)

WRITING_CH = pygame.mixer.Channel(1)
MUSIC_CH   = pygame.mixer.Channel(2)

writing_loop = pygame.mixer.Sound("soundeffects/pen.wav")
music_loop = pygame.mixer.Sound("soundeffects/darkfantasyambience.mp3")

writing_loop.set_volume(1)
music_loop.set_volume(0.3)
MUSIC_CH.set_volume(0.3)
WRITING_CH.set_volume(1)


def start_writing_noise():
    WRITING_CH.play(writing_loop, loops=-1)

def stop_writing_noise():
    WRITING_CH.stop()

def start_bg_music():
    MUSIC_CH.play(music_loop, loops=-1)

def stop_bg_music():
    MUSIC_CH.stop()
