### Get out of jail free card, house buying, mortgaging, turn order

#
#Settings
#

#
#File Names
#

version = "Australian"

properties = "info/" + version + "/Properties.txt"
prices = "info/" + version + "/Prices.txt"
housePrices = "info/" + version + "/HousePrices.txt"
propertiesPositions = "info/propertyPositions.txt"
colourGroups = "info/colourgroups.txt"

#
#House Rules
#

freeParkingCash = False
landOnGo = False
buyOnDoubles = False
auctionPropertyNotBought = False
unlimitedHouses = False

#
#
#

#
#Starting Cash
#

moneyMultiplier = 10
startingMoney = (1500 * moneyMultiplier)

money = (1500 * moneyMultiplier)

#
#Imports
#

from random import randint
import tkinter

#
#
#

#
#Classes
#

class Property():
    name = ""
    price = 0
    ableToPurchase = False
    owned = "none"
    colour = ""
    currentHouses = 0

    def __init__(self, nameP, priceP, ableToPurchaseP, ownedP, colourP):
        self.name = nameP
        self.price = priceP
        self.owned = ownedP
        self.ableToPurchase = ableToPurchaseP
        self.colour = colourP
        self.currentHouses = 0

    def UpdateOwned(self, isOwned):
        self.owned = isOwned

    def UpdateHouses(self, houses):
        self.currentHouses = houses

#
#Global Variables
#

asset = 0

spaceNum = 0

jailRoll = False

chanceName = "Chance"
communityChestName = "Community Chest"

colours = ["brown", "lBlue", "pink", "orange", "red", "yellow", "green", "dBlue"]
amountOfProperties = [2, 3, 3, 3, 3, 3, 3, 2]
amountOfPropertiesCurrently = [0, 0, 0, 0, 0, 0, 0, 0]

#
#
#

#
# Initialisation
#

places = []
file1 = open(properties, "r")
file2 = open(prices, "r")
file3 = open(colourGroups, "r")
file4 = open(housePrices, "r")
file5 = open(propertiesPositions, "r")

for i in range(0, 40):

    name = file1.readline().rstrip()
    price = int(file2.readline())
    colour = file3.readline().rstrip()
    housePrice = int(file4.readline())

    if int((file5.readline()).rstrip()) == 1:
        ableToPurchase = True
    else:
        ableToPurchase = False

    prop = Property(name, price, ableToPurchase, "none", colour) # nameP, priceP, ableToPurchaseP, ownedP, colourP

    places.append(prop)

file1.close()
file2.close()
file3.close()
file4.close()
file5.close()

#
#
#

#
#Functions
#


def rollDice():
    print("")
    print("Rolling Dice...")
    
    roll1 = randint(1, 6)
    roll2 = randint(1, 6)
    combRoll = roll1+roll2
    print(combRoll)

    if roll1 == roll2:
        print("Doubles")
    
    print("")

    return roll1, roll2, combRoll

###


def gotoJail():

    global spaceNum
    global jailRoll
    
    spaceNum = 10
    jailRoll = True

###


def buying():

    global money
    global asset

    cantBuy = False

    if places[spaceNum].owned != "none" or not places[spaceNum].ableToPurchase:
        cantBuy = True

    if not cantBuy:

        print("Is " + places[spaceNum].name + " purchased? ")
        isBought = input(": ")

        if isBought == "yes":
            print("How much rent is owed? ")
            rentOwed = int(input(": "))

            money = money - rentOwed

            places[spaceNum].UpdateOwned("other")
            
        else:
        
            if places[spaceNum].price <= money + asset: ## Todo need to mortgage properties for this
                print("I'd like to buy this property")

                money = money - places[spaceNum].price

                places[spaceNum].UpdateOwned("me")

                asset += 0.5 * places[spaceNum].price

                if places[spaceNum].colour != "":
                    incrementColour(places[spaceNum].colour)
                    #houseBuying(colourGroupsArr[spaceNum])
                
            else:
                print("I cannot afford this property")
                
                if auctionPropertyNotBought:
                    print("Placeholder")
                print("")
    else:
        print("I can't buy " + places[spaceNum].name)

###


def movement(moveSpaces):

    global spaceNum
    global money

    spaceNum += moveSpaces

    if landOnGo and spaceNum == 40:
        print("Landed on go!")
        money = money + (200 * moneyMultiplier)

    if spaceNum >= 40:
        print("Passing go")
        money = money + (200 * moneyMultiplier)
        
    spaceNum = spaceNum % 40

    if places[spaceNum].name == "Go to Jail":
        gotoJail()

###


def houseBuying(colour):
    
    global asset
    global money

    indexNum = -1

    for i in range(0, len(colours)):
        if colour == colours[i]:
            indexNum = i

###


def incrementColour(colour):

    indexNum = -1

    for i in range(0, len(colours)):
        if colour == colours[i]:
            indexNum = i

    amountOfPropertiesCurrently[indexNum] += 1

def turn():

    global spaceNum
    global jailRoll
    global chanceName
    global communityChestName
    global money

    jailDblCount = 0

    roll1, roll2, combRoll = rollDice()
    
    if jailRoll:
        if roll1 == roll2:

            jailRoll = False
            print("Out of jail")

        else:
            print("Still in jail")

    else:

        if roll1 == roll2:
            while roll1 == roll2:

                jailDblCount += 1

                if jailDblCount == 3:
                    gotoJail()
                    break

                movement(combRoll)

                if buyOnDoubles:
                    buying()

                roll1, roll2, combRoll = rollDice()

            movement(combRoll)

        else:
            movement(combRoll)

        if (places[spaceNum].name == chanceName) or (places[spaceNum].name == communityChestName):
            print("I got a " + places[spaceNum].name + " card")
            print("Did I get moved on the board by the card?")
            moved = input(": ")

            if moved == "yes":
                print("What space number did I get moved to?")
                spaceNum = int(input(": "))
                if spaceNum == 10:
                    gotoJail()
                else:
                    buying()

            print("Money change caused")
            change = int(input(": "))

            money = money + change

        elif not places[spaceNum].owned == "me":
            buying()

        else:
            print("I own this property")

        if places[spaceNum].name == "Go to Jail":
            gotoJail()

        print("Next persons turn")

###

#def noMoney(amount)

#
#
#

#
#Play
#

#
#Setup
#

print("Rolling dice to determine turn order")
rollDice()

#
#
#

######
######
######

while asset+money > 0:

    print("")
    print("Money = " + str(money))
    print("Assets = " + str(asset))
    print("Total = " + str(money+asset))
    print("")

    print("What is my money change since last turn")
    change = int(input(": "))

    if money + change < 0:
        print("Placeholder")
    else:
        money = money + change

    turn()

    print("I'm on space " + places[spaceNum].name)

print("I lost")

######
######
######
