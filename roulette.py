from random import randint
import re, time

debug=False

def spinCylinder(noOfChambers):
	print("Spinning cylinder...")
	time.sleep(.5)
	print("Done.")
	return randint(0,noOfChambers-1)

def spinRevolverOnTable(noOfPlayers):
	print("Spinning revolver on table...")
	time.sleep(.5)
	print("Done.")
	return randint(0,noOfPlayers-1)

def playGame(gameParams, players):
	# Play the game with the (remaining) players
	isFirstGo=True
	isPlayerDead=False
	
	while not isPlayerDead:
		if isFirstGo or gameParams["reSpinCylinder"]:
			chamberNo = spinCylinder(gameParams["noOfChambers"])
			activeChamberNo=0
		if isFirstGo or gameParams["reSpinRevolver"]:
			playerNo = spinRevolverOnTable(gameParams["noOfPlayers"])

		isFirstGo=False

		prompt="{}'s go. Hit enter to pull trigger".format(players[playerNo])
		if debug:
			print(prompt)
		else:
			input(prompt)
		time.sleep(.25)
		activeChamberNo = (activeChamberNo+1) % gameParams["noOfChambers"]

		if debug:
			print("Bullet in chamber {}: Active chamber (after pulling trigger): {}".format(chamberNo, activeChamberNo))

		if activeChamberNo==chamberNo:
			print("BANG!")
			print("{} is DEAD".format(players[playerNo]))
			gameParams["noOfPlayers"] = gameParams["noOfPlayers"] -1
			players.remove(players[playerNo])
			isPlayerDead=True
		else:
			print("click")
			playerNo = (playerNo+1) % (gameParams["noOfPlayers"])

def createPlayers(noOfPlayers):
	# Create <noOfPlayers> players
	players = []
	
	for playerNo in range(noOfPlayers):
		player = "Player " + str(playerNo+1)
		players.append(player)
	
	return players

def getPositiveInteger(prompt):
	isValidInput=False
	while not isValidInput:
		try:
			response=int(input(prompt))
			if response > 0:
				isValidInput=True
			else:
				print("This must be a numeric (positive integer) value. Please try again.")
		except ValueError:
			print("This must be a numeric (positive integer) value. Please try again.")
	return response

def getBoolean(prompt):
	isValidInput=False
	value=False
	while not isValidInput:
		response=input(prompt)
		if re.match("Y|y(es)?", response):
			isValidInput=True
			value=True
		elif re.match("N|n(o)?", response):
			isValidInput=True
		else:
			print("This must be a (Y)es for (N)o answer. Please try again.")
	return value

def getGameParams():
	# Get the game parameters from the console
	noOfChambers=getPositiveInteger("No. of Chambers in Cylinder: ")
	reSpinCylinder=getBoolean("Spin cylinder between pulls of trigger: ")
	isValidInput=False
	while not isValidInput:
		noOfPlayers=getPositiveInteger("No. of Players: ")
		if not reSpinCylinder and noOfPlayers > noOfChambers:
			print("No. of players cannot be greater than no. of chambers in cylinder if you choose not to spin cylinder between pulls. Please try again.")
		else :
			isValidInput=True
	reSpinRevolver=False
	if reSpinCylinder:
		reSpinRevolver=getBoolean("Spin revolver on table between pulls of trigger: ")
	return {"noOfChambers": noOfChambers, "reSpinCylinder": reSpinCylinder, "noOfPlayers":noOfPlayers, "reSpinRevolver": reSpinRevolver}

def play():
	# Main function
	print("===== russkaya ruletka =====".upper())
	print("--- Wanna take a chance? ---")

	gameParams=getGameParams()
	players=createPlayers(gameParams["noOfPlayers"])

	while gameParams["noOfPlayers"] > 1:
		playGame(gameParams, players)
		if debug:
			print("{} player(s) left: {}".format(gameParams["noOfPlayers"], players))

	print("{} is the only surviving player".format(players[0]))

if __name__ == '__main__':
	play()
