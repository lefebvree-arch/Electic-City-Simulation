# Electric City (prototype Python/Pygame)

## Install
1. Install Python 3.
2. In a terminal run: `pip install pygame`
3. Run: `python electric_city.py`

## Gameplay
- Use the main menu to start a new city or load one of three save slots.
- Choose a building in the construction panel, then click an empty parcel on the map to place it.
- The parcel map is endless. Walk with ZQSD; the camera follows your character. Buildings block the path.
- The explorer and changing sky show the time of day. Solar production drops at night.
- The catalog has more than 50 production and storage machines in technology categories. Scroll in the catalog to see them all.
- Press R or click RECHERCHE to open the research tree. Selling energy earns research points for better equipment.
- Click **GRAPHIQUES** or press G to see recent production, consumption and battery storage.
- Equipment illustrations are drawn as detailed Pygame sprites, with distinct panels, turbines, batteries, dams, chargers and power plants.
- The day/night cycle changes solar output.
- Wind production varies.
- Batteries store energy and help during shortages.
- Demand and sales generate revenue.
- Save from the game menu or the main menu. The game also autosaves to slot 1 when a new day starts.
- Space pauses; use the on-screen buttons to change speed or save. Escape returns to the main menu.
- F3 opens the test menu.

This is a prototype and uses simplified energy/economy calculations.
