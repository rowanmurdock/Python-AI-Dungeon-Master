import tkinter as tk
from tkinter import *


PLAYER_STATE = {
    'name': "Adventurer",
    'health': 100,
    'inventory': [],
    'class': "None"
}

CLASS_INVENTORY = {
    "vagabond": ["Length of rope", "Small crossbow"],
    "warrior": ["Brass warhammer", "Rusty plate armor"],
    "spellcaster": ["Ancient Ritual Dagger", "Ancient spellbook"]
}

game_setup = 2

def submit_action():
    """Handles the user's input and simulates an action."""

    global game_setup

    action = entry_input.get().strip()
    
    entry_input.delete(0, tk.END)

    if not action:
        return
    
    story_text.insert(tk.END, f"\n> {PLAYER_STATE['name']}: {action}")
    
    response_text = ""


    
    match game_setup:
        case 2:
            PLAYER_STATE['name'] = action
            game_setup = 1
            response_text = "Ah, I understand. Your name is {PLAYER_STATE[name]}. Are you a vagabond, warrior, or spellcaster?"
        case 1:
            chosen_class = action.lower()
        
            if chosen_class in CLASS_INVENTORY:
                PLAYER_STATE['class'] = chosen_class.capitalize()
                PLAYER_STATE['inventory'] = CLASS_INVENTORY[chosen_class]
                game_setup = 0                
                response_text = (
                    f"\n[GM]: The spirits acknowledge the choice of a {PLAYER_STATE['class']}! "
                    f"Your starting items are: {', '.join(PLAYER_STATE['inventory'])}. "
                    f"Your adventure begins now in the Whispering Forest. What do you do?"
                )
            else:
                response_text = (
                    f"\n[GM]: I do not recognize that path. Please choose a valid class: "
                    f"**VAGABOND**, **WARRIOR**, or **SPELLCASTER**."
                )
        case _: 
            response_text = f"\n[GM]: The game is running! Your action '{action}' is noted. The AI is still thinking... (Simulated Response)"
        
    

    story_text.insert(tk.END, response_text)
    
    story_text.see(tk.END)

def start_game_prompt():
    """Sets the initial text and command for the user."""
    story_text.insert(tk.END, "Welcome to the AI Adventure! The Game Master requires your details. To begin, please enter your name...\n")

app = Tk()
app.geometry("1000x600")
app.title("AI Adventure")
story_text = Text(app, width=18,wrap=tk.WORD, background="#000000", foreground="#177300")
story_text.insert("1.0", "To begin your adventure, enter your name...")
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