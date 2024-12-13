# Contains the main game loop and handles room navigation, user input, and storytelling.

def get_valid_input(prompt, valid_options):
    # Continuously prompts the user for input until a valid option is provided.
    while True:
        choice = input(prompt).lower()
        if choice in valid_options:
            return choice
        print(f"Invalid input. Please enter {valid_options}")

# Adds an item to the player's inventory if it's not already present.
def add_to_inventory(world, item):
    if item not in world["inv"]:
        world["inv"].append(item)

def describe_inventory(world):
    if world["inv"] == []:
        print("Your inventory is empty.")
    else:
        print("Your inventory includes:")
    for item in world["inv"]:
        if item == "key":
            print("-key")
        elif item == "axe":
            print("-axe")

# Checks if the player has all necessary items to proceed to the final battle.
def check_final_battle(world):
    if {"key", "axe"}.issubset(world["inv"]):
        world["loc"] = "final battle"

# Updates the player's location and handles a condition where the player moves excessively.
def move_to_location(world, new_location):
    if len(world["locations"]) > 6:
        print("While you were going back and forth between the living room and the dining room\n"
              "a ghost attacks you from behind and kills you.")
        world["loc"] = "dead"
    else:
        world["locations"].append(new_location)
        world["loc"] = new_location

# Handles the gameplay logic for the walkway location.
def walkway(world, fileParagraphs):
    print("\n", fileParagraphs[1])
    userInput = get_valid_input("Where do you want to go? (Enter 'living room' or 'dining room')\n>", ["living room", "dining room"])
    move_to_location(world, userInput)

# Handles the gameplay logic for the living room location.
def living_room(world, fileParagraphs):
    while True:
        if world["locations"].count("living room") < 2:  # First visit to the living room.
            print("\n", fileParagraphs[2])
            userInput = get_valid_input("Will you attempt to take the key from the monster? (Enter 'yes' or 'no')\n>", ["yes", "no"])
            if userInput == "yes":
                add_to_inventory(world, "key")
                check_final_battle(world)
                if not {"key", "axe"}.issubset(world["inv"]):
                    print("Excellent. You have successfully stolen the key!")
                    describe_inventory(world)
                    print("Now, it's time to go to the dining room.")
                    move_to_location(world, "dining room")
                break
            if userInput == "no":
                print("You decide to not steal the key and instead go to the dining room.")
                move_to_location(world, "dining room")
                break
        else:  # Returning to the living room.
            print("\nYou have returned to the living room with the monster and your friend.")
            userInput = get_valid_input("Will you steal the key from the monster this time? (Enter 'yes' or 'no')\n>", ["yes", "no"])
            if userInput == "yes":
                add_to_inventory(world, "key")
                describe_inventory(world)
                check_final_battle(world)
                if not {"key", "axe"}.issubset(world["inv"]):
                    print("Excellent. You have successfully stolen the key!")
                    describe_inventory(world)
                    print("Now, it's time to go to the dining room.")
                    move_to_location(world, "dining room")
                break
            if userInput == "no":
                print("You decide to not steal the key and instead go to the dining room.")
                move_to_location(world, "dining room")
                break

# Handles the gameplay logic for the dining room location.
def dining_room(world, fileParagraphs):
    while True:
        if world["locations"].count("dining room") < 2:  # First visit to the dining room.
            print("\n", fileParagraphs[3])
            userInput = get_valid_input("Will you open the vase? (Enter 'yes' or 'no')\n>", ["yes", "no"])
            if userInput == "yes":
                add_to_inventory(world, "axe")
                check_final_battle(world)
                print(fileParagraphs[4])
                if not {"key", "axe"}.issubset(world["inv"]):
                    describe_inventory(world)
                move_to_location(world, "living room")
                break
            if userInput == "no":
                print(fileParagraphs[5])
                world["loc"] = "dead"
                break
        if world["locations"].count("dining room") == 2 and "purple gremlin" not in world["vic"]:  # Returning with new options.
            print("\nYou have returned to the dining room. This time, you notice there is another door.\n"
                  "You may enter through the other door or return to the living room.")
            userInput = get_valid_input("Which will you choose? (Enter 'living room' or 'new door')\n>", ["living room", "new door"])
            if userInput == "living room":
                move_to_location(world, userInput)
                break
            if userInput == "new door":  # Initiates combat with the purple gremlin.
                print("Behind the door, there is a purple gremlin that jumps out and attacks you!\nTime to fight!")
                print(f"Purple gremlin hp: {enemy2['hp']}\nPurple gremlin attack: {enemy2['atk']}")
                combat(world, player, enemy2)
                break
        if world["locations"].count("dining room") > 2 and "purple gremlin" not in world["vic"]:
            print("\nYou have returned to the dining room.")
            userInput = get_valid_input("Which will you open the new door or return to the living room? (Enter 'living room' or 'new door')\n>", ["living room", "new door"])
            if userInput == "living room":
                move_to_location(world, userInput)
                break
            if userInput == "new door":  # Initiates combat with the purple gremlin.
                print("Behind the door, there is a purple gremlin that jumps out and attacks you!\nTime to fight!")
                print(f"Purple gremlin hp: {enemy2['hp']}\nPurple gremlin attack: {enemy2['atk']}")
                combat(world, player, enemy2)
                break
        else:
            print("You have returned to the dining room. But there is nothing more to do here, so you return to the living room.")
            move_to_location(world, "living room")
            break

# Handles the combat system logic.
def combat(world, player, enemy):
    try:
        import combat  # Assuming external combat logic exists.
        result = combat.battle(player, enemy)
        if enemy == enemy1:
            if result == "enemy dead":
                print(f"The monster collapses on the ground dead.\n"
                      "You then use the key to open the cage and free your friend!\n"
                      "CONGRATULATIONS! YOU WIN!")
                return
            elif result == "player dead":
                print("Sadly, the monster has won this fight. It pulls you closer and gobbles you down!\nGAME OVER")
                world["loc"] = "dead"
                return
            else:
                print("You have killed the monster, but during the fight you were wounded fatally. You collapse on the ground dead.\nGAME OVER")
                world["loc"] = "dead"
                return
        if enemy == enemy2:
            if result == "enemy dead":
                print("You have defeated the purple gremlin and automatically regain full hp!")
                player["hp"] = 20
                world["vic"].append("purple gremlin")
                print("Back to the living room!")
                move_to_location(world, "living room")
                return
            elif result == "player dead":
                print("You tried your best. But the purple gremlin has defeated you.")
                world["loc"] = "dead"
                return
            else:
                print("You have killed the purple gremlin. But during the fight you were mortally wounded. You collapse on the floor dead.")
                world["loc"] = "dead"
                return
    except Exception as e:
        print(f"An unexpected error occurred in the battle: {e}")

def save_results(player, world):
    # Saves the player's progress to a text file.
    try:
        with open("saveResults.txt", "w") as f:
            f.write(f"name: {player['name']}\n")
            f.write(f"health points: {player['hp']}\n")
            f.write(f"inventory: {world['inv']}\n")
    except IOError:
        # Handles cases where the file cannot be written.
        print("Error: Unable to save game results.")

def game_loop(world, fileParagraphs):
    # Runs the main game loop until the game ends.
    while True:
        if world["loc"] == "dead":
            print("GAME OVER")
            break

        # Check if the player has the necessary items to trigger the final battle.
        if {"key", "axe"}.issubset(world["inv"]):
            world["loc"] = "final battle"

        # Handle different game states based on the player's location.
        if world["loc"] == "final battle":
            describe_inventory(world)
            print(f"\nYou have successfully grabbed both the key and the axe.\nIt's time for the final showdown between you and the monster.\n"
                  "The Monster comes towards you and the fight begins!")
            print(f"Monster hp: {enemy1['hp']}\nMonster attack: {enemy1['atk']}")
            combat(world, player, enemy1)  # Initiates combat with the monster.
            break
        elif world["loc"] == "walkway":
            walkway(world, fileParagraphs)  # Processes the "walkway" location.
        elif world["loc"] == "living room":
            living_room(world, fileParagraphs)  # Processes the "living room" location.
        elif world["loc"] == "dining room":
            dining_room(world, fileParagraphs)  # Processes the "dining room" location.

def main():
    # Starts the game by initializing the game state and running the main loop.
    world = {
        "loc": "walkway",  # The player's current location.
        "inv": [],  # The player's inventory.
        "locations": [],  # List of locations visited.
        "vic": []  # Placeholder for potential future use (e.g., victories).
    }

    try:
        # Reads room descriptions from the "rooms.txt" file.
        with open("rooms.txt", "r") as file:
            fileParagraphs = file.read().split("\n\n")
    except FileNotFoundError:
        # Handles cases where the file is not found.
        print("Error: The file 'rooms.txt' was not found. Please ensure it exists.")
        return
    except IOError:
        # Handles other file-related issues.
        print("Error: An issue occurred while reading the file.")
        return

    print("Welcome to the Haunted Mansion!")
    print("Please enter your name for this adventure:")
    userInput = input(">")  # Gets the player's name.

    global player
    # Initializes the player's attributes.
    player = {
        "name": userInput,
        "hp": 20,  # Player's health points.
        "atk": 5  # Player's attack power.
    }

    global enemy1
    # Initializes the attributes of the first enemy.
    enemy1 = {
        "name": "Monster",
        "hp": 20,  # Monster's health points.
        "atk": 5  # Monster's attack power.
    }

    global enemy2
    # Initializes the attributes of the second enemy.
    enemy2 = {
        "name": "purple gremlin",
        "hp": 10,  # Gremlin's health points.
        "atk": 3  # Gremlin's attack power.
    }

    # Welcomes the player and provides initial game details.
    print(f"\nWelcome to the Haunted Mansion {player['name']}!")
    print(fileParagraphs[0], end="\n\n")
    print(f"Your hp: {player['hp']}\nYour attack: {player['atk']}")
    describe_inventory(world)
    walkway(world, fileParagraphs)  # Starts the game at the "walkway" location.
    game_loop(world, fileParagraphs)  # Enters the main game loop.

main()