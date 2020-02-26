import copy
import timeit
from QLearner import QLearningPlayer
import random

class Game:
    """
    This class provides all features for this board game.

    """
    # class constructor
    def __init__(self, row, col):
        if row < 3 or col < 3:
            print("board too small")
        else:
            self.score = 0
            self.rewards = [0, 0]
            self.total_row = row
            self.total_col = col
            self.moves = []
            self.init_state = [['O' for _ in range(col)]] + [['_' for _ in range(col)] for _ in range(row - 2)] + [['X' for _ in range(col)]]
            self.prev_state = None
            self.board = [['O' for _ in range(col)]] + [['_' for _ in range(col)] for _ in range(row - 2)] + [['X' for _ in range(col)]]


    def can_move(self, row, col, horizontal_move, side):
        """
         This function will handle all possible cases
        :param: row, col, horizontal_move,side
        :return: True if can make a move, otherwise False
        """
        if row >= self.total_row or row < 0 or col >= self.total_col or col < 0:
            return False
        if self.board[row][col] != side:
            return False
        if side == 'X' and row == 0:
            return False
        if side == 'O' and row == self.total_row - 1:
            return False
        if col + horizontal_move < 0 or col + horizontal_move >= self.total_col:
            return False
        if self.board[row - (1 if side == 'X' else -1)][col + horizontal_move] == side:
            return False

        return True
    
    def get_available_moves(self, side):
        """
            Get next available moves givin current state.
            side: player side
        """
        moves = []
        for piece in self.get_pieces(side):
            for h_move in range(-1, 2):
                if not self.can_move(piece[0], piece[1], h_move, side):
                    continue
                # self.board[piece[0]][piece[1]] == 'X':
                moves.append(((piece[0], piece[1]), h_move))
                # else:
                    # moves.append((piece[0], piece[1] + h_move, 'O'))
                    
        return moves

    def make_move(self, row, col, horizontal_move):
        """
        This function will make the move and assigns utility scores accordingly
        :param: row,col,horizontal_move
        :return: None
        """
        self.prev_state = copy.deepcopy(self.board)
        if self.board[row][col] == 'X':
            self.board[row][col] = '_'
            if self.board[row - 1][col + horizontal_move] == 'O':
                self.score += 1
                self.rewards[0] += 20
                self.rewards[1] -= 20
            if row == 1:
                self.score += 5
                self.rewards[0] += 100
                self.rewards[1] -= 100
            self.board[row - 1][col + horizontal_move] = 'X'
        elif self.board[row][col] == 'O':
            self.board[row][col] = '_'
            if self.board[row + 1][col + horizontal_move] == 'X':
                self.score -= 1
                self.rewards[0] -= 50
                self.rewards[1] += 50
            if row == self.total_row - 2:
                self.score -= 5
                self.rewards[1] += 100
                self.rewards[0] -= 100
            self.board[row + 1][col + horizontal_move] = 'O'


    def game_finish(self, side):
        """

        :param: side
        :return: if the game is finished(True/False)
        """
        if len(self.get_pieces('X')) == 0:
            return True
        if len(self.get_pieces('O')) == 0:
            return True
        for piece in self.get_pieces(side):
            if piece[0] == (0 if side == 'X' else self.total_row - 1):
                return True

        return False

    def get_score(self, side):
        """

        :param: side
        :return: scores of each player
        """
        if side == 'X':
            return self.score
        else:
            return -self.score
        
    def get_reward(self):
        return self.rewards

    def get_pieces(self, side):
        """
           This function loops through the board and return locations of
           all piece of specified player
        """
        output = []
        for i in range(self.total_row):
            for j in range(self.total_col):
                if self.board[i][j] == side:
                    output.append((i, j))
        return output
    
    def get_state(self):
        """
        Return the 2d list numerical representation of the board
        """
        return tuple(tuple(x) for x in self.board)
    
    def get_prev_state(self):
        """
        Return the previous state of the board
        """
        return tuple(tuple(x) for x in self.prev_state)

    # print out the whole board
    def __str__(self):
        return ('\n'.join([str(row_idx) + ' ' + 
                ''.join(row) for row_idx, row in enumerate(self.board)]) + '\n  ' + 
                ''.join(map(str, list(range(self.total_col)))) + '\n')


def minimax(board, currDepth, maxTurn):
    """
    :param: board,currDepth,maxTurn
    :return: best_move, best_score

    This function will traverse all node in the search tree which has all possible cases.
    It will then choose and return the best move with best utility score. The running time of this
    function will be higher than that of alpha-beta pruning which is higher than cutting-off search.
    """
    best_move = ((0, 0), 0)
    best_score = 0

    # base case
    if currDepth == 0:
        return best_move, board.get_score('O')

    # do action -- move forward by one step
    for piece in board.get_pieces('O' if maxTurn else 'X'):
        for h_move in range(-1, 2):
            if board.can_move(piece[0], piece[1], h_move, 'O' if maxTurn else 'X'):
                copy_board = copy.deepcopy(board)
                copy_board.make_move(piece[0], piece[1], h_move)

                score = minimax(copy_board, currDepth - 1, not maxTurn)[1]

                if maxTurn:
                    if score >= best_score:
                        best_score = score
                        best_move = (piece, h_move)
                else:
                    if score <= best_score:
                        best_score = score
                        best_move = (piece, h_move)

    return best_move, best_score


def alpha_beta(board, currDepth, maxTurn, alpha, beta):

    """
    :param: board, currDepth, maxTurn, alpha, beta
    :return: best_move, value

    This function will update alpha and beta levels and prune when beta <= alpha.
    The base case here is to return the best utility score and this is also recursively
    done for each level
    """

    best_move = ((0, 0), 0)

    # base case
    if currDepth == 0:
        return best_move, board.get_score('O')

    if maxTurn:
        value = -1000
    else:
        value = 1000
    # do action -- move forward by one step
    for piece in board.get_pieces('O' if maxTurn else 'X'):
        # best_score = beta if maxTurn else alpha
        for h_move in range(-1, 2):
            if board.can_move(piece[0], piece[1], h_move, 'O' if maxTurn else 'X'):
                copy_board = copy.deepcopy(board)
                copy_board.make_move(piece[0], piece[1], h_move)

                score = alpha_beta(copy_board, currDepth - 1, not maxTurn, alpha, beta)[1]

                if maxTurn:
                    if score >= value:
                        value = score
                        best_move = (piece, h_move)
                        alpha = max(value, alpha)
                        if beta <= alpha:
                            break
                else:
                    if score <= value:
                        value = score
                        best_move = (piece, h_move)
                        beta = min(value, beta)
                        if beta <= alpha:
                            break

    return best_move, value



def cutoff_test(depth):
    """

    :param depth:
    :return: depth

    This cutoff test will cut off at certain level as for common cases
    """
    return depth <= 2


def eval(board, maxTurn):
    """

    :param: board,maxTurn
    :return: probablity of winning

     Evaluation function of Cuttingoff. This function calculates
     probablity of winning for each player
    """
    temp_locX = board.total_row
    temp_locO = 0

    # Different evaluation function for different piece
    if not maxTurn:
        location = board.get_pieces('X')
        piece_onboard = len(location)
        for i in location:
            if location[i][0] < temp_locX:
                temp_locX = location[i][0]
        return temp_locX * 0.4 + piece_onboard * 0.6
    else:
        location = board.get_pieces('O')
        piece_onboard = len(location)
        for i in location:
            if location[i][0] > temp_locO:
                temp_locO = location[i][0]
        return temp_locO * 0.6 + piece_onboard * 0.4


def cuttingoff_search(board, currDepth, maxTurn, alpha, beta):
    """

    :param: board, currDepth, maxTurn, alpha, beta
    :return: best_move, value

    Cuttingoff_search is almost the same as alpha-beta pruning except for the base case.
    The base case here used a cutoff test to reduce the levels of searching by evaluating
    the chance of winning for both pieces or players.
    """

    best_move = ((0, 0), 0)

    # base case
    if cutoff_test(currDepth):
        return eval(board, maxTurn)

    if maxTurn:
        value = -1000
    else:
        value = 1000

    # do action -- for every piece of each player on the board, it will loop through
    # all the possible cases and choose the move with largest utility score
    for piece in board.get_pieces('O' if maxTurn else 'X'):
        for h_move in range(-1, 2):
            if board.can_move(piece[0], piece[1], h_move, 'O' if maxTurn else 'X'):
                copy_board = copy.deepcopy(board)
                copy_board.make_move(piece[0], piece[1], h_move)

                score = alpha_beta(copy_board, currDepth - 1, not maxTurn, alpha, beta)[1]  # recursive call

                if maxTurn:
                    if score >= value:
                        value = score
                        best_move = (piece, h_move)
                        alpha = max(value, alpha)
                        if beta <= alpha:
                            break

                else:
                    if score <= value:
                        value = score
                        best_move = (piece, h_move)
                        beta = min(value, beta)
                        if beta <= alpha:
                            break

    return best_move, value


def q_learning_train(g, row, col, num_training_iter):
    player1 = QLearningPlayer('X')
    player2 = QLearningPlayer('O')

    win_list = [0, 0]

    print("Training {} iterations...".format(num_training_iter))
    for i in range(1, num_training_iter + 1):
        counter = 0
        is_game = True
        game = copy.deepcopy(g)

        while is_game:

            # counter used for switching player. This is human player's turn.
            if counter % 2 == 0:
                is_game = not player1.complete_move(game)

            else:
                is_game = not player2.complete_move(game)
            counter += 1

        rewards = game.get_reward()
        win_idx = rewards.index(max(rewards))
        win_list[win_idx] += 1

        if i % 100 == 0:
            print(game)
            print("{}/{} done.".format(i, num_training_iter))

    player_idx = win_list.index(max(win_list))

    if player_idx == 0:
        print("Player: {}".format('O'))
        return player1

    else:
        print("Player: {}".format('X'))
        return player2


def play(g, algo_choice, depth, q_player):
    """

    :param: g, algo_choice, depth, q_player
    :return: None

    Activate game for each algorithm
    """
    counter = 0
    is_game = True
    print(g)

    while is_game:

        # counter used for switching player. This is human player's turn.
        if counter % 2 == 0:
            cant_move = True

            # check the validity of inputs
            while(cant_move):
                x = int(input('Please enter x coordinate you want to move:'))
                y = int(input('Please enter y coordinate you want to move:'))
                step = int(input('Please enter horizontal moves you want:'))
                cant_move = not g.can_move(x, y, step, 'X')
                if cant_move:
                    print("Invalid move, please re-enter.")

            # make move on the board
            g.make_move(x, y, step)
            counter += 1
            print(g)

            # function call to check if game is finished
            if g.game_finish('X'):
                is_game = False

        # Agent's turn or 'O' or Max turn
        else:
            # Make a copy of the board for search trees
            simulate_board = copy.deepcopy(g)

            start = timeit.default_timer()  # Time calculator

            # For each choice, run different algorithm
            if algo_choice == 1:
                player_move = minimax(simulate_board, depth, True)[0]
            elif algo_choice == 2:
                player_move = alpha_beta(simulate_board, depth, True, -1000, 1000)[0]
            elif algo_choice == 3:
                player_move = cuttingoff_search(simulate_board, depth, True, -1000, 1000)[0]

            else:

                actions = g.get_available_moves('O')
                state = g.get_state()
                qs = [q_player.getQ(state,a) for a in actions]
                maxQ = max(qs)
                player_move = q_player.choose_action(state, actions)

                if qs.count(maxQ) > 1:
                    print(qs.count(maxQ))
                    #more than 1 best option; choose among them randomly
                    best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
                    i = random.choice(best_options)
                else:
                    i = qs.index(maxQ)

                player_move = actions[i]

            stop = timeit.default_timer()  # Time calculator
            print('Time ', stop - start)

            # Agent makes move on the board
            g.make_move(player_move[0][0], player_move[0][1], player_move[1])
            counter += 1
            print(g)

            # Check if game is finished
            if g.game_finish('O'):
                is_game = False


def main():

    check_input = True
 
    # This is the depth of search tree
    depth = 4
 
    # Check validity of inputs
    while(check_input):
        row = int(input('How many rows you want for the board game?'))
        col = int(input('How many columns?'))
        print('Which algorithm you would like to run this game?') 
        print('1. Minimax 2. Alpha-beta 3. Cutting-off search. 4. QLearning')
        choice = int(input('Please enter between 1 to 4: '))
        if row <= 0 or col <= 0 or choice < 1 or choice < 1 or choice > 4:
            check_input = True
        else:
            check_input = False
 
    # call class game constructor
    g = Game(row, col)
    q_player = None

    if choice == 4:
        num_training_iter = int(input('How many training iterations?'))
        q_player = q_learning_train(g, g.total_row, g.total_col, num_training_iter)


    # Play games between human player and agent
    play(g, choice, depth, q_player)


if __name__ == "__main__":
    main()
