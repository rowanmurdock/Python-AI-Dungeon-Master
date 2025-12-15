# AI Dark Fantasy Adventure 

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Gemini API](https://img.shields.io/badge/AI-Gemini_2.5_Flash-orange)
![Status](https://img.shields.io/badge/Status-Prototype-green)

A simple, dark fantasy text adventure game built with **Python's Tkinter** for the GUI and powered by the **Gemini 2.5 Flash API** to manage the story, NPC interactions, and persistent player state.

## Overview

This project explores the intersection of classic text-based gaming and modern Large Language Models (LLMs). Unlike traditional text adventures with hard-coded paths, this game uses generative AI to act as a dynamic Game Master.

The game is set in the custom world of **Brukk** (featuring the regions of Moru, Borok, Hotaru, Gull, and Rune). The AI maintains a consistent dark fantasy tone while enforcing game rules.

## Features

* **AI Game Master:** Powered by Google's Gemini 2.5 Flash model, the GM dynamically generates scenarios, dialogue, and combat outcomes.
* **Persistent Player State:** The application acts as a bridge between the UI and the LLM. It extracts a specific JSON structure from the AI's natural language response to track:
    * Health & Inventory
    * Current Location
    * Player Class
    * Player hunger levels
    * Player win condition/goal
    * World time/time of day
    * Player Name
* **Dynamic Storytelling:** No two playthroughs are exactly the same, even if the world lore stays the same. The story unfolds organically based on your inputs within the lore of Brukk, which you can explore through multiple playthroughs.
* **Class Selection:** Choose from three distinct starting classes, each with unique starting items:
    * **Vagabond**
    * **Warrior**
    * **Spellcaster**

## Installation & Setup

### 1. Prerequisites
* **Python 3.8+**
* **Google GenAI API Key** (Get one from [Google AI Studio](https://aistudio.google.com/))
* **MedievalSharp Font**

### 2. Environment Setup
To ensure the GUI renders the fantasy aesthetic correctly, you must install the **MedievalSharp** font.
* [Download MedievalSharp from Google Fonts](https://fonts.google.com/specimen/MedievalSharp)

### 3. Install Dependencies
Create a new directory for your project and install the necessary library

```bash
pip install google-genai
```

### 4. API Key Configuration
The game relies on your API key being set as an environment variable named GOOGLE_API_KEY, using an env file.

```bash
GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

### 5. Run the Game
Save your code as main.py (or similar) and run it from your terminal:
```bash
python main.py
```

## How to Play
* Start: The game will prompt you to enter your name.

* Choose a Class: Select one of the three starting classes: Vagabond, Warrior, or Spellcaster.

* Adventure Begins: Once your class is chosen, the AI Game Master will provide the starting scenario.

* Input Commands: Type your intended action into the input box and click Submit Command.

* Examples: "I walk east toward the river," "I try to talk to the fish person," or "I check my supplies."

* State Tracking: The AI handles the consequences of your actions. Watch the sidebar as it automatically updates your Health, Inventory, Hunger, and Time of Day.

### Roadmap & Future Features
The following features are planned for future updates to deepen the Brukk experience:

* Expanded World: Deeper lore and specific locations for Moru, Borok, Hotaru, Gull, and Rune.

* NPC Relationships: Systems to track reputation with specific factions.

* Dynamic Visuals: AI-generated images triggered by specific location keywords.

* Quest Log: A UI element to track active tasks requested by NPCs.

* Visual Map: A generated map of the region to help with navigation.

* Progression System: Experience points (XP) and unlockable skills.

* Advanced Combat: Specific turn-based fighting mechanics and stats.

* Save/Load System: Ability to save the JSON state to a local file.

* Tone Selector: Menu options to change the AI's narrative style or world difficulty.
