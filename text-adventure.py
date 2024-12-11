def get_valid_input(prompt, valid_options):
    while True:
        choice = input(prompt).lower()
        if choice in valid_options:
            return choice
        print(f"Invalid input. Please enter {valid_options}")
        
def add_to_inventory(world, item):
    if item not in world["inv"]:
        world["inv"].append(item)
        print(f"{item} added to inventory.")

def check_final_battle(world):
    if {"key", "axe"}.issubset(world["inv"]):
        world["loc"] = "final battle"
        
def move_to_location(world, new_location):
    #Update the current location and record the movement.
    if len(world["locations"]) > 6:
            print("While you were going back and forth between the living room and the dining room\n"
                "a ghost attacks you from behind and kills you.")
            world["loc"] = "dead"
    else:
        world["locations"].append(new_location)
        world["loc"] = new_location

def walkway(world, fileParagraphs):
    print(fileParagraphs[1])
    userInput = get_valid_input("Where do you want to go? (Enter 'living room' or 'dining room')\n>", ["living room", "dining room"])
    move_to_location(world, userInput)

def livingRoom(world, fileParagraphs):
    while True:
        if world["locations"].count("living room") < 2: # If the player has not already been to the living room it will read a detailed descritpion of the living room.
            print(fileParagraphs[2])
            userInput = get_valid_input("Will you attempt to take the key from the monster? (Enter 'yes' or 'no')\n>", ["yes", "no"])
            if userInput == "yes":
                add_to_inventory(world, "key")
                check_final_battle(world)
                if not {"key", "axe"}.issubset(world["inv"]):
                    print("Excellent. You have successfully stolen the key!\n"
                        "Now, it's time to go to the dining room.")
                    move_to_location(world, "dining room")
                break
            if userInput == "no":
                print("You decide to not steal the key and instead go to the dining room.")
                move_to_location(world, "dining room")
                break
        else: # If the player has already been here, it will read the text below instead.
            print("You have returned to the living room with the monster and your friend.")
            userInput = get_valid_input("Will you steal the key from the monster this time? (Enter 'yes' or 'no')\n>", ["yes", "no"])
            if userInput == "yes":
                add_to_inventory(world, "key")
                check_final_battle(world)
                if not {"key", "axe"}.issubset(world["inv"]):
                    print("Excellent. You have successfully stolen the key!\n"
                        "Now, it's time to go to the dining room.")
                    move_to_location(world, "dining room")
                break
            if userInput == "no":
                print("You decide to not steal the key and instead go to the dining room.")
                move_to_location(world, "dining room")
                break

def diningRoom(world, fileParagraphs):
    while True:
        if world["locations"].count("dining room") < 2: # If the player has not already been to the dining room it will read a detailed descritpion of the dining room.
            print(fileParagraphs[3])
            userInput = get_valid_input("Will you open the vase? (Enter 'yes' or 'no')\n>", ["yes", "no"])
            if userInput == "yes":
                add_to_inventory(world, "axe")
                check_final_battle(world)
                print(fileParagraphs[4])
                move_to_location(world, "living room")
                break
            if userInput == "no":
                print(fileParagraphs[5])
                world["loc"] = "dead"
                break
        if world["locations"].count("dining room") == 2 and "purple gremlin" not in world["vic"]: # If they have been here before, they will find that there is another door. They may open it or go back to the living room.
            print("You have returned to the dining room. This time, you notice there is another door.\n"
                "you may enter through the other door or return to the living room.")
            userInput = get_valid_input("Which will you choose? (Enter 'living room' or 'new door')\n>", ["living room", "new door"])
            if userInput == "living room":
                    move_to_location(world, userInput)
                    break
            if userInput == "new door": # I am trying to turn this into a battle scenario
                    print("Behind the door, there is a purple gremlin that jumps out and attacks you!")
                    print("Time to fight!")
                    combat(world, player, enemy2)
                    break
        if world["locations"].count("dining room") > 2 and "purple gremlin" not in world["vic"]:
            print("You have returned to the dining room.")
            userInput = get_valid_input("Which will you open the new door or return to the living room? (Enter 'living room' or 'new door')\n>", ["living room", "new door"])
            if userInput == "living room":
                    move_to_location(world, userInput)
                    break
            if userInput == "new door": # I am trying to turn this into a battle scenario
                    print("Behind the door, there is a purple gremlin that jumps out and attacks you!")
                    print("Time to fight!")
                    combat(world, player, enemy2)
                    break
        else:
            print("You have returned to the dining room. But there is nothing more to do here, so you return to the living room.")
            move_to_location(world, "living room")
            break

def combat(world, player, enemy):
    try:
        import fight
        result = fight.battle(player, enemy)
        if enemy == enemy1:
            if result == "enemy dead":
                print(f"The monster collapses on the ground dead.")
                return
            else:
                print("You tried your best. But the monster has defeated you.")
                world["loc"] = "dead"
        if enemy == enemy2:
            if result == "enemy dead":
                print(f"You have defeated the purple gremlin and automatically regain full hp!")
                player["hp"] = 20
                world["vic"].append("purple gremlin")
                print("Back to the living room!")
                move_to_location(world, "living room")
                return
            else:
                print("You tried your best. But your foe has defeated you.")
                world["loc"] = "dead"
    except Exception as e:
        print(f"An unexpected error occurred in the battle: {e}")

def saveResults(player, world):
    try:
        with open("saveResults.txt", "w") as f:
            f.write(f"name: {player['name']}\n")
            f.write(f"health points: {player['hp']}\n")
            f.write(f"inventory: {world['inv']}\n")
    except IOError:
        print("Error: Unable to save game results.")


def game_loop(world, fileParagraphs):
    # Run the main game loop until the game ends.
    while True:
        if world["loc"] == "dead":
            print("GAME OVER")
            break
        if {"key", "axe"}.issubset(world["inv"]):
            world["loc"] = "final battle"

        if world["loc"] == "final battle":
            print(f"You have successfully grabbed both the key and the axe.\nIt's time for the final showdown between you and the monster!\n"
          "The Monster comes towards you and the fight begins!")
            combat(world, player, enemy1)
            break
        elif world["loc"] == "walkway":
            walkway(world, fileParagraphs)
        elif world["loc"] == "living room":
            livingRoom(world, fileParagraphs)
        elif world["loc"] == "dining room":
            diningRoom(world, fileParagraphs)

def main():
    # Starts the game by initializing the world and player, and runs the main loop.
    world = {
        "loc": "walkway",
        "inv": [],
        "locations": [],
        "vic": []
    }

    try:
        with open("rooms.txt", "r") as file:
            fileParagraphs = file.read().split("\n\n")
    except FileNotFoundError:
        print("Error: The file 'rooms.txt' was not found. Please ensure it exists.")
        return
    except IOError:
        print("Error: An issue occurred while reading the file.")
        return

    print("Welcome to the Haunted Mansion!")
    print("Please enter your name for this adventure")
    userInput = input()
    global player
    player = {
        "name" : userInput,
        "hp" : 20,
        "atk" : 5
    }
    global enemy1
    enemy1 = {
        "name" : "Monster",
        "hp" : 20,
        "atk" : 5
    }
    global enemy2
    enemy2 = {
        "name" : "purple gremlin",
        "hp" : 10,
        "atk" : 3
    }
    print(fileParagraphs[0], end="\n\n")
    walkway(world, fileParagraphs)
    game_loop(world, fileParagraphs)

main()