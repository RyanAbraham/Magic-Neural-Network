# Ryan Abraham
# February 9, 2017
# The world's first normal network

import random
import numpy as np
import pickle
import names

costs = [0] * 2 + [1] * 20 + [2] * 30 + [3] * 20 + [4] * 15 + [5] * 10 + [6] * 5 + [7] * 2 + [8] * 1
costDict = {}
powerDict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
toughDict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
keywordDict = {"Deathtouch": 0, "Flying": 0, "Lifelink": 0, "Menace": 0, "Trample": 0, "Defender": 0, None: 0}

class Card(object):
	# Constructor
	def __init__(self, name, cost, effect, power, toughness):
		if(power < 0):
			power = 0
		if(toughness < 1):
			toughness = 1
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
		totalPoints = powerDict.get(self.power, 0) + toughDict.get(self.toughness, 0) + keywordDict.get(self.effect, 0)
		print("\n" + self.toString())
		feedback = input("\nWhat do you think of this card? Too [S]trong, too [W]eak, or [G]ood?\n")
		if(feedback.lower() == "s"):
			modifier = 1
		elif(feedback.lower() == "w"):
			modifier = -1
		elif(feedback.lower() == "vs"):
			modifier = 2
		elif(feedback.lower() == "vw"):
			modifier = -2
		elif(feedback.lower() == "v"):
			save_dicts()
			updateDicts = False
		elif(feedback.lower() == "l"):
			load_dicts()
			updateDicts = False
		else:
			# The card is good, so record what made it good
			# Calculate the point value of the card by adding all the traits
			# Associate the point value with the cost of the card
			pointList = costDict.get(self.cost, [])
			pointList.append(totalPoints)
			costDict[self.cost] = pointList
			updateDicts = False
		if (updateDicts):
			# Update the point values associated with the traits used
			# Adjust the expected point value of the CMC
			mean = int(np.mean(costDict.get(self.cost, 0)))
			pointList = costDict.get(self.cost, [])
			pointList.append(mean - modifier)
			costDict[self.cost] = pointList
			# If the trait is not already in the dict, set it to 0 and then modify it
			powerDict[self.power] = powerDict.get(self.power, 0) + modifier
			toughDict[self.toughness] = toughDict.get(self.toughness, 0) + modifier
			keywordDict[self.effect] = keywordDict.get(self.effect, 0) + modifier
			print("Costs:       " + str(costDict))
			print("Powers:      " + str(powerDict))
			print("Toughnesses: " + str(toughDict))
			print("Keywords:    " + str(keywordDict))


	# Make a string of the card's attributes
	def toString(self):
		if(self.effect == None):
			return("%s\nCMC: %d\n%d/%d" % (self.name, self.cost, self.power, self.toughness))
		return("%s\nCMC: %d\n%s\n%d/%d" % (self.name, self.cost, self.effect, self.power, self.toughness))



# Generate a random card
def generateCard():
	cost = random.choice(costs)

	expectedPoints = int(np.mean(costDict.get(cost, 0)))
	#print("Expected: " + str(expectedPoints))

	effect = random.choice(list(keywordDict)) if random.choice((True, False)) else None
	expectedPoints -= keywordDict.get(effect, 0)

	power = generateValue(powerDict, expectedPoints, 2)
	expectedPoints -= powerDict.get(power, 0)

	toughness = generateValue(toughDict, expectedPoints, 1)

	name = names.get_full_name()

	generatedCard = Card(name, cost, effect, power, toughness)
	return generatedCard


# Generate a value for a trait
def generateValue(traitDict, expectedPoints, left):
	target = expectedPoints / left
	diff = float('inf')
	for key,value in traitDict.items():
	    if diff > abs(target-value):
	        diff = abs(target-value)
	        fkey = key
	return int(random.triangular(fkey-3, fkey+3))


def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def save_dicts():
	save_obj(costDict, "costs")
	save_obj(powerDict, "powers")
	save_obj(toughDict, "toughs")
	save_obj(keywordDict, "keywords")
	print("--DICTIONARIES SAVED--")


def load_dicts():
	global costDict
	costDict = load_obj("costs")
	global powerDict
	powerDict = load_obj("powers")
	global toughDict
	toughDict = load_obj("toughs")
	global keywordDict
	keywordDict = load_obj("keywords")
	print("--DICTIONARIES LOADED--")



# Main
print("Welcome to the Magic Normal Network!")
#triDict = {-1: 0,0: 0,1: 0}
#for x in range(0,1000):
	#num = int(random.triangular(1,3))
	#triDict[num] = triDict.get(num, 0) + 1
#print(triDict)

while True:
	testCard = generateCard()
	testCard.train()
#load_dicts()
#for x in range(0,10):
#	testCard = generateCard()
#	print("\n" + testCard.toString())