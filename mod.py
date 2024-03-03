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
                    get_skirmish_pgr_address, get_unit_melee_dmg_address, read, write, unit_names)


def write_with_uninst_info(shc, address, value, size):
    if str(size) not in uninstall.keys():
        uninstall[str(size)] = {}
    if str(address) not in uninstall[str(size)]:
        uninstall[str(size)][str(address)] = read(shc, address, size)
    write(shc, address, value, size)


def apply_aob_as_patch(address, array):
    with open(exe_path, "r+b") as shc:
        offset = address
        for elem in array:
            if type(elem) == tuple:
                value = elem[0]
                size = elem[1]
            else:
                value = elem
                size = 1
            write_with_uninst_info(shc, offset, value, size)
            offset += size


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

            if "baseMeleeDamage" in current_unit.keys():
                for defender in unit_names:
                    address = get_unit_melee_dmg_address(key, defender)
                    write_with_uninst_info(shc, address, current_unit["baseMeleeDamage"], size)

            if "meleeDamageVs" in current_unit.keys():
                for defender in current_unit["meleeDamageVs"]:
                    address = get_unit_melee_dmg_address(key, defender)
                    write_with_uninst_info(shc, address, current_unit["meleeDamageVs"][defender], size)


def modify_resources(resources):
    with open(exe_path, "r+b") as shc:
        size = 4
        for resource in resources:
            res_data = resources[resource]

            if "buy" in res_data.keys():
                address = get_resource_buy_address(resource)
                write_with_uninst_info(shc, address, res_data["buy"], size)

            if "sell" in res_data.keys():
                address = get_resource_sell_address(resource)
                write_with_uninst_info(shc, address, res_data["sell"], size)

            if resource == "Leather" and any(["baseDelivery" in res_data.keys(), "skirmishBonus" in res_data.keys()]):
                leather_base_delivery = res_data.get("baseDelivery", 1)
                leather_skirmish_bonus = int(res_data.get("skirmishBonus", 1))
                apply_aob_as_patch(0x15A52E, [
                    0x6A, leather_skirmish_bonus,
                    0x6A, leather_base_delivery,
                    0x50,
                    0xE9, 0x40, 0xAB, 0xEA, 0xFF
                ])

                apply_aob_as_patch(0x5078, [
                    0x66, 0x89, 0xAE, 0x04, 0xDC, 0x45, 0x01,
                    0xE9, 0xB4, 0x54, 0x15, 0x00
                ])
            else:
                if "baseDelivery" in res_data.keys():
                    resource_addr_map = {
                        "Wood": 0x14D60E,
                        "Stone": 0x1513E4,
                        "Iron": 0x16672E,
                        "Pitch": 0x15219E,
                        "Meat": 0x1506A8,
                        "Apple": 0x154591,
                        "Cheese": 0x154D44,
                        "Bread": 0x156383,
                        "Wheat": 0x152F6E,
                        "Hop": 0x153AE6
                    }
                    if resource in resource_addr_map.keys():
                        write_with_uninst_info(shc, resource_addr_map[resource], res_data["baseDelivery"], 1)
                    else:
                        errors.append(f"Delivery modification for {resource} is not supported!")

                if "skirmishBonus" in res_data.keys():
                    bonus_addr_map = {
                        "Wood": 0x14D605,
                        "Stone": 0x1513E2,
                        "Iron": 0x166726,
                        "Pitch": 0x152195,
                        "Hop": 0x153AE2,
                        "Meat": 0x15069F,
                        "Apple": 0x15458F,
                        "Cheese": 0x154D3B
                    }
                    if resource in bonus_addr_map.keys():
                        write_with_uninst_info(shc, bonus_addr_map[resource], int(res_data["skirmishBonus"]), 1)
                    else:
                        errors.append(f"Production bonus modification for {resource} is not supported!")


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
                write_with_uninst_info(shc, 0x5BBCD, variety_bonuses[2], 1)


def install_tax_reset_feature(reset_value):
    with open(exe_path, "r+b") as shc:
        shc.seek(0)
        shc.seek(0x11E)
        original_section_count = int.from_bytes(shc.read(1), byteorder='little')

    if original_section_count != 5:
        errors.append("Error UCP not installed, tax_reset change is not applied.")
        return

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


def modify_taxation_rules(taxation_rules):
    with open(exe_path, "r+b") as shc:
        if tax_table := taxation_rules.get("gold"):
            tax_jumpout_instructions = [
                0xE8, 0xE6, 0xB2, 0xFA, 0xFF,  # call 40459B
                0xE8, 0x3F, 0xB3, 0xFA, 0xFF,  # call 4045F9
                0xEB, 0x02,  # jump over 2 bytes
                0x90, 0x90,
                0xC1, 0xF8, 0x03,  # sar eax,03
                0x83, 0x3D, 0xF0, 0x4D, 0x35, 0x02, 0x00
                # cmp dword ptr [Stronghold_Crusader_Extreme.exe+1F54DF0],00
            ]
            apply_aob_as_patch(0x592B0, tax_jumpout_instructions)

            bribe_jumpout_instructions = [
                0xE8, 0x26, 0xB2, 0xFA, 0xFF,  # call 40459B
                0xE8, 0x7F, 0xB2, 0xFA, 0xFF,  # call 4045F9
                0x90,
                0xC1, 0xF8, 0x02  # sar eax,02
            ]
            apply_aob_as_patch(0x59370, bribe_jumpout_instructions)

            custom_tax_instructions = [
                0x8A, 0x44, 0x24, 0x0C,                          # mov eax [esp+0C]
                0x66, 0x8B, 0x04, 0x45, 0xAD, 0x45, 0x40, 0x00,  # mov ax,[eax*2+Stronghold_Crusader_Extreme.exe+45AD]
                0x0F, 0xAF, 0x44, 0x24, 0x10,                    # imul eax,[esp+10]
                0xC3                                             # return
            ]
            apply_aob_as_patch(0x459B, custom_tax_instructions)

            apply_aob_as_patch(0x45AD, [(int(float(a) * 100), 2) for a in tax_table])

            apply_aob_as_patch(0x45F9, [
                0x52,
                0x51,
                0x8B, 0xC8,
                0xBA, 0x67, 0x66, 0x66, 0x66,
                0xF7, 0xEA,
                0xD1, 0xFA,
                0x8B, 0xC1,
                0xC1, 0xF8, 0x1F,
                0x29, 0xC2,
                0x8B, 0xC2,
                0x59,
                0x5A,
                0xC3,
            ])
            neutral_level = tax_table.index("0.00")
        else:
            neutral_level = 3

        if popularity := taxation_rules.get("popularity"):
            apply_aob_as_patch(0x3B09D, [
                0x83, 0xF8, neutral_level,
                0x7D, 0x09,                          # jnl 0043B0AB
                0x83, 0x7C, 0x24, 0x10, 0x00,        # cmp dword ptr [esp+10],00 { 0 }
                0x7F, 0x02,                          # jle 0043B0AB
                0xB0, neutral_level,                 # mov al,03 { 3 }
                0xC1, 0xE0, 0x02,                    # shl eax,02 { 2 }
                0x8B, 0x80, 0xBC, 0xB0, 0x43, 0x00,  # mov eax,[eax+0043B0BC]
                0xE9, 0x84, 0x00, 0x00, 0x00,        # jmp 0043B13D
                0x90,                                # nop
                0x90,                                # nop
                0x90                                 # nop
            ] + [(x, 4) for x in popularity] + [0] * 75)
            write_with_uninst_info(shc, 0x3EBC4, neutral_level, 1)
            apply_aob_as_patch(0x3EBC4, [
                neutral_level,
                0x7D, 0x0E,
                0x83, 0x7C, 0x24, 0x18, 0x00,
                0x7F, 0x07,
                0xB8, neutral_level, 0x00, 0x00, 0x00,  # mov eax,00000003
                0xEB, 0x06,                             # jmp 0043EBDB
                0x8B, 0x80, 0xC0, 0x0B, 0x1F, 0x01,     # mov eax,[eax+011F0BC0]
                0xC1, 0xE0, 0x02,                       # shl eax,02
                0x8B, 0xB0, 0xBC, 0xB0, 0x43, 0x00,     # mov esi,[eax+0043B0BC]
                0xEB, 0x76                              # jmp 0043EC5C
            ] + [0] * 118)

            apply_aob_as_patch(0x5BC5D, [
                neutral_level,
                0x7D, 0x06,
                0x85, 0xED,
                0x7F, 0x02,
                0xB0, neutral_level,
                0xC1, 0xE0, 0x02,
                0x8B, 0x80, 0xBC, 0xB0, 0x43, 0x00,
                0xE9, 0x80, 0x00, 0x00, 0x00
            ] + [0] * 128)
        elif neutral_level != 3:
            errors.append("You must include popularity table for your tax table with different neutral level!")

        if advantage_multipliers := taxation_rules.get("advantage_multiplier"):
            human_big_ai_medium = advantage_multipliers["human_big_ai_medium"]
            ai_big = advantage_multipliers["ai_big"]
            write_with_uninst_info(shc, 0x59326, human_big_ai_medium, 4)
            write_with_uninst_info(shc, 0x592FA, ai_big, 4)


def modify_fear_factor_rules(fear_factor_rules):
    with open(exe_path, "r+b") as shc:
        for key in fear_factor_rules:
            if key == "popularity_per_good_level":
                write_with_uninst_info(shc, 0x3F664, fear_factor_rules[key], 1)
                write_with_uninst_info(shc, 0x3EDBC, fear_factor_rules[key], 1)
                write_with_uninst_info(shc, 0x5BE5B, fear_factor_rules[key], 1)
            elif key == "popularity_per_bad_level":
                write_with_uninst_info(shc, 0x3F66E, fear_factor_rules[key], 1)
                write_with_uninst_info(shc, 0x3EDC8, fear_factor_rules[key], 1)
                write_with_uninst_info(shc, 0x5BE69, fear_factor_rules[key], 1)
            elif key == "productivity":
                productivity = fear_factor_rules["productivity"]
                write_with_uninst_info(shc, 0x590FF, productivity[0], 4)
                write_with_uninst_info(shc, 0x5910C, productivity[1], 4)
                write_with_uninst_info(shc, 0x59119, productivity[2], 4)
                write_with_uninst_info(shc, 0x59126, productivity[3], 4)
                write_with_uninst_info(shc, 0x59133, productivity[4], 4)
                write_with_uninst_info(shc, 0x5913F, productivity[5], 4)
                write_with_uninst_info(shc, 0x5914C, productivity[6], 4)
                write_with_uninst_info(shc, 0x59159, productivity[7], 4)
                write_with_uninst_info(shc, 0x59166, productivity[8], 4)
                write_with_uninst_info(shc, 0x59179, productivity[9]-productivity[10], 1)
                write_with_uninst_info(shc, 0x5917C, productivity[10], 1)
            elif key == "coverage":
                coverage_val = fear_factor_rules[key]
                apply_aob_as_patch(0xB42E,[
                    0xE9, 0xB7, 0x91, 0xFF, 0xFF,  # jump out to 4045EA
                    0x41  # inc ecx
                ])
                apply_aob_as_patch(0x45EA, [
                    0x85, 0xC9,  # test ecx, ecx
                    0x74, 0x01,  # jn by one
                    0x49,  # dec ecx
                    0xC1, 0xF9, coverage_val,  # sar ecx, coverage_value
                    0xE9, 0x3C, 0x6E, 0x00, 0x00  # jump back to inc ecx
                ])
            elif key == "combat_bonus":
                damage_table = fear_factor_rules[key]
                enable_custom_combat_bonus(damage_table)


def enable_custom_combat_bonus(damage_table):
    combat_jumpout_instructions = [
        0x31, 0xC9,  # xor ecx, ecx
        0xE9, 0xA1, 0x2F, 0xED, 0xFF,  # jmp 4045C8 (45C8)
        0x90, 0x90, 0x90, 0x90  # nop nop nop nop
    ]
    apply_aob_as_patch(0x131620, combat_jumpout_instructions)

    custom_combat_instructions = [
        0x8A, 0x88, 0xDD, 0x45, 0x40, 0x00,  # mov cl,[eax+004045DD]
        0x0F, 0xAF, 0x4C, 0x24, 0x04,  # imul ecx,[esp+04]
        0xE9, 0x53, 0xD0, 0x12, 0x00  # jmp 0053162B
    ]
    apply_aob_as_patch(0x45C8, custom_combat_instructions)

    apply_aob_as_patch(0x45D8, damage_table)


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
            modify_resources(val)
        elif cfg == "population_gathering_rate":
            modify_population_gathering_rate(val)
        elif cfg == "religion":
            modify_religion_rules(val)
        elif cfg == "beer":
            modify_beer_rules(val)
        elif cfg == "food":
            modify_food_rules(val)
        elif cfg == "fear_factor":
            modify_fear_factor_rules(val)
        elif cfg == "taxation":
            modify_taxation_rules(val)
        elif cfg == "special":
            for key, change in val.items():
                if not ("special" in uninstall):
                    uninstall["special"] = {}

                if key == "tax_reset":
                    uninstall["special"]["tax_reset"] = copy.deepcopy(change)
                    reset_value = change["value"]
                    install_tax_reset_feature(reset_value)
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
                    except Exception as e:
                        errors.append(f"{e.args[0]}: {e.args[1]}")


if __name__ == "__main__":
    argp = argparse.ArgumentParser()
    argp.add_argument("-gamepath", required=False,
                      help="Folder of SHC Extreme, defaults to parent directory")
    argp.add_argument("-create_uninst", action="store_true", required=False,
                      help="Create uninstall.json to be able to revert changes later.")

    settings = argp.parse_args()
    errors = []
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

    if errors:
        ctypes.windll.user32.MessageBoxW(0, "\n".join(errors), "Errors occured in installation", 0)
