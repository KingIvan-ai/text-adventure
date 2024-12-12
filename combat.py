from random import *

def diceRoll(roll):
    rSplit = roll.split("d")

    numDice = int(rSplit[0])
    diceSize = int(rSplit[1])

    diceList = []
    for i in range(numDice):
        diceList.append(randint(1,diceSize))
    
    return diceList

def turn(attacker, defender, who):
    while True:
        if who == "player":
            print("Pick an option (enter '1' or '2'): ")
            print("1: Attack")
            print("2: Heal")
            decision = input()
        else:
            if (randint(1,2) == 1):  # 50% chance
                decision = "1" # enemy decided to attack
            else:
                decision = "2" # enemy decided to do nothing
    
        # Apply effect of decision
        if decision == "1":
            defender["hp"] -= attacker["atk"]
            print(f"{attacker['name']} hits {defender['name']} for {attacker['atk']} damage")
            break
        elif decision == "2":
            healAmt = sum(diceRoll("1d4"))
            attacker["hp"] += healAmt
            if attacker["hp"] > 20:
                attacker["hp"] = 20
            print(f"{attacker['name']} rests and recovers {healAmt} hp")
            break
        else:
            print("Invalid input. Please enter '1' or '2'")

def battle(player, enemy):

    while True:
        turn(player, enemy, "player")
        turn(enemy, player, "enemy")
        print(f"{player['name']} has {player['hp']} hp left")
        print(f"{enemy['name']} has {enemy['hp']} hp left")
        if (player["hp"] <= 0 and enemy["hp"] > 0):
            return "player dead"
        if (enemy["hp"] <= 0 and player["hp"] > 0):
            return "enemy dead"
        if (player["hp"] <= 0 and enemy["hp"] <=0):
            return "both dead"