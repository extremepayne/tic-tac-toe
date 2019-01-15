#Tic-Tac-Toe_strategy.py
#Allows the user to compete agansist a computer opponent.
#Based off of Michael Dawson's example program- Tic-Tac-Toe_basic.py
#The second in a series of Tic-Tac-Toe games.
#Changes made in this edition form the exterior POV:
#The user can select a difficulty level and cannot cause errors.
#Changes from the interior POV:
#ask_yes_no() and ask_number() debugged
#computer_move() replaced with class Computer's move function
#display_instruct() updated slightly
#decide_difficulty() created
#main() updated to accomadate changes.
#features to include next time:
#add classes Player, Human and Game
#make Human and Computer inherit from Player
#make it so Game does not have to know whether it is getting a move from a Computer or Human
#update congrat_winner() to take difficulty into account
#Add multiplayer option
#add pauses from time.wait() in time module

#global constants
X = "X"
O = "O"
EMPTY = " "
TIE = "TIE"
NUM_SQUARES = 9
FIRST_MOVE = X
import random

class Computer(object):
	"""Creates a move for the computer"""
	def __init__(self, computer, human):
		self.computer = computer
		self.human = human

	def __str__(self):
		return_value = """instance of class Computer.
Atrributes:
self.computer = """
		return_value += self.computer
		return_value += "\nself.human = "
		return_value += self.human
		return return_value

	def move(self, board, difficulty):
		#detirmine difficulty
		if difficulty == "Hard":
			#Hard has extra special strategy that requires knowing who went first
			if FIRST_MOVE == self.computer:
				move = self.strategizeHard(board)
				return move
			else:
				move = self.defendHard(board)
				return move
		elif difficulty == "Medium":
			move = self.moveMedium(board)
			return move
		elif difficulty == "Easy":
			move = self.moveEasy(board)
			return move
		else:
			move = self.moveRandom(board)
			return move


	def moveMedium(self, board):
		# make a copy of the board to work with.
		board = board[:]
		#the best positions to have, in order
		BEST_MOVES = (4, 0, 2, 6, 8, 1, 3, 5, 7)

		# if computer can win, take that move
		for move in legal_moves(board):
			board[move] = self.computer
			if winner(board) == self.computer:
				return move
			#done checking this move, undo it
			board[move] = EMPTY
		#if human can win, block that move
		for move in legal_moves(board):
			board[move] = self.human
			if winner(board) == self.human:
				return move
			#done checking this move, undo it
			board[move] = EMPTY
		#Since no one can win on the next move, pick best open square
		for move in BEST_MOVES:
			if move in legal_moves(board):
				return move


	def moveRandom(self, board):
		move = None
		while move not in legal_moves(board):
			move = random.randrange(NUM_SQUARES)
		return move

	def moveEasy(self, board):
		# if computer can win, take that move
		board = board[:]
		for move in legal_moves(board):
			board[move] = self.computer
			if winner(board) == self.computer:
				return move
			#done checking this move, undo it
			board[move] = EMPTY	
		#At this point, we randomly choose a number that chooses wether to...
		number = random.randint(1,3)
		if number == 1:
			#make an informed move or...
			move = self.moveMedium(board)
			return move
		else:
			#make a random move
			move = self.moveRandom(board)
			return move


	def defendHard(self, board):
		#Just a little bit of extra defense
		# it might seem easier to put these all into compound conditions, but think how long that would be.
		if board == [self.human, EMPTY, EMPTY, EMPTY, self.computer, EMPTY, EMPTY, EMPTY, self.human]:
			return 1
		elif board == [EMPTY, EMPTY, self.human, EMPTY, self.computer, EMPTY, self.human, EMPTY, EMPTY]:
			return 1
		elif board == [EMPTY, EMPTY, EMPTY, EMPTY, self.computer, self.human, EMPTY, self.human, EMPTY]:
			return 8
		elif board == [EMPTY, EMPTY, EMPTY, EMPTY, self.computer, self.human, self.human, EMPTY, EMPTY]:
			return 8
		elif board == [EMPTY, EMPTY, self.human, EMPTY, self.computer, EMPTY, EMPTY, self.human, EMPTY]:
			return 8
		elif board == [self.human, EMPTY, EMPTY, EMPTY, self.computer, EMPTY, EMPTY, self.human, EMPTY]:
			return 6
		else:
			#At this point, there is nothing else the computer can do to prevent losses.
			move = self.moveMedium(board)
			return move


	def strategizeHard(self, board):
		#strategy for the computer
		#Try writing out the board and seeing why the assigned move might be useful.
		#There's no way I am explaining every single example.
		#All of them either lead to or create a "Double Threat"
		#For example:
		# X |   | X
		#----------
		#   | O |
		#----------
		# O |   | X
		#both moves 1 and 5 will result in X winning and O can only block one of them, so X wins
		#this is also what defendHard() is preventing.
		#If the move doen't make sense, go through and see what it would fall through to 
		#the next time. Then look there and see if the move makes sense. Some will fall 
		#through to inside moveMedium. 
		if self.computer not in board:
			return 0
		elif board == [self.computer, EMPTY, EMPTY, EMPTY, self.human, EMPTY, EMPTY, EMPTY, EMPTY]:
			return 8
		elif board == [self.computer, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, self.human]:
			return 2
		elif board == [self.computer, self.human, self.computer, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, self.human]:
			return 6
		elif board == [self.computer, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, self.human, EMPTY, EMPTY]:
			return 8
		elif board == [self.computer, EMPTY, self.human, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]:
			return 8
		elif board == [self.computer, EMPTY, EMPTY, self.human, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]:
			return 2
		elif board == [self.computer, self.human, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]:
			return 6
		elif board == [self.computer, EMPTY, EMPTY, EMPTY, EMPTY, self.human, EMPTY, EMPTY, EMPTY]:
			return 6
		elif board == [self.computer, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, self.human, EMPTY]:
			return 6
		else:
			move = self.moveMedium(board)
			return move




def display_instruct(Difficulty):
	"""Display game instructions."""
	print("Welcome to Tic-Tac-Toe")
	print("Difficulty:", Difficulty)
	print("""
The board is set up like this:
	0 | 1 | 2 
	---------
	3 | 4 | 5
	---------
	6 | 7 | 8
The first player to get three in a row wins. 
Now we will begin.""")


def ask_yes_no(question):
	"""Ask for a number within a range."""
	response = input(question)
	while response not in ("y", "n"):
		#Extra feedback to user
		print("That was not either y or n.")
		response = input(question)
	return response


def ask_number(question, low, high):
	"""Ask for a number within a range"""
	#Make sure they enter a number
	error = None
	response = None
	while response not in range(low, high):
		if error == False:
			#Extra feedback to user
			print("That number was not in the range asked for.")
		try:
			response = int(input(question))
		except ValueError:
			print("That response was not a number.")
			#Don't want to tell them they didn't put in a number
			#and then tell them their number was not in the range.
			error = True
		else:
			error = False
	return response


def pieces():
	"""Detirmine who goes first"""
	go_first = ask_yes_no("Do you wish to go first? (y/n)")
	if go_first == "y":
		print("\nTake the first move, then. You'll need it.")
		human = X
		computer = O
	else:
		print("\nYour bravery will be your undoing...I will go first.")
		computer = X
		human = O
	return computer, human


def new_board():
	"""Create a new game board"""
	board = []
	for square in range(NUM_SQUARES):
		board.append(EMPTY)
	return board


def display_board(board):
	"""Display board"""
	print("\n\t", board[0], "|", board[1], "|", board[2])
	print("\t", "---------")
	print("\t", board[3], "|", board[4], "|", board[5])
	print("\t", "---------")
	print("\t", board[6], "|", board[7], "|", board[8], "\n")


def legal_moves(board):
	"""Creates a list of legal moves"""
	moves = []
	for square in range(NUM_SQUARES):
		if board[square] == EMPTY:
			moves.append(square)
	return moves


def winner(board):
	"""Detirmine the game's winner."""
	WAYS_TO_WIN = ((0, 1, 2),
		(3, 4, 5),
		(6, 7, 8), 
		(0, 3, 6),
		(1, 4, 7),
		(2, 5, 8),
		(0, 4, 8),
		(2, 4, 6))
	for row in WAYS_TO_WIN:
		if board[row[0]] == board[row[1]] == board[row[2]] != EMPTY:
			winner = board[row[0]]
			return winner
	if EMPTY not in board:
		return TIE
	return None


def human_move(board, human):
	"""Get human move"""
	legal = legal_moves(board)
	move = None
	while move not in legal:
		move = ask_number("Where will you move? (O-8):", 0, NUM_SQUARES)
		if move not in legal:
			print("That square is already occupied. Choose another one.")
	print("Fine...")
	return move

def next_turn(turn):
	"""switch turns"""
	if turn == X:
		return O
	else:
		return X

def congrat_winner(the_winner, computer, human):
	if the_winner != TIE:
		print(the_winner, "won!\n")
	else:
		print("It's a tie!")
	if the_winner == computer:
		print("As I predictded, human. I am triuphant once more!")

	elif the_winner == human:
		print("NOOOOOO! Somehow you tricked me! But never again.")

	elif the_winner == TIE:
		print("You were lucky, human, and managed to tie me. \nCelebrate today, for this is the best you will ever acheive.")

def decide_difficulty():
	"""Lets the user choose a difficulty level, or quit."""
	print("""
		Here are the difficulty options.

		0 - Quit
		1 - Random
		2 - Easy
		3 - Medium
		4 - Hard""")
	Difficulty = None
	while Difficulty not in ("Hard", "Medium", "Easy", "Random", "Quit"):
		Difficulty = input("\nWhat is your choice?")
		if Difficulty == "0":
			Difficulty = "Quit"
		elif Difficulty == "1":
			Difficulty = "Random"
		elif Difficulty == "2":
			Difficulty = "Easy"
		elif Difficulty == "3":
			Difficulty = "Medium"
		elif Difficulty == "4":
			Difficulty = "Hard"
		else:
			if Difficulty == "":
				print("Please enter a difficulty level. If you would like to quit, enter 0.")
			elif Difficulty not in ("Hard", "Medium", "Easy", "Random", "Quit"):
				print(Difficulty, "is not an option. Please choose again.")
			else:
				print("That works, too. Please enter a number next time, though.")
	return Difficulty




def main():

	Difficulty = decide_difficulty()
	while Difficulty != "Quit":
		display_instruct(Difficulty)
		computer, human = pieces()
		computer_object = Computer(computer, human)
		turn = X
		board = new_board()
		display_board(board)
		while not winner(board):
			if turn == human:
				move = human_move (board, human)
				board[move] = human
			else:
				move = computer_object.move(board, Difficulty)
				board[move] = computer
				print("I will take square number", move)
			display_board(board)
			turn = next_turn(turn)

		the_winner = winner(board)
		congrat_winner(the_winner, computer, human)
		Difficulty = decide_difficulty()


main()
input("\n\nPress the enter key to exit.")


