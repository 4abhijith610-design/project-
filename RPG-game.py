import random
import json
import os
import time

SAVE_FILE = "eldoria_save.json"

# -------------------- DATA --------------------

RARITIES = {
    "Common": {"mult": 1.0, "crit": 0, "price": 50, "req_lvl": 1},
    "Uncommon": {"mult": 1.1, "crit": 2, "price": 100, "req_lvl": 3},
    "Rare": {"mult": 1.3, "crit": 5, "price": 200, "req_lvl": 8},
    "Super Rare": {"mult": 1.5, "crit": 8, "price": 350, "req_lvl": 15},
    "Epic": {"mult": 1.8, "crit": 12, "price": 600, "req_lvl": 25},
    "Mythical": {"mult": 2.2, "crit": 18, "price": 1000, "req_lvl": 40},
    "Legendary": {"mult": 2.8, "crit": 25, "price": 1800, "req_lvl": 60},
}

WEAPONS = [
    ("Wooden Sword", "Common", 10), ("Rusty Axe", "Common", 11),
    ("Training Bow", "Common", 9), ("Iron Sword", "Rare", 18),
    ("Steel Axe", "Rare", 20), ("Long Bow", "Rare", 17),
    ("Crystal Blade", "Super Rare", 25), ("Shadow Dagger", "Super Rare", 27),
    ("Lightning Bow", "Super Rare", 24), ("Flame Sword", "Epic", 34),
    ("Ice Spear", "Epic", 32), ("Thunder Hammer", "Epic", 36),
    ("Phoenix Blade", "Mythical", 45), ("Demon Slayer", "Mythical", 48),
    ("Celestial Staff", "Mythical", 44), ("Dragon King's Sword", "Legendary", 60),
    ("Blade of Eternity", "Legendary", 65), ("Bow of the Gods", "Legendary", 62),
    ("Moon Blade", "Uncommon", 14), ("Forest Bow", "Uncommon", 13),
    ("Knight's Mace", "Uncommon", 15), ("Void Katana", "Epic", 38)
]

ARMOR = [
    ("Cloth Armor", "Common", 5, 20, 10, 1),
    ("Leather Armor", "Common", 7, 25, 12, 2),
    ("Iron Armor", "Rare", 12, 45, 15, 3),
    ("Steel Armor", "Rare", 15, 55, 20, 4),
    ("Crystal Armor", "Super Rare", 20, 70, 30, 5),
    ("Shadow Armor", "Super Rare", 22, 65, 35, 7),
    ("Flame Armor", "Epic", 28, 90, 40, 8),
    ("Ice Armor", "Epic", 30, 100, 45, 9),
    ("Phoenix Armor", "Mythical", 38, 130, 60, 12),
    ("Demon Armor", "Mythical", 42, 140, 65, 14),
    ("Celestial Armor", "Legendary", 50, 170, 80, 18),
    ("Dragon Armor", "Legendary", 60, 200, 100, 20),
]

POTIONS = {
    "Small Health Potion": {"type": "hp", "value": 50, "price": 30},
    "Medium Health Potion": {"type": "hp", "value": 100, "price": 60},
    "Large Health Potion": {"type": "hp", "value": 250, "price": 120},
    "Giant Health Potion": {"type": "hp", "value": 500, "price": 250},
    "Ultimate Health Potion": {"type": "hp_full", "value": 0, "price": 500},
    "Small Mana Potion": {"type": "mana", "value": 30, "price": 30},
    "Medium Mana Potion": {"type": "mana", "value": 75, "price": 60},
    "Large Mana Potion": {"type": "mana", "value": 150, "price": 120},
    "Giant Mana Potion": {"type": "mana", "value": 300, "price": 250},
    "Ultimate Mana Potion": {"type": "mana_full", "value": 0, "price": 500},
    "Health Mana Mix": {"type": "mixed", "value": 100, "price": 150},
    "Greater Mix Potion": {"type": "mixed", "value": 250, "price": 300},
    "Attack Buff Potion": {"type": "attack_buff", "value": 15, "price": 150},
    "Defense Buff Potion": {"type": "defense_buff", "value": 15, "price": 150},
    "Critical Buff Potion": {"type": "crit_buff", "value": 10, "price": 200},
}

ENEMY_NAMES = [
    "Goblin", "Wolf", "Slime", "Zombie", "Skeleton",
    "Orc", "Bandit", "Troll", "Dark Archer", "Giant Spider",
    "Vampire", "Werewolf", "Necromancer", "Ice Golem", "Fire Demon",
    "Sand Beast", "Desert Raider", "Ancient Mummy", "Ruins Guardian",
    "Dark Knight", "Castle Mage", "Lava Beast", "Volcanic Demon",
    "Frost Giant", "Sky Serpent", "Temple Guardian", "Demon Warrior",
    "Abyssal Beast"
]

BOSSES = {
    10: "Goblin King",
    20: "Forest Guardian",
    30: "Ancient Golem",
    40: "Vampire Lord",
    50: "Dragon Rider",
    60: "Demon General",
    70: "Ice Titan",
    80: "Shadow Emperor",
    90: "Celestial Dragon",
    100: "Ancient Demon King"
}

REGIONS = [
    "Village", "Forest", "Cave", "Desert", "Ruins",
    "Castle", "Volcano", "Frozen Mountain", "Sky Temple", "Demon Realm"
]

SKILLS = {
    "Warrior": [
        ("Slash", 10, 1.5),
        ("Shield Bash", 15, 1.7),
        ("Rage", 20, 2.0),
        ("Earthquake", 30, 2.8)
    ],
    "Mage": [
        ("Fireball", 15, 1.8),
        ("Ice Blast", 20, 2.1),
        ("Thunder Strike", 30, 2.7),
        ("Meteor", 45, 3.5)
    ],
    "Archer": [
        ("Multi Shot", 12, 1.6),
        ("Poison Arrow", 18, 1.9),
        ("Explosive Arrow", 28, 2.6),
        ("Sniper Shot", 40, 3.5)
    ],
    "Assassin": [
        ("Backstab", 12, 1.8),
        ("Smoke Bomb", 18, 2.0),
        ("Shadow Strike", 28, 2.8),
        ("Instant Kill", 45, 4.0)
    ]
}

CLASS_STATS = {
    "Warrior": {"hp": 150, "mana": 50, "attack": 30, "defense": 25, "crit": 8},
    "Mage": {"hp": 100, "mana": 150, "attack": 35, "defense": 15, "crit": 12},
    "Archer": {"hp": 110, "mana": 100, "attack": 30, "defense": 20, "crit": 18},
    "Assassin": {"hp": 90, "mana": 100, "attack": 40, "defense": 10, "crit": 25}
}


# -------------------- HELPER FUNCTIONS --------------------

def weapon_data(name):
    for w in WEAPONS:
        if w[0] == name:
            return w
    return WEAPONS[0]


def armor_data(name):
    for a in ARMOR:
        if a[0] == name:
            return a
    return None


def weapon_price(weapon):
    name, rarity, damage = weapon
    return int(RARITIES[rarity]["price"] * (1 + damage / 20))


def armor_price(armor):
    name, rarity, defense, hp, mana, crit_resist = armor
    return int(RARITIES[rarity]["price"] * (1 + defense / 10))


def rarity_required_level(rarity):
    return RARITIES[rarity]["req_lvl"]


def get_player_stats(player):
    """Calculates player stats dynamically based on base stats + equipment."""
    base_hp = player["base_hp"] + (player["level"] - 1) * 15
    base_mana = player["base_mana"] + (player["level"] - 1) * 10
    base_attack = player["base_attack"] + (player["level"] - 1) * 4
    base_defense = player["base_defense"] + (player["level"] - 1) * 3
    base_crit = player["base_crit"]

    max_hp = base_hp
    max_mana = base_mana
    defense = base_defense
    attack = base_attack

    if player["weapon"]:
        w = weapon_data(player["weapon"])
        attack += int(w[2] * RARITIES[w[1]]["mult"])
        crit_chance = base_crit + RARITIES[w[1]]["crit"]
    else:
        crit_chance = base_crit

    if player["armor"]:
        a = armor_data(player["armor"])
        if a:
            defense += a[2]
            max_hp += a[3]
            max_mana += a[4]

    return {
        "max_hp": max_hp,
        "max_mana": max_mana,
        "attack": attack,
        "defense": defense,
        "crit": crit_chance
    }


# -------------------- PLAYER CREATION --------------------

def create_player():
    print("\n=== CHARACTER CREATION ===")
    name = input("Enter Player Name: ").strip() or "Hero"

    while True:
        print("\nChoose Your Class")
        print("1. Warrior")
        print("2. Mage")
        print("3. Archer")
        print("4. Assassin")

        choice = input("Enter choice: ")
        classes = {"1": "Warrior", "2": "Mage", "3": "Archer", "4": "Assassin"}

        if choice in classes:
            player_class = classes[choice]
            break
        print("Invalid choice.")

    s = CLASS_STATS[player_class]

    player = {
        "name": name,
        "class": player_class,
        "level": 1,
        "exp": 0,
        "next_exp": 100,
        "base_hp": s["hp"],
        "base_mana": s["mana"],
        "base_attack": s["attack"],
        "base_defense": s["defense"],
        "base_crit": s["crit"],
        "hp": s["hp"],
        "mana": s["mana"],
        "crit_damage": 2.0,
        "gold": 300,
        "weapon": WEAPONS[0][0],
        "armor": ARMOR[0][0],
        "potions": {"Small Health Potion": 3, "Small Mana Potion": 2},
        "inventory": [],
        "bosses_defeated": [],
        "enemies_defeated": 0,
        "weapons_collected": 1,
        "rare_items": 0,
        "start_time": time.time(),
        "total_play_time": 0
    }

    stats = get_player_stats(player)
    player["hp"] = stats["max_hp"]
    player["mana"] = stats["max_mana"]

    print("\nCharacter created successfully!")
    return player


def show_stats(player):
    stats = get_player_stats(player)
    print("\n========== PLAYER STATS ==========")
    print("Name:", player["name"])
    print("Class:", player["class"])
    print("Level:", player["level"])
    print("EXP:", player["exp"], "/", player["next_exp"])
    print("HP:", player["hp"], "/", stats["max_hp"])
    print("Mana:", player["mana"], "/", stats["max_mana"])
    print("Attack:", stats["attack"])
    print("Defense:", stats["defense"])
    print("Critical Chance:", stats["crit"], "%")
    print("Gold:", player["gold"])
    print("Weapon:", player["weapon"] or "None")
    print("Armor:", player["armor"] or "None")
    print("Enemies Defeated:", player["enemies_defeated"])
    print("Bosses Defeated:", len(player["bosses_defeated"]))


# -------------------- LEVELING --------------------

def gain_exp(player, amount):
    player["exp"] += amount

    while player["exp"] >= player["next_exp"] and player["level"] < 100:
        player["exp"] -= player["next_exp"]
        player["level"] += 1
        player["next_exp"] = 100 + player["level"] * 25

        stats = get_player_stats(player)
        player["hp"] = stats["max_hp"]
        player["mana"] = stats["max_mana"]

        print("\n*** LEVEL UP! ***")
        print("You reached Level", player["level"])
        print("HP, Mana, Attack and Defense increased!")

        if player["level"] % 5 == 0 and player["level"] < 100:
            print("New skill/passive unlocked at level", player["level"])


# -------------------- ENEMIES & BOSSES --------------------

def create_enemy(player, boss=False):
    level = player["level"]

    if boss:
        name = BOSSES[level]
        hp = 300 + level * 35
        attack = 30 + level * 4
        defense = 15 + level * 2
        return {
            "name": name,
            "level": level,
            "hp": hp,
            "max_hp": hp,
            "attack": attack,
            "defense": defense,
            "boss": True,
            "turn": 0
        }

    index = min((level - 1) // 4, len(ENEMY_NAMES) - 1)
    name = random.choice(ENEMY_NAMES[max(0, index - 2):min(len(ENEMY_NAMES), index + 3)])

    hp = random.randint(50, 80) + level * 12
    attack = random.randint(10, 18) + level * 2
    defense = random.randint(5, 10) + level

    return {
        "name": name,
        "level": level,
        "hp": hp,
        "max_hp": hp,
        "attack": attack,
        "defense": defense,
        "boss": False,
        "turn": 0
    }


# -------------------- COMBAT --------------------

def use_potion(player, buff_tracker):
    stats = get_player_stats(player)
    available = [p for p, count in player["potions"].items() if count > 0]

    if not available:
        print("You have no potions.")
        return False

    print("\nPotions:")
    for i, potion in enumerate(available, 1):
        print(f"{i}. {potion} x{player['potions'][potion]}")

    try:
        choice = int(input("Choose potion (0 to cancel): "))
        if choice == 0:
            return False
        potion = available[choice - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return False

    data = POTIONS[potion]
    player["potions"][potion] -= 1

    if data["type"] == "hp":
        player["hp"] = min(stats["max_hp"], player["hp"] + data["value"])
        print("HP restored by", data["value"])
    elif data["type"] == "mana":
        player["mana"] = min(stats["max_mana"], player["mana"] + data["value"])
        print("Mana restored by", data["value"])
    elif data["type"] == "hp_full":
        player["hp"] = stats["max_hp"]
        print("HP fully restored.")
    elif data["type"] == "mana_full":
        player["mana"] = stats["max_mana"]
        print("Mana fully restored.")
    elif data["type"] == "mixed":
        player["hp"] = min(stats["max_hp"], player["hp"] + data["value"])
        player["mana"] = min(stats["max_mana"], player["mana"] + data["value"])
        print("HP and Mana restored.")
    elif data["type"] == "attack_buff":
        buff_tracker["attack"] = (data["value"], 3)
        print("Attack increased for 3 turns!")
    elif data["type"] == "defense_buff":
        buff_tracker["defense"] = (data["value"], 3)
        print("Defense increased for 3 turns!")
    elif data["type"] == "crit_buff":
        buff_tracker["crit"] = (data["value"], 3)
        print("Critical chance increased for 3 turns!")

    return True


def basic_attack(player, enemy, buff_tracker):
    stats = get_player_stats(player)
    atk = stats["attack"] + buff_tracker["attack"][0]
    crit_chance = stats["crit"] + buff_tracker["crit"][0]

    damage = max(1, atk - enemy["defense"])

    if random.randint(1, 100) <= crit_chance:
        damage = int(damage * player["crit_damage"])
        print("\nCRITICAL HIT!")

    enemy["hp"] -= damage
    print("You dealt", damage, "damage.")


def use_skill(player, enemy):
    skills = SKILLS[player["class"]]
    stats = get_player_stats(player)

    print("\nSkills:")
    for i, skill in enumerate(skills, 1):
        print(f"{i}. {skill[0]} - Mana: {skill[1]}")

    try:
        choice = int(input("Choose skill (0 to cancel): "))
        if choice == 0:
            return False
        name, mana_cost, multiplier = skills[choice - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return False

    if player["level"] < (choice * 3):
        print("You have not unlocked this skill yet.")
        return False

    if player["mana"] < mana_cost:
        print("Not enough mana.")
        return False

    player["mana"] -= mana_cost
    damage = max(1, int(stats["attack"] * multiplier) - enemy["defense"])

    if name == "Instant Kill" and random.randint(1, 100) <= 5:
        enemy["hp"] = 0
        print("\nINSTANT KILL!")
        return True

    enemy["hp"] -= damage
    print(f"{name} dealt {damage} damage.")
    return True


def enemy_turn(player, enemy, is_defending, buff_tracker):
    enemy["turn"] += 1
    stats = get_player_stats(player)
    player_def = stats["defense"] + buff_tracker["defense"][0]

    if enemy["boss"]:
        roll = random.randint(1, 100)
        if roll <= 15 and enemy["hp"] < enemy["max_hp"]:
            heal_amount = int(enemy["max_hp"] * 0.15)
            enemy["hp"] = min(enemy["max_hp"], enemy["hp"] + heal_amount)
            print(f"\n{enemy['name']} used HEAL and restored {heal_amount} HP!")
            return

    damage = max(1, enemy["attack"] - player_def)

    if enemy["boss"] and enemy["turn"] % 3 == 0:
        damage = int(damage * 1.8)
        print("\nBOSS SPECIAL ATTACK!")
    elif random.randint(1, 100) <= 10:
        damage = int(damage * 1.5)
        print(f"\n{enemy['name']} landed a CRITICAL HIT!")

    if is_defending:
        damage = max(1, damage // 2)
        print("Your defense reduced the incoming damage!")

    player["hp"] -= damage
    print(f"{enemy['name']} dealt {damage} damage to you.")


def update_buffs(buff_tracker):
    for buff_type in list(buff_tracker.keys()):
        val, turns = buff_tracker[buff_type]
        if turns > 0:
            turns -= 1
            if turns == 0:
                buff_tracker[buff_type] = (0, 0)
                print(f"Your {buff_type} buff expired.")
            else:
                buff_tracker[buff_type] = (val, turns)


def battle(player, enemy):
    print("\n================================")
    print("BATTLE:", enemy["name"])
    print("================================")

    buff_tracker = {"attack": (0, 0), "defense": (0, 0), "crit": (0, 0)}

    while player["hp"] > 0 and enemy["hp"] > 0:
        stats = get_player_stats(player)
        print(f"\nYour HP: {player['hp']}/{stats['max_hp']} | Mana: {player['mana']}/{stats['max_mana']}")
        print(f"Enemy HP: {enemy['hp']}/{enemy['max_hp']}")
        print("\n1. Attack  2. Skills  3. Heal  4. Potion")
        print("5. Defend  6. Inventory  7. Stats  8. Run")

        choice = input("Choose action: ")
        player_action = False
        is_defending = False

        if choice == "1":
            basic_attack(player, enemy, buff_tracker)
            player_action = True
        elif choice == "2":
            player_action = use_skill(player, enemy)
        elif choice == "3":
            heal = min(40 + player["level"] * 3, stats["max_hp"] - player["hp"])
            player["hp"] += heal
            print("You healed", heal, "HP.")
            player_action = True
        elif choice == "4":
            player_action = use_potion(player, buff_tracker)
        elif choice == "5":
            is_defending = True
            print("You prepare to defend. Incoming damage reduced by 50%.")
            player_action = True
        elif choice == "6":
            show_inventory(player)
            continue
        elif choice == "7":
            show_stats(player)
            continue
        elif choice == "8":
            if enemy["boss"]:
                print("You cannot run from a boss!")
                continue
            if random.randint(1, 100) <= 50:
                print("You escaped!")
                return "escaped"
            print("You failed to escape!")
            player_action = True
        else:
            print("Invalid choice.")
            continue

        if enemy["hp"] <= 0:
            break

        if player_action:
            enemy_turn(player, enemy, is_defending, buff_tracker)
            update_buffs(buff_tracker)

    if player["hp"] <= 0:
        print("\nGAME OVER! You were defeated.")
        return "dead"

    print("\n*** VICTORY! ***")
    print("You defeated", enemy["name"])
    player["enemies_defeated"] += 1

    exp = 40 + player["level"] * 10
    gold = random.randint(30, 80) + player["level"] * 5

    if enemy["boss"]:
        exp *= 3
        gold *= 3

    player["gold"] += gold
    gain_exp(player, exp)

    print("EXP gained:", exp)
    print("Gold gained:", gold)

    loot_drop(player, enemy)
    return "win"


# -------------------- LOOT --------------------

def loot_drop(player, enemy):
    print("\n--- LOOT ---")
    roll = random.random() * 100

    if roll < 50:
        potion = random.choice(list(POTIONS.keys()))
        player["potions"][potion] = player["potions"].get(potion, 0) + 1
        print("Potion dropped:", potion)
    elif roll < 75:
        weapon = random.choice(WEAPONS)
        if player["level"] >= rarity_required_level(weapon[1]):
            player["inventory"].append({"kind": "weapon", "name": weapon[0]})
            player["weapons_collected"] += 1
            if weapon[1] != "Common":
                player["rare_items"] += 1
            print(f"Weapon dropped: {weapon[0]} ({weapon[1]})")
    elif roll < 95:
        armor = random.choice(ARMOR)
        if player["level"] >= rarity_required_level(armor[1]):
            player["inventory"].append({"kind": "armor", "name": armor[0]})
            if armor[1] != "Common":
                player["rare_items"] += 1
            print(f"Armor dropped: {armor[0]} ({armor[1]})")
    else:
        player["inventory"].append({"kind": "material", "name": "Ancient Crystal"})
        print("Material dropped: Ancient Crystal")

    if enemy["boss"]:
        rare_weapon = random.choice([w for w in WEAPONS if w[1] in ["Epic", "Mythical", "Legendary"]])
        player["inventory"].append({"kind": "weapon", "name": rare_weapon[0]})
        print(f"BOSS REWARD: {rare_weapon[0]} ({rare_weapon[1]})")


# -------------------- INVENTORY & EQUIP --------------------

def show_inventory(player):
    print("\n========== INVENTORY ==========")
    weapons = [i["name"] for i in player["inventory"] if i["kind"] == "weapon"]
    armors = [i["name"] for i in player["inventory"] if i["kind"] == "armor"]
    materials = [i["name"] for i in player["inventory"] if i["kind"] == "material"]

    print("\nWeapons:", ", ".join(weapons) if weapons else "None")
    print("Armor:", ", ".join(armors) if armors else "None")
    print("Materials:", ", ".join(materials) if materials else "None")

    print("\nPotions:")
    for name, count in player["potions"].items():
        if count > 0:
            print(f"- {name} x{count}")

    print("\nEquipped Weapon:", player["weapon"] or "None")
    print("Equipped Armor:", player["armor"] or "None")


def equip_menu(player):
    while True:
        print("\n--- EQUIP / UNEQUIP MENU ---")
        print("1. Equip Weapon/Armor")
        print("2. Unequip Weapon")
        print("3. Unequip Armor")
        print("4. Back")

        choice = input("Choose: ")
        if choice == "1":
            equip_item(player)
        elif choice == "2":
            if player["weapon"]:
                player["inventory"].append({"kind": "weapon", "name": player["weapon"]})
                print(f"Unequipped {player['weapon']}.")
                player["weapon"] = None
            else:
                print("No weapon equipped.")
        elif choice == "3":
            if player["armor"]:
                player["inventory"].append({"kind": "armor", "name": player["armor"]})
                print(f"Unequipped {player['armor']}.")
                player["armor"] = None
            else:
                print("No armor equipped.")
        elif choice == "4":
            break


def equip_item(player):
    equippable = [i for i in player["inventory"] if i["kind"] in ["weapon", "armor"]]
    if not equippable:
        print("No equippable items in inventory.")
        return

    print("\nAvailable Equipment:")
    for i, item in enumerate(equippable, 1):
        print(f"{i}. [{item['kind'].upper()}] {item['name']}")

    try:
        choice = int(input("Choose item to equip (0 cancel): "))
        if choice == 0:
            return
        selected = equippable[choice - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    if selected["kind"] == "weapon":
        data = weapon_data(selected["name"])
        if player["level"] < rarity_required_level(data[1]):
            print(f"Level too low! Requires Level {rarity_required_level(data[1])}.")
            return
        if player["weapon"]:
            player["inventory"].append({"kind": "weapon", "name": player["weapon"]})
        player["weapon"] = selected["name"]
        player["inventory"].remove(selected)
        print(f"Equipped {selected['name']}.")

    elif selected["kind"] == "armor":
        data = armor_data(selected["name"])
        if player["level"] < rarity_required_level(data[1]):
            print(f"Level too low! Requires Level {rarity_required_level(data[1])}.")
            return
        if player["armor"]:
            player["inventory"].append({"kind": "armor", "name": player["armor"]})
        player["armor"] = selected["name"]
        player["inventory"].remove(selected)
        print(f"Equipped {selected['name']}.")


# -------------------- SHOP --------------------

def shop(player):
    while True:
        print("\n========== VILLAGE SHOP ==========")
        print("Gold:", player["gold"])
        print("1. Buy Weapon  2. Buy Armor  3. Buy Potion  4. Sell Item  5. Exit")

        choice = input("Choose: ")
        if choice == "1":
            for i, w in enumerate(WEAPONS, 1):
                price = weapon_price(w)
                print(f"{i}. {w[0]} ({w[1]}) - Lvl Req: {rarity_required_level(w[1])} - {price} Gold")

            try:
                n = int(input("Choose weapon (0 cancel): "))
                if n == 0:
                    continue
                w = WEAPONS[n - 1]
            except (ValueError, IndexError):
                print("Invalid choice.")
                continue

            price = weapon_price(w)
            if player["gold"] >= price:
                player["gold"] -= price
                player["inventory"].append({"kind": "weapon", "name": w[0]})
                player["weapons_collected"] += 1
                print("Weapon bought.")
            else:
                print("Not enough gold.")

        elif choice == "2":
            for i, a in enumerate(ARMOR, 1):
                price = armor_price(a)
                print(f"{i}. {a[0]} ({a[1]}) - Lvl Req: {rarity_required_level(a[1])} - {price} Gold")

            try:
                n = int(input("Choose armor (0 cancel): "))
                if n == 0:
                    continue
                a = ARMOR[n - 1]
            except (ValueError, IndexError):
                print("Invalid choice.")
                continue

            price = armor_price(a)
            if player["gold"] >= price:
                player["gold"] -= price
                player["inventory"].append({"kind": "armor", "name": a[0]})
                print("Armor bought.")
            else:
                print("Not enough gold.")

        elif choice == "3":
            names = list(POTIONS.keys())
            for i, p in enumerate(names, 1):
                print(f"{i}. {p} - {POTIONS[p]['price']} Gold")

            try:
                n = int(input("Choose potion (0 cancel): "))
                if n == 0:
                    continue
                potion = names[n - 1]
            except (ValueError, IndexError):
                print("Invalid choice.")
                continue

            price = POTIONS[potion]["price"]
            if player["gold"] >= price:
                player["gold"] -= price
                player["potions"][potion] = player["potions"].get(potion, 0) + 1
                print("Potion bought.")
            else:
                print("Not enough gold.")

        elif choice == "4":
            sell_item(player)
        elif choice == "5":
            break


def sell_item(player):
    if not player["inventory"]:
        print("Nothing to sell.")
        return

    for i, item in enumerate(player["inventory"], 1):
        print(f"{i}. {item['kind'].title()} - {item['name']}")

    try:
        n = int(input("Choose item to sell (0 cancel): "))
        if n == 0:
            return
        item = player["inventory"][n - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    if item["kind"] == "weapon":
        price = weapon_price(weapon_data(item["name"])) // 2
    elif item["kind"] == "armor":
        price = armor_price(armor_data(item["name"])) // 2
    else:
        price = 50

    player["gold"] += price
    player["inventory"].pop(n - 1)
    print("Sold for", price, "gold.")


# -------------------- WORLD --------------------

def current_region(player):
    index = min((player["level"] - 1) // 10, 9)
    return REGIONS[index]


def check_boss(player):
    level = player["level"]
    if level in BOSSES and level not in player["bosses_defeated"]:
        print("\n================================")
        print("BOSS BATTLE DETECTED!")
        print(BOSSES[level])
        print("================================")

        boss = create_enemy(player, boss=True)
        result = battle(player, boss)

        if result == "win":
            player["bosses_defeated"].append(level)
            print("\nRegion cleared!")
        return result
    return None


def explore(player):
    region = current_region(player)
    print("\nYou entered:", region)

    boss_result = check_boss(player)
    if boss_result == "dead":
        return False
    if boss_result == "win":
        return True

    enemy = create_enemy(player)
    result = battle(player, enemy)
    return result != "dead"


# -------------------- SAVE / LOAD --------------------

def save_game(player):
    if "start_time" in player:
        player["total_play_time"] += time.time() - player["start_time"]
        player["start_time"] = time.time()

    try:
        with open(SAVE_FILE, "w") as file:
            json.dump(player, file, indent=4)
        print("Game saved successfully.")
    except OSError as e:
        print("Could not save game:", e)


def load_game():
    try:
        with open(SAVE_FILE, "r") as file:
            player = json.load(file)
        player["start_time"] = time.time()
        print("Game loaded successfully.")
        return player
    except (OSError, json.JSONDecodeError):
        print("No valid save file found.")
        return None


# -------------------- MENUS --------------------

def instructions():
    print("""
========== INSTRUCTIONS ==========
Explore the world and defeat enemies.
Gain EXP and level up. Every 10 levels a boss appears.
Defeat the boss to unlock the next region.
Use weapons, armor, skills, and potions to survive.
Maximum level: 100.
""")


def game_menu(player):
    while True:
        stats = get_player_stats(player)
        print("\n======================================")
        print(" LEGENDS OF THE FORGOTTEN REALM")
        print("======================================")
        print(f"Region: {current_region(player)} | Lvl: {player['level']}")
        print(f"HP: {player['hp']}/{stats['max_hp']} | Gold: {player['gold']}")
        print("\n1. Explore  2. Shop  3. Inventory  4. Equip/Unequip")
        print("5. View Stats  6. Save Game  7. Instructions  8. Exit")

        choice = input("Choose: ")

        if choice == "1":
            alive = explore(player)
            if not alive:
                return "dead"
            if player["level"] == 100 and 100 in player["bosses_defeated"]:
                return "victory"
        elif choice == "2":
            shop(player)
        elif choice == "3":
            show_inventory(player)
        elif choice == "4":
            equip_menu(player)
        elif choice == "5":
            show_stats(player)
        elif choice == "6":
            save_game(player)
        elif choice == "7":
            instructions()
        elif choice == "8":
            save_game(player)
            print("Game saved. Goodbye!")
            return "exit"
        else:
            print("Invalid choice.")


def victory_screen(player):
    total_time = player["total_play_time"]
    if "start_time" in player:
        total_time += time.time() - player["start_time"]
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)

    print("""
========================================
       YOU SAVED ELDORIA!
========================================
       VICTORY!
========================================
""")
    print("Player Name:", player["name"])
    print("Final Level:", player["level"])
    print("Total Gold:", player["gold"])
    print("Bosses Defeated:", len(player["bosses_defeated"]))
    print("Enemies Defeated:", player["enemies_defeated"])
    print("Weapons Collected:", player["weapons_collected"])
    print("Rare Items Found:", player["rare_items"])
    print(f"Total Play Time: {minutes}m {seconds}s")
    print("Final Score:", player["level"] * 100 + player["enemies_defeated"] * 10)


def game_over_menu(player):
    print("\n========== GAME OVER ==========")
    print("1. Retry  2. Load Save  3. Exit")

    choice = input("Choose: ")
    if choice == "1":
        return create_player()
    if choice == "2":
        loaded = load_game()
        return loaded if loaded else create_player()
    return None


# -------------------- MAIN --------------------

def main():
    while True:
        print("""
========================================
   LEGENDS OF THE FORGOTTEN REALM
========================================
1. New Game  2. Continue  3. Instructions  4. Exit
""")
        choice = input("Choose: ")

        if choice == "1":
            player = create_player()
        elif choice == "2":
            player = load_game()
            if player is None:
                continue
        elif choice == "3":
            instructions()
            continue
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
            continue

        result = game_menu(player)

        if result == "victory":
            victory_screen(player)
            break
        elif result == "dead":
            player = game_over_menu(player)
            if player is None:
                break


if __name__ == "__main__":
    main()