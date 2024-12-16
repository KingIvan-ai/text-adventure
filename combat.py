# Implements the combat mechanics, including dice rolling, turn-based logic, and battle resolution.

# This file contains functions related to a simple text-based battle simulation.
# It includes:
# 1. A function to simulate rolling dice for variable damage or healing.
# 2. A turn-based system for players and enemies to perform actions.
# 3. A battle loop to execute the combat sequence until a winner is determined.

from random import *

# Function: diceRoll
# Purpose: Simulates rolling a specified number of dice of a given size (e.g., "2d6" rolls two six-sided dice).
# Parameters:
# - roll (str): A string representing the dice roll in the format "XdY", 
#   where X is the number of dice and Y is the size of the dice (e.g., "1d20" rolls one 20-sided die).
# Returns:
# - diceList (list): A list of integers representing the result of each individual die roll.
def diceRoll(roll):
    rSplit = roll.split("d")

    numDice = int(rSplit[0])
    diceSize = int(rSplit[1])

    diceList = []
    for i in range(numDice):
        diceList.append(randint(1, diceSize))
    
    return diceList

# Function: turn
# Purpose: Executes a single turn for a player or an enemy. The current actor can choose to attack or heal.
# Parameters:
# - attacker (dict): The dictionary containing information about the attacking character 
#   (name, hp, atk - attack power).
# - defender (dict): The dictionary containing information about the defending character (name, hp).
# - who (str): A string specifying who is taking the turn ("player" or "enemy").
# Returns:
# - None: This function directly modifies the hp of the attacker or defender within the dictionaries provided.
def turn(attacker, defender, who):
    while True:
        if who == "player":
            print("Pick an option (enter '1' or '2'): ")
            print("1: Attack")
            print("2: Heal")
            decision = input()
        else:
            if (randint(1, 2) == 1):  # 50% chance
                decision = "1" # enemy decided to attack
            else:
                decision = "2" # enemy decided to heal
    
        # Apply effect of decision
        if decision == "1":
            defender["hp"] -= attacker["atk"]
            print(f"{attacker['name']} hits {defender['name']} for {attacker['atk']} damage")
            break
        elif decision == "2":
            healAmt = sum(diceRoll("1d4"))  # Roll 1d4 for healing
            attacker["hp"] += healAmt
            if attacker["hp"] > 20:  # Cap maximum hp at 20
                attacker["hp"] = 20
            print(f"{attacker['name']} rests and recovers {healAmt} hp")
            break
        else:
            print("Invalid input. Please enter '1' or '2'")

# Function: battle
# Purpose: Runs the main battle loop, allowing the player and the enemy to take turns until one or both are defeated.
# Parameters:
# - player (dict): A dictionary containing the player's stats (name, hp, atk).
# - enemy (dict): A dictionary containing the enemy's stats (name, hp, atk).
# Returns:
# - (str): A string indicating the outcome of the battle ("player dead", "enemy dead", or "both dead").
def battle(player, enemy):
    while True:
        turn(player, enemy, "player")  # Player takes a turn
        turn(enemy, player, "enemy")  # Enemy takes a turn
        print(f"{player['name']} has {player['hp']} hp left")
        print(f"{enemy['name']} has {enemy['hp']} hp left")
        
        # Determine the outcome of the battle
        if (player["hp"] <= 0 and enemy["hp"] > 0):
            return "player dead"
        if (enemy["hp"] <= 0 and player["hp"] > 0):
            return "enemy dead"
        if (player["hp"] <= 0 and enemy["hp"] <= 0):
            return "both dead"
