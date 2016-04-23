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
	global boardSize
	global board
	board=[[' ']*boardSize for i in range(boardSize)]

def checkBoardEmpty(boardPassed):
	global boardSize
	for row in range(boardSize):
		for col in range(boardSize):
			if(boardPassed[row][col]==' '):
				return(True)
	return(False)

def checkNoOfMoves(boardPassed):
	global compChoice
	global playerChoice
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
	global boardSize
	global rewardDict
	winString=checkForWin(boardPassed)
	boardMoves=checkNoOfMoves(boardPassed)
	if(winString[0]=='Win' and winString[2]==compChoice):
		return(boardWeight*(boardSize+1-boardMoves[0])*winPoints)
	elif(winString[0]=='Win' and winString[2]==playerChoice):
		return(boardWeight*(boardSize+1-boardMoves[1])*losePoints)
	elif(winString[0]=='Draw'):
		return(drawPoints)
	else:
		reward=0
		for row in range(boardSize):
			for col in range(boardSize):
				if(boardPassed[row][col]==' '):
					#boardCopy=deepcopy(boardPassed)
					boardPassed[row][col]=compChoice if(compTurn) else playerChoice
					rewardDictKey=boardToKey(boardPassed, not compTurn)
					if(not rewardDictKey in rewardDict):
						rewardDict[rewardDictKey]=playAhead(boardPassed, not compTurn)
					reward+=rewardDict[rewardDictKey]
					boardPassed[row][col]=' '
		
		return(reward)

def getNextMove_NewellSimon(boardPassed):

	global boardSize
	global compChoice
	global playerChoice
	global compFirstMove
	global playerFirst

	boardCopy=deepcopy(boardPassed)

	print('0', boardCopy, playerFirst)
	# 0 play the center if comp has the first move
	if(compFirstMove and not(playerFirst) and boardSize%2!=0 and boardCopy[boardSize//2][boardSize//2]==' '):
		compFirstMove=not compFirstMove
		return((boardSize//2)*boardSize+(boardSize//2))

	print('1', boardCopy)
	# 1 check if the computer can win by row, column or diagonal
	for row in range(boardSize):
		for col in range(boardSize):
			if(boardCopy[row][col]==' '):
				boardCopy[row][col]=compChoice
				winCheckResult=['', '', '']
				winCheckResult=checkForWin(boardCopy)
				boardCopy[row][col]=' '

				if(winCheckResult[0]=='Win' and winCheckResult[2]==compChoice): return(row*boardSize+col)

	print('2', boardCopy)
	# 2 comp has not won, check if player can win and block that area
	for row in range(boardSize):
		for col in range(boardSize):
			if(boardCopy[row][col]==' '):
				boardCopy[row][col]=playerChoice
				winCheckResult=['', '', '']
				winCheckResult=checkForWin(boardCopy)
				boardCopy[row][col]=' '

				if(winCheckResult[0]=='Win' and winCheckResult[2]==playerChoice): return(row*boardSize+col)

	print('3', boardCopy)
	# 3 create a fork for the comp
	for row in range(boardSize):
		for col in range(boardSize):
			if(boardCopy[row][col]==' '):
				boardCopy[row][col]=compChoice

				winTypeList=[0, 0, 0]

				for i in range(boardSize):
					for j in range(boardSize):
						if(boardCopy[i][j]==' '):
							boardCopy[i][j]=compChoice
							winCheckResult=['', '', '']
							winCheckResult=checkForWin(boardCopy)
							if(winCheckResult[0]=='Win' and winCheckResult[0]==compChoice):
								if(winCheckResult[1]=='Row'): winTypeList[0]+=1
								elif(winCheckResult[1]=='Col'): winTypeList[1]+=1
								elif(winCheckResult[2]=='Diag'): winTypeList[2]+=1

							if((winTypeList[0]>=1 and winTypeList[1]>=1) or (winTypeList[1]>=1 and winTypeList[2]>=1) or (winTypeList[0]>=1 and winTypeList[2]>=1)):
								return(row*boardSize+col)
							
							boardCopy[i][j]=' '

				boardCopy[row][col]=' '

	print('4', boardCopy)
	# 4 block the opponents fork
	for row in range(boardSize):
		for col in range(boardSize):
			if(boardCopy[row][col]==' '):
				boardCopy[row][col]=playerChoice

				winTypeList=[0, 0, 0]

				for i in range(boardSize):
					for j in range(boardSize):
						if(boardCopy[i][j]==' '):
							boardCopy[i][j]=playerChoice
							winCheckResult=['', '', '']
							winCheckResult=checkForWin(boardCopy)
							if(winCheckResult[0]=='Win' and winCheckResult[0]==playerChoice):
								if(winCheckResult[1]=='Row'): winTypeList[0]+=1
								elif(winCheckResult[1]=='Col'): winTypeList[1]+=1
								elif(winCheckResult[2]=='Diag'): winTypeList[2]+=1

							if((winTypeList[0]>=1 and winTypeList[1]>=1) or (winTypeList[1]>=1 and winTypeList[2]>=1) or (winTypeList[0]>=1 and winTypeList[2]>=1)):
								return(row*boardSize+col)
							
							boardCopy[i][j]=' '

				boardCopy[row][col]=' '

	print('5', boardCopy)
	# 5 play the center, best for first move of the comp, meaning less for even sized boards
	if(boardCopy[boardSize//2][boardSize//2]==' ' and boardSize%2!=0): return((boardSize//2)*boardSize+(boardSize//2))

	print('6', boardCopy)
	# 6 opposite corner, check if player is in some corner, play the opposite corner of that
	if(boardCopy[0][0]==playerChoice and boardCopy[-1][-1]==' '): return((boardSize-1)*boardSize+(boardSize-1))
	elif(boardCopy[0][-1]==playerChoice and boardCopy[-1][0]==' '): return((boardSize-1)*boardSize)
	elif(boardCopy[-1][0]==playerChoice and boardCopy[0][-1]==' '): return(boardSize-1)
	elif(boardCopy[-1][-1]==playerChoice and boardCopy[0][0]==' '): return(0)

	print('7', boardCopy)
	# 7 empty corner, check if any corner is empty and make a move there
	if(boardCopy[0][0]==' '): return(0)
	elif(boardCopy[0][-1]==' '): return(boardSize-1)
	elif(boardCopy[-1][0]==' '): return((boardSize-1)*boardSize)
	elif(boardCopy[-1][-1]==' '): return((boardSize-1)*boardSize+(boardSize-1))

	print('8', boardCopy)
	# 8 empty side.. dont know how this strategy will be modified for boards of size more than 3
	for i in range(1, boardSize-1):
		if(boardCopy[0][i]==' '): return(i)	#top row
		elif(boardCopy[-1][i]==' '): return((boardSize-1)*boardSize+i)	#bottom row
		elif(boardCopy[i][0]==' '): return(i*boardCopy)	#left column
		elif(boardCopy[i][boardSize-1]==' '): return(i*boardCopy+(boardSize-1))


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
	initializeBoard()
	printBoardPositions()
	#python input not supported in sublime text console
	playerChoice=input("Choose X or O, X plays first: ")
	if(playerChoice!='X' and playerChoice!='O'):
		print("Bad Player!, restart.") 
	else:
		compChoice='O' if playerChoice=='X' else 'X'
		playerFirst=True if playerChoice=='X' else False

	global board
	global boardSize
	global compFirstMove
	global playerFirst

	if(playerFirst):
		playerPos=int(input("Enter Position: "))
		while(not checkValidPosition(board, playerPos)):
			playerPos=int(input("Wrong Position, Enter New Position: "))
		board[playerPos//boardSize][playerPos%boardSize]=playerChoice

	compTurn=True
	while(checkForWin(board)[0]!='Win' and checkForWin(board)[0]!='Draw'):
		if(not(compFirstMove and not(playerFirst))): printBoard(board)
		if(compTurn):
			compPos=getNextMove_NewellSimon(board)
			board[compPos//boardSize][compPos%boardSize]=compChoice
			compTurn=not compTurn
		else:
			playerPos=int(input("Enter Position: "))
			while(not checkValidPosition(board, playerPos)):
				playerPos=int(input("Wrong Position, Enter New Position: "))
			board[playerPos//boardSize][playerPos%boardSize]=playerChoice
			compTurn=not compTurn

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
board=[]
playerFirst=False
compFirstMove=True
boardSize=3
compChoice='O'
playerChoice='X'

winPoints=10
drawPoints=5
losePoints=-10
boardWeight=1

rewardDict={}

#main code begins here
if(boardSize>10):
	print("Both of us don't have time to play such a big game!")
else:
	wantToPlay='Y'
	while(wantToPlay=='Y'):
		board=[]
		boardMain()
		wantToPlay=input('Play again? Y for yes : ')

#printBoard(boardToPrint)
