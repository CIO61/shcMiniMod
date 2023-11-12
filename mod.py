import copy
import json
import os
import argparse
import sys
import ctypes

from assets import (get_building_cost_address, get_building_health_address, get_building_population_address,
                    get_unit_health_address, get_unit_arrow_dmg_address, get_unit_xbow_dmg_address,
                    get_unit_stone_dmg_address, get_resource_buy_address, get_resource_sell_address,
                    get_scenario_pgr_address, get_scenario_pgr_crowded_address,
                    get_skirmish_pgr_address, get_unit_melee_dmg_address, read, write)


def write_with_uninst_info(shc, address, value, size):
    if str(address) not in uninstall[str(size)]:
        uninstall[str(size)][str(address)] = read(shc, address, size)
    write(shc, address, value, size)


def apply_aob_as_patch(address, array):
    with open(exe_path, "r+b") as shc:
        shc.seek(0)
        shc.seek(address)
        for elem in array:
            if type(elem) == tuple:
                value = elem[0]
                size = elem[1]
                shc.write(int(value).to_bytes(size, byteorder='little'))
            else:
                shc.write(int(str(elem)).to_bytes(1, byteorder='little'))


def modify_religion_rules(religion_rules):
    with open(exe_path, "r+b") as shc:
        for key in religion_rules:
            if key == "thresholds":
                thresholds = religion_rules[key]
                write_with_uninst_info(shc, 0x5BD62, thresholds[0], 1)
                write_with_uninst_info(shc, 0x5BD6B, thresholds[1], 1)
                write_with_uninst_info(shc, 0x5BD77, thresholds[2], 1)
                write_with_uninst_info(shc, 0x5BD85, thresholds[3], 1)

                write_with_uninst_info(shc, 0x401DF, thresholds[0], 1)
                write_with_uninst_info(shc, 0x401E8, thresholds[1], 1)
                write_with_uninst_info(shc, 0x401F4, thresholds[2], 1)
                write_with_uninst_info(shc, 0x40202, thresholds[3], 1)

                write_with_uninst_info(shc, 0x40241, thresholds[0] - 1, 1)
                write_with_uninst_info(shc, 0x40250, thresholds[1] - 1, 1)
                write_with_uninst_info(shc, 0x4025F, thresholds[2] - 1, 1)
                write_with_uninst_info(shc, 0x4026E, thresholds[3] - 1, 1)

                write_with_uninst_info(shc, 0x40248, thresholds[0], 4)
                write_with_uninst_info(shc, 0x40257, thresholds[1], 4)
                write_with_uninst_info(shc, 0x40266, thresholds[2], 4)
                write_with_uninst_info(shc, 0x40275, thresholds[3], 4)

                write_with_uninst_info(shc, 0x3EE52, thresholds[0] - 1, 1)
                write_with_uninst_info(shc, 0x3EE5B, thresholds[1] - 1, 1)
                write_with_uninst_info(shc, 0x3EE67, thresholds[2] - 1, 1)
                write_with_uninst_info(shc, 0x3EE75, thresholds[3] - 1, 1)
            elif key == "bonuses":
                bonuses = religion_rules[key]
                write_with_uninst_info(shc, 0x401EC, bonuses[0], 4)
                write_with_uninst_info(shc, 0x401F8, bonuses[1], 1)
                write_with_uninst_info(shc, 0x4020B, bonuses[2] - bonuses[3], 1)
                write_with_uninst_info(shc, 0x4020E, bonuses[3], 4)

                write_with_uninst_info(shc, 0x3EE5F, bonuses[0], 4)
                write_with_uninst_info(shc, 0x3EE6B, bonuses[1], 4)
                write_with_uninst_info(shc, 0x3EE7E, bonuses[2] - bonuses[3], 1)
                write_with_uninst_info(shc, 0x3EE81, bonuses[3], 1)

                write_with_uninst_info(shc, 0x5BD6F, bonuses[0], 4)
                write_with_uninst_info(shc, 0x5BD7B, bonuses[1], 4)
                write_with_uninst_info(shc, 0x5BD8E, bonuses[2] - bonuses[3], 1)
                write_with_uninst_info(shc, 0x5BD91, bonuses[3], 4)
            elif key == "church_bonus":
                church_bonus = religion_rules[key]
                write_with_uninst_info(shc, 0x5BDA0, church_bonus, 1)
                write_with_uninst_info(shc, 0x4039D, church_bonus, 1)
                write_with_uninst_info(shc, 0x3EE92, church_bonus, 1)
            elif key == "cathedral_bonus":
                cathedral_bonus = religion_rules[key]
                write_with_uninst_info(shc, 0x5BDAC, cathedral_bonus, 1)
                write_with_uninst_info(shc, 0x403AC, cathedral_bonus, 1)
                write_with_uninst_info(shc, 0x3EE9E, cathedral_bonus, 1)


def modify_beer_rules(beer_rules):
    with open(exe_path, "r+b") as shc:
        for key in beer_rules:
            if key == "thresholds":
                thresholds = beer_rules[key]
                write_with_uninst_info(shc, 0X3B481, thresholds[0], 1)
                write_with_uninst_info(shc, 0X3B48A, thresholds[1], 1)
                write_with_uninst_info(shc, 0X3B496, thresholds[2], 1)
                write_with_uninst_info(shc, 0X3B4A4, thresholds[3], 1)

                write_with_uninst_info(shc, 0x3EF1B, thresholds[0], 1)
                write_with_uninst_info(shc, 0x3EF24, thresholds[1], 1)
                write_with_uninst_info(shc, 0x3EF30, thresholds[2], 1)
                write_with_uninst_info(shc, 0x3EF3E, thresholds[3], 1)

                write_with_uninst_info(shc, 0x5BDF8, thresholds[0], 1)
                write_with_uninst_info(shc, 0x5BE08, thresholds[1], 1)
                write_with_uninst_info(shc, 0x5BE14, thresholds[2], 1)
                write_with_uninst_info(shc, 0x5BE22, thresholds[3], 1)
            elif key == "bonuses":
                bonuses = beer_rules[key]
                write_with_uninst_info(shc, 0x3B48E, bonuses[0], 1)
                write_with_uninst_info(shc, 0x3B49A, bonuses[1], 1)
                write_with_uninst_info(shc, 0x3B4AD, bonuses[2] - bonuses[3], 1)
                write_with_uninst_info(shc, 0x3B4AF, bonuses[3], 4)

                write_with_uninst_info(shc, 0x3EF28, bonuses[0], 1)
                write_with_uninst_info(shc, 0x3EF34, bonuses[1], 1)
                write_with_uninst_info(shc, 0x3EF47, bonuses[2] - bonuses[3], 1)
                write_with_uninst_info(shc, 0x3EF4A, bonuses[3], 1)

                write_with_uninst_info(shc, 0x5BE0C, bonuses[0], 1)
                write_with_uninst_info(shc, 0x5BE18, bonuses[1], 1)
                write_with_uninst_info(shc, 0x5BE2B, bonuses[2] - bonuses[3], 1)
                write_with_uninst_info(shc, 0x5BE2E, bonuses[3], 1)
            elif key == "coverage_per_inn":
                coverage_per_inn = beer_rules[key]
                write_with_uninst_info(shc, 0x59077, coverage_per_inn * 100, 4)


def modify_food_rules(food_rules):
    with open(exe_path, "r+b") as shc:
        for key in food_rules:
            if key == "ration_bonuses":
                ration_bonuses = food_rules[key]
                write_with_uninst_info(shc, 0x3B90C, ration_bonuses[0], 4)
                write_with_uninst_info(shc, 0x3B951, ration_bonuses[0], 4)
                write_with_uninst_info(shc, 0x3B948, ration_bonuses[1], 4)
                write_with_uninst_info(shc, 0x3B937, ration_bonuses[2], 1)
                write_with_uninst_info(shc, 0x3B92A, ration_bonuses[3], 4)

                write_with_uninst_info(shc, 0x3EAC3, ration_bonuses[0], 4)
                write_with_uninst_info(shc, 0x3EAFB, ration_bonuses[0], 4)
                write_with_uninst_info(shc, 0x3EAF5, ration_bonuses[1] - 1, 1)
                write_with_uninst_info(shc, 0x3EAE2, ration_bonuses[2] - 3, 1)
                write_with_uninst_info(shc, 0x3EAD5, ration_bonuses[3], 4)

                write_with_uninst_info(shc, 0x5BB66, ration_bonuses[0], 4)
                write_with_uninst_info(shc, 0x5BB78, ration_bonuses[0], 4)
                write_with_uninst_info(shc, 0x5BB85, ration_bonuses[1] - 1, 1)
                write_with_uninst_info(shc, 0x5BBA1, ration_bonuses[2], 4)
                write_with_uninst_info(shc, 0x5BB97, ration_bonuses[3], 4)
            elif key == "variety_bonuses":
                variety_bonuses = food_rules[key]
                write_with_uninst_info(shc, 0x3BADD, variety_bonuses[0] - 2, 1)
                write_with_uninst_info(shc, 0x3BAE7, variety_bonuses[1] - 3, 1)
                write_with_uninst_info(shc, 0x3BAF0, variety_bonuses[2], 4)

                write_with_uninst_info(shc, 0x3EB1B, variety_bonuses[0], 1)
                write_with_uninst_info(shc, 0x3EB25, variety_bonuses[1], 1)
                write_with_uninst_info(shc, 0x3EB2F, variety_bonuses[2], 1)

                write_with_uninst_info(shc, 0x5BBB9, variety_bonuses[0], 1)
                write_with_uninst_info(shc, 0x5BBC3, variety_bonuses[1], 1)
                write_with_uninst_info(shc, 0x5BB4D, variety_bonuses[2], 1)


def modify_building_stats(buildings):
    with open(exe_path, "r+b") as shc:
        size = 4
        for key in buildings:
            current_building = buildings[key]

            if "cost" in current_building.keys():
                address = get_building_cost_address(key)

                for cost in current_building["cost"]:
                    write_with_uninst_info(shc, address, cost, size)
                    address += size

            if "health" in current_building.keys():
                address = get_building_health_address(key)
                write_with_uninst_info(shc, address, current_building["health"], size)

            if "housing" in current_building.keys():
                address = get_building_population_address(key)
                write_with_uninst_info(shc, address, current_building["housing"], size)


def modify_unit_stats(units):
    with open(exe_path, "r+b") as shc:
        size = 4
        for key in units:
            current_unit = units[key]

            if "health" in current_unit.keys():
                address = get_unit_health_address(key)
                write_with_uninst_info(shc, address, current_unit["health"], size)

            if "arrowDamage" in current_unit.keys():
                address = get_unit_arrow_dmg_address(key)
                write_with_uninst_info(shc, address, current_unit["arrowDamage"], size)

            if "xbowDamage" in current_unit.keys():
                address = get_unit_xbow_dmg_address(key)
                write_with_uninst_info(shc, address, current_unit["xbowDamage"], size)

            if "stoneDamage" in current_unit.keys():
                address = get_unit_stone_dmg_address(key)
                write_with_uninst_info(shc, address, current_unit["stoneDamage"], size)

            if "meleeDamageVs" in current_unit.keys():
                for defender in current_unit["meleeDamageVs"]:
                    address = get_unit_melee_dmg_address(key, defender)
                    write_with_uninst_info(shc, address, current_unit["meleeDamageVs"][defender], size)


def modify_trade_costs(resources):
    with open(exe_path, "r+b") as shc:
        size = 4
        for key in resources:
            current_resource = resources[key]

            if "buy" in current_resource.keys():
                address = get_resource_buy_address(key)
                write_with_uninst_info(shc, address, current_resource["buy"], size)

            if "sell" in current_resource.keys():
                address = get_resource_sell_address(key)
                write_with_uninst_info(shc, address, current_resource["sell"], size)


def modify_population_gathering_rate(gathering_rates):
    with open(exe_path, "r+b") as shc:
        size = 4
        for pgr in gathering_rates:
            current_pgr = gathering_rates[pgr]

            if pgr == "Skirmish":
                for threshold in current_pgr:
                    address = get_skirmish_pgr_address(threshold)
                    write_with_uninst_info(shc, address, current_pgr[threshold], size)

            if pgr == "Scenario_lt_100":
                for threshold in current_pgr:
                    address = get_scenario_pgr_address(threshold)
                    write_with_uninst_info(shc, address, current_pgr[threshold], size)

            if pgr == "Scenario_gt_100":
                for threshold in current_pgr:
                    address = get_scenario_pgr_crowded_address(threshold)
                    write_with_uninst_info(shc, address, current_pgr[threshold], size)


def install_tax_reset_feature(reset_value):
    with open(exe_path, "r+b") as shc:
        shc.seek(0)
        shc.seek(0x11E)
        original_section_count = int.from_bytes(shc.read(1), byteorder='little')

    if original_section_count != 5:
        ctypes.windll.user32.MessageBoxW(0, "Error UCP not installed, tax_reset change failed",
                                         "Tax change install error", 0)
        sys.exit(1)

    # Increase image size to accommodate for extra code
    with open(exe_path, "r+b") as shc:
        write(shc, 0x168, 0x2B90000, 4)
        write(shc, 0x2B9, 0x70, 1)
        write(shc, 0x2C1, 0x70, 1)

    # Reset tax on < 1 popularity
    tax_instructions = [
        0x3D, 0x64, 0x00, 0x00, 0x00,
        0x7F, 0x12,
        0x83, 0xBC, 0x3E, 0x88, 0x56, 0x0C, 0x00, reset_value,
        0x7E, 0x08,
        0xC6, 0x84, 0x3E, 0x88, 0x56, 0x0C, 0x00, reset_value,
        0x89, 0x84, 0x3E, 0xB4, 0x38, 0x0C, 0x00,
        0xE9, 0x09, 0xCB, 0x4C, 0xFD  # 45BB2E
    ]
    apply_aob_as_patch(0x7BE000, tax_instructions)

    position = 0x2F8F000 - 0x45bb2c

    apply_aob_as_patch(0x5BB27, [
            0xE9, (position, 4),
            0x90,
            0x90,
        ])

    apply_aob_as_patch(0x7BE025, [0x90] * 11)

    # Zero-out tax gold on < 1 popularity
    zero_tax_instructions = [
        0x66, 0x83, 0xBB, 0xA8, 0x72, 0x0C, 0x00, 0x64,
        0x7D, 0x0C,
        0x83, 0x3E, reset_value,
        0x7E, 0x07,
        0xB8, 0x03, 0x00, 0x00, 0x00,
        0x7F, 0x02,
        0x8B, 0x06,
        0x83, 0xF8, reset_value,

        0xE9, 0x60, 0xD1, 0x4C, 0xFD,  # 45C1B0
    ]
    apply_aob_as_patch(0x7BE030, zero_tax_instructions)

    position = 0x2F8F030 - 0x45C1B0

    apply_aob_as_patch(0x5C1AB, [0xE9, (position, 4)])
    apply_aob_as_patch(0x7BE050, [0x90]*0xFB0)


def uninstall_tax_reset_feature():
    # Reset image size to original ucp section size
    with open(exe_path, "r+b") as shc:
        write(shc, 0x168, 0x2F8E000, 4)
        write(shc, 0x2B9, 0x50, 1)
        write(shc, 0x2C1, 0x50, 1)

    # Undo tax reset change
    original_tax_reset_instructions = [0x89, 0x84, 0x3E, 0xB4, 0x38, 0x0C, 0x00]
    apply_aob_as_patch(0x5BB27, original_tax_reset_instructions)

    original_tax_gold_instructions = [0x8B, 0x06, 0x83, 0xF8, 0x03]
    apply_aob_as_patch(0x5C1AB, original_tax_gold_instructions)


def enable_custom_taxation(tax_table):
    tax_jumpout_instructions = [
        0xE9, 0xDF, 0xB2, 0xFA, 0xFF,             # jmp Stronghold_Crusader_Extreme.exe+459B
        0x90, 0x90,                               # nop nop
        0xC1, 0xF8, 0x03,                         # sar eax,02 { 2 }
        0x83, 0x3D, 0xF0, 0x4D, 0x35, 0x02, 0x00  # cmp dword ptr [Stronghold_Crusader_Extreme.exe+1F54DF0],00
    ]
    apply_aob_as_patch(0x592B7, tax_jumpout_instructions)

    custom_tax_instructions = [
        0x8A, 0x80, 0xBB, 0x45, 0x40, 0x00,  # mov al,[eax+Stronghold_Crusader_Extreme.exe+45BB]
        0x0F, 0xAF, 0x44, 0x24, 0x0C,        # imul eax,[esp+0C]
        0xE9, 0x13, 0x4D, 0x05, 0x00,        # jmp Stronghold_Crusader_Extreme.exe+5937C
    ]
    apply_aob_as_patch(0x459B, custom_tax_instructions)

    bribe_jumpout_instructions = [
        0x8B, 0x44, 0x24, 0x08,        # mov eax,[esp+08]
        0xE9, 0x32, 0xB2, 0xFA, 0xFF,  # jmp Stronghold_Crusader_Extreme.exe+45AB
        0x90, 0x90,                    # nop nop
        0xC1, 0xF8, 0x02               # sar eax,01
    ]
    apply_aob_as_patch(0x59370, bribe_jumpout_instructions)

    custom_bribe_instructions = [
        0x8A, 0x80, 0xBB, 0x45, 0x40, 0x00,  # mov al,[eax+Stronghold_Crusader_Extreme.exe+45BB]
        0x0F, 0xAF, 0x44, 0x24, 0x0C,        # imul eax,[esp+0C]
        0xE9, 0xC0, 0x4D, 0x05, 0x00         # jmp Stronghold_Crusader_Extreme.exe+5937C
    ]
    apply_aob_as_patch(0x45AB, custom_bribe_instructions)

    apply_aob_as_patch(0x45BB, [int(float(a)*20) for a in tax_table if a != "0.00"])


def enable_custom_combat_bonus(damage_table):
    combat_jumpout_instructions = [
        0x31, 0xC9,                    # xor ecx, ecx
        0xE9, 0xA1, 0x2F, 0xED, 0xFF,  # jmp 4045C8 (45C8)
        0x90, 0x90, 0x90, 0x90         # nop nop nop nop
    ]
    apply_aob_as_patch(0x131620, combat_jumpout_instructions)

    custom_combat_instructions = [
        0x8A, 0x88, 0xDD, 0x45, 0x40, 0x00,  # mov cl,[eax+004045DD]
        0x0F, 0xAF, 0x4C, 0x24, 0x04,        # imul ecx,[esp+04]
        0xE9, 0x53, 0xD0, 0x12, 0x00         # jmp 0053162B
    ]
    apply_aob_as_patch(0x45C8, custom_combat_instructions)

    apply_aob_as_patch(0x45D8, damage_table)


def uninstall_custom_combat_bonus():
    original_combat_bonus_instructions = [
        0x83, 0xC0, 0x14,
        0x0F, 0xAF, 0x44, 0x24, 0x04,
        0x8D, 0x0C, 0x80
    ]
    apply_aob_as_patch(0x531620, original_combat_bonus_instructions)

    codecave_cleanup = [0x03] * 27
    apply_aob_as_patch(0x4045C8, codecave_cleanup)


def uninstall_custom_taxation():
    original_tax_instructions = [0x0F, 0xAF, 0x44, 0x24, 0x0C, 0x99, 0x2B, 0xC2, 0xD1, 0xF8]
    apply_aob_as_patch(0x592B7, original_tax_instructions)

    original_bribe_instructions = [0xB8, 0x05, 0x00, 0x00, 0x00, 0x2B, 0x44, 0x24, 0x08, 0x0F, 0xAF, 0x44, 0x24, 0x0C]
    apply_aob_as_patch(0x59370, original_bribe_instructions)

    codecave_cleanup = [0x03] * 43  # original content in the code cave
    apply_aob_as_patch(0x459B, codecave_cleanup)


def install_mod():
    if os.path.exists(configpath):
        with open(configpath, "r") as f:
            config = json.load(f)
    else:
        print("Cannot find config.json (must be in same directory as installer)!", file=sys.stderr)

    if os.path.isfile(uninst_path):
        with open(uninst_path, "r") as f:
            try:
                uninstall.update(json.load(f))
            except json.JSONDecodeError:
                pass

    if "4" not in uninstall:
        uninstall["4"] = {}

    for cfg, val in config.items():
        if cfg == "buildings":
            modify_building_stats(val)
        elif cfg == "units":
            modify_unit_stats(val)
        elif cfg == "resources":
            modify_trade_costs(val)
        elif cfg == "population_gathering_rate":
            modify_population_gathering_rate(val)
        elif cfg == "religion":
            modify_religion_rules(val)
        elif cfg == "beer":
            modify_beer_rules(val)
        elif cfg == "food":
            modify_food_rules(val)
        elif cfg == "special":
            for key, change in val.items():
                if not ("special" in uninstall):
                    uninstall["special"] = {}

                if key == "tax_reset":
                    uninstall["special"]["tax_reset"] = copy.deepcopy(change)
                    reset_value = change["value"]
                    install_tax_reset_feature(reset_value)
                elif key == "custom_taxation":
                    uninstall["special"]["custom_taxation"] = copy.deepcopy(change)
                    tax_table = change["table"]
                    enable_custom_taxation(tax_table)
                elif key == "custom_combat_bonus":
                    uninstall["special"]["custom_combat_bonus"] = copy.deepcopy(change)
                    damage_table = change["table"]
                    enable_custom_combat_bonus(damage_table)
                elif key == "assassin_rally_speed":
                    uninstall["special"]["assassin_rally_speed"] = copy.deepcopy(change)
                    speed = change["value"] & 0xF
                    assassin_rally_aob = [0x66, 0xBA, speed, 0x00, 0x90, 0x90, 0x90]
                    apply_aob_as_patch(0x174A60, assassin_rally_aob)

        elif cfg == "other":
            with open(exe_path, "r+b") as shc:
                for change in val:
                    address = int(change["address"], 16)
                    size = change["size"]

                    if str(size) not in uninstall:
                        uninstall[str(size)] = {}

                    if type(change["value"]) != list:
                        write_with_uninst_info(shc, address, change["value"], size)

                    elif type(change["value"]) == list:
                        for item in change["value"]:
                            write_with_uninst_info(shc, address, item, size)
                            address += size

    if settings.create_uninst:
        with open("uninstall.json", "w") as f:
            json.dump(uninstall, f, indent=4)


def uninstall_mod():
    if os.path.isfile(uninst_path):
        with open(uninst_path, "r") as f:
            try:
                uninstall.update(json.load(f))
            except json.JSONDecodeError:
                return

        with open(exe_path, "r+b") as shc:
            for size in uninstall:
                for key in uninstall[size]:
                    try:
                        write(shc, int(key), uninstall[size][key], int(size))
                    except:
                        if "tax_reset" in uninstall[size]:
                            uninstall_tax_reset_feature()
                        if "assassin_rally_speed" in uninstall[size]:
                            assassin_rally_aob = [0x66, 0x8B, 0x96, 0x88, 0xD3, 0x45, 0x01]
                            shc.seek(0)
                            shc.seek(0x174A60)
                            for elem in assassin_rally_aob:
                                shc.write(elem.to_bytes(1, byteorder='little'))
                        if "custom_taxation" in uninstall[size]:
                            uninstall_custom_taxation()
                        if "custom_combat_bonus" in uninstall[size]:
                            uninstall_custom_combat_bonus()


if __name__ == "__main__":
    argp = argparse.ArgumentParser()
    argp.add_argument("-gamepath", required=False,
                      help="Folder of SHC Extreme, defaults to parent directory")
    argp.add_argument("-create_uninst", action="store_true", required=False,
                      help="Create uninstall.json to be able to revert changes later.")

    settings = argp.parse_args()
    if settings.gamepath:
        gamedir = os.path.abspath(settings.gamepath)
    else:
        gamedir = os.path.abspath(os.path.join(".", ".."))
    if getattr(sys, "frozen", False):
        my_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        my_dir = os.path.dirname(os.path.abspath(__file__))

    uninst_path = os.path.join(my_dir, "uninstall.json")
    configpath = os.path.join(my_dir, "config.json")
    uninstall = {}
    retries = 0
    if "Stronghold_Crusader_Extreme.exe" not in os.listdir(gamedir):
        ctypes.windll.user32.MessageBoxW(0, f"Stronghold_Crusader_Extreme.exe not found in {gamedir}",
                                         "Game not found", 0)
        sys.exit(1)

    exe_path = os.path.join(gamedir, "Stronghold_Crusader_Extreme.exe")

    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        uninstall_mod()
    else:
        install_mod()
