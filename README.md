A simple, dark fantasy text adventure game built with Python's Tkinter for the GUI and powered by the Gemini 2.5 Flash API to manage the story, NPC interactions, and persistent player state.

Features
AI Game Master: The Gemini 2.5 Flash model acts as the Game Master, maintaining a dark fantasy tone and enforcing game rules.
Persistent Player State: The game tracks and updates the player's name, class, health, inventory, and current location using a specific JSON-like structure extracted from the AI's response.
Dynamic Storytelling: The adventure unfolds based on the player's actions within the custom world of Brukk (Moru, Borok, Hotaru, Gull, and Rune regions).
Class Selection: Players choose a starting class (Vagabond, Warrior, or Spellcaster) that grants specific starting inventory items.

Installation and Setup
1. Prerequisites
   
  Python 3.8+

  A Gemini API Key (get one from Google AI Studio).

  MedievalSharp font installed

3. Set up the Environment
   
  The application uses the MedievalSharp font. For the GUI to display correctly, please ensure this font is installed on your system. You can download it directly from Google Fonts.
Create a new directory for your project and install the necessary library:
pip install google-genai

4. API Key Configuration
The code relies on your API key being set as an environment variable named GOOGLE_API_KEY.

    -On Linux/macOS:
export GOOGLE_API_KEY="YOUR_API_KEY_HERE"

    -On Windows (Command Prompt):
set GOOGLE_API_KEY="YOUR_API_KEY_HERE"

5. Run the Game
Save your code as game.py (or similar) and run it from your terminal:
python main.py

How to Play
Start: The game will prompt you to enter your name.
Choose a Class: Select one of the three starting classes: Vagabond, Warrior, or Spellcaster.
Adventure Begins: Once your class is chosen, the AI Game Master will provide the starting scenario.
Input Commands: Type your intended action (e.g., "I walk east toward the river," or "I try to talk to the fish person") into the input box and click Submit Command.
State Tracking: The AI handles the consequences of your actions, updates your health and inventory, and continues the story.

Future features:
- More in depth world
- Relationships with NPC groups
- Adding images depending on keywords
- Adding quest log with quests NPCs have asked of you
- Adding time
- Adding map
- Adding skill or experience system
- More specific fighting/combat gameplay
- Saving and loading
- Menu with different AI tones/worlds to choose from
