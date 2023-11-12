from functools import partial

building_names = [
    "Hovel",
    "House",
    "Woodcutter hut",
    "Ox tether",
    "Iron mine",
    "Pitch rig",
    "Hunters hut",
    "Mercenary post",
    "Barracks",
    "Stockpile",
    "Armory",
    "Fletcher",
    "Blacksmith",
    "Poleturner",
    "Armourer",
    "Tanner",
    "Bakery",
    "Brewery",
    "Granary",
    "Quarry",
    "Quarrypile",
    "Inn",
    "Apothecary",
    "Engineers guild",
    "Tunnelers guild",
    "Marketplace",
    "Well",
    "Oil smelter",
    "Siege tent",
    "Wheat farm",
    "Hop farm",
    "Apple farm",
    "Dairy farm",
    "Mill",
    "Stables",
    "Chapel",
    "Church",
    "Cathedral",
    "Ruins",
    "Keep one",
    "Keep two",
    "Keep three",
    "Keep four",
    "Keep five",
    "Large gatehouse",
    "Small gatehouse",
    "Main wood",
    "Postern gate",
    "Drawbridge",
    "Tunnel",
    "Campfire",
    "Signpost",
    "Parade ground",
    "Fire ballista",
    "Campground",
    "Parade ground",
    "Parade ground",
    "Parade ground",
    "Parade ground",
    "Gatehouse",
    "Tower",
    "Gallows",
    "Stocks",
    "Witch hoist",
    "Maypole",
    "Garden",
    "Killing pit",
    "Pitch ditch",
    "unused",
    "Water pot",
    "Keepdoor left",
    "Keepdoor right",
    "Keepdoor",
    "Tower one",
    "Tower two",
    "Tower three",
    "Tower four",
    "Tower five",
    "unused2",
    "Catapult",
    "Trebuchet",
    "Siege tower",
    "Battering ram",
    "Portable shield",
    "unused3",
    "Mangonel",
    "Tower Ballista",
    "unused4",
    "unused5",
    "unused6",
    "Cesspit",
    "Burning stake",
    "Gibbet",
    "Dungeon",
    "Stretching rack",
    "Flogging rack",
    "Chopping block",
    "Dunking stool",
    "Dog cage",
    "Statue",
    "Shrine",
    "Bee hive",
    "Dancing bear",
    "Pond",
    "Bear cave",
    "European Outpost",
    "Mercenary Outpost"
]

unit_names = [
    "Peasant",
    "Burning man",
    "Woodcutter",
    "Fletcher",
    "Tunneler",
    "Hunter",
    "Quarry mason",
    "Quarry grunt",
    "Quarry ox",
    "Pitch worker",
    "Wheat farmer",
    "Hops farmer",
    "Apple farmer",
    "Dairy farmer",
    "Miller",
    "Baker",
    "Brewer",
    "Poleturner",
    "Blacksmith",
    "Armourer",
    "Tanner",
    "European archer",
    "European crossbowman",
    "European spearman",
    "European pikeman",
    "European maceman",
    "European swordsman",
    "European knight",
    "Ladderman",
    "Engineer",
    "Iron miner1",
    "Iron miner2",
    "Priest",
    "Healer",
    "Drunkard",
    "Innkeeper",
    "Monk",
    "unknown1",
    "Catapult",
    "Trebuchet",
    "Mangonel",
    "Trader",
    "Trader horse",
    "Deer",
    "Lion",
    "Rabbit",
    "Camel",
    "Crow",
    "Seagull",
    "Siege tent",
    "Cow",
    "Hunter dog",
    "Fireman",
    "Ghost",
    "Lord",
    "Lady",
    "Jester",
    "Siege tower",
    "Battering ram",
    "Portable shield",
    "Tower ballista",
    "Chicken",
    "Mother",
    "Child",
    "Juggler",
    "Fireeater",
    "Dog",
    "unknown2",
    "unknown3",
    "Arabian archer",
    "Arabian slave",
    "Arabian slinger",
    "Arabian assassin",
    "Arabian horse archer",
    "Arabian swordsman",
    "Arabian firethrower",
    "Fire ballista"
]

resource_names = [
    "Wood",
    "Hop",
    "Stone",
    "Blank1",
    "Iron",
    "Pitch",
    "Blank2",
    "Wheat",
    "Bread",
    "Cheese",
    "Meat",
    "Fruit",
    "Beer",
    "Blank3",
    "Flour",
    "Bow",
    "Xbow",
    "Spear",
    "Pike",
    "Mace",
    "Sword",
    "Leather",
    "Armor"
]

building_cost_base = 0x1c21e4
building_health_base = 0x1ba21c
building_population_base = 0x1ba43c

unit_health_base = 0x74eaf4
unit_arrow_dmg_base = 0x74ec34
unit_xbow_dmg_base = 0x74eeb4
unit_stone_dmg_base = 0x74ed74

# 16 bytes from last of one unit to start of next unit
unit_melee_dmg_base = 0x74f134

resource_buy_base = 0x217358
resource_sell_base = 0x2173c0

scenario_pgr_base = 0x6B8FAC
scenario_pgr_crowded_base = 0x6B9004
skirmish_pgr_base = 0x6B9058

popularity_thresholds = [str(x) for x in range(0, 101, 5)]


def get_address(name_list: list, base_address, size, name):
    index = name_list.index(name)
    if index == -1:
        raise Exception(f"Invalid name: {name}")
    return base_address + index * size


get_building_cost_address = partial(get_address, building_names, building_cost_base, 20)
get_building_health_address = partial(get_address, building_names, building_health_base, 4)
get_building_population_address = partial(get_address, building_names, building_population_base, 4)

get_unit_health_address = partial(get_address, unit_names, unit_health_base, 4)
get_unit_arrow_dmg_address = partial(get_address, unit_names, unit_arrow_dmg_base, 4)
get_unit_xbow_dmg_address = partial(get_address, unit_names, unit_xbow_dmg_base, 4)
get_unit_stone_dmg_address = partial(get_address, unit_names, unit_stone_dmg_base, 4)

get_resource_buy_address = partial(get_address, resource_names, resource_buy_base, 4)
get_resource_sell_address = partial(get_address, resource_names, resource_sell_base, 4)

get_scenario_pgr_address = partial(get_address, popularity_thresholds, scenario_pgr_base, 4)
get_scenario_pgr_crowded_address = partial(get_address, popularity_thresholds, scenario_pgr_crowded_base, 4)
get_skirmish_pgr_address = partial(get_address, popularity_thresholds, skirmish_pgr_base, 4)


def get_unit_melee_dmg_address(attacker_name, defender_name):
    attacker_index = unit_names.index(attacker_name)
    defender_index = unit_names.index(defender_name)
    if attacker_index == -1:
        raise Exception("Invalid unit name")
    if defender_index == -1:
        raise Exception("Invalid unit name")
    return unit_melee_dmg_base + defender_index * 4 + attacker_index * 16 + attacker_index * (len(unit_names) - 1) * 4


def read(shc, address, size):
    shc.seek(0)
    shc.seek(address)
    return int.from_bytes(shc.read(size), byteorder='little')


def write(shc, address, value, size):
    shc.seek(0)
    shc.seek(address)
    try:
        if int(value) < 0:
            shc.write(int(value).to_bytes(size, byteorder='little', signed=True))
        else:
            shc.write(int(value).to_bytes(size, byteorder='little'))
    except ValueError:
        shc.write(int(value, base=16).to_bytes(size, byteorder='little'))
