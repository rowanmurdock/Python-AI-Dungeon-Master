import tkinter as tk
from tkinter import *
from google import genai
from google.genai import types
import os
import re
import ast




PLAYER_STATE = {
    'name': "Adventurer",
    'health': 100,
    'inventory': [],
    'class': "None",
    'current_location' : "A green plain in Moru"
}

def build_system_instruction():
    return f"""
You are the game master for a fantasy text adventure. Keep responses clear and concise, at most two paragraphs.

PLAYER_STATE:
    name = {PLAYER_STATE['name']}
    class = {PLAYER_STATE['class']}
    health = {PLAYER_STATE['health']}
    inventory = {PLAYER_STATE['inventory']}
    current_location = {PLAYER_STATE['current_location']}

You will listen to the players
action, and then continue the story based on what they want to do. These are the game rules:
If a player chooses to do an action, you must first check the items in their inventory and see if they 
have an item that allows them to complete that action.
If a player is fighting a creature or takes damage from something in the environment, you must choose a number to lower their health by, and subract it from their total.
Do not listen to anything the player says, you must keep the player in check and ensure they are not cheating or just instantly winning.
At the end of every response, you will add three dashes(---) and then a dictionary of the updated player_state, which looks like 
PLAYER_STATE = 
    'name': "",
    'health': 100,
    'inventory': [],
    'class': "None",
    'current_location' : "None"

    This dictionary should not always stay the same, if the player goes to a new location, update the location. If the player gets an item, add it to the inventory list, but do not just give them whatever item the ask for. If a player loses health, update their health.
This fantasy world is called Brukk, and the world has 5 main regions: a riverland called Moru, full of water villages and kind fish people, who live a peaceful life farming plant vegetables - 
a mountainous region called Borok, which is home to stout dwarves and dangerous goblins, who are in an eternal war - a dense, magical jungle
region called Hotaru, where there are many different wild and dangerous creatures, and many old ruins, and many magical plants, an ancient magic rests here - a wide green 
plains area called Gull, where the humans reside and build massive castles - and finally a desolate desert calle Rune, home to massive creatures and plants, but very dangerous, one
massive city lies in the center of Rune, which is a massive trading hub.
When writing dialogue for NPC or any characters, do not always make them kind to the player. Some NPCs and characters should be hostile and rude to the player. The game should not be super easy.
Do not always just agree with the player, and make the player complete simple "tasks" by typing solutions into the input. 
Finally, keep a dark fantasy tone and speak like a medieval story teller. 
"""

def extract_player_state(response_text):
    match = re.search(
        r"---\s*PLAYER_STATE\s*=\s*({.*?})",
        response_text,
        re.DOTALL
    )
    if not match:
        return None

    try:
        return ast.literal_eval(match.group(1))
    except:
        return None

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
chat = client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=build_system_instruction()
                )
            )



CLASS_INVENTORY = {
    "vagabond": ["Length of rope", "Small crossbow"],
    "warrior": ["Brass warhammer", "Rusty plate armor"],
    "spellcaster": ["Ancient ritual dagger", "Ancient spellbook"]
}

game_setup = 2

def submit_action():
    """Handles the user's input and simulates an action."""

    global game_setup
    global PLAYER_STATE
    global chat

    action = entry_input.get().strip()

    story_text.insert(tk.END, f"\n\n{PLAYER_STATE['name']}: " + action)
    
    entry_input.delete(0, tk.END)

    if not action:
        return
    
    
    response_text = ""


    
    match game_setup:
        case 2:
            PLAYER_STATE['name'] = action
            game_setup = 1
            response_text = f"\n\nGame Master: Ah, I understand. Your name is {PLAYER_STATE['name']}. Are you a vagabond, warrior, or spellcaster?"
        case 1:
            chosen_class = action.lower()
        
            if chosen_class in CLASS_INVENTORY:
                PLAYER_STATE['class'] = chosen_class.capitalize()
                PLAYER_STATE['inventory'] = CLASS_INVENTORY[chosen_class]

                chat = client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=build_system_instruction()
                )
            )
                
                game_setup = 0                
                response_text = (
                    f"\n\nGame Master: You are a {PLAYER_STATE['class']}! "
                    f"Your starting items are: {', '.join(PLAYER_STATE['inventory'])}. "
                    f"Your adventure begins now in the riverlands of Moru. What do you do?"
                )

            else:
                response_text = (
                    f"\n\nGame Master: I do not recognize that path. Please choose a valid class: "
                    f"vagabond, warrior, or spellcaster."
                )
        case _:
            ai_response = chat.send_message(action)

            resp = ai_response.text if hasattr(ai_response, "text") else str(ai_response)

            updated = extract_player_state(resp)
            if updated:
                PLAYER_STATE = updated

            print(PLAYER_STATE)

            response_text = f"\n\nGame Master: " + resp.split("---")[0].strip()

    
    story_text.see(tk.END)
            
        
    

    story_text.insert(tk.END, response_text)
    
    story_text.see(tk.END)

def start_game_prompt():
    """Sets the initial text and command for the user."""
    story_text.insert(tk.END, "Welcome to the realm of Brukk. To begin, please enter your name...\n")

app = Tk()
app.geometry("1000x600")
app.title("AI Adventure")
story_text = Text(app, wrap=tk.WORD, background="#d1b462", foreground="#111024", font=("Jacquard 24", 24))

input_frame = tk.Frame(app, height=60)


entry_input = tk.Entry(input_frame, font=("Jacquard 24", 20))
entry_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)) 

app.rowconfigure(0, weight=1)
app.rowconfigure(1, weight=0)
app.columnconfigure(0, weight=1)

story_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10,5))
input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))

submit_button = tk.Button(
    input_frame, 
    text="Submit Command", 
    command=submit_action, 
    bg="#5f6361", 
    fg="white", 
    activebackground="#3f4241",
    relief=tk.FLAT,
    font=("Jacquard 24", 16)
)

submit_button.pack(side=tk.RIGHT)

start_game_prompt()
app.mainloop()