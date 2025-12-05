import re
import ast

PLAYER_STATE = {
    'name': "Adventurer",
    'health': 100,
    'hunger':100,
    'inventory': [],
    'class': "None",
    'current_location': "A green plain in Moru",
    'gold': 20,
    'day' : 0,
    'time_of_day': 0,
    'objective': []
}

CLASS_INVENTORY = {
    "vagabond": ["Length of rope", "Small crossbow", "Short tanto", "Bread loaf (3)"],
    "warrior": ["Brass warhammer", "Rusty plate armor", "Dried meat (5)"],
    "spellcaster": ["Ancient ritual dagger", "Ancient spellbook", "Dried fruits", "Cured meats"]
}

WIN_CONDITIONS = {
    "Home and Hearth": ["Be married and own a home", 0],
    "Becoming Ruler": ["Become King or Queen of one of the 5 realms: Moru, Borok, Gull, Hotaru, or Rune", 0],
    "Dragon's Hoard": ["Have 50,000 gold coins", 0]
}

game_setup = 3


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
