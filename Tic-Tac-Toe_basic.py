#Tic-Tac-Toe_basic.py
#Michael Dawson's Tic-Tac-Toe program
#Allows the user to compete agansist a computer opponent.

#Global Constants
X = "X"
O = "O"
EMPTY = " "
TIE = "TIE"
NUM_SQUARES = 9

def display_instruct():
	"""Display game instructions."""
	print(
		"""blah blah blah
		board set up like this:
		0 | 1 | 2 
		---------
		3 | 4 | 5
		---------
		6 | 7 | 8
		blah blah blah 
		first one to three in a row wins. 
		Lets do this""")


def ask_yes_no(question):
	"""Ask for a number within a range."""
	response = None
	while response not in ("y", "n"):
		response = input(question)
	return response


def ask_number(question, low, high):
	"""Ask for a number within a range"""
	response = None
	while response not in range(low, high):
		response = int(input(question))
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


def computer_move(board, computer, human):
	"""make computer move"""
	# make a copy of the board to work with.
	board = board[:]
	#the best positions to have, in order
	BEST_MOVES = (4, 0, 2, 6, 8, 1, 3, 5, 7)

	print("I shall take square number", end = " ")
	# if computer can win, take that move
	for move in legal_moves(board):
		board[move] = computer
		if winner(board) == computer:
			print(move)
			return move
		#done checking this move, undo it
		board[move] = EMPTY
	#if human can win, block that move
	for move in legal_moves(board):
		board[move] = human
		if winner(board) == human:
			print(move)
			return move
		#done checking this move, undo it
		board[move] = EMPTY
	#Since no one can win on the next move, pick best open square
	for move in BEST_MOVES:
		if move in legal_moves(board):
			print(move)
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
		print("You were lucky, human, and managed to tie me. /nCelebrate today, for this is the best you will ever acheive.")


def main():
	display_instruct()
	computer, human = pieces()
	turn = X
	board = new_board()
	display_board(board)

	while not winner(board):
		if turn == human:
			move = human_move (board, human)
			board[move] = human
		else:
			move = computer_move(board, computer, human)
			board[move] = computer
		display_board(board)
		turn = next_turn(turn)

	the_winner = winner(board)
	congrat_winner(the_winner, computer, human)


main()
input("\n\nPress the enter key to exit.")
