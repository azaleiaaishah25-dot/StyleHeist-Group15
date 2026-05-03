import pygame

#Master switch 
pygame.init() 

#1. Setup & Variables
tile_size = 60
WIDTH, HEIGHT = 1200, 800 #Resolution Full HD
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Style Heist - Detective Game")
clock = pygame.time.Clock() #limit the pc fps 
font = pygame.font.SysFont(None, 30)

dialogue_active = False
current_dialogue = []
dialogue_index = 0
dialogue_text_shown = ""
text_speed = 2
text_counter = 0

can_interact = False
current_npc = None

current_quest = None
quest_log = {}

# NPC DATA
dialogue_data = {
    (13, 6): {
        "dialogue": ["Well now, you look like you’ve walked straight out of a different world.", "That outfit.. I don’t think I’ve seen anything like it."],
        "quest": "find_artifact",
        "type": "main"
    },
    (13, 11): {
        "dialogue": ["Nice suit.", "Stay sharp."],
        "quest": None,
        "type": "side"
    }
}


#2. The Maps (Scene to Scene)
# --- 2. THE MAPS (MUSEUM - RE-RE-REDESIGN) ---
# I have cleared a massive 10x10 square around Column 30, Row 15.
museum_map = [
    "111111111111111111111111111111111111111111111111111111111111", # 00
    "100000000000000111111111111111111111111111100000000000000001", 
    "100500000000000100000000000000000000000000100000000000005001",
    "100000333330000000000000000000000000000000000003333300000001",
    "100000333330000000000000000000000000000000000003333300000001", # Ancient Wing
    "100000333330000100000000000000000000000000100003333300000001",
    "111000111110000111111111111111111111111111100001111100011111",
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100111111001111111111110000000011111111111111100111111000001", # Row 09
    "100100001001000000000010000000010000000000000100100001000001", # 10
    "100103301001000000000000000000000000000000000100103301000001",
    "100103301001000000000000000000000000000000000100103301000001",
    "100100001001000000000000000000000000000000000100100001000001",
    "100111111001000000000000000000000000000000000100111111000001",
    "100000000000000000000000000000000000000000000000000000000001", # 15 (SPAWN)
    "100000000000000000000000000000000000000000000000000000000001",
    "100111111001000000000000000000000000000000000100111111000001",
    "100100001001000000000000000000000000000000000100100001000001",
    "100106001001000000000000000000000000000000000100106001000001",
    "100100001001000000000000000000000000000000000100100001000001", # 20
    "100111111001111111111110000000011111111111111100111111000001",
    "100000000000000000000001000000010000000000000000000000000001",
    "100000000000000000000001000000010000000000000000000000000001",
    "111111111111100111111111000000011111111100111111111111111111",
    "100000000000100100000000000000000000000100100000000000000001", # 25
    "100000000000100100000000000000000000000100100000000000000001",
    "100333333300000000000000000000000000000000000333333300000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000100100000000000000000000000100100000000000000001",
    "111100111111100111111111110000111111111100111111100111111111", # 30
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "111111111111111111111111110000111111111111111111111111111111", # 35 (EXIT)
    "111111111111111111111111110000111111111111111111111111111111",
    "111111111111111111111111110000111111111111111111111111111111",
    "111111111111111111111111110440111111111111111111111111111111", # 38 (PORTAL)
    "111111111111111111111111111111111111111111111111111111111111"  # 39
]

#Jazz Age

era_1920s_map = [
    "111111111111111111111111111111", 
    "100000000000000000000000000001",
    "101111111000000000011111111101", 
    "101111111000030000011111111101",
    "101112211000000000011122111101", 
    "100000000000000000000000000001", 
    "100000000000050000000000000001", 
    "100000000000000000000000000001",
    "100003000000444400000000030001", 
    "100000000000444400000000000001",
    "100000000000000000000000000001",
    "100000000000000000050000000001", 
    "100000000000000000000000000001", 
    "101112211000000000011122111101", 
    "101111111000030000011111111101", 
    "101111111000000000011111111101",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "111111111111111111111111111111"  
]


interior_1920s_club = [
    "11111111111111111111", 
    "10000000000000000001",
    "10333330000000000001", 
    "10333330000000000001",
    "10000000000000000001",
    "10000000000500000001", 
    "10000000000000000001",
    "11111100000000011111", 
    "10000000000000000001",
    "10000000000000000001", 
    "10003300033000330001", 
    "10003300000000330001",
    "10000000000000000001",
    "11111111221111111111", 
    "11111111111111111111"
]


interior_1920s_warehouse = [
    "11111111111111111111", 
    "10000000000000000001",
    "10111111000011111101", 
    "10000000000000000001",
    "10111100111100000001", 
    "10111100111100000001",
    "10000000000000111101", 
    "10000000000000111101",
    "10110060011000000001", 
    "10111111110000000001",
    "10000000000005000001", 
    "10000000000000000001",
    "10000000000000000001",
    "11111111221111111111", 
    "11111111111111111111"
]


interior_1920s_bank = [
    "11111111111111111111",
    "10000000000000000001",
    "10111100000000111101", 
    "10000000000000000001",
    "10000011111100000001",
    "10000010000100000001", 
    "10000010060100000001", 
    "10000011111100000001",
    "10000000000000000001",
    "10000000000005000001", 
    "10000000000000000001",
    "10000000000000000001",
    "11111111221111111111", 
    "11111111111111111111"
]

era_1960s_map = [
    "111111111111111111111111111111",
    "100000000000000000000000000001",
    "100033300000000000003333000001",
    "100033300000500000003333000001",
    "100000000000000000000000000001",
    "100000000001111100000000000001",
    "100000000001000100000000000001",
    "100050000021000100000005000001",
    "100000000001000100000000000001",
    "100000000001111100000000000001",
    "100000000000000000000000000001",
    "100000000000444400000000000001",
    "100000000000444400000000000001",
    "100000000000000000000000000001",
    "100033300000000000003333000001",
    "100033300000500000003333000001",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "111111111111111111111111111111"

]

era_1980s_map = [
    "111111111111111111111111111111",
    "100000000000000000000000000001",
    "101111111000000000011111111101",
    "101000001000000000010000001101",
    "101000001020060000010000001101",
    "101000001000000000010000001101",
    "101111111000000000011111111101",
    "100000000000000000000000000001",
    "100000000000444400000000000001",
    "100000000000444400000000000001",
    "100000000000000000000000000001",
    "101111111000000000011111111101",
    "101000001000000000010000001101",
    "101000001000050000010000001101",
    "101000001000000000010000001101",
    "101111111000000000011111111101",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "111111111111111111111111111111"
]

era_1990s_map = [
    "111111111111111111111111111111",
    "100000000000000000000000000001",
    "100000333300000000003333000001",
    "100000333300050000003333000001",
    "100000000000000000000000000001",
    "100011111000000000011111000001",
    "100010001000000000010001000001",
    "100010001000000000010001000001",
    "100011111000000000011111000001",
    "100000000000444400000000000001",
    "100000000000444400000000000001",
    "100000000000000000000000000001",
    "100000002000050000000000000001",
    "100000000000000000000000000001",
    "100033300000000000003333000001",
    "100033300000000000003333000001",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "111111111111111111111111111111"
]

building_data = {
    # 1920s: CLub entrance (left-top building)
     ("1920s", 4, 4): {"name": "Club", "target_map": interior_1920s_club, "spawn": (9, 11)},
    ("1920s", 5, 4): {"name": "Club", "target_map": interior_1920s_club, "spawn": (9, 11)},
    ("1920s", 6, 4): {"name": "Club", "target_map": interior_1920s_club, "spawn": (9, 11)},
    ("1920s", 7, 4): {"name": "Club", "target_map": interior_1920s_club, "spawn": (9, 11)},

    # --- 1920s: Bank entrance (right-top building) ---
    ("1920s", 21, 4): {"name": "Bank", "target_map": interior_1920s_bank, "spawn": (9, 11)},
    ("1920s", 22, 4): {"name": "Bank", "target_map": interior_1920s_bank, "spawn": (9, 11)},
    ("1920s", 23, 4): {"name": "Bank", "target_map": interior_1920s_bank, "spawn": (9, 11)},
    ("1920s", 24, 4): {"name": "Bank", "target_map": interior_1920s_bank, "spawn": (9, 11)},

    # --- 1920s: Warehouse entrance (right-bottom building) ---
    ("1920s", 21, 13): {"name": "Warehouse", "target_map": interior_1920s_warehouse, "spawn": (9, 11)},
    ("1920s", 22, 13): {"name": "Warehouse", "target_map": interior_1920s_warehouse, "spawn": (9, 11)},
    ("1920s", 23, 13): {"name": "Warehouse", "target_map": interior_1920s_warehouse, "spawn": (9, 11)},
    ("1920s", 24, 13): {"name": "Warehouse", "target_map": interior_1920s_warehouse, "spawn": (9, 11)},

    # --- 1960s: Cafe entrance ---
    ("1960s", 10, 7): {"name": "Cafe", "target_map": interior_1920s_club, "spawn": (9, 11)},  # placeholder interior

    # --- 1980s: Office entrance ---
    ("1980s", 10, 4): {"name": "Office", "target_map": interior_1920s_bank, "spawn": (9, 11)},  # placeholder interior

    # --- 1990s: Mall entrance ---
    ("1990s", 8, 12): {"name": "Mall", "target_map": interior_1920s_warehouse, "spawn": (9, 11)},  # placeholder interior

    # =========================================================
    # INTERIOR EXITS
    # These match the "2" tiles inside your interior maps.
    # =========================================================

    # Club / Cafe use the same placeholder interior_1920s_club.
    ("Club", 8, 13): {"name": "1920s", "target_map": era_1920s_map, "spawn": (5, 5)},
    ("Club", 9, 13): {"name": "1920s", "target_map": era_1920s_map, "spawn": (5, 5)},
    ("Cafe", 8, 13): {"name": "1960s", "target_map": era_1960s_map, "spawn": (10, 8)},
    ("Cafe", 9, 13): {"name": "1960s", "target_map": era_1960s_map, "spawn": (10, 8)},

    # Bank / Office use the same placeholder interior_1920s_bank.
    ("Bank", 8, 12): {"name": "1920s", "target_map": era_1920s_map, "spawn": (22, 5)},
    ("Bank", 9, 12): {"name": "1920s", "target_map": era_1920s_map, "spawn": (22, 5)},
    ("Office", 8, 12): {"name": "1980s", "target_map": era_1980s_map, "spawn": (10, 5)},
    ("Office", 9, 12): {"name": "1980s", "target_map": era_1980s_map, "spawn": (10, 5)},

    # Warehouse / Mall use the same placeholder interior_1920s_warehouse.
    ("Warehouse", 8, 13): {"name": "1920s", "target_map": era_1920s_map, "spawn": (22, 12)},
    ("Warehouse", 9, 13): {"name": "1920s", "target_map": era_1920s_map, "spawn": (22, 12)},
    ("Mall", 8, 13): {"name": "1990s", "target_map": era_1990s_map, "spawn": (8, 13)},
    ("Mall", 9, 13): {"name": "1990s", "target_map": era_1990s_map, "spawn": (8, 13)},
}



current_era = "Museum"
game_map = museum_map #Starting at the Museum

#Fog of war 
visited_map = [[False for _ in range(len(museum_map[0]))] for _ in range(len(museum_map))]


#3. Player Variables
player_size = tile_size
player_size = 60
player_x = 1500
player_y = 1600
speed = 6 #pixels per movements in a frame = FPS


#4. Images
duck_img = pygame.image.load("Images/duck_with_knife.jpg").convert_alpha()
duck_img = pygame.transform.scale(duck_img, (player_size, player_size))

tree_img = pygame.image.load("Images/pixel_tree.jpg").convert_alpha()
tree_img = pygame.transform.scale(tree_img, (tile_size, tile_size))

#5. Functions (Logic)

def check_collision(x, y, current_map):
    player_rect = pygame.Rect(x, y, player_size, player_size)
    for row_index, row in enumerate(current_map):
        for col_index, tile in enumerate(row):
            if tile in ["1", "3", "5"]:
                wall_rect = pygame.Rect(col_index * tile_size, row_index * tile_size, tile_size, tile_size)
                if player_rect.colliderect(wall_rect):
                    return True
                
    return False

def transition_to(new_map_array, new_era_name, spawn_tile_x, spawn_tile_y):
    global game_map, current_era, player_x, player_y, visited_map
    
    
    game_map = new_map_array
    current_era = new_era_name
    
    player_x = spawn_tile_x * tile_size
    player_y = spawn_tile_y * tile_size
    
    visited_map = [[False for _ in range(len(game_map[0]))] for _ in range(len(game_map))]
    
    pygame.time.delay(250)

#6. Main Game Loop
running = True
while running: 
    clock.tick(60) #fps, frame per second

    #A. Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e:
                if not dialogue_active and can_interact:
                    if current_npc in dialogue_data:
                        npc_data = dialogue_data[current_npc]

                        current_dialogue = npc_data["dialogue"]
                        current_quest = npc_data.get("quest")

                        dialogue_active = True
                        dialogue_index = 0
                        dialogue_text_shown = ""
                        text_counter = 0

                        # Add quest to log
                        if current_quest:
                            quest_log[current_quest] = "started"

            elif event.key == pygame.K_SPACE:
                if dialogue_active:
                    if dialogue_text_shown != current_dialogue[dialogue_index]:
                        # finish typing instantly
                        dialogue_text_shown = current_dialogue[dialogue_index]
                    else:
                        dialogue_index += 1
                        text_counter = 0
                        dialogue_text_shown = ""

                        if dialogue_index >= len(current_dialogue):
                            dialogue_active = False

    if not dialogue_active:
        hotkeys = pygame.key.get_pressed()

        new_x = player_x
        new_y = player_y

        if hotkeys[pygame.K_w]:
            new_y -= speed
        if hotkeys[pygame.K_s]:
            new_y += speed
        if hotkeys[pygame.K_a]:
            new_x -= speed
        if hotkeys[pygame.K_d]:
            new_x += speed

    #Move X
    if not check_collision(new_x, player_y, game_map):
        player_x = new_x
    #Move Y
    if not check_collision(player_x, new_y, game_map):
        player_y = new_y
    
    camera_x = player_x - (WIDTH // 2)
    camera_y = player_y - (HEIGHT // 2)

    map_pixel_width = len(game_map[0]) * tile_size
    map_pixel_height = len(game_map) * tile_size

    camera_x = max(0, min(camera_x, map_pixel_width - WIDTH))
    camera_y = max(0, min(camera_y, map_pixel_height - HEIGHT))

    player_col = player_x // tile_size
    player_row = player_y // tile_size

    can_interact = False
    current_npc = None

    for row in range(player_row - 1, player_row + 2):
        for col in range(player_col - 1, player_col + 2):
            if 0 <= row < len(game_map) and 0 <= col < len(game_map[0]):
                if game_map[row][col] == "5":
                    can_interact = True
                    current_npc = (col, row)

    #What Player can see
    reveal_radius = 3
    for row in range(player_row - reveal_radius, player_row + reveal_radius + 1):
        for col in range(player_col - reveal_radius, player_col + reveal_radius + 1):
            if 0 <= row < len(game_map) and 0 <= col < len (game_map[0]):
                visited_map[row][col] = True


    #C. Teleportation Logic & Door logic
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            
            if tile in ["4", "2", "7", "8", "9"]: 
                trigger_rect = pygame.Rect(col_index * tile_size, row_index * tile_size, tile_size, tile_size)

               
                if player_rect.colliderect(trigger_rect):

                    if tile == "4": 
                        if current_era == "Museum":
                            transition_to(era_1920s_map, "1920s", 14, 10)

                        elif current_era == "1920s":
                            transition_to(era_1960s_map, "1960s", 14, 10)

                        elif current_era == "1960s":
                            transition_to(era_1980s_map, "1980s", 14, 10)

                        elif current_era == "1980s":
                            transition_to(era_1990s_map, "1990s", 14, 10)

                        else:
                            transition_to(museum_map, "Museum", 30, 15)
                    
                    elif tile == "2": 

                        print("Checking:", current_era, col_index, row_index)

                        key = (current_era, col_index, row_index)

                        if key in building_data:
                            building = building_data[key]

                            transition_to(
                                building["target_map"],
                                building["name"],
                                building["spawn"][0],
                                building["spawn"][1]
                            )
                        
                    visited_map = [[False for _ in range(len(game_map[0]))] for _ in range(len(game_map))]

                    pygame.time.delay(200)
                    break

                if dialogue_active:
                    if dialogue_index < len(current_dialogue):
                        full_text = current_dialogue[dialogue_index]

                        if text_counter < len(full_text):
                            text_counter += text_speed
                            dialogue_text_shown = full_text[:text_counter]
                                    
    #D. Drawing
    screen.fill((10, 20, 20))

    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            
            world_x = col_index * tile_size
            world_y = row_index * tile_size

            screen_x = world_x - camera_x
            screen_y = world_y - camera_y
            
            if -tile_size < screen_x < WIDTH and -tile_size < screen_y < HEIGHT:
                if tile == "1":
                    pygame.draw.rect(screen, (90, 90, 90), (screen_x, screen_y, tile_size, tile_size))
                elif tile == "2":
                    pygame.draw.rect(screen, (101, 67, 33), (screen_x, screen_y, tile_size, tile_size))
                elif tile == "3":
                    screen.blit(tree_img, (screen_x, screen_y))
                elif tile == "4":
                    pygame.draw.rect(screen, (200, 150, 50), (screen_x, screen_y, tile_size, tile_size)) # Portal
                elif tile == "5":
                    pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y, tile_size, tile_size)) # NPC Placeholder
                elif tile == "6":
                    pygame.draw.rect(screen, (255, 20, 147), (screen_x, screen_y, tile_size, tile_size))
                elif tile == "9":
                    pygame.draw.rect(screen, (101, 67, 33), (screen_x, screen_y, tile_size, tile_size))
                else:
                    pygame.draw.rect(screen, (200, 200, 200), (screen_x, screen_y, tile_size, tile_size))
            
            # Grid lines
            pygame.draw.rect(screen, (0, 0, 0), (screen_x, screen_y, tile_size, tile_size), 1)

    # Draw Player
    screen.blit(duck_img, (player_x - camera_x, player_y - camera_y))

    # ---Mini-Map---
    mini_tile = 5
    map_width = len(game_map[0]) * mini_tile
    start_x = WIDTH - map_width - 20
    start_y = 20

    #1. Mini Map
    pygame.draw.rect(screen, (30, 30, 30), (start_x - 2, start_y -2, map_width + 4, len(game_map) * mini_tile + 4))

    #2. Draw Tiles
    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            if visited_map[row_index][col_index]:
                mini_x = start_x + (col_index * mini_tile)
                mini_y = start_y + (row_index * mini_tile)

                if tile == "1": #wall
                    pygame.draw.rect(screen, (150, 150, 150), (mini_x, mini_y, mini_tile, mini_tile))
                elif tile == "4": #Portal
                    pygame.draw.rect(screen, (200, 150, 50), (mini_x, mini_y, mini_tile, mini_tile))
                else:
                    pygame.draw.rect(screen, (70, 70, 70), (mini_x, mini_y, mini_tile, mini_tile))


    player_mini_x = start_x + (player_x // tile_size) * mini_tile
    player_mini_y = start_y + (player_y // tile_size) * mini_tile
    pygame.draw.circle(screen, (0, 255, 0 ), (player_mini_x + mini_tile//2, player_mini_y + mini_tile//2), 3)

    era_label = font.render(f"TIMELINE: {current_era}", True, (255, 255, 0)) #Yellow Color
    screen.blit(era_label, (20, 20))

    if can_interact and not dialogue_active:
        hint = font.render("Press E", True, (255, 255, 255))
        screen.blit(hint, (player_x - camera_x, player_y - camera_y - 30))

    if dialogue_active:
        box_height = 150
        box_rect = pygame.Rect(50, HEIGHT - box_height - 30, WIDTH - 100, box_height)

        pygame.draw.rect(screen, (0, 0, 0), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 3)

        if dialogue_index < len(current_dialogue):
            rendered_text = font.render(dialogue_text_shown, True, (255, 255, 255))
            screen.blit(rendered_text, (box_rect.x + 20, box_rect.y + 20))

        hint = font.render("SPACE to continue", True, (200, 200, 200))
        screen.blit(hint, (box_rect.x + 20, box_rect.y + 80))    

    pygame.display.update()

pygame.quit()

#4/19/2026 and Earlier dates
#Summary on what I have done in my part for the games:
#Refactored the Architecture, Resolution Upgrade
#Mega Map Installation, Museum and 1920s Jazz Age, Scrolling Camera, Camera Clamping
#Teleportation System, Fog of War Mini-Map, Scene Transitions

