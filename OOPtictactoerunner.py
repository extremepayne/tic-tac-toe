#OOPTic-Tac-Toe.py
#Allows the user to simulate games, agansist a computer or human opponent. Or even two comuters battling!
#Based off of Michael Dawson's example program- Tic-Tac-Toe_basic.py
#The third in a series of Tic-Tac-Toe games.
#Changes made in this edition form the exterior POV:
#human v. human and computer v. computer games are now possible.
#Changes from the interior POV:
#Player class genralized to represent any kind of player
#features to work on (maybe in next version):
#GUI enabled
#update congrat_winner() to take difficulty into account
#add pauses from time.wait() in time module

#global constants
X = "X"
O = "O"
EMPTY = " "
TIE = "TIE"
NUM_SQUARES = 9
FIRST_MOVE = X
import random, time

class Player(object):
	"""Gets a move for the player"""
	def __init__(self, identity, player_piece, opponent_piece, difficulty):
		self.identity = identity
		self.player_piece = player_piece
		self.opponent_piece = opponent_piece
		self.difficulty = difficulty

	def __str__(self):
		return_value = """instance of class Player.
Atrributes:
self.player_piece = """
		return_value += self.player_piece
		return_value += "\nself.opponent_piece = "
		return_value += self.opponent_piece
		return_value += "\nself.identity = "
		return_value += self.identity
		return_value += "\nself.difficulty = "
		return_value += str(self.difficulty)
		return return_value

	def move(self, board):
		if self.identity == "computer":	
			time.sleep(1.5)
			#detirmine difficulty
			if self.difficulty == "Hard":
				#Hard has extra special strategy that requires knowing who went first
				if FIRST_MOVE == self.player_piece:
					move = self.strategizeHard(board)
					return move
				else:
					move = self.defendHard(board)
					return move
			elif self.difficulty == "Medium":
				move = self.moveMedium(board)
				return move
			elif self.difficulty == "Easy":
				move = self.moveEasy(board)
				return move
			else:
				move = self.moveRandom(board)
				return move
		elif self.identity == "human":
			move = self.human_move(board)
			return move


	def human_move(self, board):
		"""Get human move"""
		legal = legal_moves(board)
		move = None
		while move not in legal:
			move = ask_number("Where will you move? (O-8):", 0, NUM_SQUARES)
			if move not in legal:
				print("That square is already occupied. Choose another one.")
		print("Good choice!")
		return move
		

	def moveMedium(self, board):
		# make a copy of the board to work with.
		board = board[:]
		#the best positions to have, in order
		BEST_MOVES = (4, 0, 2, 6, 8, 1, 3, 5, 7)

		# if computer can win, take that move
		for move in legal_moves(board):
			board[move] = self.player_piece
			if winner(board) == self.player_piece:
				return move
			#done checking this move, undo it
			board[move] = EMPTY
		#if human can win, block that move
		for move in legal_moves(board):
			board[move] = self.opponent_piece
			if winner(board) == self.opponent_piece:
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
			board[move] = self.player_piece
			if winner(board) == self.player_piece:
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
		if board == [self.opponent_piece, EMPTY, EMPTY, EMPTY, self.player_piece, EMPTY, EMPTY, EMPTY, self.opponent_piece]:
			return 1
		elif board == [EMPTY, EMPTY, self.opponent_piece, EMPTY, self.player_piece, EMPTY, self.opponent_piece, EMPTY, EMPTY]:
			return 1
		elif board == [EMPTY, EMPTY, EMPTY, EMPTY, self.player_piece, self.opponent_piece, EMPTY, self.opponent_piece, EMPTY]:
			return 8
		elif board == [EMPTY, EMPTY, EMPTY, EMPTY, self.player_piece, self.opponent_piece, self.opponent_piece, EMPTY, EMPTY]:
			return 8
		elif board == [EMPTY, EMPTY, self.opponent_piece, EMPTY, self.player_piece, EMPTY, EMPTY, self.opponent_piece, EMPTY]:
			return 8
		elif board == [self.opponent_piece, EMPTY, EMPTY, EMPTY, self.player_piece, EMPTY, EMPTY, self.opponent_piece, EMPTY]:
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
		if self.player_piece not in board:
			return 0
		elif board == [self.player_piece, EMPTY, EMPTY, EMPTY, self.opponent_piece, EMPTY, EMPTY, EMPTY, EMPTY]:
			return 8
		elif board == [self.player_piece, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, self.opponent_piece]:
			return 2
		elif board == [self.player_piece, self.opponent_piece, self.player_piece, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, self.opponent_piece]:
			return 6
		elif board == [self.player_piece, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, self.opponent_piece, EMPTY, EMPTY]:
			return 8
		elif board == [self.player_piece, EMPTY, self.opponent_piece, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]:
			return 8
		elif board == [self.player_piece, EMPTY, EMPTY, self.opponent_piece, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]:
			return 2
		elif board == [self.player_piece, self.opponent_piece, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]:
			return 6
		elif board == [self.player_piece, EMPTY, EMPTY, EMPTY, EMPTY, self.opponent_piece, EMPTY, EMPTY, EMPTY]:
			return 6
		elif board == [self.player_piece, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, self.opponent_piece, EMPTY]:
			return 6
		else:
			move = self.moveMedium(board)
			return move



#Update to print more detailed info concerning difficulty level.
def display_instruct(player1_identity, player2_identity):
	"""Display game instructions."""
	print("\n\nWelcome to Tic-Tac-Toe")
	time.sleep(1.5)
	print("As player1,", player1_identity)
	time.sleep(1.7)
	print("As player2,", player2_identity)
	time.sleep(1.7)
	print("The board is set up like this:")
	time.sleep(1.7)
	print("""
	0 | 1 | 2 
	---------
	3 | 4 | 5
	---------
	6 | 7 | 8""")
	time.sleep(4.9)
	print("The first player to get three in a row wins. \nNow we will begin.")
	time.sleep(3.8)


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


#debug
def players_identities():
	"""Detirmine who goes first"""
	player1_identity = ask_yes_no("Will player1 (who goes first) be a human or computer?(y=human, n=computer)")
	player2_identity = ask_yes_no("Will player2 (who goes second) be a human or computer?(y=human, n=computer)")
	if player1_identity == "y":
		player1_identity = "human"
	else:
		player1_identity = "computer"
	if player2_identity == "y":
		player2_identity = "human"
	else:
		player2_identity = "computer"
	return player1_identity, player2_identity


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



def next_turn(turn):
	"""switch turns"""
	if turn == X:
		return O
	else:
		return X

#debug
def congrat_winner(the_winner, player1_piece, player2_piece):
	if the_winner != TIE:
		print(the_winner, "won!\n")
	else:
		print("It's a tie!")
	if the_winner == player1_piece:
		print("Congratulations, player1!")

	elif the_winner == player2_piece:
		print("Congratulations, player2")

#debug
def decide_difficulty(player_used):
	"""Lets the user choose a difficulty level for a player"""
	print("Here are the difficulty options for", end = " ")
	print(player_used)
	print("""
		1-random
		2-easy
		3-medium
		4-hard
		""")
	Difficulty = None
	while Difficulty not in ("Hard", "Medium", "Easy", "Random"):
		Difficulty = input("\nWhat is your choice?")
		if Difficulty == "1":
			Difficulty = "Random"
			print(player_used, "has been set to", Difficulty)
		elif Difficulty == "2":
			Difficulty = "Easy"
			print(player_used, "has been set to", Difficulty)
		elif Difficulty == "3":
			Difficulty = "Medium"
			print(player_used, "has been set to", Difficulty)
		elif Difficulty == "4":
			Difficulty = "Hard"
			print(player_used, "has been set to", Difficulty)
		else:
			if Difficulty == "":
				print("Please enter a difficulty level.")
			else:
				print(Difficulty, "is not an option. Please choose again, using the number")
		time.sleep(2.5)

	return Difficulty

def play_again():
	answer = ask_yes_no("Do you wish to play again?")
	if answer == "y":
		return True
	else:
		return False

#need to debug
def main():

	play = None
	while play != False:
		#Are the players computer or human?
		player1_identity, player2_identity = players_identities()
		#If they are a computer, set a difficulty level
		if player1_identity == "computer":
			player1_difficulty = decide_difficulty("player1")
		else:
			player1_difficulty = None
		if player2_identity == "computer":
			player2_difficulty = decide_difficulty("player2")
		else:
			player2_difficulty = None
		#Show them how it's done
		display_instruct(player1_identity, player2_identity)
		#initialize peices
		player1_piece = "X"
		player2_piece = "O"
		#initialize player objects
		player1 = Player(player1_identity, player1_piece, player2_piece, player1_difficulty)
		player2 = Player(player2_identity, player2_piece, player1_piece, player2_difficulty)
		#X goes first
		turn = X
		#You need a clean board to play on
		board = new_board()
		display_board(board)
		#begin playing
		while not winner(board):
			if turn == player1_piece:
				move = player1.move(board)
				board[move] = player1_piece
			else:
				move = player2.move(board)
				board[move] = player2_piece
			display_board(board)
			turn = next_turn(turn)
		
		#finish up
		the_winner = winner(board)
		congrat_winner(the_winner, player1_piece, player2_piece)
		#do they want to play again?
		play = play_again()

#Start the game
main()
#once main() ends, the player is done playing
input("\n\nPress the enter key to exit.")
#The End! :)

