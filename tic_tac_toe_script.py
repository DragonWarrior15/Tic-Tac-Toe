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
	for i in range(boardSize):
		tempList=[]
		for j in range(boardSize):
			tempList.append(' ')
		board.append(tempList)

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

def getNextMove(boardPassed):
	global boardSize
	rewardMatrix=[[-100000]*boardSize]*boardSize
	
	for row in range(boardSize):
		for col in range(boardSize):
			if(boardPassed[row][col]==' '):
				boardCopy=deepcopy(boardPassed)
				boardCopy[row][col]=compChoice
				rewardMatrix[row][col]=playAhead(boardCopy, False)

	#print(rewardMatrix)
	maxRow=0
	maxCol=0
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
	returnBoard=[[' ']*boardSize]*boardSize

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

	if(playerFirst):
		playerPos=int(input("Enter Position: "))
		while(not checkValidPosition(board, playerPos)):
			playerPos=int(input("Wrong Position, Enter New Position: "))
		board[playerPos//boardSize][playerPos%boardSize]=playerChoice

	compTurn=True
	while(checkForWin(board)[0]!='Win' and checkForWin(board)[0]!='Draw'):
		printBoard(board)
		if(compTurn):
			compPos=getNextMove(board)
			#print(compPos)
			board[compPos//boardSize][compPos%boardSize]=compChoice
			compTurn=not compTurn
		else:
			playerPos=int(input("Enter Position: "))
			while(not checkValidPosition(board, playerPos)):
				playerPos=int(input("Wrong Position, Enter New Position: "))
			board[playerPos//boardSize][playerPos%boardSize]=playerChoice
			compTurn=not compTurn

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
boardSize=3
compChoice='O'
playerChoice='X'

winPoints=10
drawPoints=0
losePoints=-10
boardWeight=10

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
