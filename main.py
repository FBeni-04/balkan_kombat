#Geci ronda kód, de kit érdekel....
import pygame
import sys
import Global
import random
from random import choice
from CountryBall import CountryBall
from pathlib import Path
import unicodedata
import os

def normalize_filename(name):
    return name.lower().replace(" ", "_")


# --- Kép indexelés: bárhogy nevezett fájlt megtalálunk ---
def _simplify_key(s: str) -> str:
    # ékezetek kiszedése + kisbetű + szóköz/kötőjel/alávonás/pont/aposztróf eldobása
    s_norm = unicodedata.normalize('NFKD', s)
    s_ascii = ''.join(ch for ch in s_norm if not unicodedata.combining(ch))
    s_ascii = s_ascii.lower()
    for ch in [' ', '_', '-', '.', "'"]:
        s_ascii = s_ascii.replace(ch, '')
    return s_ascii

IMAGE_DIR = Path('./images')
IMAGE_INDEX: dict[str, Path] = {}

def _build_image_index():
    IMAGE_INDEX.clear()
    if not IMAGE_DIR.exists():
        print(f"[WARN] Képmappa nem létezik: {IMAGE_DIR.resolve()}")
        return
    for p in IMAGE_DIR.iterdir():
        if p.is_file() and p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}:
            key = _simplify_key(p.stem)
            # Ha duplikált kulcs lenne, ne írjuk felül vakon — de itt az első nyer
            IMAGE_INDEX.setdefault(key, p)

_build_image_index()

def load_image_smart(name: str, size=(100, 100)) -> pygame.Surface:
    """
    Bárhogy írt 'name' alapján megpróbáljuk megtalálni a fájlt a ./images mappában.
    Ha nincs találat, helyettesítő (placeholder) felületet ad vissza.
    """
    key = _simplify_key(name)
    path = IMAGE_INDEX.get(key)

    # Extra esély: néha a kiterjesztés nélkül mentett logók több variánssal léteznek
    if path is None:
        # próbáljuk meg közvetlenül az eredeti nevet is (szóközökkel)
        raw = IMAGE_DIR / f"{name}.png"
        if raw.exists():
            path = raw

    if path and path.exists():
        try:
            img = pygame.image.load(str(path)).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            return img
        except Exception as e:
            print(f"[ERR] Nem sikerült betölteni: {path} -> {e}")

    # --- Placeholder, ha nincs kép ---
    w, h = size
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(surf, (80, 80, 80), surf.get_rect(), width=3)
    # rövid felirat középre, hogy lásd, mi hiányzik
    try:
        fnt = pygame.font.SysFont("Arial", 16)
        txt = fnt.render(name[:12], True, (200, 200, 200))
        surf.blit(txt, ( (w - txt.get_width())//2, (h - txt.get_height())//2 ))
    except:
        pass
    print(f"[WARN] Kép nem található: '{name}' (kulcs: '{key}')")
    return surf



countries = [
    "Szerbia", "Bosnia", "Albánia", "Koszovó", "Észak-Macedónia",
    "Görögország", "Törökország", "Bulgária", "Románia", "Szlovénia",
    "Horvátország", "Montenegró"
]

weapon_data = {
    "Szerbia": {
        "item": "Teniszlabda",
        "person": "Arkan"
    },
    "Albánia": {
        "item": "Albán sas",
        "person": "Skander bég"
    },
    "Bosnia": {
        "item": "Akna",
        "person": "Alija Izetbegovic"
    },
    "Koszovó": {
        "item": "Albánia",
        "person": "Bill Clinton"
    },
    "Észak-Macedónia": {
        "item": "Kézilabda",
        "person": "Nagy Sándor"
    },
    "Görögország": {
        "item": "Diszkosz",
        "person": "Zeus"
    },
    "Törökország": {
        "item": "Kebab",
        "person": "Atatürk"
    },
    "Románia": {
        "item": "Roma",
        "person": "Vlad Tepes"
    },
    "Szlovénia": {
        "item": "Kerékpár",
        "person": "Primoz Roglic"
    },
    "Bulgária": {
        "item": "Focilabda",
        "person": "Vaszil Levszki"
    },
    "Horvátország": {
        "item": "Cevapcici",
        "person": "Luka Modric"
    },
    "Montenegró": {
        "item": "Vizilabda",
        "person": "Ivan Crnojevic"
    }
}


weaknesses = {
    "Szerbia": "NATO",
    "Albánia": "Ortodox kereszt",
    "Bosnia": "Akna",
    "Koszovó": "Slobodan Milosevic",
    "Észak-Macedónia": "Görögország",
    "Görögország": "Adó",
    "Törökország": "Keresztény kereszt",
    "Románia": "Ceausescu",
    "Szlovénia": "Adó",
    "Horvátország": "Slobodan Milosevic",
    "Montenegró": "Altató",
    "Bulgária": "Roma"
}


"""
Az intro
"""

def show_intro():
    width, height = Global.WIDTH, Global.HEIGHT
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Balkan Kombat")
    clock = pygame.time.Clock()

    balls = [CountryBall(name, i) for i, name in enumerate(countries)]

    font = pygame.font.SysFont("Arial", 64)
    title_surface = font.render("Balkan Kombat", True, Global.WHITE)
    title_alpha = 0
    title_surface.set_alpha(title_alpha)

    running = True
    all_arrived = False

    while running:
        screen.fill(Global.BLACK)
        all_arrived = True

        for ball in balls:
            ball.update()
            ball.draw(screen)
            if (ball.direction == 1 and ball.x < ball.target_x) or (ball.direction == -1 and ball.x > ball.target_x):
                all_arrived = False

        if all_arrived:
            if title_alpha < 255:
                title_alpha += 4
                title_surface.set_alpha(title_alpha)
            screen.blit(title_surface, (width // 2 - title_surface.get_width() // 2, 30))
            if title_alpha >= 255:
                pygame.time.wait(1500)
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


def show_menu():
    width, height = Global.WIDTH, Global.HEIGHT
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Balkan Kombat - Menu")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 36)
    title_font = pygame.font.SysFont("Arial", 64)
    single_rect = pygame.Rect(width // 2 - 150, 200, 300, 70)
    multi_rect = pygame.Rect(width // 2 - 150, 300, 300, 70)

    # belépéskor töröljük az esetleges régi eseményeket + debounce idő
    pygame.event.clear()
    enter_time = pygame.time.get_ticks()
    click_enabled_after_ms = 300

    running = True
    mode = None
    while running:
        screen.fill(Global.BLACK)

        pygame.draw.rect(screen, (100, 100, 255), single_rect)
        pygame.draw.rect(screen, (100, 255, 100), multi_rect)

        # FEHÉR felirat, hogy látszódjon a fekete háttéren
        title_surface = title_font.render("Balkan Kombat", True, Global.WHITE)
        screen.blit(title_surface, (width // 2 - title_surface.get_width() // 2, 80))
        single_text = font.render("Single Player Mode", True, Global.BLACK)
        multi_text = font.render("Multiplayer Mode", True, Global.BLACK)
        screen.blit(single_text, (single_rect.x + 20, single_rect.y + 15))
        screen.blit(multi_text, (multi_rect.x + 20, multi_rect.y + 15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # csak akkor fogadjuk el, ha letelt a debounce
                if pygame.time.get_ticks() - enter_time >= click_enabled_after_ms:
                    if single_rect.collidepoint(event.pos):
                        mode = "single"; running = False
                    elif multi_rect.collidepoint(event.pos):
                        mode = "multi"; running = False

        pygame.display.update()
        clock.tick(60)

    return mode

    

def select_countries(mode="multi"):
    width, height = Global.WIDTH, Global.HEIGHT
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pick a country")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 36)
    title_font = pygame.font.SysFont("Arial", 48)

    country_images = []
    cols = 4
    spacing_x = 250
    spacing_y = 140

    for i, name in enumerate(countries):
        img = load_image_smart(name, size=(100, 100))   # <--- ITT!
        x = 100 + (i % cols) * spacing_x
        y = 180 + (i // cols) * spacing_y
        rect = pygame.Rect(x, y, 100, 100)
        country_images.append({"name": name, "img": img, "rect": rect})

    selected = []
    current_player = 1

    running = True
    while running:
        screen.fill(Global.BLACK)

        title = title_font.render("Picking Countries", True, Global.WHITE)
        screen.blit(title, (width // 2 - title.get_width() // 2, 40))

        if mode == "single":
            instruction_text = "Player 1 válasszon! (A gép kap egy másikat.)"
        else:
            instruction_text = f"Player {current_player} válasszon!"
        instruction = font.render(instruction_text, True, Global.WHITE)
        screen.blit(instruction, (width // 2 - instruction.get_width() // 2, 100))

        for entry in country_images:
            screen.blit(entry["img"], entry["rect"])
            if entry["name"] in selected:
                idx = selected.index(entry["name"])
                color = (255, 0, 0) if idx == 0 else (0, 255, 0)
                pygame.draw.rect(screen, color, entry["rect"], 4)

            name_text = font.render(entry["name"], True, Global.WHITE)
            name_x = entry["rect"].x + (100 - name_text.get_width()) // 2
            screen.blit(name_text, (name_x, entry["rect"].bottom + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for entry in country_images:
                    if entry["rect"].collidepoint(event.pos):
                        if entry["name"] not in selected:
                            selected.append(entry["name"])
                            if mode == "single":
                                # gép választ egy másikat
                                remaining = [c for c in countries if c not in selected]
                                ai_pick = random.choice(remaining)
                                selected.append(ai_pick)
                                print(f"Játékos 1: {selected[0]}")
                                print(f"CPU: {selected[1]}")
                                running = False
                            else:
                                if current_player == 1:
                                    current_player = 2
                                else:
                                    print(f"Játékos 1: {selected[0]}")
                                    print(f"Játékos 2: {selected[1]}")
                                    running = False
                            break

        pygame.display.update()
        clock.tick(60)

    return selected





def start_game(mode, player1_country, player2_country):
    width, height = Global.WIDTH, Global.HEIGHT
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Balkan Kombat - Fight!")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 36)
    title_font = pygame.font.SysFont("Arial", 48)

    img1 = load_image_smart(player1_country, size=(100, 100))
    img2 = load_image_smart(player2_country, size=(100, 100))

    ground_y = height - 150
    p1_x, p1_y = 150, ground_y
    p2_x, p2_y = width - 250, ground_y

    speed = 5
    p1_vel_y = 0; p2_vel_y = 0
    gravity = 1
    jump_strength = 15
    p1_on_ground = True; p2_on_ground = True

    hp1 = 5; hp2 = 5
    rw1 = 0; rw2 = 0
    rounds = 3; current_round = 1
    winner_text = ""; template = ""

    p1_weapons = [weapon_data[player1_country]["item"], weapon_data[player1_country]["person"], weaknesses[player2_country]]
    p2_weapons = [weapon_data[player2_country]["item"], weapon_data[player2_country]["person"], weaknesses[player1_country]]

    projectiles = []
    end_timer = 0

    # --- AI paraméterek (csak single módban használt) ---
    ai_attack_cd = 0
    ai_jump_cd = 0
    ai_pref_dist = 180
    ai_rand_jump_chance = 0.01 

    running = True
    while running:
        screen.fill(Global.BLACK)

        title = title_font.render(f"Round {current_round} / {rounds}", True, Global.WHITE)
        screen.blit(title, (width // 2 - title.get_width() // 2, 30))
        screen.blit(img1, (p1_x, p1_y))
        screen.blit(img2, (p2_x, p2_y))

        hp1_text = font.render(f"{player1_country}: {hp1} HP", True, Global.WHITE)
        hp2_text = font.render(f"{player2_country}: {hp2} HP", True, Global.WHITE)
        screen.blit(hp1_text, (150, height // 2 + 70))
        screen.blit(hp2_text, (width - 250, height // 2 + 70))

        if template:
            round_win_surface = font.render(template, True, (255, 255, 255))
            screen.blit(round_win_surface, (width // 2 - round_win_surface.get_width() // 2, height - 160))

        # --- Játékos 1 irányítás ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            p1_x -= speed
        if keys[pygame.K_d]:
            p1_x += speed
        if keys[pygame.K_w] and p1_on_ground:
            p1_vel_y = -jump_strength; p1_on_ground = False

        # --- Játékos 2: MULTI esetben a nyilak; SINGLE esetben AI ---
        if mode == "multi":
            if keys[pygame.K_LEFT]:
                p2_x -= speed
            if keys[pygame.K_RIGHT]:
                p2_x += speed
            if keys[pygame.K_UP] and p2_on_ground:
                p2_vel_y = -jump_strength; p2_on_ground = False
        else:
            # --- AI mozgás ---
            dist = p2_x - p1_x
            if abs(dist) > ai_pref_dist + 20:
                # túl messze van -> közeledjen
                p2_x -= speed if dist > 0 else -speed
            elif abs(dist) < ai_pref_dist - 20:
                # túl közel -> távolodjon
                p2_x += speed if dist > 0 else -speed

            # néha ugorjon
            if p2_on_ground and ai_jump_cd <= 0 and random.random() < ai_rand_jump_chance:
                p2_vel_y = -jump_strength; p2_on_ground = False
                ai_jump_cd = 90  # ~1.5s 60 FPS-nél

            # lőtávon belül támadjon cooldownnal
            if ai_attack_cd <= 0 and abs(dist) <= 400:
                weapon = choice(p2_weapons)
                damage = random.randint(2, 4) if weapon == weaknesses[player1_country] else random.randint(1, 2)
                img = load_image_smart(weapon, size=(50, 50))
                projectiles.append([img, p2_x, p2_y, -1, (p1_x, p1_y, 'p1', damage)])
                ai_attack_cd = 45  # kb 0.75s

            # cooldownok csökkentése
            if ai_attack_cd > 0: ai_attack_cd -= 1
            if ai_jump_cd > 0: ai_jump_cd -= 1

        # --- Pálya szél korlát ---
        p1_x = max(0, min(p1_x, width - 100))
        p2_x = max(0, min(p2_x, width - 100))

        # --- Gravitáció és ugrás ---
        p1_y += p1_vel_y
        if not p1_on_ground:
            p1_vel_y += gravity
        if p1_y >= ground_y:
            p1_y = ground_y; p1_vel_y = 0; p1_on_ground = True

        p2_y += p2_vel_y
        if not p2_on_ground:
            p2_vel_y += gravity
        if p2_y >= ground_y:
            p2_y = ground_y; p2_vel_y = 0; p2_on_ground = True

        # --- Események (lövések gombbal; AI már fent kezeli) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN and not winner_text:
                # P2 lövés csak MULTI alatt gombbal
                if mode == "multi" and event.key == pygame.K_SPACE:
                    weapon = choice(p2_weapons)
                    damage = random.randint(2, 4) if weapon == weaknesses[player1_country] else random.randint(1, 2)
                    img = load_image_smart(weapon, size=(50, 50))
                    projectiles.append([img, p2_x, p2_y, -1, (p1_x, p1_y, 'p1', damage)])

                # P1 lövés
                if event.key == pygame.K_s:
                    weapon = choice(p1_weapons)
                    damage = random.randint(2, 4) if weapon == weaknesses[player2_country] else random.randint(1, 2)
                    img = load_image_smart(weapon, size=(50, 50))
                    projectiles.append([img, p1_x + 50, p1_y, 1, (p2_x, p2_y, 'p2', damage)])

        # --- Lövedékek frissítése ---
        updated_projectiles = []
        for proj in projectiles:
            img, x, y, direction, (target_x, target_y, target_player, damage) = proj
            x += 10 * direction  # sebesség
            if target_player == 'p1' and abs(x - p1_x) < 30 and abs(y - p1_y) < 30:
                hp1 -= damage; continue
            elif target_player == 'p2' and abs(x - p2_x) < 30 and abs(y - p2_y) < 30:
                hp2 -= damage; continue

            if 0 <= x <= width:
                screen.blit(img, (x, y))
                updated_projectiles.append([img, x, y, direction, (target_x, target_y, target_player, damage)])

        projectiles = updated_projectiles

        # --- Kör/győzelem logika ---
        if (hp1 <= 0 or hp2 <= 0) and not winner_text:
            if hp1 <= 0 < hp2:
                    rw2 += 1; template = f"{player2_country} megnyerte a(z) {current_round}. kört!"
            elif hp2 <= 0 < hp1:
                    rw1 += 1; template = f"{player1_country} megnyerte a(z) {current_round}. kört!"
            else:
                    rw1 += 0.5; rw2 += 0.5; template = f"Döntetlen a(z) {current_round}. körben!"
            
            current_round += 1

            if current_round > rounds:
                pygame.time.wait(1500)
                if rw1 > rw2:
                    winner_text = f"{player1_country} nyert! ({rw1}:{rw2})"
                elif rw2 > rw1:
                    winner_text = f"{player2_country} nyert! ({rw2}:{rw1})"
                else:
                    winner_text = f"Döntetlen! ({rw1}:{rw2})"

                screen.fill((0, 0, 0))  # előző képernyő törlése (sztornózás)
                font = pygame.font.Font(None, 74)
                text_surface = font.render(winner_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
                screen.blit(text_surface, text_rect)
                pygame.display.flip()

                # --- kis várakozás ---
                pygame.time.wait(2000)

                # --- vissza a menübe ---
                pygame.event.clear()
                return

       
            else:
                pygame.time.wait(1000)
                hp1 = 5; hp2 = 5; template = ""

        pygame.display.update()
        clock.tick(60)




# Futtatás
pygame.init()
pygame.event.clear() 
pygame.mixer.music.load("dubioza.ogg")
pygame.mixer.music.play(-1, start=14.0)
show_intro()
while True:
    mode = show_menu()
    selected_countries = select_countries(mode=mode)
    start_game(mode, selected_countries[0], selected_countries[1])
