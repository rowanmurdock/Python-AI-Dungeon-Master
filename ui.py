import tkinter as tk
from ai import new_chat
from state import PLAYER_STATE, CLASS_INVENTORY, WIN_CONDITIONS, extract_player_state
import re
import sounds as sound
from PIL import Image, ImageTk
import os
import json
import glob
from helpers import *


story_text = None
entry_input = None
health_label = None
gold_label = None
loc_label = None
hunger_label = None
date_time_label = None
app = None
top_bar = None
time_icons = {}
time_icon_label = None
game_setup = 3



bg_color = "#3d3a35"

chat = new_chat()
goal = None


def load_game(file_name):
    global PLAYER_STATE, game_setup
    try:
        with open(file_name, 'r') as json_file:
            load_data = json.load(json_file)

        game_setup = 0


        PLAYER_STATE['name'] = load_data['name']
        PLAYER_STATE['health'] = load_data['health']
        PLAYER_STATE['hunger'] = load_data['hunger']
        PLAYER_STATE['inventory'] = load_data['inventory']
        PLAYER_STATE['class'] = load_data['class']
        PLAYER_STATE['current_location'] = load_data['current_location']
        PLAYER_STATE['gold'] = load_data['gold']
        PLAYER_STATE['day'] = load_data['day']
        PLAYER_STATE['time_of_day'] = load_data['time_of_day']
        PLAYER_STATE['objective'] = load_data['objective']

        prompt = (
                    f"SYSTEM: LOAD GAME DATA.\n"
                    f"Player: {PLAYER_STATE['name']}\n"
                    f"Location: {PLAYER_STATE['current_location']}\n"
                    f"Inventory: {PLAYER_STATE['inventory']}\n"
                    f"Objective: {PLAYER_STATE['objective']}\n"
                    f"CRITICAL STATS: Health is exactly {PLAYER_STATE['health']}/100 and Hunger is exactly {PLAYER_STATE['hunger']}/100.\n"
                    f"Summary: {load_data['game_history']}\n"
                    f"INSTRUCTION: You must resume the narrative. Do NOT reset stats. Do NOT heal the player. Do NOT rest the hunger."
                )
        load_game_start = chat.send_message(prompt).text

        load_game_start = "\n\n" + load_game_start.split("---")[0].strip()


        build_game_ui()
        story_text.insert(tk.END, "Game Master:" + f"Loaded {PLAYER_STATE['name']} (Day {PLAYER_STATE['day']}).\n\n{load_game_start}")

    except Exception as e:
        print("Error loading game:" + e)
            

def submit_action():
    global chat, goal, game_time, bg_color, top_bar, health_label, gold_label, hunger_label, date_time_label, loc_label, time_icon_label, game_setup

    action = entry_input.get().strip()
    entry_input.delete(0, tk.END)

    if not action:
        return

    story_text.insert(tk.END, f"\n\n{PLAYER_STATE['name']}: {action}")
    story_text.see(tk.END)

    response_text = ""

    match game_setup:
        case 3:
            PLAYER_STATE['name'] = action.capitalize()
            game_setup = 2
            response_text = (
                f"\n\nGame Master: Ah, I understand. Your name is {PLAYER_STATE['name']}. "
                f"There are many paths in Brukk. Are you a wandering vagabond, a brutal warrior, or a mystical spellcaster?"
            )

        case 2:
            chosen = action.lower()

            if chosen in CLASS_INVENTORY:
                PLAYER_STATE['class'] = chosen.capitalize()
                PLAYER_STATE['inventory'] = CLASS_INVENTORY[chosen]
                chat = new_chat()
                game_setup = 1

                response_text = (
                    f"\n\nGame Master: Very interesting, you are a {PLAYER_STATE['class']}! "
                    f"Your starting items are: {', '.join(PLAYER_STATE['inventory'])}. "
                    f"A {PLAYER_STATE['class']} named {PLAYER_STATE['name']}. What could possibly be your goal in this world? Do you wish "
                    "to become ruler of a realm? Perhaps find love, settle down, and make a home in this cruel realm? Or is it unimaginable wealth that you seek?"
                )

            else:
                response_text = (
                    "\n\nGame Master: I do not recognize that path. Choose vagabond, warrior, or spellcaster."
                )

        case 1:
            chosen = action.lower()

            if re.search(r"\blove\b", chosen):
                PLAYER_STATE['objective'] = WIN_CONDITIONS["Home and Hearth"]
                game_setup = 0
                goal =  WIN_CONDITIONS["Home and Hearth"]

            elif re.search(r"\bwealth\b", chosen):
                PLAYER_STATE['objective'] = WIN_CONDITIONS["Dragon's Hoard"]
                game_setup = 0
                goal =  WIN_CONDITIONS["Dragon's Hoard"]

            elif re.search(r"\bruler\b", chosen):
                PLAYER_STATE['objective'] = WIN_CONDITIONS["Becoming Ruler"]
                game_setup = 0
                goal =  WIN_CONDITIONS["Becoming Ruler"]


            else:
                response_text = (
                    "\n\nGame Master: That is not a worthy goal. Choose ruler, love, or wealth."
                )
                typewriter_write(story_text, response_text)
                return
            
            match PLAYER_STATE['objective'][0]:
                case "Be married and own a home":
                    response_text = (
                    f"\n\nGame Master: A noble goal, to find love in this cold world. "
                    f"To accomplish your goal, you must {PLAYER_STATE['objective'][0].lower()}. Now, your journey begins in a small green plain in the riverlands of Moru."
                )
                case "Become King or Queen of one of the 5 realms: Moru, Borok, Gull, Hotaru, or Rune":
                    response_text = (
                    f"\n\nGame Master: An ambitious goal, to conquer a realm of this world. "
                    f"To accomplish your goal, you must {PLAYER_STATE['objective'][0].lower()}. Now, your journey begins in a small green plain in the riverlands of Moru."
                )
                case "Have 50,000 gold coins":
                    response_text = (
                    f"\n\nGame Master: A greedy goal, to gain this much wealth. "
                    f"To accomplish your goal, you must {PLAYER_STATE['objective'][0]}. Now, your journey begins in a small green plain in the riverlands of Moru."
                )

        case _:
            
            if PLAYER_STATE['health'] <= 0:
                game_setup = 3
                PLAYER_STATE.update({
                    'name': "Adventurer",
                    'health': 100,
                    'hunger': 100,
                    'inventory': [],
                    'class': "None",
                    'current_location': "A green plain in Moru",
                    'gold': 5,
                    'day': 0,
                    'time_of_day': 0,
                    'objective': []
                })
                chat = new_chat()
                response_text = (
                    f"\n\nGame Master: You have met death in {PLAYER_STATE['current_location'][0]}.lower()+{PLAYER_STATE['current_location'][1:]}. "
                    "You can now create a new character. Enter a new name:"
                )
                typewriter_write(story_text, response_text)
                return
            
            # if PLAYER_STATE['objective'][1] == 1:
            #     response_text = (
            #         f"\n\nGame Master: You have fulfilled your ultimate objective of {PLAYER_STATE['objective'][0]}. "
            #     )
            #     story_text.insert(tk.END, response_text)
            #     return

            ai_response = chat.send_message(action)
            raw = ai_response.text if hasattr(ai_response, "text") else str(raw)


            old_time = time_as_float(
                PLAYER_STATE["day"],
                PLAYER_STATE["time_of_day"]
            )

            updated = extract_player_state(raw)
            if updated:
                PLAYER_STATE.update(updated)

                new_time = time_as_float(
                    PLAYER_STATE["day"],
                    PLAYER_STATE["time_of_day"]
                )

                elapsed = max(0, new_time - old_time)

                hunger_loss = int(elapsed * 20)
                PLAYER_STATE["hunger"] = max(0, PLAYER_STATE["hunger"] - hunger_loss)

                health_label.config(text=f"Health: {PLAYER_STATE['health']}")
                gold_label.config(text=f"Gold: {PLAYER_STATE['gold']}")
                hunger_label.config(text=f"Hunger: {PLAYER_STATE['hunger']}")
                loc_label.config(
                    text=f"I'm at {PLAYER_STATE['current_location'][0].lower() + PLAYER_STATE['current_location'][1:]}"
                )

                current_time_str = get_time_string(PLAYER_STATE['time_of_day'])

                time_icon_label.configure(image=time_icons[current_time_str])


                match get_time_string(PLAYER_STATE['time_of_day']):
                    case "Morning":
                        bg_color = "#F9D69E"
                    case "Afternoon":
                        bg_color = "#1e98bd"
                    case "Evening": 
                        bg_color = "#fb9062"
                    case "Night":
                        bg_color = "#110636"
                    case _:
                        bg_color = "#3d3a35"

                app.configure(bg=bg_color)
                top_bar.configure(bg=bg_color)
                for lbl in (health_label, gold_label, hunger_label, date_time_label, loc_label, time_icon_label):
                    lbl.configure(bg=bg_color)



                date_time_label.config(
                    text=f"Day {PLAYER_STATE['day']}, {current_time_str}"
                )

            if len(PLAYER_STATE['objective']) == 0 or PLAYER_STATE['objective'] != goal:
                PLAYER_STATE['objective'] = goal

            response_text = "\n\nGame Master: " + raw.split("---")[0].strip()
            sound_effects_for_text(response_text)


    print(PLAYER_STATE)
    typewriter_write(story_text, response_text)

def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

def load_game_menu():
    global app
    clear_window()
    app.configure(bg=bg_color)

    tk.Label(app, text="Select a Save File", bg=bg_color, fg="white", 
             font=("MedievalSharp", 30, "bold")).pack(pady=20)

    container = tk.Frame(app, bg=bg_color)
    container.pack(fill=tk.BOTH, expand=True, padx=100, pady=10)

    canvas = tk.Canvas(container, bg=bg_color, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    
    scrollable_frame = tk.Frame(canvas, bg=bg_color)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=780)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    if not os.path.exists("saves"):
        tk.Label(scrollable_frame, text="No 'saves' folder found.", bg=bg_color, fg="white", font=("MedievalSharp", 18)).pack(pady=20)
    else:
        save_files = glob.glob("saves/*.json")
        
        if not save_files:
            tk.Label(scrollable_frame, text="No save files found.", bg=bg_color, fg="white", font=("MedievalSharp", 18)).pack(pady=20)
        
        for filepath in save_files:
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                name = data.get('name', 'Unknown')
                day = data.get('day', 0)
                player_class = data.get('class', 'Unknown')
                
                display_text = f"{name}  |  Day {day}  |  {player_class}"

                btn = tk.Button(scrollable_frame, 
                                text=display_text, 
                                command=lambda f=filepath: load_game(f),
                                bg="#5f6361", 
                                fg="white", 
                                font=("MedievalSharp", 16), 
                                anchor="w",
                                padx=20,
                                relief=tk.RAISED)
                btn.pack(fill=tk.X, pady=5, ipady=5)

            except Exception as e:
                print(f"Skipping corrupt file {filepath}: {e}")

    tk.Button(app, text="Back to Main Menu", command=build_main_menu, 
              bg="#8c3b3b", fg="white", font=("MedievalSharp", 16)).pack(pady=20)


def build_main_menu():
    global app, time_icons

    if app is None:
        app = tk.Tk()
        app.title("AI Adventure")
        app.geometry("1000x800")
        
        time_icons = {
            "Morning": ImageTk.PhotoImage(Image.open("assets/clockmorning.png").resize((32, 32), Image.LANCZOS)),
            "Afternoon": ImageTk.PhotoImage(Image.open("assets/clock afternoon.png").resize((32, 32), Image.LANCZOS)),
            "Evening": ImageTk.PhotoImage(Image.open("assets/clockevening.png").resize((32, 32), Image.LANCZOS)),
            "Night": ImageTk.PhotoImage(Image.open("assets/clocknight.png").resize((32, 32), Image.LANCZOS)),
        }

    clear_window()
    app.configure(bg=bg_color)

    menu_frame = tk.Frame(app, bg=bg_color, bd=5, relief=tk.RIDGE)
    menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=600, height=500)

    title_label = tk.Label(menu_frame, text="Realm of Brukk", bg=bg_color, font=("MedievalSharp", 50, "bold"))
    title_label.pack(pady=(50, 20))

    subtitle_label = tk.Label(menu_frame, text="An AI Dungeon Adventure", bg=bg_color,  font=("MedievalSharp", 20))
    subtitle_label.pack(pady=(0, 50))

    # Buttons
    new_game_btn = tk.Button(menu_frame, text="New Game", command=build_game_ui, 
                              fg="white", font=("MedievalSharp", 24), width=15, relief=tk.FLAT, activebackground="#3f4241")
    new_game_btn.pack(pady=10)

    load_game_btn = tk.Button(menu_frame, text="Load Game", command=load_game_menu, 
                              fg="white", font=("MedievalSharp", 24), width=15, relief=tk.FLAT, activebackground="#3f4241")
    load_game_btn.pack(pady=10)

    exit_btn = tk.Button(menu_frame, text="Exit", command=app.quit, 
                         bg="#8c3b3b", fg="white", font=("MedievalSharp", 18), width=10, relief=tk.FLAT)
    exit_btn.pack(pady=(40, 0))

    return app


def build_game_ui():
    global story_text, entry_input, health_label, gold_label, loc_label, hunger_label, date_time_label, bg_color, app, top_bar, time_icon_label, time_icons

    clear_window()
    app.title("AI Adventure")
    app.configure(bg=bg_color)
    

    time_icons = {
        "Morning": ImageTk.PhotoImage(
            Image.open("assets/clockmorning.png").resize((32, 32), Image.LANCZOS)
        ),
        "Afternoon": ImageTk.PhotoImage(
            Image.open("assets/clock afternoon.png").resize((32, 32), Image.LANCZOS)
        ),
        "Evening": ImageTk.PhotoImage(
            Image.open("assets/clockevening.png").resize((32, 32), Image.LANCZOS)
        ),
        "Night": ImageTk.PhotoImage(
            Image.open("assets/clocknight.png").resize((32, 32), Image.LANCZOS)
        ),
    }

    top_bar = tk.Frame(app, bg=bg_color, height=30)
    top_bar.grid(row=0, column=0, sticky="ew")

    health_label = tk.Label(top_bar, text=f"Health: {PLAYER_STATE['health']}",
                            bg=top_bar.cget("bg"), fg="white", font=("MedievalSharp", 16))
    health_label.pack(side=tk.RIGHT, padx=10)

    gold_label = tk.Label(top_bar, text=f"Gold: {PLAYER_STATE['gold']}",
                          bg=top_bar.cget("bg"), fg="white", font=("MedievalSharp", 16))
    gold_label.pack(side=tk.RIGHT, padx=10)

    hunger_label = tk.Label(top_bar, text=f"Hunger: {PLAYER_STATE['hunger']}",
                          bg=top_bar.cget("bg"), fg="white", font=("MedievalSharp", 16))
    hunger_label.pack(side=tk.RIGHT, padx=10)

    current_time_str = get_time_string(PLAYER_STATE['time_of_day'])
    date_time_label = tk.Label(top_bar, text=f"Day {PLAYER_STATE['day']}, {current_time_str}",
                          bg=top_bar.cget("bg"), fg="white", font=("MedievalSharp", 16))
    date_time_label.pack(side=tk.RIGHT, padx=10)

    time_icon_label = tk.Label(
    top_bar,
    image=time_icons[get_time_string(PLAYER_STATE["time_of_day"])],
    bg=top_bar.cget("bg")
    )
    time_icon_label.pack(side=tk.RIGHT, padx=(0, 4))

    loc_label = tk.Label(top_bar,
                         text=f"I'm at {PLAYER_STATE['current_location'][0].lower() + PLAYER_STATE['current_location'][1:]}",
                         bg=top_bar.cget("bg"), fg="white", font=("MedievalSharp", 16))
    loc_label.pack(side=tk.LEFT, padx=10)

    story_text = tk.Text(app, wrap=tk.WORD, background="#d1b462",
                         foreground="#111024", font=("MedievalSharp", 35))
    story_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=(10, 5))

    input_frame = tk.Frame(app, height=60)
    input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

    entry_input = tk.Entry(input_frame, font=("MedievalSharp", 20))
    entry_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

    submit_button = tk.Button(
        input_frame,
        text="Submit Command",
        command=submit_action,
        bg="#5f6361",
        fg="white",
        activebackground="#3f4241",
        relief=tk.FLAT,
        font=("MedievalSharp", 16)
    )
    submit_button.pack(side=tk.RIGHT)

    inventory_button = tk.Button(
        top_bar, text="Inventory",
        command=show_inventory,
        bg="#5f6361",
        fg="white",
        relief=tk.FLAT,
        font=("MedievalSharp", 16)
    )
    inventory_button.pack(side=tk.RIGHT, padx=10)

    menu_button = tk.Button(
        top_bar, text="Menu",
        command=save_game,
        bg="#5f6361",
        fg="white",
        relief=tk.FLAT,
        font=("MedievalSharp", 16)
    )
    menu_button.pack(side=tk.RIGHT, padx=10)

    app.rowconfigure(1, weight=1)
    app.columnconfigure(0, weight=1)

    app.bind("<Return>", lambda e: submit_action())
    app.bind("<Tab>", lambda e: show_inventory())

    story_text.insert(tk.END, "Welcome to the realm of Brukk. To begin, please enter your name...")

    return app
