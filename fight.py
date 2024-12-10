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
    if who == "player":
        print("Pick an option: ")
        print("1: Attack")
        print("2: Heal")
        decision = input() # Ideally, we would validate their input
    else:
        if (randint(1,2) == 1):  # 50% chance
            decision = "1" # enemy decided to attack
        else:
            decision = "2" # enemy decided to do nothing
    
    # Apply effect of decision
    if decision == "1":
        defender["hp"] -= attacker["atk"]
        print(f"{attacker['name']} hits {defender['name']} for {attacker['atk']} damage")
    if decision == "2":
        healAmt = sum(diceRoll("1d4"))
        attacker["hp"] += healAmt
        print(f"{attacker['name']} rests and recovers {healAmt} hp")

def battle(player, enemy):
    print(f"A {enemy['name']} approches {player['name']}, ready to fight")

    while True:
        turn(player, enemy, "player")
        turn(enemy, player, "enemy")
        print(f"{player['name']} has {player['hp']} hp left")
        print(f"{enemy['name']} has {enemy['hp']} hp left")
        if (player["hp"] <= 0):
            return "player dead"
        if (enemy["hp"] <= 0):
            return "enemy dead"