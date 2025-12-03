import re
import ast

PLAYER_STATE = {
    'name': "Adventurer",
    'health': 100,
    'inventory': [],
    'class': "None",
    'current_location': "A green plain in Moru",
    'gold': 5
}

CLASS_INVENTORY = {
    "vagabond": ["Length of rope", "Small crossbow"],
    "warrior": ["Brass warhammer", "Rusty plate armor"],
    "spellcaster": ["Ancient ritual dagger", "Ancient spellbook"]
}

game_setup = 2


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
