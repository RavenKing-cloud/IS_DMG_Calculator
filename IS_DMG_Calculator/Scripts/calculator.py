import math
import random
import xml.etree.ElementTree as ET


def calculate_damage(attacker_level, attacker_bap, attacker_attack, defender_level, defender_defense, crit, rng,
                     equipment, type_modifier, evade):
    """
    Calculates the damage inflicted by an attacking unit to a defending unit.

    Args:
        attacker_level (int): Level of the attacking unit.
        attacker_bap (int): Base attack power of the attacking unit.
        attacker_attack (int): Attack stat of the attacking unit.
        defender_level (int): Level of the defending unit.
        defender_defense (int): Defense stat of the defending unit.
        crit (float): Critical hit multiplier.
        rng (float): Random factor between 0.85 and 0.9999999999.
        equipment (float): Equipment multiplier.
        type_modifier (float): Type effectiveness multiplier.
        evade (float): Evade multiplier.

    Returns:
        int: The calculated damage value.
    """
    attack_check = attacker_attack * attacker_bap
    defense_check = (2 * defender_level) / 6 * defender_defense / 100
    level_factor = (2 * attacker_level) / 5 + 2
    attack_defense_factor = attack_check / defense_check
    other_factor = 1  # Modify this based on other factors in your game

    crit_check = 1.5 if crit >= 0.99 else 1

    damage = (((level_factor * attack_defense_factor) / 4.25) + 15) * crit_check * rng * equipment * type_modifier * other_factor * evade

    return math.floor(damage)

def calculate_type_modifier(move_type, defender_type, type_chart):
    """
    Calculates the type effectiveness multiplier between the move type and the defender's type.

    Args:
        move_type (str): Type of the attacking move.
        defender_type (str): Type of the defending unit.
        type_chart (dict): Dictionary containing the type chart data.

    Returns:
        float: The calculated type effectiveness multiplier.
    """
    if move_type in type_chart and defender_type in type_chart[move_type]:
        return type_chart[move_type][defender_type]

    return 1.0


def load_type_chart(file_name):
    """
    Loads the type chart from an XML file.

    Args:
        file_name (str): Name of the XML file.

    Returns:
        dict: Dictionary containing the type chart data.
    """
    try:
        tree = ET.parse(file_name)
        root = tree.getroot()

        type_chart = {}
        for move_type in root.findall("type"):
            type_name = move_type.get("name")
            type_chart[type_name] = {}

            for defender_type in move_type.findall("defender"):
                defender_name = defender_type.get("name")
                effectiveness = float(defender_type.get("effectiveness"))
                type_chart[type_name][defender_name] = effectiveness

        return type_chart

    except ET.ParseError:
        raise ValueError("Invalid XML file.")
    except FileNotFoundError:
        raise ValueError(f"{file_name} file not found.")


# Example usage
if __name__ == "__main__":
    attacker_level = 10
    attacker_bap = 5
    attacker_attack = 200
    defender_level = 10
    defender_defense = 80
    move_type = "Fire"
    defender_type = "Grass"
    crit = random.uniform(0.01, 0.99999999999999)
    rng = random.uniform(0.85, 0.99999999999999)
    equipment = 1.0  # Modify this based on the attacker's equipment
    evade = 1.0  # Modify this based on the defender's evade stat

    type_chart = load_type_chart("type_chart.xml")
    type_modifier = calculate_type_modifier(move_type, defender_type, type_chart)
    damage = calculate_damage(attacker_level, attacker_bap, attacker_attack, defender_level, defender_defense, crit, rng,
                              equipment, type_modifier, evade)

    print(f"Damage: {damage}")