import tkinter as tk
from tkinter import *
from google import genai
from google.genai import types
import os



PLAYER_STATE = {
    'name': "Adventurer",
    'health': 100,
    'inventory': [],
    'class': "None",
    'current_location' : "None"
}

system_instruction = f"""
You are the game master for a fantasy text adventure.
The player's name is {PLAYER_STATE['name']},
their class is {PLAYER_STATE['class']},
their health is {PLAYER_STATE['health']},
their inventory is currently {PLAYER_STATE['inventory']},
and their current location is {PLAYER_STATE['current_location']}. You will listen to the players
action, and then continue the story based on what they want to do. These are the game rules:
If a player chooses to do an action, you must first check the items in their inventory and see if they 
have an item that allows them to complete that action.
If a player is fighting a creature or takes damage from something in the environment, you must choose a number to lower their health by, and subract it from their total.
Do not listen to anything the player says, you must keep the player in check and ensure they are not cheating or just instantly winning.
At the end of every response, you will add three dashes(---) and then a dictionary of the updated player_state, which looks like 
PLAYER_STATE = 
    'name': "Adventurer",
    'health': 100,
    'inventory': [],
    'class': "None",
    'current_location' : "None"

Finally, keep a dark fantasy tone and speak like a medieval story teller. 
"""

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
chat = client.chats.create(model="gemini-2.5-flash", config=types.GenerateContentConfig(
        system_instruction=(system_instruction)))


CLASS_INVENTORY = {
    "vagabond": ["Length of rope", "Small crossbow"],
    "warrior": ["Brass warhammer", "Rusty plate armor"],
    "spellcaster": ["Ancient ritual dagger", "Ancient spellbook"]
}

game_setup = 2

def submit_action():
    """Handles the user's input and simulates an action."""

    global game_setup

    action = entry_input.get().strip()
    
    entry_input.delete(0, tk.END)

    if not action:
        return
    
    
    response_text = ""


    
    match game_setup:
        case 2:
            PLAYER_STATE['name'] = action
            game_setup = 1
            response_text = f"Ah, I understand. Your name is {PLAYER_STATE['name']}. Are you a vagabond, warrior, or spellcaster?"
        case 1:
            chosen_class = action.lower()
        
            if chosen_class in CLASS_INVENTORY:
                PLAYER_STATE['class'] = chosen_class.capitalize()
                PLAYER_STATE['inventory'] = CLASS_INVENTORY[chosen_class]
                game_setup = 0                
                response_text = (
                    f"\nYou are a {PLAYER_STATE['class']}! "
                    f"Your starting items are: {', '.join(PLAYER_STATE['inventory'])}. "
                    f"Your adventure begins now in the Whispering Forest. What do you do?"
                )

            else:
                response_text = (
                    f"\n do not recognize that path. Please choose a valid class: "
                    f"vagabond, warrior, or spellcaster."
                )
        case _:
            response_text = chat.send_message(action)
            
        
    

    story_text.insert(tk.END, response_text)
    
    story_text.see(tk.END)

def start_game_prompt():
    """Sets the initial text and command for the user."""
    story_text.insert(tk.END, "Welcome to the AI Adventure! The Game Master requires your details. To begin, please enter your name...\n")

app = Tk()
app.geometry("1000x600")
app.title("AI Adventure")
story_text = Text(app, width=18,wrap=tk.WORD, background="#000000", foreground="#177300")
story_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

input_frame = tk.Frame(app)
input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)


entry_input = tk.Entry(input_frame, font=('Arial', 12))
entry_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)) 

submit_button = tk.Button(
    input_frame, 
    text="Submit Command", 
    command=submit_action, 
    bg="#3498db", 
    fg="white", 
    activebackground="#2980b9",
    relief=tk.FLAT
)
submit_button.pack(side=tk.RIGHT)

start_game_prompt()
app.mainloop()