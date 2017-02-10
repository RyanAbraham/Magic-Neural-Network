# Ryan Abraham
# February 9, 2017
# The world's first normal network

import random
import numpy as np
import pickle

costs = [0] * 2 + [1] * 20 + [2] * 30 + [3] * 20 + [4] * 15 + [5] * 10 + [6] * 5 + [7] * 2 + [8] * 1
costDict = {}
powerDict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
toughDict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
keywordDict =

class Card(object):
	# Constructor
	def __init__(self, name, cost, effect, power, toughness):
		self.name = name
		self.cost = cost
		self.effect = effect
		self.power = power
		self.toughness = toughness
		if(effect == ""):
			self.effect = None

	# Train the network by prompting the user for feedback
	def train(self):
		updateDicts = True
		print("\n" + self.toString())
		feedback = input("\nWhat do you think of this card? Too [S]trong, too [W]eak, or [G]ood?\n")
		if(feedback.lower() == "s"):
			modifier = 1
		elif(feedback.lower() == "w"):
			modifier = -1
		elif(feedback.lower() == "v"):
			save_dicts()
			updateDicts = False
		elif(feedback.lower() == "l"):
			load_dicts()
			updateDicts = False
		else:
			# The card is good, so record what made it good
			# Calculate the point value of the card by adding all the traits
			totalPoints = powerDict.get(self.power, 0) + toughDict.get(self.toughness, 0)
			print(totalPoints)
			# Associate the point value with the cost of the card
			pointList = costDict.get(self.cost, [])
			pointList.append(totalPoints)
			costDict[self.cost] = pointList
			modifier = 0
		if (updateDicts):
			# Update the point values associated with the traits used
			# If the trait is not already in the dict, set it to 0 and then modify it
			powerDict[self.power] = powerDict.get(self.power, 0) + modifier
			toughDict[self.toughness] = toughDict.get(self.toughness, 0) + modifier
			print("Costs:       " + str(costDict))
			print("Powers:      " + str(powerDict))
			print("Toughnesses: " + str(toughDict))



	# Make a string of the card's attributes
	def toString(self):
		if(self.effect == None):
			return("%s\nCMC: %d\n%d/%d" % (self.name, self.cost, self.power, self.toughness))
		return("%s\nCMC: %d\n%s\n%d/%d" % (self.name, self.cost, self.effect, self.power, self.toughness))



# Generate a random card
def generateCard():
	cost = random.choice(costs)
	expectedPoints = int(np.mean(costDict.get(cost, 0)))
	print("Expected: " + str(expectedPoints))
	power = generateValue(powerDict, expectedPoints)
	toughness = generateValue(toughDict, expectedPoints)
	generatedCard = Card("Test", cost, None, power, toughness)
	return generatedCard

# Generate a value for a trait
def generateValue(traitDict, expectedPoints):
	target = expectedPoints/2
	diff = float('inf')
	fkey = int(random.triangular(0,10))
	for key,value in traitDict.items():
	    if diff > abs(target-value):
	        diff = abs(target-value)
	        fkey = key
	return fkey

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_dicts():
	save_obj(costDict, "costDict")
	save_obj(powerDict, "powerDict")
	save_obj(toughDict, "toughDict")
	print("--DICTIONARIES SAVED--")

def load_dicts():
	global costDict
	costDict = load_obj("costDict")
	global powerDict
	powerDict = load_obj("powerDict")
	global toughDict
	toughDict = load_obj("toughDict")
	print("--DICTIONARIES LOADED--")



# Main
print("Welcome to the Magic Normal Network!")
while True:
	testCard = generateCard()
	testCard.train()
