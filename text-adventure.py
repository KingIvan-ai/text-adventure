# A list that keeps track of where the player has been.
# Each time a room is entered, the list will append the name of that room.
locations = []

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
    world["locations"].append(new_location)
    print(world["locations"])
    world["loc"] = new_location

# The walkway function reads from a text file to set the scene for this location.
# Then it present the player with the option of enetering the living room or dining room.
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
                print(world["inv"]) # I did this just to visualize what things were being added throughout the program during testing. I will remove it when the program is finished.
                print("Excellent. You have successfully stolen the key!\n"
                    "Now, it's time to go to the dining room.")
                move_to_location(world, "dining room")
                break
            if userInput == "no":
                print("You decide to not steal the dog's jewelry and instead go to the dining room.")
                move_to_location(world, "dining room")
                break
        else: # If the player has already been here, it will read the text below instead.
            print("You have returned to the living room with the monster and your friend.")
            userInput = get_valid_input("Will you steal the key from the monster this time? (Enter 'yes' or 'no')\n>", ["yes", "no"])
            if userInput == "yes":
                add_to_inventory(world, "key")
                check_final_battle(world)
                print(world["inv"]) # I did this just to visualize what things were being added throughout the program during testing. I will remove it when the program is finished.
                print("Excellent. You have successfully stolen the key!\n"
                    "Now, it's time to go to the dining room.")
                move_to_location(world, "dining room")
                break
            if userInput == "no":
                print("You decide to not steal the dog's jewelry and instead go to the dining room.")
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
        else: # If they have been here before, they will find that there is another door. They may open it or go back to the living room.
            print("You have returned to the dining room. This time, you notice there is another door.\n"
                "you may enter through the other door or return to the living room.")
            userInput = get_valid_input("Which will you choose? (Enter 'living room' or 'new door')\n>", ["living room", "new door"])
            if userInput == "living room":
                    move_to_location(world, userInput)
                    break
            if userInput == "new door": # I am trying to turn this into a battle scenario
                    print("Behind the door, there is a monster that jumps out and kills you.")
                    move_to_location(world, "dead")
                    break

# This will be a final scenario that will automatically take place
# When the player has successfully grabbed both the key and the axe
# I am still working on it.
def finalFight(world):
    import fight

    result = fight.battle(player, enemy)
    if result == "enemy dead":
        print(f"The {enemy['name']} collapses on the ground")
        print("YOU WIN!")
    else:
        print(f"The world goes dark for our hero {player['name']}")


def saveResults (player, world): 
    f = open ("saveResults.txt", "w")
    print(player)
    f.write(f"name: {player["name"]}\n")
    f.write(f"health points: {player["hp"]}\n")
    f.write(f"inventory: {world["inv"]}\n")
    f.close

# The main function starts by creating a name for our player 
# and then defining variouis dictionaries that will be used throughout the program such as world["inv"]
# It also reads the introductory text and contains a while loop for deciding which function to run.
def main():
    world = {}
    world["loc"] = "walkway"
    world["inv"] = []
    print("Welcome to the Haunted Mansion!")
    print("Please enter your name for this adventure")
    userInput = input()
    global player
    player = {
        "name" : userInput,
        "hp" : 20,
        "atk" : 5
    }
    global enemy
    enemy = {
        "name" : "The Monster",
        "hp" : 20,
        "atk" : 5
    }
    with open("rooms.txt", "r") as file:
        fileContents = file.read()
        fileParagraphs = fileContents.split("\n\n")
        print(fileParagraphs[0], end="\n\n")
    walkway(world)

    # A while loop that tells the program which function to run depending on world["loc"]
    while True:
        if world["loc"] == "dead":
            saveResults(player, world)
            return "GAME OVER"
        if len(locations) > 6:
            print("While you were going back and forth between the living room and the dining room\n"
                "a ghost attacks you from behind and kills you.")
            world["player"] = "dead"
        if {"key", "axe"}.issubset(world["inv"]):
            world["loc"] = "living room 2"
        if world["loc"] == "walkway":
            walkway(world)
        if world["loc"] == "living room":
            livingRoom(world)
        if world["loc"] == "dining room":
            diningRoom(world)
        if world["loc"] == "final fight":
            finalFight(world)
        

main()