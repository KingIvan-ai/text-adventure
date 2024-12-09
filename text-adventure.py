locations = []

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

def livingRoom(world):
    while True:
        if locations.count("living room") < 2:
            with open("rooms.txt", "r") as file:
                        fileContents = file.read()
                        fileParagraphs = fileContents.split("\n\n")
                        print(fileParagraphs[2])
        else:
            print("You have returned to the living room with the monster and your friend.\n\
Will you steal the key from the monster this time? (Enter 'yes' or 'no')")

        monsterChoice = input("> ")

        if(monsterChoice == "yes"):
            print("Excellent. You have successfully stolen the key!\n"
                "Now, it's time to go back to the dining room.")
            world["inv"].append("key")
            print(world["inv"])
            world["loc"] = "dining room"
            locations.append("dining room")
            print(locations)
            break
        elif(monsterChoice == "no"):
            print("You decide to not steal the dog's jewelry and instead go to the dining room.")
            world["loc"] = "dining room"
            locations.append("dining room")
            print(locations)
            break
        else: 
            print("Invalid choice. Please enter yes or no.")

def diningRoom(world):
    while True:
        if locations.count("dining room") < 2:
                with open("rooms.txt", "r") as file:
                        fileContents = file.read()
                        fileParagraphs = fileContents.split("\n\n")
                        print(fileParagraphs[3])
        else:
            print("You have returned to the dining room. This time, you notice there is another door.\n\
you may enter through the other door or return to the living room. Which will you choose?\n\
(Enter 'living room' or 'new door')")
            userInput = input(">")
            if userInput == "living room":
                    world["loc"] = "living room"
            if userInput == "new door":
                    print("Behind the door, there is a monster that jumps out and kills you.")
                    world["player"] = "dead"
                    break

        vaseChoice = input("> ")

        if(vaseChoice == "yes" and locations.count("living room") == 0):
            with open("rooms.txt", "r") as file:
                fileContents = file.read()
                fileParagraphs = fileContents.split("\n\n")
                print(fileParagraphs[4])
            world["inv"].append("axe")
            print(world["inv"])
            world["loc"] = "living room"
            locations.append("living room")
            print(locations)
            break
        elif(vaseChoice == "yes" and locations.count("living room") > 0):
            print("You grab the axe and return to the living room.")
            world["inv"].append("axe")
            print(world["inv"])
            world["loc"] = "living room"
            locations.append("living room")
            print(locations)
            break
        elif(vaseChoice == "no"):
            with open("rooms.txt", "r") as file:
                fileContents = file.read()
                fileParagraphs = fileContents.split("\n\n")
                print(fileParagraphs[5])
                world["player"] = "dead"
                break
        else: 
            print("Invalid choice. Please enter yes or no.")

def livingRoom2(world):
    pass

def main():
    world = {}
    world["loc"] = "walkway"
    world["inv"] = []
    print("Welcome to the Haunted Mansion!")
    print("Please enter your name for this adventure")
    userInput = input()
    world["player"] = userInput
    with open("rooms.txt", "r") as file:
        fileContents = file.read()
        fileParagraphs = fileContents.split("\n\n")
        print(fileParagraphs[0], end="\n\n")
    walkway(world)

    while True:
        if world["player"] == "dead":
            return print("GAME OVER")
        if len(locations) > 6:
            print("While you were going back and forth between the living room and the dining room\n\
a ghost attacks you from behind and kills you")
            world["player"] = "dead"
        if {"key", "axe"}.issubset(world["inv"]):
            world["loc"] = "living room 2"
        if world["loc"] == "walkway":
            walkway(world)
        if world["loc"] == "living room":
            livingRoom(world)
        if world["loc"] == "dining room":
            diningRoom(world)
        if world["loc"] == "living room 2":
            livingRoom2(world)

main()