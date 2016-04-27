'''
Newell Simon Strategy

A player can play a perfect game of Tic-tac-toe (to win or, at least, draw) if they choose the first available move from the following list, each turn, as used in Newell and Simon's 1972 tic-tac-toe program.[6]

Win: If the player has two in a row, they can place a third to get three in a row.
Block: If the opponent has two in a row, the player must play the third themselves to block the opponent.
Fork: Create an opportunity where the player has two threats to win (two non-blocked lines of 2).
Blocking an opponent's fork:
Option 1: The player should create two in a row to force the opponent into defending, as long as it doesn't result in them creating a fork. For example, if "X" has a corner, "O" has the center, and "X" has the opposite corner as well, "O" must not play a corner in order to win. (Playing a corner in this scenario creates a fork for "X" to win.)
Option 2: If there is a configuration where the opponent can fork, the player should block that fork.
Center: A player marks the center. (If it is the first move of the game, playing on a corner gives "O" more opportunities to make a mistake and may therefore be the better choice; however, it makes no difference between perfect players.)
Opposite corner: If the opponent is in the corner, the player plays the opposite corner.
Empty corner: The player plays in a corner square.
Empty side: The player plays in a middle square on any of the 4 sides.
'''
from copy import deepcopy
import random

def printBoard(boardToPrint):
	print()
	global boardSize
	for i in range(0, boardSize):
		stringToPrint='| '
		for j in range(0, boardSize-1):
			stringToPrint+=str(boardToPrint[i][j])+' | '
		stringToPrint+=str(boardToPrint[i][-1])+' |'
		print(stringToPrint)
	print()

def checkValidPosition(boardPassed, num):
	if(boardPassed[num//boardSize][num%boardSize]!=' '):
		return(False)
	else:
		return(True)

def printBoardPositions():
	boardPositions=[]
	global boardSize
	tempInt=0
	for i in range(boardSize):
		tempList=[]
		for j in range(boardSize):
			if(tempInt<10):
				tempList.append('0'+str(tempInt))
			else:
				tempList.append(str(tempInt))
			tempInt+=1
		boardPositions.append(tempList)

	printBoard(boardPositions)

def initializeBoard():
	global boardSize, board
	board=[[' ']*boardSize for i in range(boardSize)]

def checkBoardEmpty(boardPassed):
	global boardSize
	for row in range(boardSize):
		for col in range(boardSize):
			if(boardPassed[row][col]==' '):
				return(True)
	return(False)

def checkNoOfMoves(boardPassed):
	global compChoice, playerChoice
	returnValueComp=0
	returnValuePlayer=0
	for i in range(boardSize):
		for j in range(boardSize):
			if(boardPassed[i][j]==compChoice):
				returnValueComp+=1
			if(boardPassed[i][j]==playerChoice):
				returnValuePlayer+=1

	return([returnValueComp, returnValuePlayer])

def checkForWin(boardPassed):
	global boardSize
	#rows check
	for row in range(boardSize):
		rowWin=True
		firstElement=boardPassed[row][0]
		for j in range(1, boardSize):
			if(boardPassed[row][j]!=firstElement or boardPassed[row][j]==' '):
				rowWin=False
				break
		if(rowWin):
			return('Win', 'Row', firstElement)
	#columns check
	for col in range(boardSize):
		colWin=True
		firstElement=boardPassed[0][col]
		for j in range(1, boardSize):
			if(boardPassed[j][col]!=firstElement or boardPassed[j][col]==' '):
				colWin=False
				break
		if(colWin):
			return('Win', 'Col', firstElement)
	#main diagonals check
	firstElement=boardPassed[0][0]
	diagWin=True
	for row in range(1, boardSize):
		if(boardPassed[row][row]!=firstElement or boardPassed[row][row]==' '):
			diagWin=False
			break
	if(diagWin):
		return('Win', 'Diag', firstElement)
	diagWin=True
	firstElement=boardPassed[0][-1]
	for row in range(1, boardSize):
		if(boardPassed[row][boardSize-1-row]!=firstElement or boardPassed[row][boardSize-1-row]==' '):
			diagWin=False
			break
	if(diagWin):
		return('Win', 'Diag', firstElement)


	#draw check
	if(checkBoardEmpty(boardPassed)):
		return('Play', '', '')
	else:
		return('Draw', '', '')

def boardToKey(boardPassed, compTurn):
	global boardSize
	returnStr=''
	for i in range(boardSize):
		for j in range(boardSize):
			returnStr+=boardPassed[i][j]
	returnStr+=compChoice if(compTurn) else playerChoice

	return(returnStr)

def playAhead(boardPassed, compTurn):
	#uses the minimax algorithm
	global boardSize, rewardDict
	winString=checkForWin(boardPassed)
	boardMoves=checkNoOfMoves(boardPassed)
	if(winString[0]=='Win' and winString[2]==compChoice):
		return(winPoints-boardMoves[0])
	elif(winString[0]=='Win' and winString[2]==playerChoice):
		return(boardMoves[1]-losePoints)
	elif(winString[0]=='Draw'):
		return(drawPoints)
	else:
		reward=0
		rewardMatrix=[[0]*boardSize for i in range(boardSize)]
		for row in range(boardSize):
			for col in range(boardSize):
				if(boardPassed[row][col]==' '):
					#boardCopy=deepcopy(boardPassed)
					boardPassed[row][col]=compChoice if(compTurn) else playerChoice
					rewardDictKey=boardToKey(boardPassed, not compTurn)
					if(not rewardDictKey in rewardDict):
						rewardDict[rewardDictKey]=playAhead(boardPassed, not compTurn)
					#reward+=rewardDict[rewardDictKey]
					rewardMatrix[row][col]=rewardDict[rewardDictKey]
					boardPassed[row][col]=' '
		
		reward=-100001 if(compTurn) else 100001
		for row in range(boardSize):
			for col in range(boardSize):
				if(compTurn):
					if(rewardMatrix[row][col]>reward and boardPassed[row][col]==' '):
						reward=rewardMatrix[row][col]
				else:
					if(rewardMatrix[row][col]<reward and boardPassed[row][col]==' '):
						reward=rewardMatrix[row][col]

		return(reward)

def forkPosition(boardPassed, moveChoice):
	boardCopy=deepcopy(boardPassed)
	for row in range(boardSize):
		for col in range(boardSize):
			if(boardCopy[row][col]==' '):
				boardCopy[row][col]=moveChoice

				winTypeList=[0, 0, 0]

				for i in range(boardSize):
					for j in range(boardSize):
						if(boardCopy[i][j]==' '):
							boardCopy[i][j]=moveChoice
							winCheckResult=['', '', '']
							winCheckResult=checkForWin(boardCopy)
							if(winCheckResult[0]=='Win' and winCheckResult[2]==moveChoice):
								if(winCheckResult[1]=='Row'): winTypeList[0]+=1
								elif(winCheckResult[1]=='Col'): winTypeList[1]+=1
								elif(winCheckResult[2]=='Diag'): winTypeList[2]+=1

							if((winTypeList[0]>=1 and winTypeList[1]>=1) or (winTypeList[1]>=1 and winTypeList[2]>=1) or (winTypeList[0]>=1 and winTypeList[2]>=1)):
								return(row*boardSize+col)
							
							boardCopy[i][j]=' '

				boardCopy[row][col]=' '

	return(-1)

def getNextMove_NewellSimon(boardPassed):

	global boardSize, compChoice, playerChoice, compFirstMove, playerFirst, firstTimeXCorner, moveNo

	boardCopy=deepcopy(boardPassed)

	#print('-2', boardCopy)
	#-2 if comp gets to play first, play a corner as its the best move
	if(moveNo==0):
		return(0)

	#print('-1', boardCopy)
	#-1 If X plays a corner and O has played the center, O should play a side middle then
	if(checkNoOfMoves(boardPassed)==[1,2]):
		XCorner=0
		if((boardPassed[0][-1]==playerChoice and boardPassed[-1][0]==playerChoice) or (boardPassed[0][0]==playerChoice and boardPassed[-1][-1]==playerChoice)):
			if(boardCopy[boardSize//2][boardSize%2]==compChoice):
				#empty side.. dont know how this strategy will be modified for boards of size more than 3
				for i in range(1, boardSize-1):
					if(boardCopy[0][i]==' '): return(i)	#top row
					elif(boardCopy[-1][i]==' '): return((boardSize-1)*boardSize+i)	#bottom row
					elif(boardCopy[i][0]==' '): return(i*boardSize)	#left column
					elif(boardCopy[i][boardSize-1]==' '): return(i*boardSize+(boardSize-1))	

	
	#print('0', boardCopy)
	# 0 play the center if comp has the first move
	if(compFirstMove and not(playerFirst) and boardSize%2!=0 and boardCopy[boardSize//2][boardSize//2]==' '):
		compFirstMove=not compFirstMove
		return((boardSize//2)*boardSize+(boardSize//2))

	#print('1', boardCopy)
	# 1 check if the computer can win by row, column or diagonal
	for row in range(boardSize):
		for col in range(boardSize):
			if(boardCopy[row][col]==' '):
				boardCopy[row][col]=compChoice
				winCheckResult=['', '', '']
				winCheckResult=checkForWin(boardCopy)
				boardCopy[row][col]=' '

				if(winCheckResult[0]=='Win' and winCheckResult[2]==compChoice): return(row*boardSize+col)

	#print('2', boardCopy)
	# 2 comp has not won, check if player can win and block that area
	for row in range(boardSize):
		for col in range(boardSize):
			if(boardCopy[row][col]==' '):
				boardCopy[row][col]=playerChoice
				winCheckResult=['', '', '']
				winCheckResult=checkForWin(boardCopy)
				boardCopy[row][col]=' '

				if(winCheckResult[0]=='Win' and winCheckResult[2]==playerChoice): return(row*boardSize+col)

	#print('3', boardCopy)
	# 3 create a fork for the comp
	forkResult=forkPosition(boardCopy, compChoice)
	if(forkResult!=-1): return(forkResult)

	#print('4', boardCopy)
	# 4 block the opponents fork
	forkResult=forkPosition(boardCopy, playerChoice)
	if(forkResult!=-1): return(forkResult)

	#print('5', boardCopy)
	# 5 play the center, meaningless for even sized boards
	if(boardCopy[boardSize//2][boardSize//2]==' ' and boardSize%2!=0): return((boardSize//2)*boardSize+(boardSize//2))

	#print('6', boardCopy)
	# 6 opposite corner, check if player is in some corner, play the opposite corner of that
	if(boardCopy[0][0]==playerChoice and boardCopy[-1][-1]==' '): return((boardSize-1)*boardSize+(boardSize-1))
	elif(boardCopy[0][-1]==playerChoice and boardCopy[-1][0]==' '): return((boardSize-1)*boardSize)
	elif(boardCopy[-1][0]==playerChoice and boardCopy[0][-1]==' '): return(boardSize-1)
	elif(boardCopy[-1][-1]==playerChoice and boardCopy[0][0]==' '): return(0)

	#print('7', boardCopy)
	# 7 empty corner, check if any corner is empty and make a move there
	if(boardCopy[0][0]==' '): return(0)
	elif(boardCopy[0][-1]==' '): return(boardSize-1)
	elif(boardCopy[-1][0]==' '): return((boardSize-1)*boardSize)
	elif(boardCopy[-1][-1]==' '): return((boardSize-1)*boardSize+(boardSize-1))

	#print('8', boardCopy)
	# 8 empty side.. dont know how this strategy will be modified for boards of size more than 3
	for i in range(1, boardSize-1):
		if(boardCopy[0][i]==' '): return(i)	#top row
		elif(boardCopy[-1][i]==' '): return((boardSize-1)*boardSize+i)	#bottom row
		elif(boardCopy[i][0]==' '): return(i*boardSize)	#left column
		elif(boardCopy[i][boardSize-1]==' '): return(i*boardSize+(boardSize-1))

	#print('9', boardCopy)
	# 9 return any empty cell
	for row in range(boardSize):
		for col in range(boardSize):
			if(boardCopy[row][col]==' '):
				return(row*boardSize+col)


def getNextMove_MiniMax(boardPassed):
	global boardSize
	rewardMatrix=[[-100000]*boardSize for i in range(boardSize)]
	
	for row in range(boardSize):
		for col in range(boardSize):
			if(boardPassed[row][col]==' '):
				boardPassed[row][col]=compChoice
				rewardMatrix[row][col]=playAhead(boardPassed, False)
				boardPassed[row][col]=' '

	#print(rewardMatrix)
	maxRow=-1
	maxCol=-1
	maxReward=-100001
	for i in range(boardSize):
		for j in range(boardSize):
			if(rewardMatrix[i][j]>maxReward and boardPassed[i][j]==' '):
				maxReward=rewardMatrix[i][j]
				maxRow=i
				maxCol=j

	#print(rewardMatrix)
	return(maxRow*boardSize+maxCol)

def qLearning():
	global gamesToPlay, learningRate, boardStateDict, playerChoice, compChoice, moveNo
	#initialize game boards
	boardStateDict={}
	explorationRate=1	#switch exploration rate to 0 after switchE% of the games
	learningRate=0.5
	gamesToPlay=100000
	switchE=0.

	winReward=1
	loseReward=-1
	drawReward=0

	noOfGamesWon=0
	noOfGamesDrew=0
	noOfGamesLost=0

	for noOfGames in range(gamesToPlay):
		moveNo=0
		if(noOfGames!=0 and noOfGames%1000==0):
			print(str(noOfGames)+' Won:'+str(noOfGamesWon)+' Lost:'+str(noOfGamesLost)+' Drew:'+str(noOfGamesDrew))
			noOfGamesWon=0
			noOfGamesDrew=0
			noOfGamesLost=0

		if(noOfGames>switchE*gamesToPlay): exploration=0

		turnFirst=random.randint(0,1)
		#turnFirst decides who plays first, here the comp is a good player and the player is the learner
		playerChoice='X' if(turnFirst==1) else 'O'
		compChoice='X' if(turnFirst==0) else 'O'
		board=[[' ']*boardSize for i in range(boardSize)]
		
		if(turnFirst==0):
			boardPos=getNextMove_NewellSimon(board)
			board[boardPos//boardSize][boardPos%boardSize]=compChoice
			moveNo+=1
		playerTurn=False

		while(checkForWin(board)[0]=='Play'):
			playerTurn=not playerTurn
			if(not playerTurn):
				boardPos=getNextMove_MiniMax(board)
				board[boardPos//boardSize][boardPos%boardSize]=compChoice
				moveNo+=1
			else:
				boardKey=boardToKey(board, playerChoice)
				if(not boardKey in boardStateDict):
					boardStateDict[boardKey]=[0]*(boardSize*boardSize)
				boardActionList=boardStateDict[boardKey]
				boardMaxReward=[i for i in range(len(boardActionList)) if(board[i//boardSize][i%boardSize]==' ')]
				if(explorationRate==0):
					boardMaxReward=[i for i in boardMaxReward if(boardStateDict[boardKey][i]==max([boardStateDict[boardKey][i] for i in boardMaxReward]))]
					if(len(boardMaxReward)>1): boardPos=boardMaxReward[random.randint(0, len(boardMaxReward)-1)]
					else: boardPos=boardMaxReward[0]
				else:
					if(len(boardMaxReward)>1): boardPos=boardMaxReward[random.randint(0, len(boardMaxReward)-1)]
					else: boardPos=boardMaxReward[0]
				
				board[boardPos//boardSize][boardPos%boardSize]=playerChoice
				moveNo+=1

			winCheckResult=checkForWin(board)

			if(winCheckResult[0]=='Win' and winCheckResult[2]==playerChoice): 
				reward=1
				noOfGamesWon+=1
				#print(playerChoice, board)
			elif(winCheckResult[0]=='Win' and winCheckResult[2]==compChoice):
				reward=-1
				noOfGamesLost+=1
			elif(winCheckResult[0]=='Draw'): 
				reward=0
				noOfGamesDrew+=1
			else:
				reward=0

			newBoardKey=boardToKey(board, playerChoice)
			if(not newBoardKey in boardStateDict):
				boardStateDict[newBoardKey]=[0]*(boardSize*boardSize)
			oldBoardKey=boardKey
			if(playerTurn):
				boardStateDict[oldBoardKey][boardPos]+=learningRate*(reward+(max(boardStateDict[newBoardKey])-boardStateDict[oldBoardKey][boardPos]))
				#print(boardStateDict[oldBoardKey])

			if(winCheckResult[0]=='Win' or winCheckResult[0]=='Draw'):
				boardStateDict[newBoardKey][boardPos]+=reward

	#print(boardStateDict)


def getNextMove_qLearning(boardPassed):
	global boardStateDict
	boardKey=boardToKey(boardPassed, compChoice)
	if(not boardKey in boardStateDict):
		boardStateDict[boardKey]=[0]*(boardSize*boardSize)
	returnList=[i for i in range(0, len(boardStateDict[boardKey])) if(boardPassed[i//boardSize][i%boardSize]==' ')]
	returnList=[i for i in returnList if(boardStateDict[boardKey][i]==(max([boardStateDict[boardKey][i] for i in returnList])))]
	if(len(returnList)==1):
		return(returnList[0])
	else:
		return(returnList[random.randint(0,len(returnList)-1)])
		

def getNextMove(boardPassed):
	global algoNumber
	if(algoNumber==0): return(getNextMove_MiniMax(boardPassed))
	elif(algoNumber==1): return(getNextMove_NewellSimon(boardPassed))
	else: return(getNextMove_qLearning(boardPassed))


def boardConverter(statePassed):
	boardSize=int(len(statePassed)**0.5)
	returnBoard=[[' ']*boardSize for i in range(boardSize)]

	for i in range(len(statePassed)):
		if(statePassed[i]==1):
			returnBoard[i//boardSize][i%boardSize]='O'
		elif(statePassed[i]==2):
			returnBoard[i//boardSize][i%boardSize]='X'
		else:
			returnBoard[i//boardSize][i%boardSize]=' '
	#print(returnBoard)
	return(returnBoard)

def boardMain():

	global board, boardSize, compFirstMove, playerFirst, moveNo

	moveNo=0
	compChoice='O'
	playerChoice='X'

	initializeBoard()
	printBoardPositions()
	#python input not supported in sublime text console
	playerChoice=input("Choose X or O, X plays first: ")
	while(playerChoice!='X' and playerChoice!='O'):
		print("Bad Player!, Select Again.")
		playerChoice=input("Choose X or O, X plays first: ")
	else:
		compChoice='O' if playerChoice=='X' else 'X'
		playerFirst=True if playerChoice=='X' else False

	if(playerFirst):
		playerPos=int(input("Enter Position: "))
		while(not checkValidPosition(board, playerPos)):
			playerPos=int(input("Wrong Position, Enter New Position: "))
		board[playerPos//boardSize][playerPos%boardSize]=playerChoice
		moveNo+=1

	compTurn=True
	while(checkForWin(board)[0]=='Play'):
		if(not(compFirstMove and not(playerFirst))): printBoard(board)
		if(compTurn):
			compPos=getNextMove(board)
			board[compPos//boardSize][compPos%boardSize]=compChoice
			compTurn=not compTurn
			moveNo+=1
		else:
			playerPos=int(input("Enter Position: "))
			while(not checkValidPosition(board, playerPos)):
				playerPos=int(input("Wrong Position, Enter New Position: "))
			board[playerPos//boardSize][playerPos%boardSize]=playerChoice
			compTurn=not compTurn
			moveNo+=1

		compFirstMove=False

	printBoard(board)
	winString=checkForWin(board)
	if(winString[0]=='Draw'): print("Match Drawn")
	elif(winString[0]=='Win'):
		if(winString[2]==compChoice):
			print("Computer Wins!")
		else:
			print("You Win!, Nice Game!")

#define global variables here
playerFirst=False
compFirstMove=True
algoNumber=2 #0 for minimax, 1 for newell-simon, 2 for qlearning
boardSize=3
compChoice='O'
playerChoice='X'

winPoints=5
drawPoints=0
losePoints=5
boardWeight=1

rewardDict={}

moveNo=0

#main code begins here
if __name__=='__main__':
	if(algoNumber==2):
		qLearning()	#run this to make the program learn the game

	if(boardSize>10):
		print("Both of us don't have time to play such a big game!, Let's Play 5x5!")
		boardSize=5
	elif(boardSize<3):
		boardSize=3
	elif(boardSize%2==0):
		#we will prefer an odd sized board as it is better playable
		boardSize-=1
	else:
		wantToPlay='Y'
		while(wantToPlay=='Y'):
			board=[]
			boardMain()
			wantToPlay=input('Play again? Y for yes : ').upper()

#printBoard(boardToPrint)
