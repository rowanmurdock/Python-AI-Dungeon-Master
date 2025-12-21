import re
import os
import json
import sounds as sound
import tkinter as tk
from ai import new_chat
from state import PLAYER_STATE


chat = new_chat()


def time_as_float(day, tod):
    return day + [0.25, 0.5, 0.75, 1.0][tod]

def sound_effects_for_text(text):
    attack_regex = re.compile(r"\b(clangs|strikes|slash|stab|strike|cut|slice|hack|thrust|pierce|cleave)\b", re.IGNORECASE)
    water_regex = re.compile(r"\b(river|creek|lake|waterfall|pond)\b", re.IGNORECASE)
    heartbeat_regex = re.compile(r"\b(heartbeat|heart beat|pulse|pulsing|thump|thudding|rhythm|heart races|heartbeat quickens|racing heart|pounding heart|pain|anxiety|anxious|stress|stressed|afraid)\b", re.IGNORECASE)
    growl_regex = re.compile(r"\b(snarl|snarling|rumble|rumbling|hiss|hissing|roar|roaring)\b", re.IGNORECASE)
    footstep_regex = re.compile(r"\b(footstep|footsteps|step|steps|tread|treading|walk|walking|stomp|stomping|creep|creeping|sneak|sneaking|stride|strides|march|marching)\b", re.IGNORECASE)
    breeze_regex = re.compile(r"\b(breeze|breezy|wind|windy|gust|gusts|gusting|draft|drafty|air current|whistling wind|soft wind|gentle wind)\b", re.IGNORECASE)
    bite_regex = re.compile(r"\b(bite|bites|biting|chew|chews|chewing|chomp|chomps|chomping|munch|munches|munching|nibble|nibbles|nibbling)\b",re.IGNORECASE)


    if attack_regex.search(text):
        sound.sword_noise()
    if water_regex.search(text):
        sound.river_noise()
    if heartbeat_regex.search(text):
        sound.heartbeat_noise()
    if growl_regex.search(text):
        sound.growl_noise()
    if footstep_regex.search(text):
        sound.footsteps_noise()
    if breeze_regex.search(text):
        sound.breeze_noise()
    if bite_regex.search(text):
        sound.bite_noise()

def get_time_string(time_num):
    match time_num:
        case 0: return "Morning"
        case 1: return "Afternoon"
        case 2: return "Evening"
        case 3: return "Night"
        case _: return "Unknown"



def typewriter_write(text_widget, text, delay=20):
    sound.start_writing_noise()
    def write_char(i=0):
        if i < len(text):
            text_widget.insert(tk.END, text[i])
            text_widget.see(tk.END)
            text_widget.after(delay, write_char, i+1)
        else:
            sound.stop_writing_noise()

    write_char()


def save_game():

    ai_summary = chat.send_message("Summarize the entire player story so far, remembering relationships and quests and any other important details. Ensure recent memory is detailed so that the player can pick up where they left off. Send only a text summary that is at most 2 paragraphs. ").text


    file_name = "saves/" + PLAYER_STATE['name'] + str(PLAYER_STATE['day']) + ".json"
    save_data = {
    'name': PLAYER_STATE['name'],
    'health': PLAYER_STATE['health'],
    'hunger': PLAYER_STATE['hunger'],
    'inventory': PLAYER_STATE['inventory'],
    'class': PLAYER_STATE['class'],
    'current_location': PLAYER_STATE['current_location'],
    'gold': PLAYER_STATE['gold'],
    'day' : PLAYER_STATE['day'],
    'time_of_day': PLAYER_STATE['time_of_day'],
    'objective': PLAYER_STATE['objective'],
    'game_history': ai_summary
}

    if not os.path.exists("saves"):
        os.makedirs("saves")
    try:
        with open(file_name, 'w') as json_file:
            json.dump(save_data, json_file, indent=4)

        story_text.insert(tk.END, f"\n\nGame saved successfully as {file_name}.")
        story_text.see(tk.END)

    except Exception as e:
        story_text.insert(tk.END, f"\n\nError saving game: {e}.")
        story_text.see(tk.END)
