# This file contains the main game loop and handles room navigation, user input, and storytelling.

# The fun tions used in this file are:
# get_valid_input(prompt, valid_options): Prompts the user for valid input until they enter an option from valid_options.
# add_to_inventory(world, item): Adds an item to the inventory if not already present.
# describe_inventory(world): Displays the player's inventory or indicates if it's empty.
# check_final_battle(world): Checks if the player has the required items for the final battle.
# move_to_location(world, new_location): Moves the player to a new location, with consequences for excessive movement.
# walkway(world, fileParagraphs): Manages gameplay in the walkway location.
# living_room(world, fileParagraphs): Manages gameplay in the living room, including stealing the key.
# dining_room(world, fileParagraphs): Manages gameplay in the dining room, including the axe or combat.
# combat(world, player, enemy): Handles combat between the player and enemy.
# save_results(player, world): Saves the player’s progress to a file.
# game_loop(world, fileParagraphs): Main loop that controls game flow based on the player’s location.
# main(): Initializes and starts the game.

# Purpose: Asks the user for input and ensures it's one of the valid options.
# Input:
# prompt: A string that asks the user for input.
# valid_options: A list of valid options that the user can choose from.
# Returns: A valid input from the user, which is one of the valid_options.
def get_valid_input(prompt, valid_options):
        choice = input(prompt).lower()
        if choice in valid_options:
            return choice
        print(f"Invalid input. Please enter {valid_options}")

# Purpose: Adds an item to the player's inventory if it is not already present.
# Input:
# world: A dictionary that stores the game state (including the inventory).
# item: The item to be added to the inventory.
# Returns: None (modifies the inventory directly).
def add_to_inventory(world, item):
    if item not in world["inv"]:
        world["inv"].append(item)

# Purpose: Describes the items in the player’s inventory.
# Input:
# world: A dictionary that stores the game state (including the inventory).
# Returns: A string that lists the items in the inventory, or a message indicating the inventory is empty.
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

# Purpose: Checks if the player has the required items for the final battle.
# Input:
# world: A dictionary that stores the game state (including the inventory).
# Returns: True if the player has the necessary items; otherwise, False.
def check_final_battle(world):
    if {"key", "axe"}.issubset(world["inv"]):
        world["loc"] = "final battle"

# Purpose: Moves the player to a new location and handles the consequences of movement.
# Input:
# world: A dictionary that stores the game state (including the player’s current location).
# new_location: A string indicating the new location the player is moving to.
# Returns: A string describing the new location, or a message about movement consequences.
def move_to_location(world, new_location):
    if len(world["locations"]) > 6:
        print("While you were going back and forth between the living room and the dining room\n"
              "a ghost attacks you from behind and kills you.")
        world["loc"] = "dead"
    else:
        world["locations"].append(new_location)
        world["loc"] = new_location

# Purpose: Handles gameplay when the player is in the walkway location.
# Input:
# world: A dictionary that stores the game state.
# fileParagraphs: A list of paragraphs describing different events or scenarios in the walkway.
# Returns: A string describing the current situation or actions in the walkway.
def walkway(world, fileParagraphs):
    print("\n", fileParagraphs[1])
    userInput = get_valid_input("Where do you want to go? (Enter 'living room' or 'dining room')\n>", ["living room", "dining room"])
    move_to_location(world, userInput)

# Purpose: Handles gameplay when the player is in the living room, including stealing the key.
# Input:
# world: A dictionary that stores the game state.
# fileParagraphs: A list of paragraphs describing different events or scenarios in the living room.
# Returns: A string describing the current situation or actions in the living room.
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

# Purpose: Handles gameplay when the player is in the dining room, including interactions like the axe or combat.
# Input:
# world: A dictionary that stores the game state.
# fileParagraphs: A list of paragraphs describing different events or scenarios in the dining room.
# Returns: A string describing the current situation or actions in the dining room.
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

# Purpose: Handles combat between the player and an enemy.
# Input:
# world: A dictionary that stores the game state.
# player: An object representing the player's current stats (e.g., health, inventory).
# enemy: An object representing the enemy’s stats (e.g., health, attack power).
# Returns: A string describing the result of the combat (win/loss or status updates).
def combat(world, player, enemy):
    try:
        import combat
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

# Purpose: Saves the player's progress to a file.
# Input:
# player: An object containing the player's stats.
# world: A dictionary that stores the game state (including the player’s progress).
# Returns: None (modifies a file to save the game state).
def save_results(player, world):
    try:
        with open("saveResults.txt", "w") as f:
            f.write(f"name: {player['name']}\n")
            f.write(f"health points: {player['hp']}\n")
            f.write(f"inventory: {world['inv']}\n")
    except IOError:
        # Handles cases where the file cannot be written.
        print("Error: Unable to save game results.")

# Purpose: Controls the main flow of the game, including movement and interactions based on the player’s location.
# Input:
# world: A dictionary that stores the game state.
# fileParagraphs: A list of paragraphs describing the scenarios or events at different locations.
# Returns: None (runs the game loop until the game ends).
def game_loop(world, fileParagraphs):
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

# Purpose: Initializes the game, sets up initial conditions, and starts the game loop.
# Input: None.
# Returns: None (calls other functions to run the game).
def main():
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