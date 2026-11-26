import json
import math
import random
from pathlib import Path

import pygame

pygame.init()
W, H = 1100, 720
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Electric City - Simulation électrique")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 18)
SM = pygame.font.SysFont("arial", 14)
BIG = pygame.font.SysFont("arial", 34, bold=True)
WHITE = (240, 245, 250); BG = (20, 28, 40); PANEL = (31, 43, 59)
GREEN = (75, 210, 130); YELLOW = (250, 205, 70); BLUE = (80, 170, 240)
RED = (235, 85, 80); GRAY = (150, 165, 180)
SAVE_FILE = Path(__file__).with_name("saves.json")
COLS, ROWS = 8, 5
CELL_W, CELL_H = 76, 74
MAP_X, MAP_Y = 25, 178
MAP_VIEW = "map"
GRAPH_CLOCK = 0.0
SHOP_CATEGORY = "Solaire"
SHOP_SCROLL = 0

builds = []

def add_build(name, kind, cost, desc, tint, icon, category, value, tier=0):
    builds.append((name, kind, cost, desc, tint, icon, category, value, tier))

# Starting kit and customers.
add_build("Panneau solaire", "solar", 180, "85 kW au soleil", YELLOW, "☀", "Solaire", 85)
add_build("Éolienne", "wind", 350, "70 kW selon le vent", BLUE, "↻", "Éolien", 70)
add_build("Batterie", "battery", 250, "+500 kWh", GREEN, "▰", "Stockage", 500)
add_build("Borne téléphone", "phone", 120, "Clients • petite demande", (175,210,255), "⌕", "Clients", 2.2)
add_build("Borne voiture", "car", 450, "Clients • recharge auto", (210,150,255), "⚡", "Clients", 10)
add_build("Quartier", "town", 900, "Clients • nouveaux habitants", (255,150,135), "⌂", "Clients", 35)
add_build("Centrale hydro", "hydro", 650, "80 kW réguliers", (90,205,220), "≈", "Hydro", 80)
add_build("Centrale biomasse", "bio", 480, "60 kW jour et nuit", (125,190,100), "♨", "Autres", 60)

# More than 50 production and storage models, grouped by technology.
solar_models = [
    ("Panneau solaire polycristallin", 220, 110, 0), ("Panneau solaire monocristallin", 360, 155, 1),
    ("Panneau solaire bifacial", 520, 210, 1), ("Panneau solaire toiture", 280, 125, 0),
    ("Panneau solaire souple", 310, 135, 0), ("Panneau solaire à couches minces", 430, 175, 1),
    ("Panneau solaire haute tension", 700, 260, 2), ("Panneau solaire tandem", 1050, 340, 2),
    ("Panneau solaire héliostat", 1500, 430, 3), ("Ferme solaire compacte", 2400, 620, 3),
    ("Ferme solaire géante", 5200, 1100, 4),
]
for i, (name, cost, power, tier) in enumerate(solar_models):
    add_build(name, f"prod_solar_{i}", cost, f"Production : {power} kW", (245,195,65), "☀", "Solaire", power, tier)

wind_models = [
    ("Micro-éolienne", 280, 90, 0), ("Éolienne terrestre", 550, 150, 1),
    ("Éolienne à pales longues", 850, 220, 1), ("Éolienne offshore", 1450, 330, 2),
    ("Éolienne flottante", 2300, 470, 2), ("Éolienne haute puissance", 3800, 700, 3),
    ("Parc éolien", 6500, 1100, 4), ("Éolienne verticale", 720, 180, 1),
]
for i, (name, cost, power, tier) in enumerate(wind_models):
    add_build(name, f"prod_wind_{i}", cost, f"Production : {power} kW", (100,180,230), "↻", "Éolien", power, tier)

hydro_models = [
    ("Roue hydraulique", 330, 70, 0), ("Micro-turbine", 680, 145, 1),
    ("Barrage miniature", 1300, 260, 1), ("Turbine fluviale", 1900, 380, 2),
    ("Centrale marémotrice", 3400, 590, 3), ("Grand barrage", 7200, 1250, 4),
]
for i, (name, cost, power, tier) in enumerate(hydro_models):
    add_build(name, f"prod_hydro_{i}", cost, f"Production : {power} kW", (65,190,210), "≈", "Hydro", power, tier)

other_models = [
    ("Générateur diesel", 420, 120, 0), ("Centrale biomasse avancée", 820, 210, 1),
    ("Géothermie", 1450, 330, 1), ("Centrale à biogaz", 1700, 390, 2),
    ("Centrale à vapeur", 2600, 520, 2), ("Réacteur expérimental", 4300, 850, 3),
    ("Centrale nucléaire", 8500, 1500, 4), ("Fusion de démonstration", 18000, 2600, 4),
    ("Générateur de secours", 620, 160, 0), ("Centrale à hydrogène", 5100, 960, 3),
]
for i, (name, cost, power, tier) in enumerate(other_models):
    add_build(name, f"prod_other_{i}", cost, f"Production : {power} kW", (135,195,115), "⚙", "Autres", power, tier)

storage_models = [
    ("Batterie lithium", 520, 900, 1), ("Batterie LFP", 760, 1450, 1),
    ("Batterie sodium-ion", 980, 2100, 1), ("Batterie solide", 1500, 3200, 2),
    ("Batterie au plomb", 320, 650, 0), ("Batterie haute capacité", 2300, 5200, 2),
    ("Supercondensateur", 1250, 1800, 2), ("Volant d'inertie", 1750, 2800, 2),
    ("Stockage à hydrogène", 2700, 4800, 3), ("Réservoir hydrogène XL", 5200, 10500, 4),
    ("Batterie sodium-soufre", 3400, 7000, 3), ("Batterie à flux", 2100, 4900, 2),
    ("Stockage thermique", 1850, 4100, 2), ("Batterie modulaire", 2900, 6200, 3),
    ("Batterie réseau", 6200, 14500, 4), ("Batterie marine", 1150, 2500, 1),
    ("Batterie portable", 190, 350, 0), ("Batterie recyclée", 430, 850, 0),
    ("Stockage gravitaire", 4800, 11000, 4), ("Méga-batterie", 12000, 30000, 4),
]
for i, (name, cost, capacity, tier) in enumerate(storage_models):
    add_build(name, f"store_{i}", cost, f"Capacité : +{capacity} kWh", (90,210,145), "▰", "Stockage", capacity, tier)

RESEARCH_BRANCHES = ["Solaire", "Éolien", "Hydro", "Autres", "Stockage"]
RESEARCH_COSTS = [15, 35, 70, 120]
RESEARCH_BRANCH = {"Solaire":"Solaire", "Éolien":"Éolien", "Hydro":"Hydro",
                   "Autres":"Autres", "Stockage":"Stockage"}
RESEARCH_BRANCH["Clients"] = None

def fresh_game():
    return {"cash": 3200.0, "battery": 250.0, "battery_cap": 500.0,
            "day": 1, "hour": 6.0, "speed": 1, "paused": False,
            "energy_total": 0.0, "sold_total": 0.0, "outages": 0,
            "wind_factor": .65, "wind_target": .65, "wind_timer": 0.0,
            "grid": {}, "history": [], "camera_x": -4, "camera_y": -2,
            "player_x": 0, "player_y": 0, "research_points": 10,
            "research": {branch: 0 for branch in RESEARCH_BRANCHES}}

game = fresh_game()
mode = "menu"
selected = 0
notice = "Choisis un bâtiment, puis une parcelle libre."
notice_timer = 4.0
admin = False

def counts():
    result = {kind: 0 for _, kind, *_ in builds}
    for kind in game["grid"].values():
        if kind in result:
            result[kind] += 1
    return result

def production():
    daylight = max(0, math.sin((game["hour"] - 6) / 12 * math.pi))
    c = counts()
    solar_power = c["solar"] * 85 * daylight
    wind_power = c["wind"] * 70 * game["wind_factor"]
    water_power = c["hydro"] * 80
    other_power = c["bio"] * 60
    for item in builds:
        amount = c[item[1]]
        if not amount or item[6] in ("Stockage", "Clients"):
            continue
        power = amount * item[7]
        if item[6] == "Solaire": solar_power += power * daylight
        elif item[6] == "Éolien": wind_power += power * game["wind_factor"]
        elif item[6] == "Hydro": water_power += power
        else: other_power += power
    return solar_power + water_power + other_power, wind_power

def item_unlocked(item):
    branch = RESEARCH_BRANCH.get(item[6])
    return item[8] == 0 or branch is None or game["research"].get(branch, 0) >= item[8]

def focus_player():
    game["camera_x"] = game["player_x"] - COLS//2
    game["camera_y"] = game["player_y"] - ROWS//2

def say(message):
    global notice, notice_timer
    notice, notice_timer = message, 3.0

def button(rect, label, active=False, color=None):
    fill = color or ((67, 105, 117) if active else (52, 70, 91))
    pygame.draw.rect(screen, fill, rect, border_radius=8)
    pygame.draw.rect(screen, (120, 150, 175), rect, 2, border_radius=8)
    surf = FONT.render(label, True, WHITE)
    screen.blit(surf, (rect[0] + (rect[2]-surf.get_width())//2,
                       rect[1] + (rect[3]-surf.get_height())//2))

def save_slots():
    try:
        data = json.loads(SAVE_FILE.read_text(encoding="utf-8")) if SAVE_FILE.exists() else {}
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}

def save_game(slot=1):
    slots = save_slots()
    state = {k: v for k, v in game.items() if k != "grid"}
    state["grid"] = game["grid"]
    slots[str(slot)] = state
    try:
        SAVE_FILE.write_text(json.dumps(slots, indent=2), encoding="utf-8")
        say(f"Partie sauvegardée dans l'emplacement {slot}.")
        return True
    except OSError:
        say("Impossible d'écrire la sauvegarde.")
        return False

def load_game(slot=1):
    global game
    data = save_slots().get(str(slot))
    if not isinstance(data, dict):
        say("Aucune sauvegarde dans cet emplacement.")
        return False
    try:
        fresh = fresh_game()
        fresh.update(data)
        allowed = {item[1] for item in builds}
        grid = fresh["grid"]
        # Convert saves created by the first map version into world coordinates.
        if isinstance(grid, list):
            grid = {f"{x},{y}": value for y, row in enumerate(grid)
                    for x, value in enumerate(row) if value is not None}
        if not isinstance(grid, dict) or any(value not in allowed for value in grid.values()):
            raise ValueError
        fresh["grid"] = grid
        fresh.setdefault("history", [])
        fresh.setdefault("research_points", 0)
        fresh.setdefault("research", {branch: 0 for branch in RESEARCH_BRANCHES})
        fresh.setdefault("player_x", 0); fresh.setdefault("player_y", 0)
        fresh.setdefault("camera_x", 0); fresh.setdefault("camera_y", 0)
        if not isinstance(fresh["research"], dict):
            raise ValueError
        for branch in RESEARCH_BRANCHES:
            fresh["research"].setdefault(branch, 0)
        game = fresh
        while f"{game['player_x']},{game['player_y']}" in game["grid"]:
            game["player_x"] += 1
        if isinstance(game["camera_x"], int) and isinstance(game["camera_y"], int):
            focus_player()
        return True
    except (TypeError, ValueError):
        say("Cette sauvegarde est abîmée.")
        return False

def draw_header(title="ELECTRIC CITY"):
    pygame.draw.rect(screen, (35, 50, 68), (0, 0, W, 90))
    text(title, 25, 17, GREEN, BIG)
    text("Développe ton réseau et alimente ta ville parcelle par parcelle.", 27, 59, GRAY, SM)

def text(s, x, y, color=WHITE, font=FONT):
    screen.blit(font.render(str(s), True, color), (x, y))

def draw_menu():
    screen.fill(BG)
    draw_header("ELECTRIC CITY")
    pygame.draw.rect(screen, PANEL, (170, 125, 760, 545), border_radius=18)
    text("Ta ville, ton énergie", 225, 155, YELLOW, BIG)
    text("Construis une centrale équilibrée, stocke l'énergie et sers tes clients.", 225, 202, GRAY)
    button((225, 255, 300, 64), "NOUVELLE PARTIE", color=(44, 120, 85))
    button((575, 255, 300, 64), "REPRENDRE", color=(45, 94, 135))
    text("SAUVEGARDES", 225, 350, YELLOW)
    slots = save_slots()
    for i in range(3):
        y = 390 + i*78
        info = slots.get(str(i+1))
        label = f"Emplacement {i+1}  •  Jour {info.get('day', '?')}" if info else f"Emplacement {i+1}  •  vide"
        text(label, 235, y+13, WHITE if info else GRAY)
        button((595, y, 120, 48), "CHARGER", bool(info))
        button((735, y, 140, 48), "SAUVEGARDER")
    text("Clique sur une sauvegarde pour la charger. Les parties sont stockées dans saves.json.",
         225, 635, GRAY, SM)

def draw_game():
    global SHOP_SCROLL
    screen.fill(BG)
    draw_header()
    c = counts(); sun, windp = production()
    pygame.draw.rect(screen, PANEL, (25, 105, 1050, 58), border_radius=10)
    text(f"Jour {game['day']} • {int(game['hour']):02d}:{int(game['hour']%1*60):02d}", 42, 122, YELLOW)
    text(f"Budget : {game['cash']:.0f} €", 250, 122, GREEN)
    text(f"Production : {sun+windp:.0f} kW", 465, 122, BLUE)
    text(f"Stock : {game['battery']:.0f}/{game['battery_cap']:.0f} kWh", 685, 122)
    text(f"Coupures : {game['outages']}", 910, 122, RED if game["outages"] else GRAY)

    pygame.draw.rect(screen, PANEL, (25, 175, 640, 434), border_radius=12)
    title = {"map":"CARTE DES PARCELLES", "graph":"GRAPHIQUES DU RÉSEAU", "research":"ARBRE DE RECHERCHE"}[MAP_VIEW]
    text(title, 42, 188, YELLOW)
    button((520, 181, 125, 34), "GRAPHIQUES" if MAP_VIEW == "map" else "CARTE", MAP_VIEW == "graph")
    if MAP_VIEW == "map":
        clock_label = "JOUR" if 6 <= game["hour"] < 20 else "NUIT"
        text(f"Case {game['player_x']},{game['player_y']} • Z Q S D pour marcher • {clock_label}", 42, 215, GRAY, SM)
        for row in range(ROWS):
            for col in range(COLS):
                x, y = MAP_X + 12 + col*CELL_W, MAP_Y + 60 + row*CELL_H
                wx, wy = game["camera_x"] + col, game["camera_y"] + row
                kind = game["grid"].get(f"{wx},{wy}")
                rect = (x, y, CELL_W-5, CELL_H-5)
                day_color = (59, 89, 76) if 6 <= game["hour"] < 20 else (36, 48, 69)
                pygame.draw.rect(screen, (47, 67, 68) if kind else day_color, rect, border_radius=7)
                pygame.draw.rect(screen, (105, 133, 125) if kind else (70, 96, 79), rect, 1, border_radius=7)
                if kind:
                    item = next(b for b in builds if b[1] == kind)
                    draw_building(item, x, y)
                else:
                    pygame.draw.circle(screen, (72,112,81), (x+15,y+16), 2)
                    pygame.draw.circle(screen, (72,112,81), (x+58,y+47), 2)
                if (wx,wy) == (game["player_x"],game["player_y"]):
                    draw_character(x, y)
        text(f"{int(game['hour']):02d}:{int(game['hour']%1*60):02d} • {clock_label}", 520, 215, YELLOW, SM)
    elif MAP_VIEW == "graph":
        draw_graphs()
    else:
        draw_research()

    if MAP_VIEW != "research":
        pygame.draw.rect(screen, PANEL, (680, 175, 395, 434), border_radius=12)
        text("CONSTRUIRE", 698, 188, YELLOW)
        text(f"Recherche : {game['research_points']:.0f} pts", 895, 188, GREEN, SM)
        categories = ["Solaire", "Éolien", "Hydro", "Autres", "Stockage", "Clients"]
        for i, category in enumerate(categories):
            x = 692 + i*62
            caption = {"Stockage":"STOCK", "Solaire":"SOL."}.get(category, category.upper())
            button((x, 221, 59, 32), caption, SHOP_CATEGORY == category)
        text("Sélection : " + builds[selected][0][:28], 698, 258, GREEN, SM)
        catalog = [item for item in builds if item[6] == SHOP_CATEGORY]
        SHOP_SCROLL = max(0, min(SHOP_SCROLL, max(0, (len(catalog)-6+1)//2)))
        visible = catalog[SHOP_SCROLL*2:SHOP_SCROLL*2+6]
        for slot, item in enumerate(visible):
            name, kind, cost, desc, tint, icon, category, value, tier = item
            x, y = 695 + (slot%2)*183, 280 + (slot//2)*94
            item_idx = builds.index(item)
            unlocked = item_unlocked(item)
            pygame.draw.rect(screen, (53,75,87) if selected == item_idx else (38,53,70), (x,y,174,84), border_radius=9)
            pygame.draw.rect(screen, tint if selected == item_idx else (73,92,108), (x,y,174,84), 2, border_radius=9)
            draw_icon(item, x+8, y+14)
            text(name[:20], x+47, y+7, WHITE if unlocked else GRAY, SM)
            text(f"{cost} €" if unlocked else f"Recherche niv. {tier}", x+47, y+28,
                 (GREEN if game["cash"] >= cost else RED) if unlocked else YELLOW, SM)
            text(desc[:24], x+8, y+63, GRAY, SM)
        text(f"{SHOP_CATEGORY} • molette dans le catalogue pour défiler", 698, 570, YELLOW, SM)
        text(f"Parcelles bâties : {len(game['grid'])} • objets : {len(builds)}", 698, 588, WHITE, SM)

    pygame.draw.rect(screen, PANEL, (25, 622, 1050, 78), border_radius=10)
    button((40, 638, 110, 44), "MENU", color=(75, 77, 93))
    button((165, 638, 105, 44), "PAUSE" if not game["paused"] else "REPRENDRE", game["paused"])
    for i, mult in enumerate((1,2,4)):
        button((285+i*85, 638, 75, 44), f"x{mult}", game["speed"] == mult)
    button((555, 638, 165, 44), "SAUVEGARDER", color=(44, 120, 85))
    button((740, 638, 135, 44), "RECHERCHE", MAP_VIEW == "research", (75,95,125))
    text(f"Ventes : {game['sold_total']:.0f} kWh", 895, 638, GRAY, SM)
    text("Espace : pause", 895, 659, GRAY, SM)
    if notice_timer > 0:
        text(notice, 42, 602, YELLOW, SM)
    text("ZQSD : marcher • G : graphiques • R : recherche", 750, 678, GRAY, SM)
    if admin:
        pygame.draw.rect(screen, (34,48,65), (350, 285, 400, 130), border_radius=14)
        text("Mode test (F3)", 380, 305, YELLOW, BIG)
        button((380, 355, 150, 45), "+5000 €")
        button((555, 355, 150, 45), "Batterie pleine")

def draw_graphs():
    history = game.get("history", [])
    text("Puissance (kW) • historique récent", 48, 222, GRAY, SM)
    plot = pygame.Rect(55, 250, 580, 150)
    pygame.draw.rect(screen, (24, 35, 49), plot, border_radius=7)
    pygame.draw.line(screen, (80, 96, 112), (plot.left, plot.bottom-1), (plot.right, plot.bottom-1), 1)
    if len(history) > 1:
        max_power = max(50, max(max(p[0], p[1]) for p in history))
        for idx, color in ((0, BLUE), (1, RED)):
            points = []
            for i, sample in enumerate(history):
                x = plot.left + int(i*(plot.width-2)/(len(history)-1))
                y = plot.bottom - 4 - int(min(1, sample[idx]/max_power)*(plot.height-8))
                points.append((x,y))
            if len(points) > 1: pygame.draw.lines(screen, color, False, points, 3)
    pygame.draw.line(screen, BLUE, (62, 414), (82,414), 3); text("Production", 88, 406, BLUE, SM)
    pygame.draw.line(screen, RED, (185, 414), (205,414), 3); text("Consommation", 211, 406, RED, SM)
    text("Niveau de batterie (kWh)", 48, 441, YELLOW, SM)
    stock = pygame.Rect(55, 466, 580, 100)
    pygame.draw.rect(screen, (24, 35, 49), stock, border_radius=7)
    if len(history) > 1:
        cap = max(1, game["battery_cap"])
        points = [(stock.left + int(i*(stock.width-2)/(len(history)-1)),
                   stock.bottom-4-int(min(1,sample[2]/cap)*(stock.height-8)))
                  for i,sample in enumerate(history)]
        if len(points) > 1: pygame.draw.lines(screen, YELLOW, False, points, 3)
    text(f"{game['battery']:.0f} / {game['battery_cap']:.0f} kWh", 48, 574, YELLOW, SM)
    text("Échelle adaptée automatiquement • 60 derniers relevés", 48, 591, GRAY, SM)

def draw_icon(item, x, y):
    """Draw a small, textured equipment symbol with native Pygame shapes."""
    name, category, tint = item[0], item[6], item[4]
    if category == "Solaire":
        panel_color = (45,105,148)
        if "Ferme" in name:
            for n in range(3):
                pygame.draw.polygon(screen, panel_color, [(x+n*10,y+19),(x+8+n*10,y+16),(x+9+n*10,y+31),(x+1+n*10,y+33)])
        elif "héliostat" in name.lower():
            pygame.draw.rect(screen, (145,155,160), (x+14,y+16,4,24))
            pygame.draw.circle(screen, (255,226,125), (x+16,y+9), 7)
            for n in range(4):
                pygame.draw.line(screen, tint, (x+16,y+16),(x+2+n*9,y+27),2)
        else:
            pygame.draw.polygon(screen, panel_color, [(x,y+18),(x+29,y+13),(x+32,y+31),(x+3,y+35)])
            pygame.draw.line(screen, (135,210,235), (x+9,y+17), (x+12,y+34), 1)
            pygame.draw.line(screen, (135,210,235), (x+20,y+15), (x+23,y+32), 1)
        pygame.draw.line(screen, tint, (x+4,y+39), (x+30,y+36), 2)
    elif category == "Éolien":
        pygame.draw.line(screen, (210,220,225), (x+16,y+18), (x+16,y+43), 3)
        pygame.draw.circle(screen, tint, (x+16,y+17), 4)
        pygame.draw.line(screen, tint, (x+16,y+17), (x+16,y+3), 3)
        pygame.draw.line(screen, tint, (x+16,y+17), (x+4,y+24), 3)
        pygame.draw.line(screen, tint, (x+16,y+17), (x+28,y+25), 3)
    elif category == "Stockage":
        if "hydrogène" in name.lower():
            pygame.draw.rect(screen, (90,145,170), (x+8,y+8,18,33), border_radius=8)
            pygame.draw.rect(screen, (195,220,220), (x+13,y+4,8,6), border_radius=2)
            pygame.draw.line(screen, (215,235,240), (x+11,y+16),(x+23,y+16),2)
        elif "volant" in name.lower() or "gravitaire" in name.lower():
            pygame.draw.circle(screen, (85,100,115), (x+17,y+24), 16)
            pygame.draw.circle(screen, tint, (x+17,y+24), 4)
            for angle in range(0,360,45):
                dx,dy=math.cos(math.radians(angle))*12,math.sin(math.radians(angle))*12
                pygame.draw.line(screen, tint, (x+17,y+24),(int(x+17+dx),int(y+24+dy)),2)
        else:
            pygame.draw.rect(screen, (70,95,110), (x+3,y+7,27,34), border_radius=4)
            pygame.draw.rect(screen, tint, (x+8,y+13,17,22), border_radius=3)
            pygame.draw.rect(screen, (220,230,225), (x+11,y+3,10,5), border_radius=2)
            for stripe in (18,24,30):
                pygame.draw.line(screen, (245,250,240), (x+11,stripe), (x+21,stripe), 2)
    elif category == "Hydro":
        if "barrage" in name.lower():
            pygame.draw.polygon(screen, (135,150,155), [(x+3,y+9),(x+29,y+14),(x+26,y+39),(x+6,y+39)])
            pygame.draw.line(screen, (100,220,230), (x+1,y+35),(x+32,y+35),3)
            for ripple in (0,7,14): pygame.draw.arc(screen, (140,225,235),(x+ripple,y+35,12,7),0,math.pi,2)
        else:
            pygame.draw.polygon(screen, (65,115,145), [(x+2,y+21),(x+30,y+15),(x+30,y+40),(x+2,y+40)])
            pygame.draw.line(screen, (100,220,230), (x+2,y+24),(x+30,y+18), 3)
            pygame.draw.circle(screen, tint, (x+19,y+30), 7, 2)
            pygame.draw.line(screen, (220,230,230), (x+19,y+23),(x+19,y+37),2)
    elif category == "Clients":
        if item[1] == "town":
            pygame.draw.polygon(screen, tint, [(x+2,y+24),(x+16,y+10),(x+31,y+24)])
            pygame.draw.rect(screen, (190,155,110), (x+6,y+23,21,19))
            pygame.draw.rect(screen, (70,90,110), (x+14,y+29,7,13))
        elif item[1] == "car":
            pygame.draw.rect(screen, tint, (x+2,y+19,30,14), border_radius=5)
            pygame.draw.polygon(screen, (175,205,225), [(x+8,y+19),(x+13,y+11),(x+24,y+11),(x+29,y+19)])
            pygame.draw.circle(screen, (30,35,45),(x+9,y+34),4); pygame.draw.circle(screen,(30,35,45),(x+26,y+34),4)
        else:
            pygame.draw.rect(screen, tint, (x+9,y+5,18,35), border_radius=5)
            pygame.draw.rect(screen, (35,50,65), (x+12,y+10,12,20), border_radius=2)
            pygame.draw.circle(screen, WHITE, (x+18,y+35), 2)
    else:
        pygame.draw.rect(screen, (96,110,118), (x+3,y+19,28,23), border_radius=3)
        pygame.draw.polygon(screen, tint, [(x+1,y+21),(x+16,y+9),(x+33,y+21)])
        pygame.draw.rect(screen, (115,125,130), (x+20,y+3,7,15))
        pygame.draw.line(screen, (215,225,225), (x+22,y+3),(x+27,y+3),2)

def draw_building(item, x, y):
    draw_icon(item, x+20, y+3)
    name = item[0]
    label = name.replace("Panneau ", "").replace("Centrale ", "")
    text(label[:12], x+3, y+49, WHITE, SM)

def draw_character(x, y):
    # Small explorer sprite, with a clock bubble so the day/night cycle is visible in-world.
    pygame.draw.ellipse(screen, (20,28,33), (x+19,y+55,38,8))
    pygame.draw.line(screen, (35,45,60), (x+31,y+47),(x+28,y+60),4)
    pygame.draw.line(screen, (35,45,60), (x+45,y+47),(x+48,y+60),4)
    pygame.draw.rect(screen, (65,145,205), (x+28,y+28,19,22), border_radius=5)
    pygame.draw.line(screen, (65,145,205), (x+29,y+32),(x+22,y+44),4)
    pygame.draw.line(screen, (65,145,205), (x+46,y+32),(x+53,y+42),4)
    pygame.draw.circle(screen, (235,190,145), (x+38,y+20), 10)
    pygame.draw.arc(screen, (72,48,36), (x+28,y+10,20,15), math.pi, math.tau, 4)
    pygame.draw.circle(screen, (35,40,45), (x+35,y+20), 1)
    pygame.draw.circle(screen, (35,40,45), (x+41,y+20), 1)
    pygame.draw.rect(screen, (247,245,225), (x+2,y+1,66,17), border_radius=6)
    pygame.draw.rect(screen, (90,105,115), (x+2,y+1,66,17), 1, border_radius=6)
    time_text = f"{int(game['hour']):02d}h{int(game['hour']%1*60):02d}"
    bubble = SM.render(time_text, True, (35,45,55))
    screen.blit(bubble, (x+7,y+2))

def draw_research():
    pygame.draw.rect(screen, PANEL, (35, 225, 1030, 365), border_radius=12)
    text(f"Points de recherche : {game['research_points']:.1f}", 55, 238, GREEN, FONT)
    text("Vends de l'énergie pour gagner des points. Chaque colonne est une branche.", 55, 262, GRAY, SM)
    branch_colors = [YELLOW, BLUE, (85,205,220), (140,205,125), GREEN]
    for col, branch in enumerate(RESEARCH_BRANCHES):
        x = 55 + col*200
        text(branch, x, 292, branch_colors[col], FONT)
        level = game["research"].get(branch, 0)
        for tier in range(4):
            y = 328 + tier*59
            if tier < 3:
                pygame.draw.line(screen, branch_colors[col], (x+76,y+47), (x+76,y+58), 3)
            unlocked = tier < level
            current = tier == level
            fill = (48,110,82) if unlocked else (55,74,91) if current else (34,45,59)
            pygame.draw.rect(screen, fill, (x,y,174,47), border_radius=8)
            pygame.draw.rect(screen, branch_colors[col] if current or unlocked else (75,88,100),
                             (x,y,174,47), 2, border_radius=8)
            label = f"Niveau {tier+1} ✓" if unlocked else f"Niveau {tier+1} • {RESEARCH_COSTS[tier]} pts"
            text(label, x+9, y+5, WHITE if current or unlocked else GRAY, SM)
            item_n = sum(1 for item in builds if item[6] == branch and item[8] == tier+1)
            text(f"Débloque {item_n} équipement(s)", x+9, y+25, GRAY, SM)
    text("Clique sur le prochain niveau d'une branche pour l'étudier.", 55, 566, YELLOW, SM)

def research_click(pos):
    mx, my = pos
    if not (328 <= my <= 552):
        return
    col = (mx-55)//200
    tier = (my-328)//59
    if 0 <= col < len(RESEARCH_BRANCHES) and 0 <= tier < 4:
        branch = RESEARCH_BRANCHES[col]
        if tier != game["research"].get(branch, 0):
            say("Étudie les niveaux dans l'ordre de la branche.")
            return
        cost = RESEARCH_COSTS[tier]
        if game["research_points"] < cost:
            say(f"Il faut {cost} points de recherche pour ce niveau.")
            return
        game["research_points"] -= cost
        game["research"][branch] = tier+1
        say(f"Recherche {branch} niveau {tier+1} terminée !")

def place(col, row):
    item = builds[selected]
    name, kind, cost = item[:3]
    key = f"{game['camera_x']+col},{game['camera_y']+row}"
    if not item_unlocked(item):
        say("Cette installation demande une recherche supplémentaire.")
    elif key == f"{game['player_x']},{game['player_y']}":
        say("Déplace ton personnage avant de construire sur cette parcelle.")
    elif key in game["grid"]:
        say("Cette parcelle est déjà occupée.")
    elif game["cash"] < cost:
        say("Tu n'as pas assez d'argent.")
    else:
        game["cash"] -= cost
        game["grid"][key] = kind
        if item[6] == "Stockage":
            game["battery_cap"] += item[7]
        say(f"{name} installé !")

def move_player(dx, dy):
    nx, ny = game["player_x"]+dx, game["player_y"]+dy
    if f"{nx},{ny}" in game["grid"]:
        say("Un bâtiment bloque le passage.")
        return
    game["player_x"], game["player_y"] = nx, ny
    focus_player()

def simulate(dt):
    global GRAPH_CLOCK
    game["hour"] += dt * game["speed"] * .28
    if game["hour"] >= 24:
        game["hour"] -= 24; game["day"] += 1
        save_game(1)  # Autosave at each new day.
    game["wind_timer"] += dt
    if game["wind_timer"] > 6:
        game["wind_timer"] = 0
        game["wind_target"] = random.uniform(.25, 1.0)
    game["wind_factor"] += (game["wind_target"] - game["wind_factor"]) * min(1, dt*.1)
    c = counts(); sun, windp = production(); gen = sun + windp
    phone_demand = c["phone"] * 2.2
    car_demand = c["car"] * 10
    town_demand = c["town"] * 35
    demand = phone_demand + car_demand + town_demand
    step = dt * game["speed"] * .28
    supplied = 0.0
    if gen > demand:
        game["battery"] = min(game["battery_cap"], game["battery"] + (gen-demand)*step)
    else:
        shortage = demand-gen
        supplied = min(game["battery"], shortage*step)
        game["battery"] -= supplied
    available = gen + (supplied/step if step > 0 else 0)
    ratio = 1 if demand <= 0 else min(1, available/demand)
    # Customer payments are boosted so a small network can grow in a few game minutes.
    game["cash"] += (phone_demand*2.0 + car_demand*4.0 + town_demand*.55)*ratio*step
    sold = demand*ratio*step
    game["sold_total"] += sold
    game["research_points"] += sold*.08
    if demand > 0 and ratio < .7:
        game["outages"] += dt
    GRAPH_CLOCK += dt
    if GRAPH_CLOCK >= .5:
        GRAPH_CLOCK = 0
        game["history"].append([gen, demand*ratio, game["battery"]])
        game["history"] = game["history"][-60:]

def main():
    global mode, selected, admin, notice_timer, game, MAP_VIEW, SHOP_CATEGORY, SHOP_SCROLL
    running = True
    while running:
        dt = min(clock.tick(60)/1000, .1)
        notice_timer = max(0, notice_timer-dt)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                if mode == "game": save_game(1)
                running = False
            elif e.type == pygame.KEYDOWN:
                if mode == "game" and e.key == pygame.K_SPACE:
                    game["paused"] = not game["paused"]
                elif mode == "game" and e.key == pygame.K_ESCAPE:
                    mode = "menu"
                elif mode == "game" and e.key == pygame.K_F3:
                    admin = not admin
                elif mode == "game" and e.key == pygame.K_z:
                    move_player(0,-1)
                elif mode == "game" and e.key == pygame.K_s:
                    move_player(0,1)
                elif mode == "game" and e.key == pygame.K_q:
                    move_player(-1,0)
                elif mode == "game" and e.key == pygame.K_d:
                    move_player(1,0)
                elif mode == "game" and e.key == pygame.K_g:
                    MAP_VIEW = "graph" if MAP_VIEW == "map" else "map"
                elif mode == "game" and e.key == pygame.K_r:
                    MAP_VIEW = "map" if MAP_VIEW == "research" else "research"
            elif e.type == pygame.MOUSEWHEEL and mode == "game":
                mx, my = pygame.mouse.get_pos()
                if 680 <= mx <= 1075 and 270 <= my <= 560 and MAP_VIEW != "research":
                    catalog = [item for item in builds if item[6] == SHOP_CATEGORY]
                    max_scroll = max(0, (len(catalog)-6+1)//2)
                    SHOP_SCROLL = max(0, min(max_scroll, SHOP_SCROLL-e.y))
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                if mode == "menu":
                    if 225 <= mx <= 525 and 255 <= my <= 319:
                        game = fresh_game(); mode = "game"; say("Nouvelle ville créée !")
                    elif 575 <= mx <= 875 and 255 <= my <= 319:
                        if load_game(1): mode = "game"; say("Partie chargée !")
                    else:
                        for i in range(3):
                            y = 390 + i*78
                            if 595 <= mx <= 715 and y <= my <= y+48:
                                if load_game(i+1): mode = "game"; say(f"Emplacement {i+1} chargé !")
                            elif 735 <= mx <= 875 and y <= my <= y+48:
                                if save_game(i+1): say(f"Partie sauvegardée dans l'emplacement {i+1}.")
                elif admin and 350 <= mx <= 750 and 285 <= my <= 415:
                    if 380 <= mx <= 530 and 355 <= my <= 400: game["cash"] += 5000
                    elif 555 <= mx <= 705 and 355 <= my <= 400: game["battery"] = game["battery_cap"]
                elif 520 <= mx <= 645 and 181 <= my <= 215:
                    MAP_VIEW = "graph" if MAP_VIEW == "map" else "map"
                elif 740 <= mx <= 875 and 638 <= my <= 682:
                    MAP_VIEW = "map" if MAP_VIEW == "research" else "research"
                elif 40 <= mx <= 150 and 638 <= my <= 682:
                    mode = "menu"
                elif 165 <= mx <= 270 and 638 <= my <= 682:
                    game["paused"] = not game["paused"]
                elif 285 <= mx <= 530 and 638 <= my <= 682:
                    game["speed"] = (1,2,4)[min(2, (mx-285)//85)]
                elif 555 <= mx <= 720 and 638 <= my <= 682:
                    save_game(1)
                elif MAP_VIEW != "research" and 692 <= mx <= 1065 and 221 <= my <= 253:
                    categories = ["Solaire", "Éolien", "Hydro", "Autres", "Stockage", "Clients"]
                    idx = (mx-692)//62
                    if 0 <= idx < len(categories):
                        SHOP_CATEGORY = categories[idx]
                        SHOP_SCROLL = 0
                elif MAP_VIEW != "research" and 695 <= mx <= 1060 and 280 <= my < 552:
                    col = 0 if mx < 878 else 1
                    row = (my-280)//94
                    slot = int(row)*2+col
                    catalog = [item for item in builds if item[6] == SHOP_CATEGORY]
                    visible = catalog[SHOP_SCROLL*2:SHOP_SCROLL*2+6]
                    if 0 <= slot < len(visible): selected = builds.index(visible[slot])
                elif MAP_VIEW == "research" and 35 <= mx <= 1065 and 225 <= my <= 590:
                    research_click(e.pos)
                elif MAP_VIEW == "map" and MAP_X+12 <= mx < MAP_X+12+COLS*CELL_W and MAP_Y+60 <= my < MAP_Y+60+ROWS*CELL_H:
                    col = (mx-(MAP_X+12))//CELL_W
                    row = (my-(MAP_Y+60))//CELL_H
                    if 0 <= col < COLS and 0 <= row < ROWS: place(col,row)
        if mode == "game" and not game["paused"] and not admin:
            simulate(dt)
        if mode == "menu":
            draw_menu()
        else:
            draw_game()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
