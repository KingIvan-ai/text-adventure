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
            livingRoom(world)
            break
        elif userInput == "dining room":
            locations.append(userInput)
            print(locations)
            world["loc"] = "dining room"
            diningRoom(world)
            break
        else:
            print("Invalid input! Please enter 'living room' or 'dining room'.")

def main():
    world = {}
    world["loc"] = "walkway"
    world["inv"] = []
    print("Welcome to the Haunted Mansion!")
    print("Please enter your name for this adventure")
    userInput = input()
    world["playerName"] = userInput
    with open("rooms.txt", "r") as file:
        fileContents = file.read()
        fileParagraphs = fileContents.split("\n\n")
        print(fileParagraphs[0], end="\n\n")
    walkway(world)

main()