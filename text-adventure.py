# A list that keeps track of where the player has been.
# Each time a room is entered, the list will append the name of that room.
locations = []

# The walkway function reads from a text file to set the scene for this location.
# Then it present the player with the option of enetering the living room or dining room.
def walkway(world):
    with open("rooms.txt", "r") as file:
        fileContents = file.read()
        fileParagraphs = fileContents.split("\n\n")
        print(fileParagraphs[1])
    while True:
        userInput = input().lower()
        if userInput == "living room":
            locations.append(userInput)
            print(locations)
            world["loc"] = "living room"
            break
        elif userInput == "dining room":
            locations.append(userInput)
            print(locations)
            world["loc"] = "dining room"
            break
        else:
            print("Invalid input! Please enter 'living room' or 'dining room'.")

# In this function, it reads from the text file to describe the scene. 
# Then the player may either choose to steal an item (the key) or not.
# Regardless of their choice, they will go to the dining room.
def livingRoom(world):
    while True:
        if locations.count("living room") < 2: # If the player has not already been to the living room it will read a detailed descritpion of the living room.
            with open("rooms.txt", "r") as file:
                        fileContents = file.read()
                        fileParagraphs = fileContents.split("\n\n")
                        print(fileParagraphs[2])
        else: # If the player has already been here, it will read the text below instead.
            print("You have returned to the living room with the monster and your friend.\n"
                "Will you steal the key from the monster this time? (Enter 'yes' or 'no')")

        monsterChoice = input("> ")

        if(monsterChoice == "yes"):
            print("Excellent. You have successfully stolen the key!\n"
                "Now, it's time to go back to the dining room.")
            world["inv"].append("key")
            print(world["inv"]) # I did this just to visualize what things were being added throughout the program during testing. I will remove it when the program is finished.
            locations.append("dining room")
            print(locations) # I did this just to visualize what things were being added throughout the program during testing. I will remove it when the program is finished
            world["loc"] = "dining room"
            break
        elif(monsterChoice == "no"):
            locations.append("dining room")
            print(locations)
            print("You decide to not steal the dog's jewelry and instead go to the dining room.")
            world["loc"] = "dining room"
            break
        else: 
            print("Invalid choice. Please enter 'yes' or 'no'.")

# In the dining room, the player may chose to break a vase or not. 
# If the vase is broken, they will find an axe; if not, they will wake up and realize this was a dream.
def diningRoom(world):
    while True:
        if locations.count("dining room") < 2: # If the player has not already been to the dining room it will read a detailed descritpion of the dining room.
                with open("rooms.txt", "r") as file:
                        fileContents = file.read()
                        fileParagraphs = fileContents.split("\n\n")
                        print(fileParagraphs[3])
        else: # If they have been here before, they will find that there is another door. They may open it or go back to the living room.
            print("You have returned to the dining room. This time, you notice there is another door.\n"
                "you may enter through the other door or return to the living room. Which will you choose?\n"
                "(Enter 'living room' or 'new door')")
            userInput = input(">")
            if userInput == "living room":
                    locations.append("living room")
                    print(locations)
                    world["loc"] = "living room"
                    break
            if userInput == "new door": # I am trying to turn this into a battle scenario
                    print("Behind the door, there is a monster that jumps out and kills you.")
                    world["loc"] = "dead"
                    break

        vaseChoice = input("> ")

        if(vaseChoice == "yes" and locations.count("living room") == 0):
            with open("rooms.txt", "r") as file:
                fileContents = file.read()
                fileParagraphs = fileContents.split("\n\n")
                print(fileParagraphs[4])
            world["inv"].append("axe")
            print(world["inv"])
            locations.append("living room")
            print(locations)
            world["loc"] = "living room"
            break
        elif(vaseChoice == "yes" and locations.count("living room") > 0):
            print("You grab the axe and return to the living room.")
            world["inv"].append("axe")
            print(world["inv"])
            locations.append("living room")
            print(locations)
            world["loc"] = "living room"
            break
        elif(vaseChoice == "no"):
            with open("rooms.txt", "r") as file:
                fileContents = file.read()
                fileParagraphs = fileContents.split("\n\n")
                print(fileParagraphs[5])
                world["loc"] = "dead"
                break
        else: 
            print("Invalid choice. Please enter yes or no.")

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